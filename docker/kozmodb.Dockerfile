# This stage's objective is to gather ONLY requirements.txt files and anything else needed to install deps.
# This stage will be run almost every build, but it is fast and the resulting layer hash will be the same unless a deps file changes.
# We do it this way because we can't copy all requirements files with a glob pattern in docker while maintaining the folder structure.
FROM python:3.10 AS deps
WORKDIR /kozmodb

# Copy requirements files and essential build files
COPY requirements/ requirements/
COPY setup.py default_handlers.txt README.md ./
COPY kozmodb/__about__.py kozmodb/
# Copy packages directory for local package installation
COPY packages/ packages/
# Now this stage only contains a few files and the layer hash will be the same if they don't change.
# Which will mean the next stage can be cached, even if the cache for the above stage was invalidated.




# Use the stage from above to install our deps with as much caching as possible
FROM python:3.10 AS build
WORKDIR /kozmodb

# Configure apt to retain downloaded packages so we can store them in a cache mount
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
# Install system dependencies, with caching for faster builds
RUN --mount=target=/var/lib/apt,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    apt update -qy \
    && apt-get upgrade -qy \
    && apt-get install -qy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    freetds-dev freetds-bin libpq5 curl # freetds-dev required to build pymssql on arm64 for mssql_handler. Can be removed when we are on python3.11+

# Use a specific tag so the file doesn't change
COPY --from=ghcr.io/astral-sh/uv:0.8.11 /uv /usr/local/bin/uv
# Copy requirements files from the first stage
COPY --from=deps /kozmodb .

# - Silence uv complaining about not being able to use hard links,
# - prevent uv from accidentally downloading isolated Python builds,
# - pick a Python,
# - and finally declare `/kozmodb` as the target dir.
ENV UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.10 \
    UV_PROJECT_ENVIRONMENT=/kozmodb \
    VIRTUAL_ENV=/venv \
    PATH=/venv/bin:$PATH

# Install local packages first, then basic requirements
# We'll install the main kozmodb package later after copying the source code
RUN --mount=type=cache,target=/root/.cache \
    uv venv /venv \
    && uv pip install pip \
    && uv pip install ./packages/kozmodb_sql_parser \
    && uv pip install ./packages/kozmodb_sql \
    && uv pip install ./packages/kozmodb_python_sdk \
    && cd packages/kozmodb_evaluator && uv pip install . && cd ../..




FROM build AS extras
ARG EXTRAS
# Install extras on top of the bare kozmodb
# The torch index is provided for "-cpu" images which install the cpu-only version of torch
RUN --mount=type=cache,target=/root/.cache \
    if [ -n "$EXTRAS" ]; then uv pip install --index-strategy unsafe-first-match --index https://pypi.org/simple --index https://download.pytorch.org/whl/ $EXTRAS; fi

# Copy all of the kozmodb code over finally
# Here is where we invalidate the cache again if ANY file has changed
COPY . .
# Install the "kozmodb" package now that we have the code for it
# The local packages are already installed from the previous stage
RUN --mount=type=cache,target=/root/.cache uv pip install "."

COPY docker/kozmodb_config.release.json /root/kozmodb_config.json

ENV PYTHONUNBUFFERED=1
ENV KOZMODB_DOCKER_ENV=1
ENV VIRTUAL_ENV=/venv
ENV PATH=/venv/bin:$PATH

EXPOSE 47334/tcp
EXPOSE 47335/tcp



# Same as extras image, but with dev dependencies installed.
# This image is used in our docker-compose
FROM extras AS dev
WORKDIR /kozmodb

# Configure apt to retain downloaded packages so we can store them in a cache mount
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
# Install system dependencies, with caching for faster builds
RUN --mount=target=/var/lib/apt,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    apt update -qy \
    && apt-get upgrade -qy \
    && apt-get install -qy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    libpq5 freetds-bin curl

# Install dev requirements and install 'kozmodb' as an editable package
# The local packages are already installed from the previous stage
RUN --mount=type=cache,target=/root/.cache \
    uv pip install -r requirements/requirements-dev.txt \
    && uv pip install --no-deps -e "."

COPY docker/kozmodb_config.release.json /root/kozmodb_config.json

ENTRYPOINT [ "bash", "-c", "watchfiles --filter python 'python -Im kozmodb --config=/root/kozmodb_config.json --api=http,mysql' kozmodb" ]




# Make sure the regular image is the default
FROM extras

ENTRYPOINT [ "bash", "-c", "python -Im kozmodb --config=/root/kozmodb_config.json --api=http,mysql" ]

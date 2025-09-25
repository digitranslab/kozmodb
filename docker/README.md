### Docker images for KozmoDB

* https://docs.kozmodb.com/setup/self-hosted/docker/
* https://hub.docker.com/u/kozmodb

## Building

Docker images are using only released versions of KozmoDB from
https://pypi.org/project/KozmoDB/ so no files in parent dir are used.

To build `release` image using version reported at
https://public.api.kozmodb.com/installer/release/docker___success___None

    docker build -f release --no-cache -t kozmodb/kozmodb .

To build `release` image with specific KozmoDB version.

    docker build -f release --build-arg VERSION=2.57.0 -t kozmodb/kozmodb .

### `beta` vs `release`

`release` image pins KozmoDB version and builds from fixed PyTorch docker
image. `beta` uses latest PyTorch image and updates KozmoDB when container
is started to a version set at
https://public.api.kozmodb.com/installer/beta/docker___success___None

## Releasing

The `build.py <beta|release>` script is used in CI to build and push images
on release.

## Running local docker compose environment (in development)

Run `docker-compose up` or `docker-compose up -d` (for `detach` mode) to launch kozmodb environment in docker compose


## Running local docker compose environment (in old manner development)



1. Run `docker-compose -f docker-compose-old-manner up` or `docker-compose -f docker-compose-old-manner up -d` (for `detach` mode) to launch kozmodb in docker-compose in old school manner (monolithic on 100%)

.PHONY: format sort lint

# Variables
ISORT_OPTIONS = --profile black
PROJECT_NAME := kozmodb

# Default target
all: format sort lint

install:
	hatch env create

install_all:
	# First install the local kozmograph package
	cd kozmograph && pip install -e .
	# Install packages that commonly cause conflicts first
	pip install "shapely>=2.0.0,<2.1.0" --prefer-binary
	pip install "numpy>=1.24.0,<2.0.0" --prefer-binary
	# Install Google packages with compatible versions
	pip install "google-api-core>=2.11.0,<3.0.0" "protobuf>=4.21.0,<5.0.0"
	# Then install other packages
	pip install ruff==0.6.9 groq together boto3 litellm ollama chromadb weaviate weaviate-client sentence_transformers \
	                        elasticsearch opensearch-py vecs pinecone pinecone-text langchain-community \
							upstash-vector azure-search-documents langchain-neo4j rank-bm25
	# Install Google AI packages separately to avoid conflicts
	pip install google-generativeai --no-deps
	pip install google-cloud-aiplatform --no-deps  
	pip install vertexai --no-deps
	# Install their dependencies
	pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
	pip install --no-cache-dir --only-binary=faiss-cpu faiss-cpu

# Format code with ruff
format:
	hatch run format

# Sort imports with isort
sort:
	hatch run isort kozmodb/

# Lint code with ruff
lint:
	hatch run lint

docs:
	cd docs && mintlify dev

build:
	hatch build

publish:
	hatch publish

clean:
	rm -rf dist

test:
	hatch run test

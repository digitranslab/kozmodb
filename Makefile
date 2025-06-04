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
	# Install basic packages without protobuf dependencies
	pip install ruff==0.6.9 groq together boto3 litellm ollama elasticsearch opensearch-py \
			upstash-vector azure-search-documents rank-bm25
	# Install sentence transformers and basic vector stores (avoid chromadb and weaviate in CI)
	pip install sentence_transformers pinecone pinecone-text vecs
	# Install langchain packages (avoid langchain-neo4j which has weaviate conflicts)
	pip install langchain-community
	# Set compatible protobuf version for Google packages
	pip install "protobuf>=5.29.0,<6.0.0"
	pip install "google-api-core>=2.11.0,<3.0.0"
	# Install Google packages at the end
	pip install google-generativeai google-ai-generativelanguage
	pip install google-cloud-aiplatform grpc-google-iam-v1 google-cloud-iam
	pip install vertexai
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

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
	# Then install other packages with binary-only faiss-cpu
	pip install ruff==0.6.9 groq together boto3 litellm ollama chromadb weaviate weaviate-client sentence_transformers vertexai \
	                        google-generativeai elasticsearch opensearch-py vecs pinecone pinecone-text langchain-community \
							upstash-vector azure-search-documents langchain-neo4j rank-bm25
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

import os

import pytest
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI

from langchain_kozmograph.graphs.kozmograph import Kozmograph

# Load environment variables from .env
load_dotenv()


@pytest.fixture
def kozmograph_connection():
    """Setup Kozmograph connection fixture."""
    url = os.getenv("KOZMOGRAPH_URI", "bolt://localhost:7687")
    username = os.getenv("KOZMOGRAPH_USERNAME", "")
    password = os.getenv("KOZMOGRAPH_PASSWORD", "")

    graph = Kozmograph(
        url=url, username=username, password=password, refresh_schema=False
    )
    yield graph

    # Cleanup: clear the database after test
    graph.query("MATCH (n) DETACH DELETE n")


@pytest.fixture
def llm_transformer():
    """Setup LLM transformer fixture."""
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-turbo")
    return LLMGraphTransformer(llm=llm)


def test_ingest_and_verify(kozmograph_connection, llm_transformer):
    """Test to ingest a document and check nodes/edges in Kozmograph."""
    text = """
        Charles Robert Darwin was an English naturalist, geologist, and biologist,
        widely known for his contributions to evolutionary biology. His proposition that
        all species of life have descended from a common ancestor is now generally
        accepted and considered a fundamental scientific concept. In a joint
        publication with Alfred Russel Wallace, he introduced his scientific theory that
        this branching pattern of evolution resulted from a process he called natural
        selection, in which the struggle for existence has a similar effect to the
        artificial selection involved in selective breeding. Darwin has been
        described as one of the most influential figures in human history and was
        honoured by burial in Westminster Abbey.
    """

    # Convert document to graph structure
    documents = [Document(page_content=text)]
    graph_documents = llm_transformer.convert_to_graph_documents(documents)

    # Ingest graph data into Kozmograph
    kozmograph_connection.add_graph_documents(graph_documents)

    # Verify nodes and edges were created
    node_count = kozmograph_connection.query("MATCH (n) RETURN count(n) AS count")[0][
        "count"
    ]
    edge_count = kozmograph_connection.query("MATCH ()-[r]->() RETURN count(r) AS count")[
        0
    ]["count"]

    assert node_count > 0, "No nodes were created!"
    assert edge_count > 0, "No edges were created!"

    print(f"✅ Test passed with {node_count} nodes and {edge_count} edges!")

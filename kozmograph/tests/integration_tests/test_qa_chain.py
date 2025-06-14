import os

import pytest
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from langchain_kozmograph.chains.graph_qa import KozmographQAChain
from langchain_kozmograph.graphs.kozmograph import Kozmograph

# Load environment variables from .env
load_dotenv()


@pytest.fixture(scope="module")
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


@pytest.fixture(scope="module")
def kozmograph_chain(kozmograph_connection):
    """Set up KozmographQAChain with OpenAI LLM."""
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

    chain = KozmographQAChain.from_llm(
        ChatOpenAI(temperature=0),
        graph=kozmograph_connection,
        model_name="gpt-4-turbo",
        allow_dangerous_requests=True,
    )
    return chain


def test_seed_graph(kozmograph_connection):
    """Test to seed the graph with Baldur's Gate 3 data."""
    query = """
        MERGE (g:Game {name: "Baldur\'s Gate 3"})
        WITH g, ["PlayStation 5", "Mac OS", "Windows", "Xbox Series X/S"] AS platforms,
                ["Adventure", "Role-Playing Game", "Strategy"] AS genres
        FOREACH (platform IN platforms |
            MERGE (p:Platform {name: platform})
            MERGE (g)-[:AVAILABLE_ON]->(p)
        )
        FOREACH (genre IN genres |
            MERGE (gn:Genre {name: genre})
            MERGE (g)-[:HAS_GENRE]->(gn)
        )
        MERGE (p:Publisher {name: "Larian Studios"})
        MERGE (g)-[:PUBLISHED_BY]->(p);
    """
    kozmograph_connection.query(query)
    kozmograph_connection.refresh_schema()

    # Verify nodes exist
    game_exists = kozmograph_connection.query(
        """MATCH (g:Game {name: "Baldur's Gate 3"}) RETURN g"""
    )
    assert len(game_exists) > 0, "Game node not created!"

    print("✅ Graph seeded successfully")


def test_qa_chain(kozmograph_chain):
    """Test QA chain to verify platform data retrieval."""
    response = kozmograph_chain.invoke("Which platforms is Baldur's Gate 3 available on?")
    result = response["result"].lower()

    # Assert the response contains all expected platforms
    expected_platforms = ["playstation 5", "mac os", "windows", "xbox series x/s"]

    for platform in expected_platforms:
        assert platform in result, f"Platform '{platform}' not found in response!"

    print("✅ QA Chain returned expected platforms")

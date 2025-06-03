import os
from getpass import getpass

import pytest
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

from langchain_kozmograph import KozmographToolkit
from langchain_kozmograph.graphs.kozmograph import Kozmograph

# Load environment variables
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
def kozmograph_agent():
    url = os.getenv("KOZMOGRAPH_URI", "bolt://localhost:7687")
    username = os.getenv("KOZMOGRAPH_USERNAME", "")
    password = os.getenv("KOZMOGRAPH_PASSWORD", "")

    """Set up Kozmograph agent with React pattern."""
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass("Enter API key for OpenAI: ")

    llm = init_chat_model("gpt-4o-mini", model_provider="openai")

    db = Kozmograph(url=url, username=username, password=password)
    toolkit = KozmographToolkit(db=db, llm=llm)

    agent_executor = create_react_agent(
        llm,
        toolkit.get_tools(),
        prompt="You will get a cypher query, try to execute it on the Kozmograph database.",
    )
    return agent_executor


def test_seed_graph(kozmograph_connection):
    """Test to seed the graph with Jon Snow node"""
    query = """
       CREATE (c:Character {name: 'Jon Snow', house: 'Stark', title: 'King in the North'})
    """
    kozmograph_connection.query(query)
    kozmograph_connection.refresh_schema()

    # Verify nodes exist
    game_exists = kozmograph_connection.query(
        """MATCH (c:Character {name: 'Jon Snow'}) RETURN c"""
    )
    assert len(game_exists) > 0, "Game node not created!"

    print("✅ Graph seeded successfully")


def test_kozmograph_agent(kozmograph_agent):
    """Test Kozmograph agent executes a Cypher query correctly."""
    example_query = "MATCH (n) WHERE n.name = 'Jon Snow' RETURN n"
    events = kozmograph_agent.stream(
        {"messages": [("user", example_query)]},
        stream_mode="values",
    )

    last_event = None
    for event in events:
        last_event = event
        event["messages"][-1].pretty_print()

    assert last_event, "Agent did not return any results!"
    assert "Jon Snow" in str(
        last_event["messages"][-1]
    ), "Expected 'Jon Snow' in the final result!"

    print("✅ Kozmograph Agent processed query successfully")

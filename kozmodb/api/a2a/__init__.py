# A2A specific imports
from kozmodb.api.a2a.common.types import (
    AgentCard,
    AgentCapabilities,
    AgentSkill,
)
from kozmodb.api.a2a.common.server.server import A2AServer
from kozmodb.api.a2a.task_manager import AgentTaskManager
from kozmodb.api.a2a.agent import KozmoDBAgent
from kozmodb.utilities.config import config


def get_a2a_app(
    project_name: str = "kozmodb",
):
    kozmodb_port = config.get("api", {}).get("http", {}).get("port", 47334)

    # Prepare A2A artefacts (agent card & task-manager)
    capabilities = AgentCapabilities(streaming=True)
    skill = AgentSkill(
        id="kozmodb_query",
        name="KozmoDB Query",
        description="Executes natural-language queries via KozmoDB agents.",
        tags=["database", "kozmodb", "query", "analytics"],
        examples=[
            "What trends exist in my sales data?",
            "Generate insights from the support tickets dataset.",
        ],
        inputModes=KozmoDBAgent.SUPPORTED_CONTENT_TYPES,
        outputModes=KozmoDBAgent.SUPPORTED_CONTENT_TYPES,
    )

    agent_card = AgentCard(
        name="KozmoDB Agent Connector",
        description=(f"A2A connector that proxies requests to KozmoDB agents in project '{project_name}'."),
        url=f"http://127.0.0.1:{kozmodb_port}",
        version="1.0.0",
        defaultInputModes=KozmoDBAgent.SUPPORTED_CONTENT_TYPES,
        defaultOutputModes=KozmoDBAgent.SUPPORTED_CONTENT_TYPES,
        capabilities=capabilities,
        skills=[skill],
    )

    task_manager = AgentTaskManager(
        project_name=project_name,
    )

    server = A2AServer(
        agent_card=agent_card,
        task_manager=task_manager,
    )
    return server.app

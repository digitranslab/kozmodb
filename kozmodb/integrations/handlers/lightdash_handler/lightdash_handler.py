from collections import OrderedDict
from kozmodb_sql_parser import parse_sql

from kozmodb.integrations.libs.const import HANDLER_CONNECTION_ARG_TYPE as ARG_TYPE
from kozmodb.integrations.handlers.lightdash_handler.api import Lightdash
from kozmodb.integrations.handlers.lightdash_handler.lightdash_tables import (
    UserTable,
    UserAbilityTable,
    OrgTable,
    OrgProjectsTable,
    OrgMembersTable,
    ProjectTable,
    WarehouseConnectionTable,
    DBTConnectionTable,
    DBTEnvironmentVarsTable,
    ChartsTable,
    SpacesTable,
    AccessTable,
    ValidationTable,
    DashboardsTable,
    QueriesTable,
    ChartHistoryTable,
    ChartConfigTable,
    ChartAdditionalMetricsTable,
    ChartTableCalculationsTable,
    SchedulerLogsTable,
    SchedulerTable,
    SchedulerJobsTable,
    SchedulerJobStatus,
)
from kozmodb.integrations.libs.api_handler import APIHandler
from kozmodb.integrations.libs.response import HandlerStatusResponse as StatusResponse


class LightdashHandler(APIHandler):

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name)
        self.connection = None
        self.is_connected = False
        self.api_key = kwargs.get("connection_data", {}).get("api_key", "")
        self.base_url = kwargs.get("connection_data", {}).get("base_url", "")
        _tables = [
            UserTable,
            UserAbilityTable,
            OrgTable,
            OrgProjectsTable,
            OrgMembersTable,
            ProjectTable,
            WarehouseConnectionTable,
            DBTConnectionTable,
            DBTEnvironmentVarsTable,
            ChartsTable,
            SpacesTable,
            AccessTable,
            ValidationTable,
            DashboardsTable,
            QueriesTable,
            ChartHistoryTable,
            ChartConfigTable,
            ChartAdditionalMetricsTable,
            ChartTableCalculationsTable,
            SchedulerLogsTable,
            SchedulerTable,
            SchedulerJobsTable,
            SchedulerJobStatus,
        ]
        for Table in _tables:
            self._register_table(Table.name, Table(self))
        self.connect()

    def connect(self) -> Lightdash:
        self.connection = Lightdash(self.base_url, self.api_key)
        return self.connection

    def check_connection(self) -> StatusResponse:
        resp = StatusResponse(False)
        if self.connection and not self.connection.is_connected():
            resp.error = "Client not connected"
        else:
            resp.success = True
        return resp

    def native_query(self, query: str) -> StatusResponse:
        ast = parse_sql(query)
        return self.query(ast)


connection_args = OrderedDict(
    api_key={
        'type': ARG_TYPE.STR,
        'description': 'API Token for accessing Lightdash instance',
        'required': True,
        'label': 'API Key',
    },
    base_url={
        'type': ARG_TYPE.STR,
        'description': 'Base URL of Lightdash instance',
        'required': True,
        'label': 'Base URL',
    }
)


connection_args_example = OrderedDict(
    api_key='23d6b9e0c2fab7eba2e8b7e452cead47',
    base_url='http://localhost:8080/'
)

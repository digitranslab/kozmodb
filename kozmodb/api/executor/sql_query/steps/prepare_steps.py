from kozmodb_sql_parser.ast import (
    Identifier,
    Constant,
    Select,
    Star,
)
from kozmodb.api.executor.planner.steps import (
    GetPredictorColumns,
    GetTableColumns,
)

from kozmodb.api.executor.sql_query.result_set import ResultSet, Column
from kozmodb.utilities.config import config

from .base import BaseStepCall


class GetPredictorColumnsCall(BaseStepCall):

    bind = GetPredictorColumns

    def call(self, step):
        kozmodb_database_name = config.get('default_project')

        predictor_name = step.predictor.parts[-1]
        dn = self.session.datahub.get(kozmodb_database_name)
        columns_names = dn.get_table_columns_names(predictor_name)

        data = ResultSet()
        for column_name in columns_names:
            data.add_column(Column(
                name=column_name,
                table_name=predictor_name,
                database=kozmodb_database_name
            ))
        return data


class GetTableColumnsCall(BaseStepCall):

    bind = GetTableColumns

    def call(self, step):

        table = step.table
        dn = self.session.datahub.get(step.namespace)
        ds_query = Select(from_table=Identifier(table), targets=[Star()], limit=Constant(0))

        response = dn.query(ds_query, session=self.session)

        data = ResultSet()
        for column in response.columns:
            data.add_column(Column(
                name=column['name'],
                type=column.get('type'),
                table_name=table,
                database=self.context.get('database')
            ))
        return data

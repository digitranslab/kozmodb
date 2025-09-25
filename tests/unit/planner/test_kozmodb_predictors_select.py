from kozmodb_sql_parser.ast import (Identifier, Select, NullConstant, Constant, Function, BinaryOperation)

from kozmodb.api.executor.planner import plan_query
from kozmodb.api.executor.planner.query_plan import QueryPlan
from kozmodb.api.executor.planner.steps import FetchDataframeStep


class TestPlanPredictorsSelect:
    def test_predictors_select_plan(self):
        query = Select(
            targets=[Identifier('column1'), Constant(1), NullConstant(), Function('database', args=[])],
            from_table=Identifier('kozmodb.predictors'),
            where=BinaryOperation(
                'and', args=[
                    BinaryOperation('=', args=[Identifier('column1'), Identifier('column2')]),
                    BinaryOperation('>', args=[Identifier('column3'), Constant(0)]),
                ]
            )
        )
        expected_plan = QueryPlan(
            integrations=['kozmodb'],
            steps=[
                FetchDataframeStep(
                    integration='kozmodb',
                    query=Select(
                        targets=[Identifier('column1', alias=Identifier('column1')),
                                 Constant(1),
                                 NullConstant(),
                                 Function('database', args=[]),
                                 ],
                        from_table=Identifier('predictors'),
                        where=BinaryOperation(
                            'and', args=[
                                BinaryOperation(
                                    '=',
                                    args=[Identifier('column1'),
                                          Identifier('column2')]
                                ),
                                BinaryOperation(
                                    '>',
                                    args=[Identifier('column3'),
                                          Constant(0)]
                                ),
                            ]
                        )
                    ),
                    step_num=0,
                ),
            ]
        )

        plan = plan_query(query, integrations=['kozmodb'])

        for i in range(len(plan.steps)):
            assert plan.steps[i] == expected_plan.steps[i]

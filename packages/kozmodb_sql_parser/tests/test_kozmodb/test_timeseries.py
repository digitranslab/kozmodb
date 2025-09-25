from kozmodb_sql_parser import parse_sql
from kozmodb_sql_parser.ast import *
from kozmodb_sql_parser.ast.kozmodb.latest import Latest
from kozmodb_sql_parser.utils import JoinType


class TestTimeSeries:
    def test_latest_in_where(self):
        sql = "SELECT time, price FROM crypto INNER JOIN pred WHERE time > LATEST"
        ast = parse_sql(sql)
        expected_ast = Select(
            targets=[Identifier('time'), Identifier('price')],
            from_table=Join(left=Identifier('crypto'),
                            right=Identifier('pred'),
                            join_type=JoinType.INNER_JOIN),
            where=BinaryOperation('>', args=[Identifier('time'), Latest()]),
        )

        assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

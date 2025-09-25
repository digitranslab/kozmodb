import pytest

from kozmodb_sql import parse_sql, ParsingException
from kozmodb_sql.parser.dialects.kozmodb import *
from kozmodb_sql.parser.ast import *


class TestDropDatasource:
    def test_drop_datasource(self):
        sql = "DROP DATASOURCE IF EXISTS dsname"
        ast = parse_sql(sql, dialect='kozmodb')
        expected_ast = DropDatasource(name=Identifier('dsname'), if_exists=True)
        assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_drop_project(self):

        sql = "DROP PROJECT dbname"
        ast = parse_sql(sql, dialect='kozmodb')

        expected_ast = DropDatabase(name=Identifier('dbname'), if_exists=False)

        assert str(ast).lower() == str(expected_ast).lower()
        assert ast.to_tree() == expected_ast.to_tree()


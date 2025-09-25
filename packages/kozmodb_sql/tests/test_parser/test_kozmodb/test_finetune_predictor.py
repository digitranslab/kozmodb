import pytest

from kozmodb_sql import parse_sql
from kozmodb_sql.parser.ast import *
from kozmodb_sql.parser.dialects.kozmodb.finetune_predictor import FinetunePredictor
from kozmodb_sql.parser.dialects.kozmodb.lexer import KozmoDBLexer


class TestFinetunePredictor:
    def test_finetune_predictor_lexer(self):
        sql = "FINETUNE kozmodb.pred FROM integration_name (SELECT * FROM table_1) USING a=1"
        tokens = list(KozmoDBLexer().tokenize(sql))
        assert tokens[0].type == 'FINETUNE'
        assert tokens[1].type == 'ID'
        assert tokens[1].value == 'kozmodb'
        assert tokens[2].type == 'DOT'
        assert tokens[3].type == 'ID'
        assert tokens[3].value == 'pred'

    def test_finetune_predictor_full(self):
        sql = "FINETUNE kozmodb.pred FROM integration_name (SELECT * FROM table_1) USING a=1, b=null"
        ast = parse_sql(sql, dialect='kozmodb')
        expected_ast = FinetunePredictor(
            name=Identifier('kozmodb.pred'),
            integration_name=Identifier('integration_name'),
            query_str="SELECT * FROM table_1",
            using={'a': 1, 'b': None},
        )
        assert ' '.join(str(ast).split()).lower() == sql.lower()
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

        # with MODEL
        sql = "FINETUNE MODEL kozmodb.pred FROM integration_name (SELECT * FROM table_1) USING a=1, b=null"
        ast = parse_sql(sql, dialect='kozmodb')

        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

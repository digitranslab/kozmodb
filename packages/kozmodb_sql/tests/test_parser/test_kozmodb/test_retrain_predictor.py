import pytest

from kozmodb_sql import parse_sql, ParsingException
from kozmodb_sql.parser.dialects.kozmodb import *
from kozmodb_sql.parser.ast import *
from kozmodb_sql.parser.dialects.kozmodb.retrain_predictor import RetrainPredictor
from kozmodb_sql.parser.dialects.kozmodb.lexer import KozmoDBLexer

class TestRetrainPredictor:
    def test_retrain_predictor_lexer(self):
        sql = "RETRAIN kozmodb.pred"
        tokens = list(KozmoDBLexer().tokenize(sql))
        assert tokens[0].type == 'RETRAIN'
        assert tokens[1].type == 'ID'
        assert tokens[1].value == 'kozmodb'
        assert tokens[2].type == 'DOT'
        assert tokens[2].value == '.'
        assert tokens[3].type == 'ID'
        assert tokens[3].value == 'pred'

    def test_retrain_predictor_ok(self):
        sql = "RETRAIN kozmodb.pred"
        ast = parse_sql(sql, dialect='kozmodb')
        expected_ast = RetrainPredictor(name=Identifier('kozmodb.pred'))
        assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

        # with model
        sql = "RETRAIN MODEL kozmodb.pred"
        ast = parse_sql(sql, dialect='kozmodb')
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_retrain_predictor_full(self):
        sql = """Retrain pred
                FROM integration_name 
                (selct * FROM aaa)
                PREDICT f1
                ORDER BY f_order_1 ASC, f_order_2
                GROUP BY f_group_1
                WINDOW 100
                HORIZON 7
                USING 
                    a=null,
                    b=1                    
                """
        ast = parse_sql(sql, dialect='kozmodb')
        expected_ast = RetrainPredictor(
            name=Identifier('pred'),
            integration_name=Identifier('integration_name'),
            query_str="selct * FROM aaa",
            targets=[Identifier('f1')],
            order_by=[OrderBy(Identifier('f_order_1'), direction='ASC'),
                      OrderBy(Identifier('f_order_2'), direction='default')],
            group_by=[Identifier('f_group_1')],
            window=100,
            horizon=7,
            using={'a': None, 'b': 1},
        )
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

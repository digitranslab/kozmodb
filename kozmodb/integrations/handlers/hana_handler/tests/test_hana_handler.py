import os
import unittest

from kozmodb.integrations.handlers.hana_handler.hana_handler import HanaHandler
from kozmodb.api.executor.data_types.response_type import RESPONSE_TYPE


"""
create schema KOZMODB;

create table KOZMODB.TEST
(
    ID          INTEGER not null,
    NAME        NVARCHAR(1),
    DESCRIPTION NVARCHAR(1)
);

create unique index KOZMODB.TEST_ID_INDEX
    on KOZMODB.TEST (ID);

alter table KOZMODB.TEST
    add constraint TEST_PK
        primary key (ID);

insert into KOZMODB.TEST
values (1, 'h', 'w');
"""


class HanaHandlerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kwargs = {
            "address": os.environ.get('HANA_ADDRESS', 'localhost'),
            "port": os.environ.get('HANA_PORT', 30015),
            "user": "DBADMIN",
            "password": os.environ.get('HANA_PASSWORD'),
            "schema": "KOZMODB",
            "encrypt": True
        }
        cls.handler = HanaHandler('test_hana_handler', cls.kwargs)

    def test_0_connect(self):
        assert self.handler.connect()

    def test_1_check_connection(self):
        assert self.handler.check_connection().success is True

    def test_2_get_columns(self):
        assert self.handler.get_columns('TEST').resp_type is not RESPONSE_TYPE.ERROR

    def test_3_get_tables(self):
        assert self.handler.get_tables().resp_type is not RESPONSE_TYPE.ERROR

    def test_4_select_query(self):
        query = 'SELECT * FROM KOZMODB.TEST WHERE ID=2'
        assert self.handler.query(query).resp_type is RESPONSE_TYPE.TABLE

    def test_5_update_query(self):
        query = 'UPDATE KOZMODB.TEST SET NAME=\'s\' WHERE ID=1'
        assert self.handler.query(query).resp_type is RESPONSE_TYPE.OK


if __name__ == "__main__":
    unittest.main(failfast=True)

"""
*******************************************************
 * Copyright (C) 2017 KozmoDB Inc. <copyright@kozmodb.com>
 *
 * This file is part of KozmoDB Server.
 *
 * KozmoDB Server can not be copied and/or distributed without the express
 * permission of KozmoDB Inc
 *******************************************************
"""

from kozmodb.api.mysql.mysql_proxy.data_types.mysql_datum import Datum
from kozmodb.api.mysql.mysql_proxy.data_types.mysql_packet import Packet


class ColumnCountPacket(Packet):
    def setup(self):
        count = self._kwargs.get('count', 0)
        self.column_count = Datum('int<lenenc>', count)

    @property
    def body(self):

        order = [
            'column_count'
        ]

        string = b''
        for key in order:
            string += getattr(self, key).toStringPacket()

        self.setBody(string)
        return self._body

    @staticmethod
    def test():
        import pprint
        pprint.pprint(
            str(ColumnCountPacket(count=1).get_packet_string())
        )


if __name__ == "__main__":
    ColumnCountPacket.test()

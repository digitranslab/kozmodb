import kozmodb.interfaces.storage.db as db
from kozmodb.api.mysql.mysql_proxy.mysql_proxy import MysqlProxy
from kozmodb.utilities import log
from kozmodb.utilities.functions import init_lexer_parsers


def start(verbose=False):
    logger = log.getLogger(__name__)
    logger.info("MySQL API is starting..")
    db.init()
    init_lexer_parsers()

    MysqlProxy.startProxy()

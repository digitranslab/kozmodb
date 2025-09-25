class KozmodbSQLException(Exception):
    pass


class ParsingException(KozmodbSQLException):
    pass


class PlanningException(KozmodbSQLException):
    pass

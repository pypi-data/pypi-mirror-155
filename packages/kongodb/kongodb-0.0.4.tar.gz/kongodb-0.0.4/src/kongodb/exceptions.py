
class KongodbException(Exception): pass

class ItemNotFoundError(KongodbException):pass
class ItemExistsError(KongodbException):pass
class NoResultsError(KongodbException): pass

from typing import cast, Dict

from cubicweb.server.session import Connection


class ApiTransaction:
    def __init__(self, repo, user):
        self.cnx = Connection(repo, user)
        self.cnx.__enter__()
        self._uuid = cast(str, self.cnx.transaction_uuid(set=True))

    @property
    def uuid(self) -> str:
        return self._uuid

    def execute(self, rql, params):
        return self.cnx.execute(rql, params)

    def commit(self):
        self.cnx.commit()

    def rollback(self):
        self.cnx.rollback()

    def end(self):
        self.cnx.__exit__(None, None, None)


class ApiTransactionsRepository(object):
    def __init__(self, repo):
        self._transactions: Dict[str, ApiTransaction] = dict()
        self._repo = repo

    def begin_transaction(self, user):
        transaction = ApiTransaction(self._repo, user)
        self._transactions[transaction.uuid] = transaction
        return transaction.uuid

    def end_transaction(self, uuid):
        transaction = self._transactions.pop(uuid)
        transaction.end()

    def __getitem__(self, uuid: str):
        return self._transactions[uuid]

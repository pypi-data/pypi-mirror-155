"""
Xero Linked Transactions API
"""

from .api_base import ApiBase


class LinkedTransactions(ApiBase):
    """
    Class for Linked Transactions API
    """

    POST_LINKED_TRANSACTION = '/api.xro/2.0/LinkedTransactions'

    def post(self, data):
        """
        Create new invoice

        Parameters:
            data (dict): Data to create invoice

        Returns:
             Response from API
        """

        return self._post_request(data, LinkedTransactions.POST_LINKED_TRANSACTION)

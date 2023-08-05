"""
Xero Tax Rates API
"""

from .api_base import ApiBase


class TaxRates(ApiBase):
    """
    Class for Tax Rates API
    """

    GET_TAX_RATES = '/api.xro/2.0/TaxRates'
    POST_TAX_RATES = '/api.xro/2.0/TaxRates'
    PUT_TAX_RATES = '/api.xro/2.0/TaxRates'

    def get_all(self):
        """
        Get all Tax Rates

        Returns:
            List of all Tax Rates
        """

        return self._get_request(TaxRates.GET_TAX_RATES)

    def post(self, data):
        """
        Create new Bank Transaction

        Parameters:
            data (dict): Data to create tax rates

        Returns:
             Response from API
        """

        return self._post_request(data, TaxRates.POST_TAX_RATES)

    def put(self, data: dict):
        """
        Create or replace tax rate

        Parameters:
            data (dict): Data to Create or replace tax rate

        Returns:
                Response from API
        """

        return self._update_request(data, TaxRates.PUT_TAX_RATES)

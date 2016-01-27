# -*- coding: utf-8 -*-

# Copyright (c) 2016 James Gardiner

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""
chwrapper.search
~~~~~~~~~~~~~~~~

This module provides a Search object to query the Companies House API.

"""

from .base import _Service


class Search(_Service):
    """Provides an interface to the Companies House API through a Search object."""

    def __init__(self, access_token=None):
        """Construct a Search object.

        Args:
            access_token (str): A valid Companies House API. If an
                access token isn't specified then looks for *CompaniesHouseKey* or
                COMPANIES_HOUSE_KEY environment variables. Defaults to None.
        """
        super(Search, self).__init__()
        self.session = self.get_session(access_token)

    def search_companies(self, term, **kwargs):
        """Search for companies by name.

        Args:
          term (str): Company name to search on
          kwargs (dict): additional keywords passed into
            requests.session.get params keyword.
        """
        params = kwargs
        params['q'] = term
        baseuri = self._BASE_URI + 'search/companies'
        res = self.session.get(baseuri, params=params)
        self.handle_http_error(res)
        return res

    def search_officers(self, term, **kwargs):
        """Search for officers by name.

        Args:
          term (str): Officer name to search on.
          kwargs (dict): additional keywords passed into
            requests.session.get params keyword.
        """
        params = kwargs
        params['q'] = term
        baseuri = self._BASE_URI + 'search/officers'
        res = self.session.get(baseuri, params=params)
        return res

    def appointments(self, num, **kwargs):
        """Search for officer appointments by officer number.

        Args:
          num (str): Officer number to search on.
          kwargs (dict): additional keywords passed into
          requests.session.get params keyword.
        """
        baseuri = self._BASE_URI + 'officers/{}/appointments'.format(num)
        res = self.session.get(baseuri, params=kwargs)
        self.handle_http_error(res)
        return res

    def address(self, num):
        """Search for company addresses by company number.

        Args:
          num (str): Officer number to search on.
        """
        baseuri = self._BASE_URI + "company/{}/registered-office-address".format(num)
        res = self.session.get(baseuri)
        self.handle_http_error(res)
        return res

    def profile(self, num):
        """Search for company profile by company number.

        Args:
          num (str): Company number to search on.
        """
        baseuri = self._BASE_URI + "company/{}".format(num)
        res = self.session.get(baseuri)
        self.handle_http_error(res)
        return res

    def insolvency(self, num):
        """Search for insolvency records by company number.

        Args:
          num (str): Company number to search on.
        """
        baseuri = self._BASE_URI + "company/{}/insolvency".format(num)
        res = self.session.get(baseuri)
        self.handle_http_error(res)
        return res

    def filing_history(self, num, transaction=None, **kwargs):
        """Search for a company's filling history by company number.

        Args:
          num (str): Company number to search on.

          transaction (Optional[str]): Filing record number.
          kwargs (dict): additional keywords passed into
            requests.session.get params keyword.
        """
        baseuri = self._BASE_URI + "company/{}/filing-history".format(num)
        if transaction is not None:
            baseuri += "/{}".format(transaction)
        res = self.session.get(baseuri, params=kwargs)
        self.handle_http_error(res)
        return res

    def charges(self, num, charge_id=None, **kwargs):
        """Search for a company's filling history by company number.

        Args:
          num (str): Company number to search on.
          transaction (Optional[str]): Filing record number.
          kwargs (dict): additional keywords passed into
          requests.session.get params keyword.
        """
        baseuri = self._BASE_URI + "company/{}/charges".format(num)
        if charge_id is not None:
            baseuri += "/{}".format(charge_id)
            res = self.session.get(baseuri, params=kwargs)
        else:
            res = self.session.get(baseuri, params=kwargs)
        return res

    def officers(self, num, **kwargs):
        """Search for a company's registered officers by company number.

        Args:
          num (str): Company number to search on.
          kwargs (dict): additional keywords passed into
            requests.session.get *params* keyword.
        """
        baseuri = self._BASE_URI + "company/{}/officers".format(num)
        res = self.session.get(baseuri, params=kwargs)
        self.handle_http_error(res)
        return res

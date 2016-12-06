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

from .base import Service


class Search(Service):
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

    @Service.rate_limit
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

    @Service.rate_limit
    def search_officers(self, term, disqualified=False, **kwargs):
        """Search for officers by name.

        Args:
          term (str): Officer name to search on.
          disqualified (Optional[bool]): True to search for disqualified
            officers
          kwargs (dict): additional keywords passed into
            requests.session.get params keyword.
        """
        search_type = 'officers' if not disqualified else 'disqualified-officers'
        params = kwargs
        params['q'] = term
        baseuri = self._BASE_URI + 'search/{}'.format(search_type)
        res = self.session.get(baseuri, params=params)
        self.handle_http_error(res)
        return res

    @Service.rate_limit
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

    @Service.rate_limit
    def address(self, num):
        """Search for company addresses by company number.

        Args:
          num (str): Company number to search on.
        """
        baseuri = self._BASE_URI + "company/{}/registered-office-address".format(num)
        res = self.session.get(baseuri)
        self.handle_http_error(res)
        return res

    @Service.rate_limit
    def profile(self, num):
        """Search for company profile by company number.

        Args:
          num (str): Company number to search on.
        """
        baseuri = self._BASE_URI + "company/{}".format(num)
        res = self.session.get(baseuri)
        self.handle_http_error(res)
        return res

    @Service.rate_limit
    def insolvency(self, num):
        """Search for insolvency records by company number.

        Args:
          num (str): Company number to search on.
        """
        baseuri = self._BASE_URI + "company/{}/insolvency".format(num)
        res = self.session.get(baseuri)
        self.handle_http_error(res)
        return res

    @Service.rate_limit
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

    @Service.rate_limit
    def charges(self, num, charge_id=None, **kwargs):
        """Search for charges against a company by company number.

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
        self.handle_http_error(res)
        return res

    @Service.rate_limit
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

    @Service.rate_limit
    def disqualified(self, num, natural=True, **kwargs):
        """Search for disqualified officers by officer ID. Searches for
           natural disqualifications by default. Specify natural=False to
           search for corporate disqualifications.

        Args:
           num (str): Company number to search on.
           natural (Optional[bool]): Natural or corporate search
           kwargs (dict): additional keywords passed into
            requests.session.get *params* keyword.
        """
        search_type = 'natural' if natural else 'corporate'
        baseuri = (self._BASE_URI +
                   'disqualified-officers/{}/{}'.format(search_type, num))
        res = self.session.get(baseuri, params=kwargs)
        self.handle_http_error(res)
        return res

    @Service.rate_limit
    def persons_significant_control(self, num, statements=False, **kwargs):
        """Search for a list of persons with significant control for a
           specified company. Specify statements=True to only search for
           officers with statements.

        Args:
            num (str, int): Company number to search on.
            statements (Optional[bool]): Search only for persons with
                statements. Default is False.
            kwargs (dict): additional keywords passed into requests.session.get
            *params* keyword.
        """
        baseuri = (self._BASE_URI +
                   'company/{}/persons-with-significant-control'.format(num))

        # Only append statements to the URL if statements is True
        if statements is True:
            baseuri += '-statements'

        res = self.session.get(baseuri, params=kwargs)
        self.handle_http_error(res)
        return res

    @Service.rate_limit
    def significant_control(self,
                            num,
                            entity_id,
                            entity_type='individual',
                            **kwargs):
        """Used to get details of a specific entity with significant control
           of a specified company.

        Args:
            num (str, int): Company number to search on.
            entity_id (str, int): Entity id to request details for
            entity_type (str, int): What type of entity to search for. Defaults
                to 'individual'. Other possible opetions are
                'corporate' (for corporate entitys), 'legal' (for legal
                persons), 'statements' (for a person with significant control
                statement) and 'secure' (for a super secure person).
            kwargs (dict): additional keywords passed into requests.session.get
            *params* keyword.
        """

        # Dict mapping entity_type strings to url strings
        entities = {'individual': 'individual',
                    'corporate': 'corporate-entity',
                    'legal': 'legal-person',
                    'statements': 'persons-with-significant-control-statements',
                    'secure': 'super-secure'}

        # Make sure correct entity_type supplied
        try:
            entity = entities[entity_type]
        except KeyError as e:
            msg = ("Wrong entity_type supplied. Please choose from " +
                   "individual, corporate, legal, statements or secure")
            raise Exception(msg) from e

        # Construct the request and return the result
        baseuri = (self._BASE_URI +
                   'company/{}/persons-with-significant-control/'.format(num) +
                   '{}/{}'.format(entity, entity_id))
        res = self.session.get(baseuri, params=kwargs)
        self.handle_http_error(res)
        return res

    @Service.rate_limit
    def document(self, document_id, **kwargs):
        """Requests for a document by the document id.
           Normally the response.content can be saved as a pdf file

        Args:
           document_id (str): The id of the document retrieved.
           kwargs (dict): additional keywords passed into
            requests.session.get *params* keyword.
        """
        baseuri = '{}document/{}/content'.format(self._DOCUMENT_URI, document_id)
        res = self.session.get(baseuri, params=kwargs)
        self.handle_http_error(res)
        return res

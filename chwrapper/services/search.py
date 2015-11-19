#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (c) 2015 James Gardiner

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from .base import Service


class Search(Service):

    BASE_URI = "https://api.companieshouse.gov.uk/"

    def search(self,
               term,
               n_items=None,
               start_index=None):

        params = {
            "q": term,
            "items_per_page": n_items,
            "start_index": start_index
        }

        res = self.session.get(self.baseuri, params=params, auth=self.session.auth)
        self.handle_http_error(res)

        return res

class CompanySearch(Search):
    def __init__(self, access_token=None):
        self.session = self.get_session(access_token)
        self.baseuri = self.BASE_URI + "search/companies"

class OfficerSearch(Search):
    def __init__(self, access_token=None):
        self.session = self.get_session(access_token)
        self.baseuri = self.BASE_URI + "search/officers"

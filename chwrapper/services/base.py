# -*- coding: utf-8 -*-

# Copyright (c) 2016 James Gardiner

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from datetime import datetime
from time import sleep
import os
import requests

from .. import __version__


class RateLimitAdapter(requests.adapters.HTTPAdapter):

    def __init__(self, **kwargs):
        super(RateLimitAdapter, self).__init__(**kwargs)

    def rate_limit(self, resp):
        if resp.headers.get("X-Ratelimit-Remain", "0") == "0":
            try:
                timestamp = int(resp.headers["X-Ratelimit-Reset"])
            except KeyError as e:
                msg = "No X-Ratelimit-Reset Header in response"
                raise KeyError(msg) from e

            reset_dt = datetime.utcfromtimestamp(timestamp)
            td = reset_dt - datetime.utcnow()

            try:
                sleep(td.total_seconds() + 1)
            except ValueError as e:
                msg = "X-Rate-Limit-Reset time is negative"
                raise ValueError(msg) from e
        return resp

    def build_response(self, req, resp):
        resp = super(RateLimitAdapter, self).build_response(req, resp)
        self.rate_limit(resp)
        return resp


class Service(object):

    def __init__(self):
        self._BASE_URI = "https://api.companieshouse.gov.uk/"
        self._DOCUMENT_URI = "https://document-api.companieshouse.gov.uk/"
        self._ignore_codes = []

    def get_session(self, access_token=None, env=None, rate_limit=True):
        access_token = (
            access_token
            or (env or os.environ).get("CompaniesHouseKey")
            or (env or os.environ).get("COMPANIES_HOUSE_KEY")
        )
        session = requests.Session()

        if rate_limit:
            session.mount(self._BASE_URI, RateLimitAdapter())

        session.params.update(access_token=access_token)

        # CH API requires a key only, which is passed as the username
        session.headers.update(
            {
                "User-Agent": " ".join(
                    [self.product_token, requests.utils.default_user_agent()]
                )
            }
        )
        session.auth = (access_token, "")
        return session

    @property
    def product_token(self):
        """A product token for use in User-Agent headers."""
        return "chwrapper/{0}".format(__version__)

    def handle_http_error(
        self, response, ignore=None, custom_messages=None, raise_for_status=True
    ):
        status = response.status_code
        ignore = ignore or []
        custom_messages = custom_messages or {}

        if status in ignore or status in self._ignore_codes:
            return None
        elif response.status_code in custom_messages.keys():
            raise requests.exceptions.HTTPError(custom_messages[response.status_code])
        elif raise_for_status:
            response.raise_for_status()

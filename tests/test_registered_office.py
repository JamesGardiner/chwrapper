import pytest
import requests
import responses

import chwrapper

@responses.activate
def test_registered_office():
    """Searching for a company"s registered address works"""

    results_keys = ["address_line_1", "address_line_2", "locality", "postal_code", "region"]

    with open("tests/registered_address_results.json") as results:
        body = results.read()

    responses.add(
        responses.GET,
        "https://api.companieshouse.gov.uk/company/12345/registered-office-address?access_token=pk.test",
        match_querystring=True,
        status=200,
        body=body,
        content_type="application/json")

    res = chwrapper.CompanyAddress("12345", access_token="pk.test").search()
    assert res.status_code == 200

    for key in sorted(res.json().keys()):
        assert key in results_keys

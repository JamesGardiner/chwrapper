import pytest
import requests
import responses

import chwrapper


@responses.activate
def test_company_search():
    "Searching by company name works"

    with open("tests/results.json") as results:
        body = results.read()

    responses.add(
        responses.GET,
        "https://api.companieshouse.gov.uk/search/companies?access_token=pk.test&q=Python",
        match_querystring=True,
        status=200,
        body=body,
        content_type="application/json")

    res = chwrapper.CompanySearch(access_token="pk.test").search("Python")

    assert res.status_code == 200
    assert sorted(res.json().keys()) == ["items", "items_per_page", "kind", "page_number", "start_index", "total_results"]
    assert sorted(res.json()["items"][0].keys()) == ["address", "company_number", "company_status", "company_type", "date_of_cessation", "date_of_creation", "description", "description_identifier", "kind", "links", "matches", "snippet", "title"]


@responses.activate
def test_officer_search():
    """Searching by officer name works."""

    with open("tests/officer_results.json") as results:
        body = results.read()

    responses.add(
        responses.GET,
        "https://api.companieshouse.gov.uk/search/officers?access_token=pk.test&q=John",
        match_querystring=True,
        status=200,
        body=body,
        content_type="application/json")

    res = chwrapper.OfficerSearch(access_token="pk.test").search("John")

    assert res.status_code == 200
    assert sorted(res.json().keys()) == ["items", "items_per_page", "kind", "page_number", "start_index", "total_results"]
    assert sorted(res.json()["items"][0].keys()) == ["address", "appointment_count", "date_of_birth", "description", "description_identifiers", "kind", "links", "matches", "snippet", "title"]


@responses.activate
def test_company_profile():
    "Getting a company profile works"

    with open("tests/profile_results.json") as results:
        body = results.read()

    responses.add(
        responses.GET,
        "https://api.companieshouse.gov.uk/company/12345?access_token=pk.test",
        match_querystring=True,
        status=200,
        body=body,
        content_type="application/json")

    res = chwrapper.CompanyInfo(access_token="pk.test").get_profile('12345')

    assert res.status_code == 200
    assert sorted(res.json()["accounts"]) == ['accounting_reference_date', 'last_accounts']


@responses.activate
def test_search_officers():
    "Searching for officers by company number works"

    with open("tests/officer_results.json") as results:
        body = results.read()

    responses.add(
        responses.GET,
        "https://api.companieshouse.gov.uk/company/12345/officers?access_token=pk.test",
        match_querystring=True,
        status=200,
        body=body,
        content_type="application/json")

    res = chwrapper.CompanyInfo(access_token="pk.test").get_officers("12345")

    assert res.status_code == 200
    assert sorted(res.json().keys()) == ["items", "items_per_page", "kind", "page_number", "start_index", "total_results"]
    assert sorted(res.json()["items"][0].keys()) == ["address", "appointment_count", "date_of_birth", "description", "description_identifiers", "kind", "links", "matches", "snippet", "title"]

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

    res = chwrapper.CompanyInfo(access_token="pk.test").get_address("12345")
    assert res.status_code == 200

    for key in sorted(res.json().keys()):
        assert key in results_keys

import pytest
import requests
import responses

import chwrapper

@responses.activate
def test_company_search():
    "Searching by company name works"

    with open('tests/results.json') as results:
        body = results.read()

    responses.add(
        responses.GET,
        'https://api.companieshouse.gov.uk/search/companies?access_token=pk.test&q=Python',
        match_querystring=True,
        status=200,
        body=body,
        content_type='application/json')

    res = chwrapper.CompanySearch(access_token="pk.test").search("Python")

    assert res.status_code == 200
    assert sorted(res.json().keys()) == ['items', 'items_per_page', 'kind', 'page_number', 'start_index', 'total_results']
    assert sorted(res.json()['items'][0].keys()) == ['address', 'company_number', 'company_status', 'company_type', 'date_of_cessation', 'date_of_creation', 'description', 'description_identifier', 'kind', 'links', 'matches', 'snippet', 'title']

@responses.activate
def test_officer_search():
    "Searching by officer name works"

    with open('tests/officer_results.json') as results:
        body = results.read()

    responses.add(
        responses.GET,
        'https://api.companieshouse.gov.uk/search/officers?access_token=pk.test&q=John',
        match_querystring=True,
        status=200,
        body=body,
        content_type='application/json')

    res = chwrapper.OfficerSearch(access_token="pk.test").search("John")

    assert res.status_code == 200
    assert sorted(res.json().keys()) == ['items', 'items_per_page', 'kind', 'page_number', 'start_index', 'total_results']
    assert sorted(res.json()['items'][0].keys()) == ['address', 'appointment_count', 'date_of_birth', 'description', 'description_identifiers', 'kind', 'links', 'matches', 'snippet', 'title']

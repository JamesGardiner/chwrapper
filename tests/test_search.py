import responses
import chwrapper


@responses.activate
def test_company_search():
    "Searching by company name works"

    with open("tests/results.json") as results:
        body = results.read()

    responses.add(
        responses.GET,
        "https://api.companieshouse.gov.uk/search/companies?" +
        "access_token=pk.test&q=Python",
        match_querystring=True,
        status=200,
        body=body,
        content_type="application/json")

    res = chwrapper.Search(access_token="pk.test").search_companies("Python")

    assert res.status_code == 200
    assert sorted(res.json().keys()) == ["items",
                                         "items_per_page",
                                         "kind", "page_number",
                                         "start_index",
                                         "total_results"]

    assert sorted(res.json()["items"][0].keys()) == ["address",
                                                     "company_number",
                                                     "company_status",
                                                     "company_type",
                                                     "date_of_cessation",
                                                     "date_of_creation",
                                                     "description",
                                                     "description_identifier",
                                                     "kind",
                                                     "links",
                                                     "matches",
                                                     "snippet",
                                                     "title"]


@responses.activate
def test_officer_appointments():
    "Searching for appointments by officer ID works."

    with open("tests/appointment_results.json") as results:
        body = results.read()

    responses.add(
        responses.GET,
        "https://api.companieshouse.gov.uk/officers/12345/" +
        "appointments?access_token=pk.test",
        match_querystring=True,
        status=200,
        body=body,
        content_type="application/json")

    res = chwrapper.Search(
        access_token="pk.test"
    ).appointments("12345")

    assert res.status_code == 200
    assert sorted(res.json().keys()) == ["items"]
    assert sorted(res.json()["items"][0]) == ['name_elements', 'occupation']


@responses.activate
def test_officer_search():
    """Searching by officer name works."""

    with open("tests/officer_results.json") as results:
        body = results.read()

    responses.add(
        responses.GET,
        "https://api.companieshouse.gov.uk/search/officers?" +
        "access_token=pk.test&q=John",
        match_querystring=True,
        status=200,
        body=body,
        content_type="application/json")

    res = chwrapper.Search(access_token="pk.test").search_officers("John")

    assert res.status_code == 200
    assert sorted(res.json().keys()) == ["items",
                                         "items_per_page",
                                         "kind",
                                         "page_number",
                                         "start_index",
                                         "total_results"]

    assert sorted(res.json()["items"][0].keys()) == ["address",
                                                     "appointment_count",
                                                     "date_of_birth",
                                                     "description",
                                                     "description_identifiers",
                                                     "kind",
                                                     "links",
                                                     "matches",
                                                     "snippet",
                                                     "title"]


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

    res = chwrapper.Search(access_token="pk.test").profile('12345')

    assert res.status_code == 200
    assert sorted(res.json()["accounts"]) == [
        'accounting_reference_date', 'last_accounts']


@responses.activate
def test_search_officers():
    "Searching for officers by company number works"

    with open("tests/officer_results.json") as results:
        body = results.read()

    responses.add(
        responses.GET,
        "https://api.companieshouse.gov.uk/company/12345/officers?" +
        "access_token=pk.test",
        match_querystring=True,
        status=200,
        body=body,
        content_type="application/json")

    res = chwrapper.Search(access_token="pk.test").officers("12345")

    assert res.status_code == 200
    assert sorted(res.json().keys()) == ["items",
                                         "items_per_page",
                                         "kind",
                                         "page_number",
                                         "start_index",
                                         "total_results"]

    assert sorted(res.json()["items"][0].keys()) == ["address",
                                                     "appointment_count",
                                                     "date_of_birth",
                                                     "description",
                                                     "description_identifiers",
                                                     "kind",
                                                     "links",
                                                     "matches",
                                                     "snippet",
                                                     "title"]


@responses.activate
def test_filing_history():
    "Searching for filing history works"

    with open("tests/filing_results.json") as results:
        body = results.read()

    responses.add(
        responses.GET,
        "https://api.companieshouse.gov.uk/company/12345/" +
        "filing-history?access_token=pk.test",
        match_querystring=True,
        status=200,
        body=body,
        content_type="application/json")

    res = chwrapper.Search(access_token="pk.test").filing_history("12345")

    assert res.status_code == 200
    assert sorted(res.json().keys()) == ['filing_history_status',
                                         'items',
                                         'items_per_page',
                                         'start_index',
                                         'total_count']

    assert sorted(res.json()["items"][0].keys()) == ['associated_filings',
                                                     'barcode',
                                                     'category',
                                                     'date',
                                                     'description',
                                                     'links',
                                                     'pages',
                                                     'paper_filed',
                                                     'transaction_id',
                                                     'type']


@responses.activate
def test_filing_transaction():
    "Searching for a specific filing transaction works"

    with open("tests/transaction_results.json") as results:
        body = results.read()

    responses.add(
        responses.GET,
        "https://api.companieshouse.gov.uk/company/12345/" +
        "filing-history/6789jhefD?access_token=pk.test",
        match_querystring=True,
        status=200,
        body=body,
        content_type="application/json")

    res = chwrapper.Search(access_token="pk.test").filing_history(
        "12345", transaction="6789jhefD")

    assert res.status_code == 200
    assert sorted(res.json().keys()) == ['category',
                                         'date',
                                         'description',
                                         'links',
                                         'pages',
                                         'paper_filed',
                                         'transaction_id',
                                         'type']

    assert sorted(res.json()["links"].keys()) == ['document_metadata',
                                                  'self']


@responses.activate
def test_insolvency():
    "Searching for an insolvency works"

    with open("tests/insolvency_results.json") as results:
        body = results.read()

    responses.add(
        responses.GET,
        "https://api.companieshouse.gov.uk/company/12345/" +
        "insolvency?access_token=pk.test",
        match_querystring=True,
        status=200,
        body=body,
        content_type="application/json")

    res = chwrapper.Search(access_token="pk.test").insolvency("12345")

    assert res.status_code == 200
    assert sorted(res.json().keys()) == ['cases', 'etag']
    assert sorted(res.json()["cases"][0].keys()) == [
        'dates', 'number', 'practitioners', 'type']


@responses.activate
def test_charges():
    "Searching for a charge works"

    keys = ['charge_number',
            'classification',
            'created_on',
            'delivered_on',
            'etag',
            'links',
            'particulars',
            'persons_entitled',
            'secured_details',
            'status',
            'transactions']

    with open("tests/charges_results.json") as results:
        body = results.read()

    responses.add(
        responses.GET,
        "https://api.companieshouse.gov.uk/company/" +
        "12345/charges?access_token=pk.test",
        match_querystring=True,
        status=200,
        body=body,
        content_type="application/json")

    res = chwrapper.Search(access_token="pk.test").charges("12345")

    assert res.status_code == 200
    assert sorted(res.json().keys()) == [
        'items',
        'part_satisfied_count',
        'satisfied_count', 'total_count',
        'unfiltered_count']
    assert sorted(res.json()["items"][0].keys()) == keys

    responses.add(
        responses.GET,
        "https://api.companieshouse.gov.uk/company/" +
        "12345/charges/6789jhefD?access_token=pk.test",
        match_querystring=True,
        status=200,
        body=body,
        content_type="application/json")

    res_charge = chwrapper.Search(
        access_token="pk.test").charges("12345", charge_id="6789jhefD")

    assert res_charge.status_code == 200
    assert sorted(res_charge.json().keys()) == [
        'items',
        'part_satisfied_count',
        'satisfied_count', 'total_count',
        'unfiltered_count']
    assert sorted(res_charge.json()["items"][0].keys()) == keys


@responses.activate
def test_registered_office():
    """Searching for a company"s registered address works"""

    results_keys = ["address_line_1", "address_line_2",
                    "locality", "postal_code", "region"]

    with open("tests/registered_address_results.json") as results:
        body = results.read()

    responses.add(
        responses.GET,
        "https://api.companieshouse.gov.uk/company/12345/" +
        "registered-office-address?access_token=pk.test",
        match_querystring=True,
        status=200,
        body=body,
        content_type="application/json")

    res = chwrapper.Search(access_token="pk.test").address("12345")
    assert res.status_code == 200

    for key in sorted(res.json().keys()):
        assert key in results_keys

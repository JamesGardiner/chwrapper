import responses
import chwrapper
import pytest


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
        content_type="application/json",
        adding_headers={'X-Ratelimit-Reset': '1460280499'})

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
        content_type="application/json",
        adding_headers={'X-Ratelimit-Reset': '1460280499'})

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
        content_type="application/json",
        adding_headers={'X-Ratelimit-Reset': '1460280499'})

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
def test_disqualified_officer_search():
    """Searching for disqualified officer by name works."""

    with open("tests/officer_results.json") as results:
        body = results.read()

    responses.add(
        responses.GET,
        "https://api.companieshouse.gov.uk/search/disqualified-officers?" +
        "access_token=pk.test&q=John",
        match_querystring=True,
        status=200,
        body=body,
        content_type="application/json",
        adding_headers={'X-Ratelimit-Reset': '1460280499'})

    s = chwrapper.Search(access_token="pk.test")
    res = s.search_officers("John", disqualified=True)

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
        content_type="application/json",
        adding_headers={'X-Ratelimit-Reset': '1460280499'})

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
        content_type="application/json",
        adding_headers={'X-Ratelimit-Reset': '1460280499'})

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
        content_type="application/json",
        adding_headers={'X-Ratelimit-Reset': '1460280499'})

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
        content_type="application/json",
        adding_headers={'X-Ratelimit-Reset': '1460280499'})

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
        content_type="application/json",
        adding_headers={'X-Ratelimit-Reset': '1460280499'})

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
        content_type="application/json",
        adding_headers={'X-Ratelimit-Reset': '1460280499'})

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
        content_type="application/json",
        adding_headers={'X-Ratelimit-Reset': '1460280499'})

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
        content_type="application/json",
        adding_headers={'X-Ratelimit-Reset': '1460280499'})

    res = chwrapper.Search(access_token="pk.test").address("12345")
    assert res.status_code == 200

    for key in sorted(res.json().keys()):
        assert key in results_keys


@responses.activate
def test_disqualified_natural():
    """Get disqualified natural officers"""

    with open("tests/results.json") as results:
        body = results.read()

    responses.add(
        responses.GET,
        "https://api.companieshouse.gov.uk/disqualified-officers/natural/" +
        "1234?access_token=pk.test",
        match_querystring=True,
        status=200,
        body=body,
        content_type="application/json",
        adding_headers={'X-Ratelimit-Reset': '1460280499'})

    res = chwrapper.Search(access_token="pk.test").disqualified("1234")

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
def test_disqualified_corporate():
    """Get disqualified corporate officers"""

    with open("tests/results.json") as results:
        body = results.read()

    responses.add(
        responses.GET,
        "https://api.companieshouse.gov.uk/disqualified-officers/corporate/" +
        "1234?access_token=pk.test",
        match_querystring=True,
        status=200,
        body=body,
        content_type="application/json",
        adding_headers={'X-Ratelimit-Reset': '1460280499'})

    res = chwrapper.Search(access_token="pk.test").disqualified("1234",
                                                                natural=False)

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


class TestSignificantControl():
    """Test the significant control endpoints"""
    s = chwrapper.Search(access_token="pk.test")

    with open("tests/results.json") as results:
        results = results.read()

    items = ["items",
             "items_per_page",
             "kind",
             "page_number",
             "start_index",
             "total_results"]

    @responses.activate
    def test_list_persons_significant_control(self):
        """Test the list of persons of significant control for a company"""
        responses.add(
            responses.GET,
            ('https://api.companieshouse.gov.uk/company/12345/' +
             'persons-with-significant-control?access_token=pk.test'),
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '1460280499'})

        res = self.s.persons_significant_control('12345')

        assert res.status_code == 200
        assert sorted(res.json().keys()) == self.items

    @responses.activate
    def test_list_persons_significant_control_no_company_number(self):
        """Tests that correct exception raised when no company number used"""
        with pytest.raises(TypeError):
            res = self.s.persons_significant_control()

    @responses.activate
    def test_persons_significant_control_statements_true(self):
        """Test list of persons with significant control statements for a company"""
        responses.add(
            responses.GET,
            ('https://api.companieshouse.gov.uk/company/12345/' +
             'persons-with-significant-control-statements?access_token=pk.test'),
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '1460280499'})

        res = self.s.persons_significant_control('12345', statements=True)

        assert res.status_code == 200
        assert sorted(res.json().keys()) == self.items

    @responses.activate
    def test_persons_significant_control_statements(self):
        """Test list of persons with significant control statements for a
           company when set statements set to False"""
        responses.add(
            responses.GET,
            ('https://api.companieshouse.gov.uk/company/12345/' +
             'persons-with-significant-control?access_token=pk.test'),
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '1460280499'})

        res = self.s.persons_significant_control('12345', statements=False)

        assert res.status_code == 200
        assert sorted(res.json().keys()) == self.items
        assert res.url == ('https://api.companieshouse.gov.uk/company/12345/' +
                           'persons-with-significant-control?' +
                           'access_token=pk.test')

    @responses.activate
    def test_person_significant_control(self):
        """Test single person of significant control for a company"""
        responses.add(
            responses.GET,
            ('https://api.companieshouse.gov.uk/company/12345/' +
             'persons-with-significant-control/individual/12345?access_token=pk.test'),
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '1460280499'})

        res = self.s.significant_control('12345', '12345')

        assert res.status_code == 200
        assert sorted(res.json().keys()) == self.items

    @responses.activate
    def test_person_significant_control_no_company_number(self):
        """Tests that correct exception raised when no company number used"""
        with pytest.raises(TypeError):
            res = self.s.significant_control()

    @responses.activate
    def test_person_significant_control_wrong_entity_string(self):
        """Tests that correct exception raised when wrong entity string used"""
        with pytest.raises(Exception):
            res = self.s.significant_control('12345',
                                             '12345',
                                             entity_type='hello')

    @responses.activate
    def test_legal_persons_significant_control(self):
        """Test legal person of significant control for a company endpoint"""
        responses.add(
            responses.GET,
            ('https://api.companieshouse.gov.uk/company/12345/' +
             'persons-with-significant-control/legal-person/12345' +
             '?access_token=pk.test'),
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '1460280499'})

        res = self.s.significant_control('12345', '12345', 'legal')

        assert res.status_code == 200
        assert sorted(res.json().keys()) == self.items

    @responses.activate
    def test_secure_persons_significant_control(self):
        """Test single secure person of significant control for a company"""
        responses.add(
            responses.GET,
            ('https://api.companieshouse.gov.uk/company/12345/' +
             'persons-with-significant-control/super-secure/12345?' +
             'access_token=pk.test'),
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '1460280499'})

        res = self.s.significant_control('12345', '12345', 'secure')

        assert res.status_code == 200
        assert sorted(res.json().keys()) == self.items

    @responses.activate
    def test_corporates_significant_control(self):
        """Test single corporate entity with significant control for a company"""
        responses.add(
            responses.GET,
            ('https://api.companieshouse.gov.uk/company/12345/' +
             'persons-with-significant-control/corporate-entity/12345?' +
             'access_token=pk.test'),
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '1460280499'})

        res = self.s.significant_control('12345', '12345', 'corporate')

        assert res.status_code == 200
        assert sorted(res.json().keys()) == self.items

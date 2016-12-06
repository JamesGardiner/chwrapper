from datetime import datetime

import chwrapper
import pytest
import responses


class TestSearch():
    """the Service.rate_limit decorator"""
    s = chwrapper.Search(access_token="pk.test")

    with open("tests/results.json") as results:
        results = results.read()

    def current_timestamp(self):
        return int(datetime.timestamp(datetime.utcnow()))

    @responses.activate
    def test_company_search(self):
        "Searching by company name works"

        responses.add(
            responses.GET,
            "https://api.companieshouse.gov.uk/search/companies?" +
            "access_token=pk.test&q=Python",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

        res = self.s.search_companies("Python")
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
    def test_officer_appointments(self):
        """Searching for appointments by officer ID works."""
        responses.add(
            responses.GET,
            "https://api.companieshouse.gov.uk/officers/12345/" +
            "appointments?access_token=pk.test",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

        res = self.s.appointments("12345")
        assert res.status_code == 200

    @responses.activate
    def test_officer_search(self):
        """Searching by officer name works."""
        responses.add(
            responses.GET,
            "https://api.companieshouse.gov.uk/search/officers?" +
            "access_token=pk.test&q=John",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

        res = chwrapper.Search(access_token="pk.test").search_officers("John")
        assert res.status_code == 200

    @responses.activate
    def test_disqualified_officer_search(self):
        """Searching for disqualified officer by name works."""
        responses.add(
            responses.GET,
            "https://api.companieshouse.gov.uk/search/disqualified-officers?" +
            "access_token=pk.test&q=John",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})
        res = self.s.search_officers("John", disqualified=True)
        assert res.status_code == 200

    @responses.activate
    def test_company_profile(self):
        """Getting a company profile works"""
        responses.add(
            responses.GET,
            "https://api.companieshouse.gov.uk/company/12345?access_token=pk.test",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})
        res = self.s.profile('12345')
        assert res.status_code == 200

    @responses.activate
    def test_search_officers(self):
        """Searching for officers by company number works"""
        responses.add(
            responses.GET,
            "https://api.companieshouse.gov.uk/company/12345/officers?" +
            "access_token=pk.test",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})
        res = chwrapper.Search(access_token="pk.test").officers("12345")
        assert res.status_code == 200

    @responses.activate
    def test_filing_history(self):
        """Searching for filing history works"""
        responses.add(
            responses.GET,
            "https://api.companieshouse.gov.uk/company/12345/" +
            "filing-history?access_token=pk.test",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

        res = self.s.filing_history("12345")
        assert res.status_code == 200

    @responses.activate
    def test_filing_transaction(self):
        """Searching for a specific filing transaction works"""
        responses.add(
            responses.GET,
            "https://api.companieshouse.gov.uk/company/12345/" +
            "filing-history/6789jhefD?access_token=pk.test",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

        res = self.s.filing_history("12345", transaction="6789jhefD")
        assert res.status_code == 200

    @responses.activate
    def test_insolvency(self):
        """Searching for an insolvency works"""
        responses.add(
            responses.GET,
            "https://api.companieshouse.gov.uk/company/12345/" +
            "insolvency?access_token=pk.test",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

        res = self.s.insolvency("12345")
        assert res.status_code == 200

    @responses.activate
    def test_charges(self):
        """Searching for a charge works"""
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

        responses.add(
            responses.GET,
            "https://api.companieshouse.gov.uk/company/" +
            "12345/charges?access_token=pk.test",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

        res = self.s.charges("12345")

        assert res.status_code == 200

        responses.add(
            responses.GET,
            "https://api.companieshouse.gov.uk/company/" +
            "12345/charges/6789jhefD?access_token=pk.test",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

        res_charge = self.s.charges("12345", charge_id="6789jhefD")
        assert res_charge.status_code == 200

    @responses.activate
    def test_registered_office(self):
        """Searching for a company's registered address works"""
        responses.add(
            responses.GET,
            "https://api.companieshouse.gov.uk/company/12345/" +
            "registered-office-address?access_token=pk.test",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

        res = self.s.address("12345")
        assert res.status_code == 200

    @responses.activate
    def test_disqualified_natural(self):
        """Get disqualified natural officers"""
        responses.add(
            responses.GET,
            "https://api.companieshouse.gov.uk/disqualified-officers/natural/" +
            "1234?access_token=pk.test",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

        res = self.s.disqualified("1234")

        assert res.status_code == 200

    @responses.activate
    def test_disqualified_corporate(self):
        """Get disqualified corporate officers"""
        responses.add(
            responses.GET,
            "https://api.companieshouse.gov.uk/disqualified-officers/corporate/" +
            "1234?access_token=pk.test",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

        res = self.s.disqualified("1234", natural=False)
        assert res.status_code == 200

    @responses.activate
    def test_getting_document(self):
        """Test for the document requesting method"""
        responses.add(
            responses.GET,
            "https://document-api.companieshouse.gov.uk/document/" +
            "1234/content?access_token=pk.test",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

        res = chwrapper.Search(access_token="pk.test").document("1234")

        assert res.status_code == 200


class TestSignificantControl():
    """Test the significant control endpoints"""
    s = chwrapper.Search(access_token="pk.test")

    def current_timestamp(self):
        return int(datetime.timestamp(datetime.utcnow()))

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
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

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
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

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
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

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
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

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
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

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
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

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
            adding_headers={'X-Ratelimit-Reset': '{}'.format(self.current_timestamp())})

        res = self.s.significant_control('12345', '12345', 'corporate')

        assert res.status_code == 200
        assert sorted(res.json().keys()) == self.items

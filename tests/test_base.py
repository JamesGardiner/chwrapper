from datetime import datetime
from datetime import timezone

import pytest
import requests
import responses

import chwrapper


def test_service_session():
    """Get a session using an api."""
    session = chwrapper.Service().get_session("pk.test")
    assert session.params.get("access_token") == "pk.test"


def test_service_session_env():
    """Get a session using the env's token."""
    session = chwrapper.Service().get_session(env={"CompaniesHouseKey": "pk.test_env"})
    assert session.params.get("access_token") == "pk.test_env"


def test_service_session_os_environ(monkeypatch):
    """Get a session using os.environ's token."""
    monkeypatch.setenv("CompaniesHouseKey", "pk.test_os_environ")
    session = chwrapper.Service().get_session()
    assert session.params.get("access_token") == "pk.test_os_environ"
    monkeypatch.undo()


def test_service_session_os_environ_caps(monkeypatch):
    """Get a session using os.environ's token."""
    monkeypatch.setenv("COMPANIES_HOUSE_KEY", "pk.test_os_environ")
    session = chwrapper.Service().get_session()
    assert session.params.get("access_token") == "pk.test_os_environ"
    monkeypatch.undo()


def test_product_token():
    """Get the product version."""
    token = chwrapper.Service().product_token
    assert token == "chwrapper/{0}".format(chwrapper.__version__)


def test_user_agent():
    """Check User-agent correctly assigned."""
    session = chwrapper.Service().get_session()
    assert session.headers["User-Agent"].startswith("chwrapper")
    assert "python-requests" in session.headers["User-Agent"]


@responses.activate
def test_custom_messages():
    """Check status code error messaging."""
    fakeurl = "https://example.com"
    responses.add(
        responses.GET,
        fakeurl,
        status=401,
        adding_headers={"X-Ratelimit-Reset": "1460280499"},
    )

    service = chwrapper.Service()
    response = service.get_session().get(fakeurl)

    with pytest.raises(requests.exceptions.HTTPError) as exc:
        service.handle_http_error(response, custom_messages={401: "error"})
    try:
        assert exc.value.message == "error"
    except AttributeError:
        assert "error" in exc.value.args[0]

    with pytest.raises(requests.exceptions.HTTPError) as exc:
        assert service.handle_http_error(response, raise_for_status=True)
    try:
        assert "401" in exc.value.message
    except AttributeError:
        assert "401" in exc.value.args[0]


@responses.activate
def test_custom_ignore_codes():
    """Check custom codes are ignored correctly."""
    fakeurl = "https://example.com"
    responses.add(
        responses.GET,
        fakeurl,
        status=429,
        adding_headers={"X-Ratelimit-Reset": "1460280499"},
    )

    service = chwrapper.Service()
    response = service.get_session().get(fakeurl)

    assert service._ignore_codes == []

    service._ignore_codes.append(429)
    assert 429 in service._ignore_codes

    ret = service.handle_http_error(response, raise_for_status=True)
    assert ret is None


@responses.activate
def test_custom_ignore_codes_raised():
    """Check custom codes are ignored correctly."""
    fakeurl = "https://example.com"
    responses.add(
        responses.GET,
        fakeurl,
        status=429,
        adding_headers={"X-Ratelimit-Reset": "1460280499"},
    )

    service = chwrapper.Service()
    response = service.get_session().get(fakeurl)

    assert service._ignore_codes == []
    assert 429 not in service._ignore_codes

    with pytest.raises(requests.exceptions.HTTPError):
        service.handle_http_error(response, raise_for_status=True)


@responses.activate
def test_no_custom_messages():
    """Check status code, when custom_messages is empty."""
    url = "https://api.companieshouse.gov.uk/search/companies"
    responses.add(
        responses.GET, url, status=401, adding_headers={"X-Ratelimit-Remain": "1"}
    )

    service = chwrapper.Service()
    response = service.get_session().get(url)

    with pytest.raises(requests.exceptions.HTTPError) as exc:
        assert service.handle_http_error(response)
    assert "401" in exc.value.args[0]


class TestRateLimiting:
    """The Service.rate_limit decorator."""
    current_timestamp = int(datetime.timestamp(datetime.now(timezone.utc)))

    s = chwrapper.Search(access_token="pk.test")

    with open("tests/results.json") as results:
        results = results.read()

    @responses.activate
    def test_rate_limit_renewal_missing(self):
        """Test execution continues when rate limit exceeded"""
        responses.add(
            responses.GET,
            "https://api.companieshouse.gov.uk/search/companies?"
            + "access_token=pk.test&q=Python",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={"X-Ratelimit-Remain": "0"},
        )

        with pytest.raises(KeyError):
            _ = self.s.search_companies("Python")

    @responses.activate
    def test_rate_limit_expired(self):
        """Test error raised if rate limit exceeded and no reset time."""
        responses.add(
            responses.GET,
            "https://api.companieshouse.gov.uk/search/companies?"
            + "access_token=pk.test&q=Python",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={"X-Ratelimit-Remain": "0"},
        )

        with pytest.raises(KeyError):
            _ = self.s.search_companies("Python")

    @responses.activate
    def test_rate_limit_renewal(self):
        """Test execution continues when rate limit exceeded."""
        responses.add(
            responses.GET,
            "https://api.companieshouse.gov.uk/search/companies?"
            + "access_token=pk.test&q=Python",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={
                "X-Ratelimit-Remain": "0",
                "X-Ratelimit-Reset": "{}".format(self.current_timestamp),
            },
        )

        res = self.s.search_companies("Python")
        assert res.status_code == 200

    @responses.activate
    def test_negative_time_raises_error_rate_limit(self):
        """Test that negative time values raise a ValueError Exception."""
        time_ten_seconds_ago = self.current_timestamp - 10
        responses.add(
            responses.GET,
            "https://api.companieshouse.gov.uk/search/companies?"
            + "access_token=pk.test&q=Python",
            match_querystring=True,
            status=200,
            body=self.results,
            content_type="application/json",
            adding_headers={
                "X-Ratelimit-Remain": "0",
                "X-Ratelimit-Reset": "{}".format(time_ten_seconds_ago),
            },
        )

        with pytest.raises(ValueError):
            _ = self.s.search_companies("Python")

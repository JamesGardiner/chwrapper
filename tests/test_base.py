import pytest
import requests
import responses

import chwrapper


def test_Service_session():
    """Get a session using an api"""
    session = chwrapper.Service().get_session('pk.test')
    assert session.params.get('access_token') == 'pk.test'


def test_Service_session_env():
    """Get a session using the env's token"""
    session = chwrapper.Service().get_session(
        env={'CompaniesHouseKey': 'pk.test_env'})
    assert session.params.get('access_token') == 'pk.test_env'


def test_Service_session_os_environ(monkeypatch):
    """Get a session using os.environ's token"""
    monkeypatch.setenv('CompaniesHouseKey', 'pk.test_os_environ')
    session = chwrapper.Service().get_session()
    assert session.params.get('access_token') == 'pk.test_os_environ'
    monkeypatch.undo()


def test_Service_session_os_environ_caps(monkeypatch):
    """Get a session using os.environ's token"""
    monkeypatch.setenv('COMPANIES_HOUSE_KEY', 'pk.test_os_environ')
    session = chwrapper.Service().get_session()
    assert session.params.get('access_token') == 'pk.test_os_environ'
    monkeypatch.undo()


def test_product_token():
    """Get the product version"""
    assert chwrapper.Service().product_token == 'chwrapper/{0}'.format(chwrapper.__version__)


def test_user_agent():
    """Check User-agent correctly assigned"""
    session = chwrapper.Service().get_session()
    assert session.headers['User-Agent'].startswith('chwrapper')
    assert 'python-requests' in session.headers['User-Agent']


@responses.activate
def test_custom_messages():
    """Check status code error messaging"""
    fakeurl = 'https://example.com'
    responses.add(responses.GET,
                  fakeurl,
                  status=401,
                  adding_headers={'X-Ratelimit-Reset': '1460280499'})

    Service = chwrapper.Service()
    response = Service.get_session().get(fakeurl)

    with pytest.raises(requests.exceptions.HTTPError) as exc:
        assert Service.handle_http_error(response,
                                         custom_messages={401: "error"})
        assert exc.value.message == 'error'

    with pytest.raises(requests.exceptions.HTTPError) as exc:
        assert Service.handle_http_error(response, raise_for_status=True)
        assert "401" in exc.value.message


@responses.activate
def test_no_custom_messages():
    """Check status code, when custom_messages is empty"""
    url = 'https://api.companieshouse.gov.uk/search/companies'
    responses.add(responses.GET, url, status=401)

    Service = chwrapper.Service()
    response = Service.get_session().get(url)

    with pytest.raises(requests.exceptions.HTTPError) as exc:
        assert Service.handle_http_error(response)
    assert "401" in exc.value.args[0]

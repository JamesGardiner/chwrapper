[![Build Status](https://travis-ci.org/JamesGardiner/chwrapper.svg?branch=master)](https://travis-ci.org/JamesGardiner/companies-house)
[![Coverage Status](https://coveralls.io/repos/github/JamesGardiner/chwrapper/badge.svg?branch=master)](https://coveralls.io/github/JamesGardiner/chwrapper?branch=master)
# chwrapper
A python wrapper around the [Companies House UK API](https://developer.companieshouse.gov.uk/api/docs/). Returns [requests.Response objects](http://docs.python-requests.org/en/latest/api/#requests.Response).

## Example usage

```python
>>> import chwrapper
>>> search_client = chwrapper.Search(access_token='secret_token')
>>> response = search_client.search_companies('dyson')
>>> response.json()
{'items': [{'address': {'address_line_1': 'Malmesbury',
    'locality': 'Wiltshire',
    'postal_code': 'SN16 0RP',
    'premises': 'Tetbury Hill'},
   'address_snippet': 'Tetbury Hill, Malmesbury, Wiltshire, SN16 0RP',
   'company_number': '03772814',
   'company_status': 'active',
   'company_type': 'ltd',
   'date_of_creation': '1999-05-18',
   'description': '03772814 - Incorporated on 18 May 1999',
   'description_identifier': ['incorporated-on'],
   'kind': 'searchresults#company',
   'links': {'self': '/company/03772814'},
   'matches': {'snippet': [1, 5, 20, 24], 'title': [1, 5]},
   'snippet': 'DYSON TECHNOLOGY · DYSON ',
   'title': 'DYSON JAMES LIMITED'},...]}
```

For further details, see the docs:

http://chwrapper.readthedocs.org/en/latest/

## Supported Endpoints
- [**Search for companies by name**] (http://chwrapper.readthedocs.io/en/latest/user/api.html#chwrapper.Search.search_companies)

- [**Search for officers by name**] (http://chwrapper.readthedocs.io/en/latest/user/api.html#chwrapper.Search.search_officers)

- [**Search for officer appointments by officer number**] (http://chwrapper.readthedocs.io/en/latest/user/api.html#chwrapper.Search.appointments)

- [**Search for company addresses by company number**] (http://chwrapper.readthedocs.io/en/latest/user/api.html#chwrapper.Search.address)

- [**Search for company profile by company number**] (http://chwrapper.readthedocs.io/en/latest/user/api.html#chwrapper.Search.profile)

- [**Search for insolvency records by company number**] (http://chwrapper.readthedocs.io/en/latest/user/api.html#chwrapper.Search.insolvency)

- [**Search for a company's filing history**] (http://chwrapper.readthedocs.io/en/latest/user/api.html#chwrapper.Search.filing_history)

- [**Search for charges against a company**] (http://chwrapper.readthedocs.io/en/latest/user/api.html#chwrapper.Search.charges)

- [**Search for officers registered against a company**] (http://chwrapper.readthedocs.io/en/latest/user/api.html#chwrapper.Search.officers)

- [**Search for disqualified officers by their ID number**] (http://chwrapper.readthedocs.io/en/latest/user/api.html#chwrapper.Search.disqualified)

- [**Search for all persons of significant control of a company**] (http://chwrapper.readthedocs.io/en/latest/user/api.html#chwrapper.Search.persons_significant_control)

- [**Search for a single person with significant control of a company**] (http://chwrapper.readthedocs.io/en/latest/user/api.html#chwrapper.Search.significant_control)

- [**Search for documents by document ID**] (http://chwrapper.readthedocs.io/en/latest/user/api.html#chwrapper.Search.documents)

## Installation

### Get the Code
chwrapper is available on [PyPi](https://pypi.python.org/pypi/chwrapper/0.2.0). Just `pip install chwrapper`.

chwrapper is also available on [GitHub](https://github.com/JamesGardiner/chwrapper).

You can either clone the public repository:
```bash
$ git clone git://github.com/JamesGardiner/chwrapper.git
```
Download the [tarball](https://github.com/nestauk/gtr/tarball/master)
```bash
$ curl -OL https://github.com/JamesGardiner/chwrapper/tarball/master
```
Or, download the zipball:
```bash
$ curl -OL https://github.com/nestauk/gtr/zipball/master
```
Once you have a copy of the source, you can install it into your Python package, or install it into your site-packages easily:
```bash
$ python setup.py install
```


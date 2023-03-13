.. _quickstart:

Quickstart
==========

Here is a quick introduction to chwrapper.

First, make sure that:

* chwrapper is :ref:`installed <install>`

Creating a search object with chwrapper is simple.
Begin by importing the chwrapper module::

    >>> import chwrapper

And then create a Search object ::

    >>> s = chwrapper.Search(access_token="12345")

This creates a :class:`Search <chwrapper.services.search.Search>` object
called ``s``.

An access token can be obtained from `Companies House
<https://developer.companieshouse.gov.uk/api/docs/index/gettingStarted.html>`_
and can either be passed explicitly to the Search object, or implicitly
as an environment variable called :code:`COMPANIES_HOUSE_KEY` or :code:`CompaniesHouseKey`.

To query the API, we can use the Search object's methods. For example::

    >>> r = s.search_companies("1234567")
    >>> r.status_code
    200
    >>> r.json
    {'start_index': 0, 'kind': 'search#companies', 'page_number': 1,
    'total_results': 1,...}

All the Search class methods can be found in the :ref:`api`.


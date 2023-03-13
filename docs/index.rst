chwrapper
=========================

Release v\ |version|. (:ref:`Installation <install>`)

chwrapper is a simple python wrapper around the `Companies House API
<https://developer.companieshouse.gov.uk/api/docs/>`_

::

    >>> import chwrapper
    >>> s = chwrapper.Search()
    >>> r = s.search_officers("John Smith")
    >>> r.status_code
    200
    >>> r.headers['content-type']
    'application/json'
    >>> r.json()
    {'kind': 'search#officers', 'items_per_page': 20, 'start_index': 0,
    'total_results': 731629,...}


User Guide
----------

.. toctree::
   :maxdepth: 2

   user/install
   user/quickstart
   user/api

Contributor Guide
-----------------

I'd welcome contributions from the community. See CONTRIBUTING.md for more info.:

.. toctree::
   :maxdepth: 2

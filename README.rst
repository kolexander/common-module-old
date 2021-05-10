===========
GRC common
===========

GRC common is a Django app to conduct GRC common info.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "common" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'grc_common',
        'grc_account
    ]

2. Add "USER_TYPE" setting to your django setting like this::

    USER_TYPE = 0
    # 0 - applicant
    # 1 - employer

3. Include the polls URLconf in your project urls.py like this::

    path('common/', include('grc_common.urls')),
    path('account/', include('grc_account.urls')),
    
4. Add account model

    TBD

4. Run ``python manage.py migrate`` to create the commons models.

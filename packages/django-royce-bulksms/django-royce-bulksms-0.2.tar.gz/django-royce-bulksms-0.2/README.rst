=====
Django Royce Bulksms
=====

Integrate Bulk sms into your project in under 2 minutes


Quick start
-----------

1. Add "roycebulksms" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'roycebulksms',
    ]

2. Include the roycebulksms URLconf in your project urls.py like this::

    path('bulksms/', include('roycebulksms.urls')),

3. Run ``python manage.py migrate`` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
    (you'll need to be authenticated to access bulk sms UI).

5. Visit http://127.0.0.1:8000/polls/ to participate in the poll.
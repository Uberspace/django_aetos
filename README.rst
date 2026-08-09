Django Aetos
============

A Django app to expose metrics to be scraped by prometheus.io.

Usage
-----

First, install django-aetos:

.. code-block:: python

    pip install django-aetos

then, add the app to `settings.py`:

.. code-block:: python

    INSTALLED_APPS = [
        # ... other apps ...
        "django_aetos",
        # ... other apps ...
    ]

configure aetos in `settings.py`:

    ℹ️ **Important**: When using `django-aetos` in a project behind a reverse proxy, include `django-xff <https://pypi.org/project/django-xff/>`_ in your project, so that a request's `REMOTE_ADDR` header gets rewritten to the correct client ip.

.. code-block:: python

    # on enabled ip allowlist with empty list, requests are denied
    AETOS_ENABLE_IP_ALLOWLIST = True
    AETOS_IP_ALLOWLIST = ["127.0.0.1"]

    # enables authentication via bearer token
    # if enabled with empty list, requests are denied
    AETOS_ENABLE_AUTH = True
    AETOS_AUTH_TOKENLIST = ["ooy9Evuth0zahka"]

and send requests to `/metrics` to Aetos in your `urls.py`:

.. code-block:: python

    from django.urls import include

    urlpatterns = [
        path("", include("django_aetos.urls")),
        # ... your other patterns ...
    ]

Then, add your own metrics using the `@metric_collector` decorator.
Your signal handler can return multiple metrics, each represented as a dict
within a list of generator.

Your `src/app/signals.py`:

.. code-block:: python

    from django_aetos.signals import metric_collector


    @metric_collector(category="cheap")
    def metric_universes_count(sender, **kwargs):
        yield {
            "name": "universes_count",
            "help": "Total number of universes",
            "type": "counter",
            "value": 1,
        }


    @metric_collector(category="expensive")
    def metric_complex_calculation(sender, **kwargs):
        yield {
            "name": "complex_metric",
            "help": "An expensive calculation",
            "type": "gauge",
            "value": some_expensive_database_query(),
        }

You can do anything you like here, like make database queries or look at files
in the filesystem.

**Multiple Metric Endpoints**

Metrics are organized by category. You can scrape different categories at different intervals:

- `/metrics` - Returns ALL metrics (all categories combined)
- `/metrics/cheap` - Returns only metrics tagged with `category="cheap"`
- `/metrics/expensive` - Returns only metrics tagged with `category="expensive"`

This allows you to scrape cheap metrics frequently and expensive metrics less often.

Categories are arbitrary strings - use any names that make sense for your use case
(e.g., "fast", "slow", "realtime", "daily", etc.).

**Legacy Pattern**

The old signal-based pattern still works for backward compatibility:

.. code-block:: python

    from django.dispatch import receiver
    from django_aetos.signals import collect_metrics


    @receiver(collect_metrics, dispatch_uid='metric_legacy')
    def metric_legacy(sender, **kwargs):
        yield {
            "name": "legacy_metric",
            "help": "Using the old pattern",
            "type": "counter",
            "value": 42,
        }

Metrics registered this way appear on `/metrics` but not on category-specific endpoints.

To make sure your receiver actually connects, add an import to your
`src/app/apps.py`:

.. code-block:: python

    from django.apps import AppConfig

    class YourAppConfig(AppConfig):
        name = "yourapp"

        def ready(self):
            from . import signals  # NOQA

Dev Setup
---------

.. code-block::

    python3 -m venv venv
    source venv/bin/activate
    make setup
    make install-dev

Testing
---------

.. code-block::

    make test

Packaging
---------

.. code-block::

    git pull
    make bump-version part=minor
    git push origin main v$(bump-my-version show current_version)

.. code-block::

    make build
    make upload-test

once the package looks good, run `make upload`.

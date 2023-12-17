Django Aetos
============

A Django app to expose metrics to be scraped by prometheus.io.

Usage
-----

First, add the app to `settings.py`:

.. code-block:: python

    INSTALLED_APPS = [
        # ... other apps ...
        "aetos",
        # ... other apps ...
    ]

and send requests to `/metrics` to Aetos in your `urls.py`:

.. code-block:: python

    from django.urls import include

    urlpatterns = [
        path("", include("django_aetos.urls")),
        # ... your other patterns ...
    ]

Then, add your own metrics. To do this, listen for the `collect_metrics` signal.
Refer to [the django docs](https://docs.djangoproject.com/en/dev/topics/signals/)
on details how to do this.

Your signal handler can return multiple metrics, each represented as a dict
within a list of generator.

Your `src/app/signals.py`:

.. code-block:: python

    from django.dispatch import receiver

    from django_aetos.signals import collect_metrics


    @receiver(collect_metrics, dispatch_uid='metric_universes_count')
    def metric_universes_count(sender, **kwargs):
        yield {
            "name": f"universes_count",
            "help": f"Total number of universes",
            "type": "counter",
            "value": 1,
        }

You can do anything you like here, like make database queries or look at files
in the filesystem.

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

    make build
    make upload-test

once the package looks good, run `make upload`.

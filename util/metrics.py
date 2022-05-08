from prometheus_client import Gauge, make_wsgi_app
from prometheus_client.core import CollectorRegistry
from werkzeug.middleware.dispatcher import DispatcherMiddleware

METRICS_REGISTRY = CollectorRegistry()
FAMILIES = {}


def make_per_generator_gauge(name, description):
    return Gauge(name, description, ["generator_name"])


CACHE_GAUGES = [
    make_per_generator_gauge(
        "aga_cache_hits",
        "asset-gen-api cache hits",
    ),
    make_per_generator_gauge(
        "aga_cache_misses",
        "asset-gen-api cache misses",
    ),
    make_per_generator_gauge(
        "aga_cache_maxsize",
        "asset-gen-api cache maxsize",
    ),
    make_per_generator_gauge(
        "aga_cache_currsize",
        "asset-gen-api cache currsize",
    )
]


def init():
    for g in CACHE_GAUGES:
        METRICS_REGISTRY.register(g)


def route(app):
    app.wsgi_app = DispatcherMiddleware(
        app.wsgi_app, {
            "/metrics": make_wsgi_app(METRICS_REGISTRY)
        }
        )


def add_run_cache_stats(func, name):
    for i, g in enumerate(CACHE_GAUGES):
        # haha, scope go brr
        def make_set_func(info_idx):
            def set_func():
                value = func.cache_info()[info_idx]
                return -1 if value is None else value

            return set_func

        g.labels(generator_name=name).set_function(make_set_func(i))

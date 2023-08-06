"""
The full documentation is avaiable here: https://docs.optimeering.no/

These are the functions available when importing __archimedes__.

Example usage:
>>> archimedes.list_ids()
...prints list of available time series
"""

from archimedes.auth import get_auth
from archimedes.configuration import ArchimedesConstants  # config
from archimedes.data.api import (
    forecast_diff,
    forecast_get,
    forecast_get_by_ref_time_interval,
    forecast_list_ref_times,
    get,
    get_intraday_trades,
    get_latest,
    get_predictions,
    get_predictions_ref_dts,
    list_ids,
    list_prediction_ids,
    list_series_price_areas,
    store_prediction,
    store_predictions,
)
from archimedes.utils import compact_print, environ, full_print

__all__ = [
    "ArchimedesConstants",
    "get_auth",
    "compact_print",
    "full_print",
    "environ",
    "get",
    "get_intraday_trades",
    "get_latest",
    "list_ids",
    "list_series_price_areas",
    "get_predictions",
    "get_predictions_ref_dts",
    "list_prediction_ids",
    "store_prediction",
    "store_predictions",
    "forecast_list_ref_times",
    "forecast_get",
    "forecast_diff",
    "forecast_get_by_ref_time_interval",
]

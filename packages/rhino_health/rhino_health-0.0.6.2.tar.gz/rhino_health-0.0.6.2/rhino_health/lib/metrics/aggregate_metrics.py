from itertools import chain
from typing import List

from funcy import compact

from rhino_health.lib.metrics.base_metric import MetricResponse, MetricResultDataType

AGGREGATION_METHOD = "aggregation_method"
"""@autoapi False"""


def sum_aggregation(
    metric: str, metric_results: List[MetricResultDataType]
) -> MetricResultDataType:
    return {metric: sum([metric_result.get(metric, 0) for metric_result in metric_results])}


def weighted_average(
    metric: str, metric_results: List[MetricResultDataType], count_variable="variable"
) -> MetricResultDataType:
    total_count = sum(
        [metric_result.get(f"{count_variable}_count", 0) for metric_result in metric_results]
    )
    return {
        metric: (
            sum(
                [
                    metric_result.get(f"{count_variable}_count", 0) * metric_result.get(metric, 0)
                    for metric_result in metric_results
                ]
            )
            / total_count
        )
    }


def standard_deviation(
    metric: str, metric_results: List[MetricResultDataType]
) -> MetricResultDataType:
    raise NotImplementedError  # TODO


# TODO: Add support/config for >1 variable/metric return and non default var names
SUPPORTED_AGGREGATE_METRICS = {
    "mean": {AGGREGATION_METHOD: weighted_average},
    "count": {AGGREGATION_METHOD: sum_aggregation},
    "std": {AGGREGATION_METHOD: standard_deviation},
}
"""
A dictionary of metrics we currently support aggregating to configuration information.
See the keys for the latest list of metrics.
"""


def calculate_aggregate_metric(
    metric_configuration, metric_results: List[MetricResultDataType]
) -> MetricResultDataType:
    metric = metric_configuration.metric_name()
    if metric not in SUPPORTED_AGGREGATE_METRICS:
        raise ValueError("Unsupported metric for aggregation")
    aggregation_method = SUPPORTED_AGGREGATE_METRICS[metric][AGGREGATION_METHOD]
    if metric_configuration.group_by is None:
        return aggregation_method(metric, metric_results)
    else:
        # We get the unique group names from the data to iterate over since not all sites have all groups
        groups = set(chain.from_iterable(metric_result.keys() for metric_result in metric_results))
        grouped_results = {}
        for group in groups:
            group_result = compact(
                [metric_result.get(group, None) for metric_result in metric_results]
            )
            grouped_results[group] = aggregation_method(metric, group_result)
        return grouped_results

import json
from typing import List

import typer

from bigeye_cli.functions import cli_api_conf_factory
from bigeye_sdk.client.datawatch_client import CoreDatawatchClient
from bigeye_sdk.client.enum import Method
from bigeye_sdk.functions.core_py_functs import int_enum_enum_list_joined
from bigeye_sdk.generated.com.torodata.models.generated import TimeIntervalType, MetricConfiguration, TimeInterval
from bigeye_sdk.log import get_logger

log = get_logger(__file__)

app = typer.Typer(help='Workspace Commands for Bigeye CLI')


# @app.command()
# def unschedule_all_metrics(
#         bigeye_conf: str = typer.Option(
#             ...
#             , "--bigeye_conf"
#             , "-b"
#             , help="Bigeye Basic Auth Configuration File")
# ):
#     api_conf = cli_api_conf_factory(bigeye_conf)
#     client = CoreDatawatchClient(api_conf=api_conf)
#
#     wids: List[int] = [s.id for s in client.get_sources().sources]
#
#     where = WhereClause(source_ids=wids)
#
#     schedule = TimeInterval(interval_value=99999999, interval_type=TimeIntervalType.DAYS_TIME_INTERVAL_TYPE)
#
#     mc = MetricConfiguration(schedule_frequency=schedule)
#
#     client.bulk_update_metrics(where=where, edit_request=mc)


@app.command()
def unschedule_all_metrics(
        bigeye_conf: str = typer.Option(
            ...
            , "--bigeye_conf"
            , "-b"
            , help="Bigeye Basic Auth Configuration File")
):
    api_conf = cli_api_conf_factory(bigeye_conf)
    client = CoreDatawatchClient(api_conf=api_conf)

    wids: List[int] = [s.id for s in client.get_sources().sources]

    # Could do bulk change by wid and metric type which are necessary in the api call.
    mcs: List[dict] = [mil.metric_configuration.to_dict()
                       for mil in client.get_metric_info_batch_post(warehouse_ids=wids).metrics]

    mc = MetricConfiguration()
    ti = TimeInterval()
    ti.interval_type = TimeIntervalType.DAYS_TIME_INTERVAL_TYPE
    ti.interval_value = 0
    mc.schedule_frequency = ti

    log.info(mc.to_json())

    ## TODO: this is an antipattern.  is there another way to set the value to 0?
    mc_dict = mc.to_dict()
    mc_dict['scheduleFrequency']['intervalValue'] = 0

    log.info(json.dumps(mc_dict))

    url = '/api/v1/metrics/batch'

    response = client._call_datawatch(Method.PUT, url=url, body=json.dumps(mc))


@app.command()
def schedule_all_metrics(
        bigeye_conf: str = typer.Option(
            None
            , "--bigeye_conf"
            , "-b"
            , help="Bigeye Basic Auth Configuration File"),
        time_interval_type: int = typer.Option(
            TimeIntervalType.HOURS_TIME_INTERVAL_TYPE.value
            , "--time_interval_type"
            , "-type"
            , help=f"Time interval type.\n {int_enum_enum_list_joined(enum=TimeIntervalType)}"),
        interval_value: int = typer.Option(
            ...
            , "--interval_value"
            , "-value"
            , help="Number of intervals to set on all metric schedules.  If 0 use unschedule all metrics.")
):
    """Schedule all metrics in a workspace."""
    api_conf = cli_api_conf_factory(bigeye_conf)
    client = CoreDatawatchClient(api_conf=api_conf)

    tit = TimeIntervalType(time_interval_type)

    wids: List[int] = [s.id for s in client.get_sources().sources]

    # Could do bulk change by wid and metric type which are necessary in the api call.
    mcs: List[dict] = [mil.metric_configuration.to_dict()
                       for mil in client.get_metric_info_batch_post(warehouse_ids=wids).metrics]

    for mc in mcs:
        mc["scheduleFrequency"] = {
            "intervalType": tit.name,
            "intervalValue": interval_value
        }

        url = "/api/v1/metrics"

        response = client._call_datawatch(Method.POST, url=url, body=json.dumps(mc))


# @app.command()
# def create(host_url: str = typer.Option(
#     'https://staging.bigeye.com'
#     , "--host_url"
#     , "-url"
#     , help="Base host url of the bigeye stack.")
#         , company: str = typer.Option(
#             ...
#             , "--company_name"
#             , "-cname"
#             , help="Company Name")
#         , name: str = typer.Option(
#             ...
#             , "--user_name"
#             , "-un"
#             , help="User name of owner.")
#         , email: str = typer.Option(
#             ...
#             , "--user_email"
#             , "-email"
#             , help="Email of owner.")
# ):
#     """Create a workspace"""
#     url = "/user/create/form"
#     fq_url = f'{host_url}{url}'
#
#     response = requests.post(fq_url
#                              , headers={"Content-Type": "application/json", "Accept": "application/json"}
#                              , data=json.dumps(locals())
#                              )
#
#     log.info(response.json())

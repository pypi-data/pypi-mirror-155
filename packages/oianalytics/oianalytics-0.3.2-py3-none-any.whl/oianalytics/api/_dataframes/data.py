from typing import Optional, Union, List
from datetime import datetime, timedelta

import pandas as pd

from .. import _credentials
from .. import endpoints
from .. import utils

__all__ = [
    "get_data_list",
    "get_time_values",
    "get_batch_values",
    "get_multiple_data_values",
    "insert_time_values",
]


def get_data_list(
    query: Optional[str] = None,
    types: Optional[List[str]] = None,
    measurement_id: Optional[str] = None,
    measurement_name: Optional[str] = None,
    tag_value_id: Optional[List[str]] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    get_all_pages: bool = True,
    multithread_pages: bool = True,
    expand_measurement: bool = True,
    extract_from_storage_unit: Optional[str] = "label",
    extract_from_tags: Optional[str] = "value",
    expand_tags: bool = True,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """
    Get the configured data from the OIAnalytics API

    Parameters
    ----------
    query: str, optional
        A text to search for specific data
    types: list of str, optional
        An array of types to search for specific data types. If omitted then all types are considered.
    measurement_id: str, optional
        The measurement id all data should have. Cannot be used in conjunction with 'measurement_name'.
    measurement_name: str, optional
        The measurement name all data should have. Cannot be used in conjunction with 'measurement_id'.
    tag_value_id: list of str, optional
        An array of tag value ids the data should have.
    page: int, optional
        Page number to retrieve. If None, the first page will be retrieved.
        The argument is ignored if 'get_all_pages' is True.
    page_size: int, optional
        The size of each page to retrieve. By default, 20 elements are retrieved.
        The argument is ignored if 'get_all_pages' is True.
    get_all_pages: bool, default True
        If True, paging is ignored and all elements are retrieved.
    multithread_pages: bool, default False
        Only used when getting all pages. If True, pages are retrieved in multiple threads simultaneously.
    expand_measurement: bool, default True
        Whether or not measurement information should be expanded into multiple columns.
    extract_from_storage_unit: {'id', 'label', None}, default 'label'
        What field should be extracted from storage unit information. If None, the full dictionary is kept.
    extract_from_tags: {'id', 'value', None}, default 'value'
        What field should be extracted for naming tags. If None, the full dictionary is kept.
    expand_tags: bool, default True
        Whether or not tags should be expanded into multiple columns.
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    A DataFrame listing data and their properties
    """

    # Args validation
    if extract_from_storage_unit not in ["id", "label", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_storage_unit': {extract_from_storage_unit}"
        )

    if extract_from_tags not in ["id", "value", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_tags': {extract_from_tags}"
        )

    # Init
    if get_all_pages is True:
        page = 0
        page_size = 500

    def get_page(page_num: int):
        page_response = endpoints.data.get_data_list(
            query=query,
            types=types,
            measurement_id=measurement_id,
            measurement_name=measurement_name,
            tag_value_id=tag_value_id,
            page=page_num,
            page_size=page_size,
            api_credentials=api_credentials,
        )
        return page_response

    def parse_page(page_response: dict):
        page_df = pd.DataFrame(page_response["content"])

        # Expected columns if content is empty
        if page_df.shape[0] == 0:
            page_df = pd.DataFrame(
                columns=[
                    "dataType",
                    "id",
                    "reference",
                    "description",
                    "measurement",
                    "tags",
                ]
            )

        # Format dataframe
        if expand_measurement is True:
            page_df = utils.expand_dataframe_column(
                page_df,
                "measurement",
                expected_keys=[
                    "id",
                    "name",
                    "storageUnit",
                    "defaultUnitFamily",
                    "quantityName",
                ],
            )

            if extract_from_storage_unit == "id":
                page_df["measurement_storageUnit"] = page_df[
                    "measurement_storageUnit"
                ].apply(lambda su: su["id"])
            elif extract_from_storage_unit == "label":
                page_df["measurement_storageUnit"] = page_df[
                    "measurement_storageUnit"
                ].apply(lambda su: su["label"])

        # Extract from tags
        if extract_from_tags == "id":
            page_df["tags"] = page_df["tags"].apply(
                lambda tl: {t["tagKey"]["id"]: t["id"] for t in tl}
            )
        elif extract_from_tags == "value":
            page_df["tags"] = page_df["tags"].apply(
                lambda tl: {t["tagKey"]["key"]: t["value"] for t in tl}
            )

        if expand_tags is True and extract_from_tags is not None:
            page_df = utils.expand_dataframe_column(page_df, "tags", add_prefix=False)

        page_df.set_index("id", inplace=True)
        return page_df

    # Query endpoint
    df = utils.concat_pages_to_dataframe(
        getter=get_page,
        parser=parse_page,
        page=page,
        get_all_pages=get_all_pages,
        multithread_pages=multithread_pages,
    )

    # Output
    return df


def get_time_values(
    data_id: str,
    start_date: Union[str, datetime],
    end_date: Union[str, datetime],
    aggregation: str,
    number_of_values: Optional[int] = None,
    aggregation_period: Optional[str] = None,
    aggregation_function: Optional[str] = None,
    unit_id: Optional[str] = None,
    name_data_from: str = "reference",
    append_unit_to_description: bool = True,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """
    Get values from a temporal data from the OIAnalytics API

    Parameters
    ----------
    data_id: str
        The data id on which values are to be retrieved
    start_date: datetime or str
        The beginning of the period to be retrieved
    end_date: datetime or str
        The end of the period to be retrieved
    aggregation: {'RAW_VALUES', 'TIME'}
        How to aggregate the values. If 'TIME', aggregation period and function should be specified.
    number_of_values: int, optional
        If > 0 returns only the number of values specified. Only works for stored data.
    aggregation_period: str, optional
        Required in case 'aggregation' is 'TIME' and is the sampling period of the expected result.
        This period should be an ISO period as described in https://en.wikipedia.org/wiki/ISO_8601#Durations
    aggregation_function: str, optional
        Required in case 'aggregation' is 'TIME' and is the aggregation function to use to aggregate the values within
        the sampling period.
        Possible values are 'FIRST', 'LAST', 'LAST_MINUS_FIRST', 'SUM', 'MIN', 'MAX', 'MEAN', 'MEDIAN', 'STDEV',
        'PERCENTILE5', 'PERCENTILE95', 'DECILE1', 'DECILE9', 'QUARTILE1', 'QUARTILE9', 'COUNT', 'MEAN_MINUS_SIGMA',
        'MEAN_PLUS_SIGMA', 'MEAN_MINUS_TWO_SIGMA', 'MEAN_PLUS_TWO_SIGMA', 'MEAN_MINUS_THREE_SIGMA',
        'MEAN_PLUS_THREE_SIGMA', 'VALUE_CHANGE'.
    unit_id: str, optional
        The id of the unit to use to express the values. If not present a default unit will be used.
        This unit should be compatible with the physical quantity of the data queried.
    name_data_from: {'id', 'reference', 'description'}
        What field should be extracted for naming data.
    append_unit_to_description: bool, default True
        Only used when 'name_data_from' is 'description'. If True, the unit is added after the description.
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    A Series containing the values of the data, indexed by 'timestamp'
    """

    # Args validation
    if name_data_from not in ["id", "reference", "description"]:
        raise ValueError(f"Unexpected value for 'name_data_from': {name_data_from}")

    # Query endpoint
    data = endpoints.data.get_time_values(
        data_id=data_id,
        start_date=start_date,
        end_date=end_date,
        aggregation=aggregation,
        number_of_values=number_of_values,
        aggregation_period=aggregation_period,
        aggregation_function=aggregation_function,
        unit_id=unit_id,
        api_credentials=api_credentials,
    )

    # Format series
    if name_data_from == "id":
        data_name = data["data"]["id"]
    elif name_data_from == "reference":
        data_name = data["data"]["reference"]
    elif name_data_from == "description":
        data_name = data["data"]["description"]
        if append_unit_to_description is True:
            data_name = f'{data_name} ({data["unit"]["label"]})'
    else:
        raise ValueError(f"Unexpected value for 'name_data_from': {name_data_from}")

    if len(data["values"]) == 0:
        timestamp_index = pd.to_datetime(data["timestamps"]).tz_localize("UTC")
    else:
        timestamp_index = pd.to_datetime(data["timestamps"])

    ser = pd.Series(
        name=data_name,
        index=timestamp_index,
        data=data["values"],
        dtype=float if len(data["values"]) == 0 else None,
    )

    ser.index.name = "timestamp"

    # Output
    return ser


def get_batch_values(
    data_id: str,
    start_date: Union[str, datetime],
    end_date: Union[str, datetime],
    aggregation: str,
    number_of_values: Optional[int] = None,
    aggregation_period: Optional[str] = None,
    aggregation_function: Optional[str] = None,
    batch_type_id: Optional[str] = None,
    batch_index_id: Optional[str] = None,
    unit_id: Optional[str] = None,
    name_data_from: str = "reference",
    append_unit_to_description: bool = True,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """
    Get values from a batch data from the OIAnalytics API

    Parameters
    ----------
    data_id: str
        The data id on which values are to be retrieved
    start_date: datetime or str
        The beginning of the period to be retrieved
    end_date: datetime or str
        The end of the period to be retrieved
    aggregation: {'RAW_VALUES', 'TIME'}
        How to aggregate the values. If 'TIME', aggregation period and function should be specified.
    number_of_values: int, optional
        If > 0 returns only the number of values specified. Only works for stored data.
    aggregation_period: str, optional
        Required in case 'aggregation' is 'TIME' and is the sampling period of the expected result.
        This period should be an ISO period as described in https://en.wikipedia.org/wiki/ISO_8601#Durations
    aggregation_function: str, optional
        Required in case 'aggregation' is 'TIME' and is the aggregation function to use to aggregate the values within
        the sampling period.
        Possible values are 'FIRST', 'LAST', 'LAST_MINUS_FIRST', 'SUM', 'MIN', 'MAX', 'MEAN', 'MEDIAN', 'STDEV',
        'PERCENTILE5', 'PERCENTILE95', 'DECILE1', 'DECILE9', 'QUARTILE1', 'QUARTILE9', 'COUNT', 'MEAN_MINUS_SIGMA',
        'MEAN_PLUS_SIGMA', 'MEAN_MINUS_TWO_SIGMA', 'MEAN_PLUS_TWO_SIGMA', 'MEAN_MINUS_THREE_SIGMA',
        'MEAN_PLUS_THREE_SIGMA', 'VALUE_CHANGE'.
    batch_type_id: str, optional
        The id of the batch type that should be used to query the values.
        If not present the batch type of the data will be used.
        This batch type should be compatible with the data batch type e.g. it should exist a genealogy between this
        batch type and the batch type of the data.
    batch_index_id: str, optional
        The id of the batch timestamp index that should be used to query the values.
        If not present the batch timestamp will be used. The batch index should belong to the batch type
    unit_id: str, optional
        The id of the unit to use to express the values. If not present a default unit will be used.
        This unit should be compatible with the physical quantity of the data queried.
    name_data_from: {'id', 'reference', 'description'}
        What field should be extracted for naming data.
    append_unit_to_description: bool, default True
        Only used when 'name_data_from' is 'description'. If True, the unit is added after the description.
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    A Series containing the values of the data, indexed by 'batch_id', 'batch_name', 'batch_timestamp'
    """

    # Args validation
    if name_data_from not in ["id", "reference", "description"]:
        raise ValueError(f"Unexpected value for 'name_data_from': {name_data_from}")

    # Query endpoint
    data = endpoints.data.get_batch_values(
        data_id=data_id,
        start_date=start_date,
        end_date=end_date,
        aggregation=aggregation,
        number_of_values=number_of_values,
        aggregation_period=aggregation_period,
        aggregation_function=aggregation_function,
        batch_type_id=batch_type_id,
        batch_index_id=batch_index_id,
        unit_id=unit_id,
        api_credentials=api_credentials,
    )

    # Format series
    if name_data_from == "id":
        data_name = data["data"]["id"]
    elif name_data_from == "reference":
        data_name = data["data"]["reference"]
    elif name_data_from == "description":
        data_name = data["data"]["description"]
        if append_unit_to_description is True:
            data_name = f'{data_name} ({data["unit"]["label"]})'
    else:
        raise ValueError(f"Unexpected value for 'name_data_from': {name_data_from}")

    data_type = data["type"]

    if len(data["values"]) == 0:
        timestamp_index = pd.to_datetime(data["timestamps"]).tz_localize("UTC")
    else:
        timestamp_index = pd.to_datetime(data["timestamps"])

    ser = pd.Series(
        name=data_name,
        index=[
            data["batchIds"],
            data["batchNames"],
            timestamp_index,
        ]
        if data_type == "batch-values"
        else timestamp_index,
        data=data["values"],
        dtype=float if len(data["values"]) == 0 else None,
    )

    if data_type == "batch-values":
        ser.index.names = ["batch_id", "batch_name", "batch_timestamp"]
    else:
        ser.index.name = "timestamp"

    # Output
    return ser


def get_multiple_data_values(
    start_date: Union[str, datetime],
    end_date: Union[str, datetime],
    aggregation: str,
    data_id: Optional[Union[str, List[str]]] = None,
    data_reference: Optional[Union[str, List[str]]] = None,
    number_of_values: Optional[int] = None,
    aggregation_period: Optional[Union[str, timedelta, pd.Timedelta]] = None,
    aggregation_function: Optional[Union[str, List[str]]] = None,
    unit_id: Optional[Union[str, List[str]]] = None,
    unit_label: Optional[Union[str, List[str]]] = None,
    name_data_from: str = "reference",
    append_unit_to_description: bool = True,
    join_series_on: Optional[str] = "index",
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """
    Get values from multiple data at once from the OIAnalytics API

    Parameters
    ----------
    start_date: datetime or str
        The beginning of the period to be retrieved
    end_date: datetime or str
        The end of the period to be retrieved
    aggregation: {'RAW_VALUES', 'TIME'}
        How to aggregate the values. If 'TIME', aggregation period and function should be specified.
    data_id: str or list of str, optional
        The array of data id to query. Required if 'data_reference' is None.
    data_reference: str or list of str, optional
        The array of data reference to query. Required if 'data_id' is None.
    number_of_values: int, optional
        If > 0 returns only the number of values specified. Only works for stored data.
    aggregation_period: str, optional
        Required in case 'aggregation' is 'TIME' and is the sampling period of the expected result.
        This period should be an ISO period as described in https://en.wikipedia.org/wiki/ISO_8601#Durations
    aggregation_function: str, optional
        Required in case 'aggregation' is 'TIME' and is the aggregation function to use to aggregate the values within
        the sampling period.
        Possible values are 'FIRST', 'LAST', 'LAST_MINUS_FIRST', 'SUM', 'MIN', 'MAX', 'MEAN', 'MEDIAN', 'STDEV',
        'PERCENTILE5', 'PERCENTILE95', 'DECILE1', 'DECILE9', 'QUARTILE1', 'QUARTILE9', 'COUNT', 'MEAN_MINUS_SIGMA',
        'MEAN_PLUS_SIGMA', 'MEAN_MINUS_TWO_SIGMA', 'MEAN_PLUS_TWO_SIGMA', 'MEAN_MINUS_THREE_SIGMA',
        'MEAN_PLUS_THREE_SIGMA', 'VALUE_CHANGE'.
    unit_id: str or list of str, optional
        The array of unit id to use to express the values. If not present a default unit will be used.
        All units should be compatible with the physical quantity of the data queried.
        If provided should be the same size as the 'data_id' or 'data_reference' array.
        It cannot be used in conjunction with 'unit_label'.
    unit_label: str or list of str, optional
        The array of unit label to use to express the values. If not present a default unit will be used.
        All units should be compatible with the physical quantity of the data queried.
        If provided should be the same size as the data id or data reference array.
        It cannot be used in conjunction with 'unit_id'.
    name_data_from: {'id', 'reference', 'description'}
        What field should be extracted for naming data.
    append_unit_to_description: bool, default True
        Only used when 'name_data_from' is 'description'. If True, the unit is added after the description.
    join_series_on: {'index', 'timestamp', None}, default 'index'
        Joining strategy for data. 'index' will only work if data is homogeneous (i.e. only time values, or batch values
        on a single batch type). If 'timestamp', only the time index will be kept.
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    If 'join_series_on' is None, each data is returned in a separate Series stored in a dictionary indexed by the data
    name.
    If 'join_series_on' is 'index' (default behaviour) or 'timestamp', a single DataFrame is returned, containing all
    the data in columns.
    """

    # Args validation
    if name_data_from not in ["id", "reference", "description"]:
        raise ValueError(f"Unexpected value for 'name_data_from': {name_data_from}")

    if join_series_on not in ["index", "timestamp", None]:
        raise ValueError(f"Unexpected value for 'join_series_on': {join_series_on}")

    # Query endpoint
    data_list = endpoints.data.get_multiple_data_values(
        start_date=start_date,
        end_date=end_date,
        aggregation=aggregation,
        data_id=data_id,
        data_reference=data_reference,
        number_of_values=number_of_values,
        aggregation_period=aggregation_period,
        aggregation_function=aggregation_function,
        unit_id=unit_id,
        unit_label=unit_label,
        api_credentials=api_credentials,
    )

    # Format series
    batch_types = {}
    data_series = {}
    for data in data_list:
        # Format series
        if name_data_from == "id":
            data_name = data["data"]["id"]
        elif name_data_from == "reference":
            data_name = data["data"]["reference"]
        elif name_data_from == "description":
            data_name = data["data"]["description"]
            if append_unit_to_description is True:
                data_name = f'{data_name} ({data["unit"]["label"]})'
        else:
            raise ValueError(f"Unexpected value for 'name_data_from': {name_data_from}")

        data_type = data["type"]
        batch_types[data_name] = (
            None if data_type == "time-values" else data["batchType"]["id"]
        )

        if len(data["values"]) == 0:
            timestamp_index = pd.to_datetime(data["timestamps"]).tz_localize("UTC")
        else:
            timestamp_index = pd.to_datetime(data["timestamps"])

        ser = pd.Series(
            name=data_name,
            index=[
                data["batchIds"],
                data["batchNames"],
                timestamp_index,
            ]
            if data_type == "batch-values" and join_series_on != "timestamp"
            else timestamp_index,
            data=data["values"],
            dtype=float if len(data["values"]) == 0 else None,
        )

        if data_type == "batch-values" and join_series_on != "timestamp":
            ser.index.names = ["batch_id", "batch_name", "batch_timestamp"]
        else:
            ser.index.name = "timestamp"

        # Store results
        data_series[data_name] = ser

    # Join series
    if join_series_on == "index":
        n_batch_types = pd.Series(batch_types).nunique(dropna=False)
        if n_batch_types > 1:
            raise ValueError(
                "'join_series_on' cannot be set to 'index' on heterogeneous data"
            )
        data_series = pd.DataFrame(data_series)

    elif join_series_on == "timestamp":
        data_series = pd.DataFrame(data_series)

    # Output
    return data_series


def insert_time_values(
    data: Union[pd.Series, pd.DataFrame],
    units: Optional[dict] = None,
    use_external_reference: bool = False,
    timestamp_index_name: str = "timestamp",
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """
    Insert time values stored in a Series or DataFrame through the OIAnalytics API

    Parameters
    ----------
    data: Series or DataFrame
        The time values to be sent to OIAnalytics. The index should be named 'timestamp'.
    units: dict, optional
        A dictionary indexed by data reference, specifying the values in which it is sent.
    use_external_reference: bool, default False
        Whether or not the data are named using their external reference (else the OIAnalytics reference is used).
    timestamp_index_name: str, default 'timestamp'
        Name of the index level containing the timestamp
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    A dictionary of the response from the API, containing the data insert report
    """

    # Init
    if units is None:
        units = {}

    if isinstance(data, pd.Series):
        data = pd.DataFrame(data)
    else:
        data = data.copy()

    # Build DTO
    payload = []

    try:
        data.index = (
            data.index.get_level_values(timestamp_index_name)
            .to_series()
            .apply(utils.get_zulu_isoformat)
        )
    except Exception:
        raise ValueError(
            "The series or dataframe must have an index level named 'timestamp' containing datetime-like values"
        )

    for col in data.columns:
        ser = data[col]
        ser.name = "value"

        # Build payload for the data
        col_dict = {"dataReference": col}
        col_dict["unit"] = units.get(col, None)
        col_dict["values"] = (
            pd.DataFrame(ser).reset_index().dropna().to_dict(orient="records")
        )

        payload.append(col_dict)

    # Query endpoint
    response = endpoints.data.insert_time_values(
        data=payload,
        use_external_reference=use_external_reference,
        api_credentials=api_credentials,
    )

    # Output
    return response

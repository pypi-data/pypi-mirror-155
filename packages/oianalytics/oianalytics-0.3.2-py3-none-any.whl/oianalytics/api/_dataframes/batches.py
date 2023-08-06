from typing import Optional, Union, List
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from .. import _credentials
from .. import endpoints
from .. import utils

__all__ = [
    "get_batch_types",
    "get_batch_type_details",
    "get_batches",
    "update_batch_values",
    "update_batch_feature_values",
]


def get_batch_types(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    get_all_pages: bool = True,
    multithread_pages: bool = True,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """
    Get the configured batch types from the OIAnalytics API

    Parameters
    ----------
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
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    A DataFrame listing batch types
    """

    # Init
    if get_all_pages is True:
        page = 0
        page_size = 500

    def get_page(page_num: int):
        page_response = endpoints.batches.get_batch_types(
            page=page_num, page_size=page_size, api_credentials=api_credentials
        )
        return page_response

    def parse_page(page_response: dict):
        page_df = pd.DataFrame(page_response["content"])

        # Expected columns if content is empty
        if page_df.shape[0] == 0:
            page_df = pd.DataFrame(columns=["id", "name"])

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


def get_batch_type_details(
    batch_type_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """
    Get details about a single batch type from the OIAnalytics API

    Parameters
    ----------
    batch_type_id: str
        The id of the batch type to be retrieved
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    A tuple of 3 DataFrames listing various properties of the batch type:
        - Steps
        - Data
        - Features
    """

    # Query endpoint
    response = endpoints.batches.get_batch_type_details(
        batch_type_id=batch_type_id, api_credentials=api_credentials
    )

    # Split content
    steps = response["steps"]
    data = response["dataList"]
    features = response["features"]

    # Format dataframes
    if len(steps) > 0:
        df_steps = pd.DataFrame(steps).set_index("id")
    else:
        df_steps = pd.DataFrame(columns=["id", "name", "localisationKeys"]).set_index(
            "id"
        )

    if len(data) > 0:
        df_data = pd.DataFrame(data).set_index("id")
    else:
        df_data = pd.DataFrame(
            columns=["id", "dataType", "reference", "description"]
        ).set_index("id")

    if len(features) > 0:
        df_features = pd.DataFrame(features).set_index("id")
    else:
        df_features = pd.DataFrame(columns=["id", "key"]).set_index("id")

    # Output
    return df_steps, df_data, df_features


def get_batches(
    batch_type_id: str,
    start_date: Union[str, datetime],
    end_date: Union[str, datetime],
    name: Optional[str] = None,
    features_value_ids: Optional[Union[str, List[str]]] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    get_all_pages: bool = True,
    multithread_pages: bool = True,
    split_steps_and_values: bool = True,
    extract_from_localisation: Optional[str] = "value",
    expand_localisation: bool = True,
    extract_from_values: Optional[str] = "reference",
    expand_value_ids: bool = True,
    extract_from_features: Optional[str] = "value",
    expand_features: bool = True,
    append_unit_to_description: bool = True,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """
    Get batch instances from the OIAnalytics API

    Parameters
    ----------
    batch_type_id: str
        The id of the batch type to be retrieved
    start_date: datetime or str
        The beginning of the period to be retrieved
    end_date: datetime or str
        The end of the period to be retrieved
    name: str, optional
        A string that should be contained by all batch names returned
    features_value_ids: str or list of str, optional
        Possibly multiple feature value ids each returned batch should match.
        If for a given feature multiple feature value ids are provided then a batch will be returned if it
        contains one of them.
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
    split_steps_and_values: bool, default True
        If True, the response will be split into two separate DataFrames instead of a single dense one.
    extract_from_localisation: {'id', 'value', None}, default 'value'
        What field should be extracted from localisation information. If None, the full dictionary is kept.
    expand_localisation: bool, default True
        Whether or not localisation information should be expanded into multiple columns.
    extract_from_values: {'id', 'reference', 'description', None}, default 'reference'
        What field should be extracted for naming data. If None, the full dictionary is kept.
    expand_value_ids: bool, default True
        Whether or not data should be expanded into multiple columns.
    extract_from_features: {'id', 'value', None}, default 'value'
        What field should be extracted for naming features. If None, the full dictionary is kept.
    expand_features: bool, default True
        Whether or not features should be expanded into multiple columns.
    append_unit_to_description: bool, default True
        Only used when 'extract_from_values' is 'description'. If True, the unit is added after the description.
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    If 'split_steps_and_values' is False, a single DataFrame containing batches and their information in dictionaries
    is returned.
    If 'split_steps_and_values' is True (default behaviour), a tuple of 2 DataFrames is returned:
        - Batch steps
        - Batch data and features
    """

    # Args validation
    if extract_from_localisation not in ["id", "value", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_localisation': {extract_from_localisation}"
        )

    if extract_from_localisation is None and expand_localisation is True:
        raise ValueError(
            "Localisation cannot be expanded if 'extract_from_values' is None"
        )

    if extract_from_values not in ["id", "reference", "description", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_values': {extract_from_values}"
        )

    if extract_from_values is None and expand_value_ids is True:
        raise ValueError("Values cannot be expanded if 'extract_from_values' is None")

    if extract_from_features not in ["id", "value", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_features': {extract_from_features}"
        )

    if extract_from_features is None and expand_features is True:
        raise ValueError(
            "Features cannot be expanded if 'extract_from_features' is None"
        )

    # Init
    if get_all_pages is True:
        page = 0
        page_size = 500

    def get_page(page_num: int):
        page_response = endpoints.batches.get_batches(
            batch_type_id=batch_type_id,
            start_date=start_date,
            end_date=end_date,
            name=name,
            features_value_ids=features_value_ids,
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
                columns=["id", "name", "timestamp", "steps", "values", "features"]
            )

        # Rename columns
        page_df.rename(
            columns={
                "id": "batch_id",
                "name": "batch_name",
                "timestamp": "batch_timestamp",
            },
            inplace=True,
        )

        # Parse dates
        page_df["batch_timestamp"] = pd.to_datetime(page_df["batch_timestamp"])

        # Set index
        page_df.set_index(["batch_id", "batch_name", "batch_timestamp"], inplace=True)
        return page_df

    # Query endpoint
    df = utils.concat_pages_to_dataframe(
        getter=get_page,
        parser=parse_page,
        page=page,
        get_all_pages=get_all_pages,
        multithread_pages=multithread_pages,
    )

    # Split steps and values
    if split_steps_and_values is True:
        # Split dataframe
        df_steps = df.drop(columns=["values", "features"])
        df_values = df.drop(columns="steps")

        # Format steps
        df_steps = df_steps.explode("steps")
        df_steps = utils.expand_dataframe_column(
            df_steps,
            "steps",
            add_prefix=False,
            expected_keys=["step", "start", "end", "localisation"],
        )
        df_steps = utils.expand_dataframe_column(
            df_steps, "step", expected_keys=["id", "name"]
        )

        df_steps["start"] = pd.to_datetime((df_steps["start"]))
        df_steps["end"] = pd.to_datetime((df_steps["end"]))

        if extract_from_localisation == "id":
            df_steps["localisation"] = df_steps["localisation"].apply(
                lambda full_loc: {loc["tagKey"]["id"]: loc["id"] for loc in full_loc}
            )
        elif extract_from_localisation == "value":
            df_steps["localisation"] = df_steps["localisation"].apply(
                lambda full_loc: {
                    loc["tagKey"]["key"]: loc["value"] for loc in full_loc
                }
            )

        if expand_localisation is True and extract_from_localisation is not None:
            df_steps = utils.expand_dataframe_column(
                df_steps, "localisation", add_prefix=False
            )

        df_steps.set_index(["step_id"], append=True, inplace=True)

        # Format values
        if extract_from_values == "id":
            df_values["values"] = df_values["values"].apply(
                lambda values: {val["data"]["id"]: val["value"] for val in values}
            )
        elif extract_from_values == "reference":
            df_values["values"] = df_values["values"].apply(
                lambda values: {
                    val["data"]["reference"]: val["value"] for val in values
                }
            )
        elif extract_from_values == "description":
            if append_unit_to_description is True:
                df_values["values"] = df_values["values"].apply(
                    lambda values: {
                        f'{val["data"]["description"]} ({val["unit"]["label"]})': val[
                            "value"
                        ]
                        for val in values
                    }
                )
            else:
                df_values["values"] = df_values["values"].apply(
                    lambda values: {
                        val["data"]["description"]: val["value"] for val in values
                    }
                )

        if expand_value_ids is True and extract_from_values is not None:
            df_values = utils.expand_dataframe_column(
                df_values, "values", add_prefix=False
            )

        if extract_from_features == "id":
            df_values["features"] = df_values["features"].apply(
                lambda features: {feat["tagKey"]["id"]: feat["id"] for feat in features}
            )
        elif extract_from_features == "value":
            df_values["features"] = df_values["features"].apply(
                lambda features: {
                    feat["tagKey"]["key"]: feat["value"] for feat in features
                }
            )

        if expand_features is True and extract_from_features is not None:
            df_values = utils.expand_dataframe_column(
                df_values, "features", add_prefix=False
            )

        # Output
        return df_steps, df_values
    else:
        return df


def update_batch_values(
    batch_type_id: str,
    data: Union[pd.Series, pd.DataFrame],
    unit_ids: Optional[dict] = None,
    batch_id_index_name: str = "batch_id",
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Init
    if unit_ids is None:
        unit_ids = {}

    if isinstance(data, pd.Series):
        data = pd.DataFrame(data)
    else:
        data = data.copy()

    data.index = data.index.get_level_values(batch_id_index_name)

    # Send each column
    def send_row(row_tuple: tuple):
        row = row_tuple[1]
        for col in row.index:
            endpoints.batches.update_batch_value(
                batch_type_id=batch_type_id,
                batch_id=str(row.name),
                data_id=col,
                value=row[col],
                unit_id=unit_ids.get(col, None),
                api_credentials=api_credentials,
            )

    with ThreadPoolExecutor() as pool:
        pool.map(send_row, data.iterrows())


def update_batch_feature_values(
    batch_type_id: str,
    data: Union[pd.Series, pd.DataFrame],
    batch_id_index_name: str = "batch_id",
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Init
    if isinstance(data, pd.Series):
        data = pd.DataFrame(data)
    else:
        data = data.copy()

    data.index = data.index.get_level_values(batch_id_index_name)

    # Send each column
    def send_row(row_tuple: tuple):
        row = row_tuple[1]
        for col in row.index:
            endpoints.batches.update_batch_feature_value(
                batch_type_id=batch_type_id,
                batch_id=str(row.name),
                feature_id=col,
                value=row[col],
                api_credentials=api_credentials,
            )

    with ThreadPoolExecutor() as pool:
        pool.map(send_row, data.iterrows())

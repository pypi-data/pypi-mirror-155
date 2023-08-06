from typing import Optional

from ... import api
from .. import _dtos
from .. import utils

__all__ = ["get_single_obs_time_data", "get_single_obs_batch_data"]


def get_single_obs_time_data(
    model_execution: Optional[_dtos.ModelExecution] = None,
    rename_data_to_source_code_name: bool = True,
    api_credentials: Optional[api.OIAnalyticsAPICredentials] = None,
):
    # Get model execution from environment if not specified
    if model_execution is None:
        model_execution = _dtos.get_default_model_execution()
        if model_execution.pythonModelInstance.dataExchangeMode != "SINGLE_OBSERVATION":
            raise ValueError("The execution has to be in single observation mode")
        if model_execution.pythonModelInstance.singleObservationContext.type != "time":
            raise ValueError(
                "The execution has to be in single observation mode on time data"
            )

    # Start date
    start_date = (
        model_execution.lastSuccessfulExecutionInstant
        - model_execution.pythonModelInstance.singleObservationContext.overlappingPeriod
    )

    # End date
    end_date = model_execution.currentExecutionInstant

    # Aggregation
    if (
        model_execution.pythonModelInstance.singleObservationContext.aggregationPeriod
        == "PT0S"
    ):
        aggregation = "RAW_VALUES"
    else:
        aggregation = "TIME"

    # Aggregation period
    if aggregation == "RAW_VALUES":
        aggregation_period = None
    else:
        aggregation_period = (
            model_execution.pythonModelInstance.singleObservationContext.aggregationPeriod
        )

    # Aggregation function
    if aggregation == "RAW_VALUES":
        aggregation_function = None
    else:
        aggregation_function = [
            input_data.aggregationFunction
            for input_data in model_execution.get_data_input_dict(
                data_type="any", mode="object"
            ).values()
        ]

    # Get data list
    input_data_references = model_execution.get_data_input_dict(
        data_type="any", mode="reference"
    )
    input_renaming_dict = utils.reverse_dict(input_data_references)

    # Get units
    input_unit_ids = [
        input_data.unit.id
        for input_data in model_execution.get_data_input_dict(
            data_type="any", mode="object"
        ).values()
    ]

    # Query endpoint
    data = api.get_multiple_data_values(
        start_date=start_date,
        end_date=end_date,
        aggregation=aggregation,
        data_id=None,
        data_reference=input_data_references.values(),
        number_of_values=None,
        aggregation_period=aggregation_period,
        aggregation_function=aggregation_function,
        unit_id=input_unit_ids,
        unit_label=None,
        name_data_from="reference",
        append_unit_to_description=False,
        join_series_on="timestamp",
        api_credentials=api_credentials,
    )

    # Rename data
    if rename_data_to_source_code_name is True:
        data = data.rename(columns=input_renaming_dict)

    # Output
    return data


def get_single_obs_batch_data(
    model_execution: Optional[_dtos.ModelExecution] = None,
    rename_data_to_source_code_name: bool = True,
    api_credentials: Optional[api.OIAnalyticsAPICredentials] = None,
):
    # Get variables from environment if not specified
    if model_execution is None:
        model_execution = _dtos.get_default_model_execution()
        if model_execution.pythonModelInstance.dataExchangeMode != "SINGLE_OBSERVATION":
            raise ValueError("The execution has to be in single observation mode")
        if model_execution.pythonModelInstance.singleObservationContext.type != "batch":
            raise ValueError(
                "The execution has to be in single observation mode on batches"
            )

    # Start date
    start_date = (
        model_execution.lastSuccessfulExecutionInstant
        - model_execution.pythonModelInstance.singleObservationContext.overlappingPeriod
    )

    # End date
    end_date = model_execution.currentExecutionInstant

    # Batch type
    batch_type_id = (
        model_execution.pythonModelInstance.singleObservationContext.batchPredicate.batchType.id
    )

    # Batch feature filters
    features_value_ids = [
        feature.id
        for feature in model_execution.pythonModelInstance.singleObservationContext.batchPredicate.featureFilters
    ]

    # Get data list
    input_data_references = model_execution.get_data_input_dict(
        data_type="any", mode="reference"
    )
    input_renaming_dict = utils.reverse_dict(input_data_references)

    # Get units
    input_unit_ids = [
        input_data.unit.id
        for input_data in model_execution.get_data_input_dict(
            data_type="any", mode="object"
        ).values()
    ]

    # Query endpoint for data
    data = None

    if len(model_execution.get_data_input_dict()) > 0:
        data = api.get_multiple_data_values(
            start_date=start_date,
            end_date=end_date,
            aggregation="RAW_VALUES",
            data_reference=input_data_references.values(),
            unit_id=input_unit_ids,
            name_data_from="reference",
            append_unit_to_description=False,
            join_series_on="index",
            api_credentials=api_credentials,
        )

        # Rename data
        if rename_data_to_source_code_name is True:
            data = data.rename(columns=input_renaming_dict)

    # Query endpoint for features & batch predicate
    features = api.get_batches(
        batch_type_id=batch_type_id,
        start_date=start_date,
        end_date=end_date,
        features_value_ids=features_value_ids,
        api_credentials=api_credentials,
    )[1]

    # Rename features
    features_renaming_dict = utils.reverse_dict(
        model_execution.get_input_dict(input_types=["BATCH_TAG_KEY"], mode="reference")
    )

    features = features[
        [col for col in features.columns if col in features_renaming_dict.keys()]
    ]

    if rename_data_to_source_code_name is True:
        features = features.rename(columns=features_renaming_dict)

    if data is None:
        data = features
    else:
        data = data.join(features, how="right")

    # Output
    return data

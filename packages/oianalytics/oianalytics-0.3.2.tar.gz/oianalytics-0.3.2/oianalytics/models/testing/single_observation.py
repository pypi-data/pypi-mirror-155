from typing import Optional, Any, Callable

import pandas as pd

from .. import _dtos
from .. import get_single_obs_batch_data, get_single_obs_time_data

__all__ = [
    "get_input_data",
    "test_load_resources",
    "test_process_data",
    "test_full_model",
]


def get_input_data(
    model_execution: Optional[_dtos.ModelExecution] = None,
    rename_data_to_source_code_name: bool = True,
):
    # Get default model_execution if not provided
    if model_execution is None:
        model_execution = _dtos.get_default_model_execution()

    # Get data
    if model_execution.pythonModelInstance.dataExchangeMode != "SINGLE_OBSERVATION":
        raise ValueError(
            "The provided model execution input is not in single observation mode"
        )

    if model_execution.pythonModelInstance.singleObservationContext.type == "time":
        return get_single_obs_time_data(
            model_execution=model_execution,
            rename_data_to_source_code_name=rename_data_to_source_code_name,
        )

    elif model_execution.pythonModelInstance.singleObservationContext.type == "batch":
        return get_single_obs_batch_data(
            model_execution=model_execution,
            rename_data_to_source_code_name=rename_data_to_source_code_name,
        )


def test_load_resources(
    load_resources: Callable,
    model_execution: Optional[_dtos.ModelExecution] = None,
):
    # Get default model_execution if not provided
    if model_execution is None:
        model_execution = _dtos.get_default_model_execution()

    # Run load_resources function
    return load_resources(**model_execution.execution_kwargs)


def test_process_data(
    process_data: Callable,
    data: pd.DataFrame,
    resources: Optional[Any] = None,
    model_execution: Optional[_dtos.ModelExecution] = None,
):
    # Get default model_execution if not provided
    if model_execution is None:
        model_execution = _dtos.get_default_model_execution()

    # Init outputs storage
    outputs = {}

    # Run process_data function
    model_outputs = data.apply(
        lambda r: pd.Series(process_data(resources=resources, **r.to_dict())),
        axis=1,
    )
    outputs["raw_outputs"] = model_outputs

    # Extract configured output data
    output_data = model_outputs[
        [
            col
            for col in model_outputs.columns
            if col in model_execution.get_data_output_dict().keys()
        ]
    ]

    if model_execution.pythonModelInstance.singleObservationContext.type == "batch":
        output_features = model_outputs[
            [
                col
                for col in model_outputs.columns
                if col
                in model_execution.get_output_dict(
                    output_types=["BATCH_TAG_KEY"]
                ).keys()
            ]
        ]

    # Rename outputs
    if model_execution.pythonModelInstance.singleObservationContext.type == "time":
        output_data_renaming_dict = model_execution.get_data_output_dict(
            data_type="any", mode="reference"
        )
    elif model_execution.pythonModelInstance.singleObservationContext.type == "batch":
        output_data_renaming_dict = model_execution.get_data_output_dict(
            data_type="any", mode="id"
        )

    output_data = output_data.rename(columns=output_data_renaming_dict)
    outputs["output_data"] = output_data

    if model_execution.pythonModelInstance.singleObservationContext.type == "batch":
        output_features_renaming_dict = model_execution.get_output_dict(
            output_types=["BATCH_TAG_KEY"], mode="id"
        )

        output_features = output_features.rename(columns=output_features_renaming_dict)
        outputs["output_features"] = output_features

    # Output
    return outputs


def test_full_model(
    load_resources: Callable,
    process_data: Callable,
    model_execution: Optional[_dtos.ModelExecution] = None,
):
    # Load data
    data = get_input_data(model_execution=model_execution)

    # Load resources
    resources = test_load_resources(
        load_resources=load_resources, model_execution=model_execution
    )

    # Process data
    return test_process_data(
        process_data=process_data,
        data=data,
        resources=resources,
        model_execution=model_execution,
    )

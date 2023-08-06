from typing import Union, Optional
import io
import time

import pandas as pd

from .. import api
from ._dtos import get_default_model_execution

__all__ = [
    "FileOutput",
    "TimeValuesOutput",
    "Delay",
    "BatchValuesOutput",
    "BatchFeaturesOutput",
    "OIModelOutputs",
]


# Output classes
class FileOutput:
    def __init__(self, file_name: str, content: Union[io.StringIO, io.BytesIO]):
        self.output_type = "file"
        self.file_name = file_name
        self.content = content

    @classmethod
    def from_pandas(
        cls,
        data: Union[pd.Series, pd.DataFrame],
        file_name: str,
        file_type: str = "csv",
        writing_kwargs: Optional[dict] = None,
    ):
        # Init
        if writing_kwargs is None:
            writing_kwargs = {}

        bio = io.BytesIO()

        # Write data
        if file_type == "excel":
            data.to_excel(bio, **writing_kwargs)
        elif file_type == "csv":
            data.to_csv(bio, **writing_kwargs)
        else:
            raise NotImplementedError(f"Unsupported file_type: {file_type}")
        bio.seek(0)

        # Create object
        return cls(file_name=file_name, content=bio)

    def send_to_oianalytics(
        self, api_credentials: Optional[api.OIAnalyticsAPICredentials] = None
    ):
        return api.endpoints.files.upload_file(
            file_content=self.content,
            file_name=self.file_name,
            api_credentials=api_credentials,
        )


class TimeValuesOutput:
    def __init__(
        self,
        data: Union[pd.Series, pd.DataFrame],
        units: Optional[dict] = None,
        rename_data: bool = True,
        use_external_reference: bool = False,
        timestamp_index_name: str = "timestamp",
    ):
        self.output_type = "time_values"

        # Rename data if specified
        data_df = data.to_frame() if isinstance(data, pd.Series) else data

        if rename_data is True:
            model_exec = get_default_model_execution()
            if model_exec is None:
                raise ValueError(
                    "Data can't be renamed without a current model_exec set globally"
                )

            output_dict = model_exec.get_data_input_dict(
                data_type="time", mode="reference"
            )
            self.data = data_df.rename(columns=output_dict)
        else:
            self.data = data_df

        # Specify units
        if units is None:
            model_exec = get_default_model_execution()
            if model_exec is not None:
                self.units = {
                    output_data.reference: output_data.unit.label
                    for output_data in model_exec.get_data_output_dict(
                        data_type="time", mode="object"
                    ).values()
                }
        else:
            self.units = units

        self.use_external_reference = use_external_reference

        self.timestamp_index_name = timestamp_index_name

    def send_to_oianalytics(
        self, api_credentials: Optional[api.OIAnalyticsAPICredentials] = None
    ):
        return api.insert_time_values(
            data=self.data,
            units=self.units,
            use_external_reference=self.use_external_reference,
            timestamp_index_name=self.timestamp_index_name,
            api_credentials=api_credentials,
        )


class BatchValuesOutput:
    def __init__(
        self,
        batch_type_id: str,
        data: Union[pd.Series, pd.DataFrame],
        units: Optional[dict] = None,
        batch_id_index_name: str = "batch_id",
        rename_data: bool = True,
    ):
        self.output_type = "batch_values"
        self.batch_type_id = batch_type_id

        # Rename data if specified
        data_df = data.to_frame() if isinstance(data, pd.Series) else data

        if rename_data is True:
            model_exec = get_default_model_execution()
            if model_exec is None:
                raise ValueError(
                    "Data can't be renamed without a current model_exec set globally"
                )

            output_dict = model_exec.get_data_output_dict(data_type="batch", mode="id")
            self.data = data_df.rename(columns=output_dict)
        else:
            self.data = data_df

        # Specify units
        if units is None:
            model_exec = get_default_model_execution()
            if model_exec is not None:
                self.units = {
                    output_data.reference: output_data.unit.id
                    for output_data in model_exec.get_data_output_dict(
                        data_type="batch", mode="object"
                    ).values()
                }
        else:
            self.units = units

        self.batch_id_index_name = batch_id_index_name

    def send_to_oianalytics(
        self, api_credentials: Optional[api.OIAnalyticsAPICredentials] = None
    ):
        return api.update_batch_values(
            batch_type_id=self.batch_type_id,
            data=self.data,
            unit_ids=self.units,
            batch_id_index_name=self.batch_id_index_name,
            api_credentials=api_credentials,
        )


class BatchFeaturesOutput:
    def __init__(
        self,
        batch_type_id: str,
        data: Union[pd.Series, pd.DataFrame],
        rename_features: bool = True,
        batch_id_index_name: str = "batch_id",
    ):
        self.output_type = "batch_features"
        self.batch_type_id = batch_type_id

        # Rename data if specified
        data_df = data.to_frame() if isinstance(data, pd.Series) else data

        if rename_features is True:
            model_exec = get_default_model_execution()
            if model_exec is None:
                raise ValueError(
                    "Features can't be renamed without a current model_exec set globally"
                )

            output_dict = model_exec.get_data_output_dict(data_type="batch", mode="id")
            self.data = data_df.rename(columns=output_dict)
        else:
            self.data = data_df

        self.batch_id_index_name = batch_id_index_name

    def send_to_oianalytics(
        self, api_credentials: Optional[api.OIAnalyticsAPICredentials] = None
    ):
        return api.update_batch_feature_values(
            batch_type_id=self.batch_type_id,
            data=self.data,
            batch_id_index_name=self.batch_id_index_name,
            api_credentials=api_credentials,
        )


class Delay:
    def __init__(self, duration=5):
        self.output_type = "delay"
        self.duration = duration

    def send_to_oianalytics(
        self, api_credentials: Optional[api.OIAnalyticsAPICredentials] = None
    ):
        time.sleep(self.duration)


class OIModelOutputs:
    def __init__(self):
        self.output_type = "outputs_queue"
        self.model_outputs = []

    def add_output(self, output_object: Union[FileOutput, TimeValuesOutput, Delay]):
        self.model_outputs.append(output_object)

    def send_to_oianalytics(
        self, api_credentials: Optional[api.OIAnalyticsAPICredentials] = None
    ):
        for model_output in self.model_outputs:
            model_output.send_to_oianalytics(api_credentials=api_credentials)

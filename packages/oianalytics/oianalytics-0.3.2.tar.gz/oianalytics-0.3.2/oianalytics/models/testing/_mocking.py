from typing import Optional, Union, List
from datetime import datetime, timedelta, timezone
import dateutil

from .. import _dtos
from ... import api

__all__ = ["TestModelExecution"]


class TestModelExecution(_dtos.ModelExecution):
    def __init__(
        self,
        test_mode: bool = True,
        last_successful_execution_instant: datetime = datetime.now(timezone.utc)
        - timedelta(hours=1),
        current_execution_instant: datetime = datetime.now(timezone.utc),
        data_exchange_mode: str = "FREE_FROM_API",
        single_observation_type: str = "time",
        single_observation_overlapping_period: timedelta = timedelta(hours=1),
        single_observation_aggregation_period: str = "PT10M",
        single_observation_batch_type_id: str = "single_obs_batch_type_id",
        single_observation_batch_type_reference: str = "single_obs_batch_type_reference",
    ):
        # Data exchange mode
        if data_exchange_mode == "FREE_FROM_API":
            single_obs_context = None
        elif data_exchange_mode == "SINGLE_OBSERVATION":
            if single_observation_type == "time":
                single_obs_context = _dtos.SingleObservationTimeContext(
                    type="time",
                    overlappingPeriod=single_observation_overlapping_period,
                    aggregationPeriod=single_observation_aggregation_period,
                )
            elif single_observation_type == "batch":
                single_obs_context = _dtos.SingleObservationBatchContext(
                    type="batch",
                    overlappingPeriod=single_observation_overlapping_period,
                    batchPredicate=_dtos.BatchPredicateValue(
                        type="batch-predicate",
                        batchType=_dtos.BatchPredicateBatchType(
                            type="batch-type",
                            id=single_observation_batch_type_id,
                            reference=single_observation_batch_type_reference,
                        ),
                        featureFilters=[],
                    ),
                )
            else:
                raise ValueError(
                    f"{single_observation_type} is not valid for 'single_observation_type'"
                )
        else:
            raise ValueError(
                f"{data_exchange_mode} is not valid for 'data_exchange_mode'"
            )

        # Dates parsing and formatting
        if isinstance(last_successful_execution_instant, str):
            last_execution = dateutil.parser.parse(last_successful_execution_instant)
        else:
            last_execution = last_successful_execution_instant
        if isinstance(current_execution_instant, str):
            current_execution = dateutil.parser.parse(current_execution_instant)
        else:
            current_execution = current_execution_instant

        # Init
        super().__init__(
            testMode=test_mode,
            credentials=None,
            lastSuccessfulExecutionInstant=last_execution.astimezone(timezone.utc),
            currentExecutionInstant=current_execution.astimezone(timezone.utc),
            pythonModelInstance=_dtos.ModelInstance(
                id="test_instance_id",
                trigger=_dtos.CronTrigger(type="cron-trigger", cron="0 0 * * * *"),
                active=False,
                dataExchangeMode=data_exchange_mode,
                singleObservationContext=single_obs_context,
                inputParameters=[],
                outputParameters=[],
            ),
        )

    @classmethod
    def from_model_execution(cls, model_execution: _dtos.ModelExecution):
        test_model_execution = cls()
        test_model_execution.testMode = model_execution.testMode
        test_model_execution.credentials = model_execution.credentials
        test_model_execution.lastSuccessfulExecutionInstant = (
            model_execution.lastSuccessfulExecutionInstant
        )
        test_model_execution.currentExecutionInstant = (
            model_execution.currentExecutionInstant
        )
        test_model_execution.pythonModelInstance = model_execution.pythonModelInstance
        return test_model_execution

    def add_single_observation_feature_filter(
        self,
        feature_id: str = "single_obs_feature_id",
        feature_reference: str = "single_obs_feature_reference",
    ):
        self.pythonModelInstance.singleObservationContext.batchPredicate.featureFilters.append(
            _dtos.BatchTagValue(
                type="batch-tag-value", id=feature_id, reference=feature_reference
            )
        )

    def add_string_input(
        self,
        source_code_name: str = "string_input",
        value: Optional[str] = "String input",
    ):
        self.pythonModelInstance.inputParameters.append(
            _dtos.StringParameter(
                type="STRING", sourceCodeName=source_code_name, value=value
            )
        )

    def add_boolean_input(
        self, source_code_name: str = "boolean_input", value: Optional[bool] = True
    ):
        self.pythonModelInstance.inputParameters.append(
            _dtos.BooleanParameter(
                type="BOOLEAN", sourceCodeName=source_code_name, value=value
            )
        )

    def add_numeric_input(
        self,
        source_code_name: str = "numeric_input",
        value: Optional[Union[int, float]] = 42,
    ):
        self.pythonModelInstance.inputParameters.append(
            _dtos.NumericParameter(
                type="NUMERIC", sourceCodeName=source_code_name, value=value
            )
        )

    def add_file_input(
        self,
        source_code_name: str = "file_input",
        value: Optional[str] = "file_id",
    ):
        self.pythonModelInstance.inputParameters.append(
            _dtos.FileParameter(
                type="FILE", sourceCodeName=source_code_name, value=value
            )
        )

    def add_period_input(
        self,
        source_code_name: str = "period_input",
        value: Optional[str] = "PT12H",
    ):
        self.pythonModelInstance.inputParameters.append(
            _dtos.PeriodParameter(
                type="PERIOD", sourceCodeName=source_code_name, value=value
            )
        )

    def add_duration_input(
        self,
        source_code_name: str = "duration_input",
        value: Optional[int] = 86_400_000,
    ):
        self.pythonModelInstance.inputParameters.append(
            _dtos.DurationParameter(
                type="DURATION", sourceCodeName=source_code_name, value=value
            )
        )

    def add_instant_input(
        self,
        source_code_name: str = "instant_input",
        value: Optional[str] = api.utils.get_zulu_isoformat(datetime.now()),
    ):
        self.pythonModelInstance.inputParameters.append(
            _dtos.InstantParameter(
                type="INSTANT", sourceCodeName=source_code_name, value=value
            )
        )

    def add_unit_input(
        self,
        source_code_name: str = "unit_input",
        unit_id: Optional[str] = "unit_id",
        unit_label: str = "Unit label",
    ):
        if unit_id is None:
            unit_value = None
        else:
            unit_value = _dtos.UnitValue(type="unit", id=unit_id, reference=unit_label)

        self.pythonModelInstance.inputParameters.append(
            _dtos.UnitParameter(
                type="UNIT", sourceCodeName=source_code_name, value=unit_value
            )
        )

    def add_measurement_input(
        self,
        source_code_name: str = "measurement_input",
        measurement_id: Optional[str] = "measurement_id",
        measurement_reference: str = "Measurement reference",
    ):
        if measurement_id is None:
            measurement_value = None
        else:
            measurement_value = _dtos.MeasurementValue(
                type="measurement", id=measurement_id, reference=measurement_reference
            )

        self.pythonModelInstance.inputParameters.append(
            _dtos.MeasurementParameter(
                type="MEASUREMENT",
                sourceCodeName=source_code_name,
                value=measurement_value,
            )
        )

    def add_tagkey_input(
        self,
        source_code_name: str = "tagkey_input",
        tagkey_id: Optional[str] = "tagkey_id",
        tagkey_reference: str = "Tag key reference",
    ):
        if tagkey_id is None:
            tagkey_value = None
        else:
            tagkey_value = _dtos.TagKeyValue(
                type="tag-key", id=tagkey_id, reference=tagkey_reference
            )

        self.pythonModelInstance.inputParameters.append(
            _dtos.TagKeyParameter(
                type="TAG_KEY",
                sourceCodeName=source_code_name,
                value=tagkey_value,
            )
        )

    def add_tagvalue_input(
        self,
        source_code_name: str = "tagvalue_input",
        tagvalue_id: Optional[str] = "tagvalue_id",
        tagvalue_reference: str = "Tag value reference",
    ):
        if tagvalue_id is None:
            tagvalue_value = None
        else:
            tagvalue_value = _dtos.TagValueValue(
                type="tag-key", id=tagvalue_id, reference=tagvalue_reference
            )

        self.pythonModelInstance.inputParameters.append(
            _dtos.TagValueParameter(
                type="TAG_VALUE",
                sourceCodeName=source_code_name,
                value=tagvalue_value,
            )
        )

    def add_data_input(
        self,
        source_code_name: str = "data_input",
        data_id: Optional[str] = "data_id",
        data_reference: str = "data_reference",
        data_type: str = "STORED_CONTINUOUS",
        unit_id: str = "unit_id",
        unit_label: str = "Unit label",
        aggregation_function: Optional[str] = None,
    ):
        if data_id is None:
            data_value = None
        else:
            data_value = _dtos.DataValue(
                type="data",
                id=data_id,
                reference=data_reference,
                dataType=data_type,
                unit=_dtos.DataUnit(id=unit_id, label=unit_label),
                aggregationFunction=aggregation_function,
            )

        self.pythonModelInstance.inputParameters.append(
            _dtos.DataParameter(
                type="DATA",
                sourceCodeName=source_code_name,
                value=data_value,
            )
        )

    def add_timedata_input(
        self,
        source_code_name: str = "timedata_input",
        data_id: Optional[str] = "timedata_id",
        data_reference: str = "timedata_reference",
        unit_id: str = "unit_id",
        unit_label: str = "Unit label",
        aggregation_function: Optional[str] = None,
    ):
        if data_id is None:
            data_value = None
        else:
            data_value = _dtos.DataValue(
                type="data",
                id=data_id,
                reference=data_reference,
                dataType="STORED_CONTINUOUS",
                unit=_dtos.DataUnit(id=unit_id, label=unit_label),
                aggregationFunction=aggregation_function,
            )

        self.pythonModelInstance.inputParameters.append(
            _dtos.StoredContinuousDataParameter(
                type="STORED_CONTINUOUS_DATA",
                sourceCodeName=source_code_name,
                value=data_value,
            )
        )

    def add_batchdata_input(
        self,
        source_code_name: str = "batchdata_input",
        data_id: Optional[str] = "batchdata_id",
        data_reference: str = "batchdata_reference",
        unit_id: str = "unit_id",
        unit_label: str = "Unit label",
        aggregation_function: Optional[str] = None,
        batch_type_id: str = "batch_type_id",
        batch_type_name: str = "Batch type name",
    ):
        if data_id is None:
            data_value = None
        else:
            data_value = _dtos.BatchDataValue(
                type="batch-data",
                id=data_id,
                reference=data_reference,
                dataType="STORED_BATCH",
                unit=_dtos.DataUnit(id=unit_id, label=unit_label),
                aggregationFunction=aggregation_function,
                batchType=_dtos.BatchType(id=batch_type_id, name=batch_type_name),
            )

        self.pythonModelInstance.inputParameters.append(
            _dtos.StoredBatchDataParameter(
                type="STORED_BATCH_DATA",
                sourceCodeName=source_code_name,
                value=data_value,
            )
        )

    def add_computed_timedata_input(
        self,
        source_code_name: str = "computed_timedata_input",
        data_id: Optional[str] = "computed_timedata_id",
        data_reference: str = "computed_timedata_reference",
        unit_id: str = "unit_id",
        unit_label: str = "Unit label",
        aggregation_function: Optional[str] = None,
    ):
        if data_id is None:
            data_value = None
        else:
            data_value = _dtos.DataValue(
                type="data",
                id=data_id,
                reference=data_reference,
                dataType="COMPUTED_CONTINUOUS",
                unit=_dtos.DataUnit(id=unit_id, label=unit_label),
                aggregationFunction=aggregation_function,
            )

        self.pythonModelInstance.inputParameters.append(
            _dtos.ComputedContinuousDataParameter(
                type="COMPUTED_CONTINUOUS_DATA",
                sourceCodeName=source_code_name,
                value=data_value,
            )
        )

    def add_computed_batchdata_input(
        self,
        source_code_name: str = "computed_batchdata_input",
        data_id: Optional[str] = "computed_batchdata_id",
        data_reference: str = "computed_batchdata_reference",
        unit_id: str = "unit_id",
        unit_label: str = "Unit label",
        aggregation_function: Optional[str] = None,
        batch_type_id: str = "batch_type_id",
        batch_type_name: str = "Batch type name",
    ):
        if data_id is None:
            data_value = None
        else:
            data_value = _dtos.BatchDataValue(
                type="batch-data",
                id=data_id,
                reference=data_reference,
                dataType="COMPUTED_BATCH",
                unit=_dtos.DataUnit(id=unit_id, label=unit_label),
                aggregationFunction=aggregation_function,
                batchType=_dtos.BatchType(id=batch_type_id, name=batch_type_name),
            )

        self.pythonModelInstance.inputParameters.append(
            _dtos.ComputedBatchDataParameter(
                type="COMPUTED_BATCH_DATA",
                sourceCodeName=source_code_name,
                value=data_value,
            )
        )

    def add_batch_timedata_input(
        self,
        source_code_name: str = "batch_timedata_input",
        data_id: Optional[str] = "batch_timedata_id",
        data_reference: str = "batch_timedata_reference",
        unit_id: str = "unit_id",
        unit_label: str = "Unit label",
        aggregation_function: Optional[str] = None,
        batch_type_id: str = "batch_type_id",
        batch_type_name: str = "Batch type name",
    ):
        if data_id is None:
            data_value = None
        else:
            data_value = _dtos.BatchDataValue(
                type="batch-data",
                id=data_id,
                reference=data_reference,
                dataType="BATCH_TIME",
                unit=_dtos.DataUnit(id=unit_id, label=unit_label),
                aggregationFunction=aggregation_function,
                batchType=_dtos.BatchType(id=batch_type_id, name=batch_type_name),
            )

        self.pythonModelInstance.inputParameters.append(
            _dtos.BatchTimeDataParameter(
                type="BATCH_TIME_DATA",
                sourceCodeName=source_code_name,
                value=data_value,
            )
        )

    def add_batch_predicate_input(
        self,
        source_code_name: str = "batch_predicate_input",
        batch_type_id: Optional[str] = "batch_type_id",
        batch_type_reference: str = "Batch type reference",
        feature_value_ids: Optional[List[str]] = None,
        feature_value_references: Optional[List[str]] = None,
    ):
        if batch_type_id is None:
            batch_predicate_value = None
        else:
            # Build feature filters
            if feature_value_ids is None and feature_value_references is None:
                feature_filters = []
            elif feature_value_ids is not None and feature_value_references is not None:
                if len(feature_value_ids) != len(feature_value_references):
                    raise ValueError(
                        "'feature_value_ids' and 'feature_value_references' should have the same length"
                    )
                else:
                    feature_filters = [
                        _dtos.BatchTagValue(
                            type="batch-tag-value",
                            id=feature_value_ids[i],
                            reference=feature_value_references[i],
                        )
                        for i in range(len(feature_value_ids))
                    ]
            elif feature_value_ids is not None:
                feature_filters = [
                    _dtos.BatchTagValue(
                        type="batch-tag-value",
                        id=fid,
                        reference=f"{fid}_reference",
                    )
                    for fid in feature_value_ids
                ]
            else:
                feature_filters = [
                    _dtos.BatchTagValue(
                        type="batch-tag-value",
                        id=f"{fref}_id",
                        reference=fref,
                    )
                    for fref in feature_value_references
                ]

            # Build batch predicate
            batch_predicate_value = _dtos.BatchPredicateValue(
                type="batch-data",
                batchType=_dtos.BatchPredicateBatchType(
                    type="batch-predicate",
                    id=batch_type_id,
                    reference=batch_type_reference,
                ),
                featureFilters=feature_filters,
            )

        self.pythonModelInstance.inputParameters.append(
            _dtos.BatchPredicateParameter(
                type="BATCH_PREDICATE",
                sourceCodeName=source_code_name,
                value=batch_predicate_value,
            )
        )

    def add_batch_structure_input(
        self,
        source_code_name: str = "batch_structure_input",
        batch_type_id: Optional[str] = "batch_type_id",
        batch_type_reference: str = "Batch type reference",
    ):
        if batch_type_id is None:
            batch_structure_value = None
        else:
            batch_structure_value = _dtos.BatchStructureValue(
                type="batch-type", id=batch_type_id, reference=batch_type_reference
            )

        self.pythonModelInstance.inputParameters.append(
            _dtos.BatchStructureParameter(
                type="BATCH_STRUCTURE",
                sourceCodeName=source_code_name,
                value=batch_structure_value,
            )
        )

    def add_batch_tagkey_input(
        self,
        source_code_name: str = "batch_tagkey_input",
        tagkey_id: Optional[str] = "batch_tagkey_id",
        tagkey_reference: str = "Batch tag key reference",
    ):
        if tagkey_id is None:
            batch_tagkey_value = None
        else:
            batch_tagkey_value = _dtos.TagKeyValue(
                type="batch-tag-key", id=tagkey_id, reference=tagkey_reference
            )

        self.pythonModelInstance.inputParameters.append(
            _dtos.BatchTagKeyParameter(
                type="BATCH_TAG_KEY",
                sourceCodeName=source_code_name,
                value=batch_tagkey_value,
            )
        )

    def add_batch_tagvalue_input(
        self,
        source_code_name: str = "batch_tagvalue_input",
        tagvalue_id: Optional[str] = "batch_tagvalue_id",
        tagvalue_reference: str = "Batch tag value reference",
    ):
        if tagvalue_id is None:
            batch_tagvalue_value = None
        else:
            batch_tagvalue_value = _dtos.TagValueValue(
                type="batch-tag-value", id=tagvalue_id, reference=tagvalue_reference
            )

        self.pythonModelInstance.inputParameters.append(
            _dtos.BatchTagValueParameter(
                type="BATCH_TAG_VALUE",
                sourceCodeName=source_code_name,
                value=batch_tagvalue_value,
            )
        )

    def add_event_type_input(
        self,
        source_code_name: str = "event_type_input",
        event_type_id: Optional[str] = "event_type_id",
        event_type_reference: str = "Event type reference",
    ):
        if event_type_id is None:
            event_type_value = None
        else:
            event_type_value = _dtos.TagKeyValue(
                type="event-type", id=event_type_id, reference=event_type_reference
            )

        self.pythonModelInstance.inputParameters.append(
            _dtos.EventTypeParameter(
                type="EVENT_TYPE",
                sourceCodeName=source_code_name,
                value=event_type_value,
            )
        )

    def add_event_tagkey_input(
        self,
        source_code_name: str = "event_tagkey_input",
        tagkey_id: Optional[str] = "event_tagkey_id",
        tagkey_reference: str = "Event tag key reference",
    ):
        if tagkey_id is None:
            event_tagkey_value = None
        else:
            event_tagkey_value = _dtos.EventTagKeyValue(
                type="event-tag-key", id=tagkey_id, reference=tagkey_reference
            )

        self.pythonModelInstance.inputParameters.append(
            _dtos.EventTagKeyParameter(
                type="EVENT_TAG_KEY",
                sourceCodeName=source_code_name,
                value=event_tagkey_value,
            )
        )

    def add_event_tagvalue_input(
        self,
        source_code_name: str = "event_tagvalue_input",
        tagvalue_id: Optional[str] = "event_tagvalue_id",
        tagvalue_reference: str = "Event tag value reference",
    ):
        if tagvalue_id is None:
            event_tagvalue_value = None
        else:
            event_tagvalue_value = _dtos.EventTagValueValue(
                type="event-tag-value", id=tagvalue_id, reference=tagvalue_reference
            )

        self.pythonModelInstance.inputParameters.append(
            _dtos.EventTagValueParameter(
                type="EVENT_TAG_VALUE",
                sourceCodeName=source_code_name,
                value=event_tagvalue_value,
            )
        )

    def add_data_output(
        self,
        source_code_name: str = "data_output",
        data_id: Optional[str] = "data_id",
        data_reference: str = "data_reference",
        data_type: str = "STORED_CONTINUOUS",
        unit_id: str = "unit_id",
        unit_label: str = "Unit label",
        aggregation_function: Optional[str] = None,
    ):
        if data_id is None:
            data_value = None
        else:
            data_value = _dtos.DataValue(
                type="data",
                id=data_id,
                reference=data_reference,
                dataType=data_type,
                unit=_dtos.DataUnit(id=unit_id, label=unit_label),
                aggregationFunction=aggregation_function,
            )

        self.pythonModelInstance.outputParameters.append(
            _dtos.DataParameter(
                type="DATA",
                sourceCodeName=source_code_name,
                value=data_value,
            )
        )

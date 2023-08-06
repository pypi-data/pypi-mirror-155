from typing import TYPE_CHECKING, List, Optional, Union

from myst.adapters.timing import to_timing_create
from myst.client import get_client
from myst.connectors.model_connector import ModelConnector
from myst.core.time.time import Time
from myst.core.time.time_delta import TimeDelta
from myst.models.timing import ScheduleTiming, TimeRangeBoundary, from_schedule_specifier, from_time_range_boundary
from myst.models.types import ItemOrSlice, UUIDOrStr, to_uuid
from myst.openapi.api.projects.models import create_model, get_model
from myst.openapi.api.projects.models.fit_policies import create_model_fit_policy, list_model_fit_policies
from myst.openapi.api.projects.models.fit_results import get_model_fit_result, list_model_fit_results
from myst.openapi.api.projects.models.inputs import list_model_inputs
from myst.openapi.api.projects.models.run_results import get_model_run_result, list_model_run_results
from myst.openapi.models.model_create import ModelCreate
from myst.openapi.models.model_fit_policy_create import ModelFitPolicyCreate
from myst.resources.connector_node import ConnectorNode
from myst.resources.input import Input
from myst.resources.policy import ModelFitPolicy
from myst.resources.result import ModelFitResult, ModelRunResult, ModelRunResultMetadata
from myst.resources.time_series import TimeSeries

if TYPE_CHECKING:  # Avoid circular imports.
    from myst.resources.project import Project


class Model(ConnectorNode):
    """A node that learns its parameters during a training phase, and produces output during a prediction phase."""

    @classmethod
    def create(
        cls, project: "Project", title: str, connector: ModelConnector, description: Optional[str] = None
    ) -> "Model":
        """Creates a new model node.

        Args:
            project: the project in which to create the model
            title: the title of the model
            connector: the model connector to use in the model node
            description: a brief description of the model

        Returns:
            the newly created model
        """
        model = create_model.request_sync(
            client=get_client(),
            project_uuid=str(project.uuid),
            json_body=ModelCreate(
                object="Node",
                type="Model",
                title=title,
                description=description,
                connector_uuid=str(connector.uuid),
                parameters=connector.parameters_exclude_none(),
            ),
        )

        return Model.parse_obj(model.dict())

    @classmethod
    def get(cls, project_uuid: UUIDOrStr, uuid: UUIDOrStr) -> "Model":
        """Gets a specific model by its identifier."""
        model = get_model.request_sync(
            client=get_client(), project_uuid=str(to_uuid(project_uuid)), uuid=str(to_uuid(uuid))
        )

        return Model.parse_obj(model.dict())

    def create_input(
        self,
        upstream_node: TimeSeries,
        group_name: str,
        output_index: int = 0,
        label_indexer: Optional[ItemOrSlice] = None,
    ) -> Input:
        """Creates an input into this model.

        Args:
            upstream_node: the time series to feed into this model
            group_name: the name of the input group on this model's connector to which to pass the data from this input
            output_index: which time dataset, out of the sequence of upstream time datasets, to pass to this model
            label_indexer: the slice of the upstream data to pass to this model

        Returns:
            the newly created input
        """
        return Input.create(
            downstream_node=self,
            upstream_node=upstream_node,
            group_name=group_name,
            output_index=output_index,
            label_indexer=label_indexer,
        )

    def list_inputs(self) -> List[Input]:
        """Lists all inputs into this model."""
        model_inputs = list_model_inputs.request_sync(
            client=get_client(), project_uuid=str(self.project), model_uuid=str(self.uuid)
        )

        return [Input.parse_obj(input_.dict()) for input_ in model_inputs.data]

    def create_fit_policy(
        self,
        schedule_timing: Union[Time, TimeDelta, ScheduleTiming],
        start_timing: Optional[TimeRangeBoundary] = None,
        end_timing: Optional[TimeRangeBoundary] = None,
        active: bool = True,
    ) -> ModelFitPolicy:
        model_fit_policy_create = ModelFitPolicyCreate(
            object="Policy",
            type="ModelFitPolicy",
            schedule_timing=to_timing_create(from_schedule_specifier(schedule_timing)),
            start_timing=to_timing_create(from_time_range_boundary(start_timing)),
            end_timing=to_timing_create(from_time_range_boundary(end_timing)),
            active=active,
        )

        model_fit_policy = create_model_fit_policy.request_sync(
            client=get_client(),
            project_uuid=str(self.project),
            model_uuid=str(self.uuid),
            json_body=model_fit_policy_create,
        )

        return ModelFitPolicy.parse_obj(model_fit_policy.dict())

    def list_fit_policies(self) -> List[ModelFitPolicy]:
        model_fit_policies = list_model_fit_policies.request_sync(
            client=get_client(), project_uuid=str(self.project), model_uuid=str(self.uuid)
        )

        return [ModelFitPolicy.parse_obj(model_fit_policy.dict()) for model_fit_policy in model_fit_policies.data]

    def list_fit_results(self) -> List[ModelFitResult]:
        model_fit_results = list_model_fit_results.request_sync(
            client=get_client(), project_uuid=str(self.project), model_uuid=str(self.uuid)
        )

        return [
            ModelFitResult.parse_obj(dict(model_fit_result.dict(), project=self.project))
            for model_fit_result in model_fit_results.data
        ]

    def get_fit_result(self, result_uuid: UUIDOrStr) -> ModelFitResult:
        model_fit_result = get_model_fit_result.request_sync(
            client=get_client(), project_uuid=str(self.project), model_uuid=str(self.uuid), uuid=str(result_uuid)
        )

        return ModelFitResult.parse_obj(dict(model_fit_result.dict(), project=self.project))

    def list_run_results(self) -> List[ModelRunResultMetadata]:
        model_run_results = list_model_run_results.request_sync(
            client=get_client(), project_uuid=str(self.project), model_uuid=str(self.uuid)
        )

        return [
            ModelRunResultMetadata.parse_obj(dict(model_run_result.dict(), project=self.project))
            for model_run_result in model_run_results.data
        ]

    def get_run_result(self, result_uuid: UUIDOrStr) -> ModelRunResult:
        model_run_result = get_model_run_result.request_sync(
            client=get_client(), project_uuid=str(self.project), model_uuid=str(self.uuid), uuid=str(result_uuid)
        )

        return ModelRunResult.parse_obj(dict(model_run_result.dict(), project=self.project))

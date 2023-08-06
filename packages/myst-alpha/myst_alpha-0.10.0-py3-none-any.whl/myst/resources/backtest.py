import time
from typing import List, Optional
from uuid import UUID

from myst.adapters.timing import to_timing_create
from myst.client import get_client
from myst.core.time.time import Time
from myst.models.timing import AbsoluteOrCronTiming, CronTiming, TimeRangeBoundary, from_time_range_boundary
from myst.models.types import UUIDOrStr, to_uuid
from myst.openapi.api.projects.backtests import create_backtest, get_backtest, list_backtests, run_backtest
from myst.openapi.models.backtest_create import BacktestCreate
from myst.openapi.models.job_state import JobState
from myst.resources.backtest_job import BacktestJob
from myst.resources.backtest_result import BacktestResult
from myst.resources.model import Model
from myst.resources.project import Project
from myst.resources.resource import Resource


class Backtest(Resource):

    title: str
    description: Optional[str]
    project: UUID
    model: UUID
    test_start_time: Time
    test_end_time: Time
    fit_start_timing: TimeRangeBoundary
    fit_end_timing: TimeRangeBoundary
    fit_reference_timing: AbsoluteOrCronTiming
    predict_start_timing: TimeRangeBoundary
    predict_end_timing: TimeRangeBoundary
    predict_reference_timing: CronTiming

    @classmethod
    def list(self, project: Project) -> List["Backtest"]:
        """Lists all backtests associated with this project."""
        backtests = list_backtests.request_sync(client=get_client(), project_uuid=str(project.uuid))

        return [Backtest.parse_obj(backtest) for backtest in backtests.data]

    @classmethod
    def create(
        cls,
        project: Project,
        title: str,
        model: Model,
        test_start_time: Time,
        test_end_time: Time,
        fit_start_timing: TimeRangeBoundary,
        fit_end_timing: TimeRangeBoundary,
        fit_reference_timing: AbsoluteOrCronTiming,
        predict_start_timing: TimeRangeBoundary,
        predict_end_timing: TimeRangeBoundary,
        predict_reference_timing: CronTiming,
        description: Optional[str] = None,
    ) -> "Backtest":
        """Creates a new backtest."""
        backtest = create_backtest.request_sync(
            client=get_client(),
            project_uuid=str(project.uuid),
            json_body=BacktestCreate(
                object="Backtest",
                title=title,
                description=description,
                model=str(model.uuid),
                test_start_time=test_start_time.to_iso_string(),
                test_end_time=test_end_time.to_iso_string(),
                fit_start_timing=to_timing_create(from_time_range_boundary(fit_start_timing)),
                fit_end_timing=to_timing_create(from_time_range_boundary(fit_end_timing)),
                fit_reference_timing=to_timing_create(fit_reference_timing),
                predict_start_timing=to_timing_create(from_time_range_boundary(predict_start_timing)),
                predict_end_timing=to_timing_create(from_time_range_boundary(predict_end_timing)),
                predict_reference_timing=to_timing_create(predict_reference_timing),
            ),
        )

        return Backtest.parse_obj(backtest.dict())

    @classmethod
    def get(cls, project_uuid: UUIDOrStr, uuid: UUIDOrStr) -> "Backtest":
        """Gets a backtest by its identifier."""
        backtest = get_backtest.request_sync(
            client=get_client(), project_uuid=str(to_uuid(project_uuid)), uuid=str(to_uuid(uuid))
        )

        return Backtest.parse_obj(backtest.dict())

    @property
    def state(self) -> JobState:
        """Returns the state of the backtest from the latest backtest job."""
        # Refresh the related job to get the most up to date state of the backtest.
        # Note that this will make a `get` request.
        return self.get_job().state

    def run(self) -> BacktestJob:
        """Runs the backtest."""
        backtest_job = run_backtest.request_sync(
            client=get_client(), project_uuid=str(self.project), uuid=str(self.uuid)
        )

        return BacktestJob.parse_obj(backtest_job.dict())

    def get_job(self) -> BacktestJob:
        """Gets the latest job associated with this backtest.

        Returns:
            the backtest job

        Raises:
            ValueError: if the job uuid cannot be inferred from a recent run
        """
        all_backtest_jobs = BacktestJob.list(project_uuid=self.project, backtest_uuid=self.uuid)

        if len(all_backtest_jobs) == 0:
            raise ValueError("This backtest has not yet been `run`. Please run the backtest before requesting a job.")
        else:
            return all_backtest_jobs[0]

    def get_result(self) -> BacktestResult:
        """Gets the latest result associated with a job for this backtest.

        Returns:
            the backtest result

        Raises:
            ValueError: if the job uuid cannot be inferred from a recent run
        """
        all_backtest_jobs = BacktestJob.list(project_uuid=self.project, backtest_uuid=self.uuid)

        if len(all_backtest_jobs) == 0:
            raise ValueError(
                "This backtest has not yet been `run`. Please run the backtest before requesting a result."
            )
        else:
            job_uuid = all_backtest_jobs[0].uuid

        return BacktestResult.get(project_uuid=self.project, backtest_uuid=self.uuid, job_uuid=job_uuid)

    def wait_until_completed(self) -> None:
        """Returns the backtest job once it has completed."""
        while True:
            refreshed_backtest_job = self.get_job()

            if refreshed_backtest_job.is_completed():
                break

            time.sleep(60)

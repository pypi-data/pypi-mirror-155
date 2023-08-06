from typing import List
from uuid import UUID

from myst.client import get_client
from myst.models.base_model import BaseModel
from myst.models.types import UUIDOrStr, to_uuid
from myst.openapi.api.projects.backtests.jobs import list_backtest_jobs
from myst.openapi.models.job_state import JobState


class BacktestJob(BaseModel):

    uuid: UUID
    backtest: UUID
    state: JobState

    @classmethod
    def list(self, project_uuid: UUIDOrStr, backtest_uuid: UUIDOrStr) -> List["BacktestJob"]:
        """Lists all jobs for the backtest."""
        backtest_jobs = list_backtest_jobs.request_sync(
            client=get_client(), project_uuid=str(to_uuid(project_uuid)), backtest_uuid=str(to_uuid(backtest_uuid))
        )

        return [BacktestJob.parse_obj(backtest_job) for backtest_job in backtest_jobs.data]

    def is_completed(self) -> bool:
        """Returns `True` if the job has completed.

        Completed jobs include both successful and failed jobs.

        Returns:
            whether the job has completed
        """
        return self.state in [JobState.SUCCESS, JobState.FAILURE]

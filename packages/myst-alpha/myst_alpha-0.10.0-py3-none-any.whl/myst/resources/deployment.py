from typing import Optional
from uuid import UUID

from myst.core.time.time import Time
from myst.resources.resource import Resource


class Deployment(Resource):
    """A particular deployment of a project.

    A deployment is "active" if its `activate_time` is not `None` and its `deactivate_time` is `None`.

    Attributes:
        title: the title of the deployment.
        project: the identifier of the project with which the deployment is associated.
        activate_time: the time at which the deployment was activated, if any.
        deactive_time: the time at which the deployment was deactivated, if any.
    """

    title: str
    project: UUID
    activate_time: Optional[Time] = None
    deactivate_time: Optional[Time] = None

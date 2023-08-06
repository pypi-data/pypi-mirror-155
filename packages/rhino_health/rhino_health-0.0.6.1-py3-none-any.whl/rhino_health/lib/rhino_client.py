from rhino_health.lib.constants import ApiEnvironment
from rhino_health.lib.endpoints.aimodel.aimodel_endpoints import AIModelEndpoints
from rhino_health.lib.endpoints.cohort.cohort_endpoints import (
    CohortEndpoints,
    CohortFutureEndpoints,
)
from rhino_health.lib.endpoints.dataschema.dataschema_endpoints import (
    DataschemaEndpoints,
    DataschemaFutureEndpoints,
)
from rhino_health.lib.endpoints.model_result.model_result_endpoints import ModelResultEndpoints
from rhino_health.lib.endpoints.project.project_endpoints import (
    ProjectEndpoints,
    ProjectFutureEndpoints,
)
from rhino_health.lib.utils import url_for

__api__ = ["RhinoClient"]


class EndpointTypes:
    """
    Constants for different endpoint types. This is how we group and separate different endpoints
    """

    PROJECT = "project"
    COHORT = "cohort"
    DATASCHEMA = "dataschema"
    AIMODEL = "aimodel"
    MODEL_RESULT = "model_action"


class SDKVersion:
    """
    Used internally for future backwards compatibility
    """

    STABLE = "0.1"
    PREVIEW = "1.0"


VERSION_TO_CLOUD_API = {SDKVersion.STABLE: "v1", SDKVersion.PREVIEW: "v1"}


VERSION_TO_ENDPOINTS = {
    SDKVersion.STABLE: {
        EndpointTypes.PROJECT: ProjectEndpoints,
        EndpointTypes.COHORT: CohortEndpoints,
        EndpointTypes.DATASCHEMA: DataschemaEndpoints,
        EndpointTypes.AIMODEL: AIModelEndpoints,
        EndpointTypes.MODEL_RESULT: ModelResultEndpoints,
    },
    SDKVersion.PREVIEW: {
        EndpointTypes.PROJECT: ProjectFutureEndpoints,
        EndpointTypes.COHORT: CohortFutureEndpoints,
        EndpointTypes.DATASCHEMA: DataschemaFutureEndpoints,
        EndpointTypes.AIMODEL: AIModelEndpoints,
        EndpointTypes.MODEL_RESULT: ModelResultEndpoints,
    },
}


class RhinoClient:
    """
    Allows access to various endpoints directly from the RhinoSession

    Attributes
    ----------
    project: Access endpoints at the project level
    cohort: Access endpoints at the cohort level
    dataschema: Access endpoints at the schema level

    Examples
    --------
    >>> session.project.get_projects()
    array[Project...]
    >>> session.cohort.get_cohort(my_cohort_id)
    Cohort

    See Also
    --------
    rhino_health.lib.endpoints.project.project_endpoints: Available project endpoints
    rhino_health.lib.endpoints.cohort.cohort_endpoints: Available cohort endpoints
    rhino_health.lib.endpoints.dataschema.dataschema_endpoints: Available dataschema endpoints
    """

    def __init__(
        self,
        rhino_api_url: str = ApiEnvironment.PROD_API_URL,
        sdk_version: str = SDKVersion.PREVIEW,
    ):
        self.rhino_api_url = rhino_api_url
        self.sdk_version = sdk_version
        if sdk_version not in VERSION_TO_ENDPOINTS.keys():
            raise ValueError(
                "The api version you specified is not supported in this version of the SDK"
            )
        self.project: ProjectEndpoints = VERSION_TO_ENDPOINTS[sdk_version][EndpointTypes.PROJECT](
            self
        )
        self.cohort: CohortEndpoints = VERSION_TO_ENDPOINTS[sdk_version][EndpointTypes.COHORT](self)
        self.dataschema: DataschemaEndpoints = VERSION_TO_ENDPOINTS[sdk_version][
            EndpointTypes.DATASCHEMA
        ](self)
        self.aimodel: AIModelEndpoints = VERSION_TO_ENDPOINTS[sdk_version][EndpointTypes.AIMODEL](
            self
        )
        self.model_result: ModelResultEndpoints = VERSION_TO_ENDPOINTS[sdk_version][
            EndpointTypes.MODEL_RESULT
        ](self)
        self.api_url = url_for(self.rhino_api_url, VERSION_TO_CLOUD_API[sdk_version])

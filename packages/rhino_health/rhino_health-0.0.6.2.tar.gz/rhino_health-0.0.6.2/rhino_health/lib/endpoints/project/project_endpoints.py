from typing import List, Optional

from rhino_health.lib.endpoints.cohort.cohort_dataclass import Cohort, FutureCohort
from rhino_health.lib.endpoints.dataschema.dataschema_dataclass import Dataschema, FutureDataschema
from rhino_health.lib.endpoints.endpoint import Endpoint
from rhino_health.lib.endpoints.project.project_dataclass import FutureProject, Project
from rhino_health.lib.endpoints.workgroup.workgroup_dataclass import FutureWorkgroup, Workgroup
from rhino_health.lib.metrics.aggregate_metrics import calculate_aggregate_metric
from rhino_health.lib.metrics.base_metric import MetricResponse


class ProjectEndpoints(Endpoint):
    """
    @autoapi False

    Rhino SDK LTS supported endpoints

    Endpoints listed here will not change
    """

    @property
    def project_dataclass(self):
        """
        @autoapi False
        """
        return Project

    @property
    def workgroup_dataclass(self):
        """
        @autoapi False
        """
        return Workgroup

    @property
    def cohort_dataclass(self):
        """
        @autoapi False
        """
        return Cohort

    @property
    def dataschema_dataclass(self):
        """
        @autoapi False
        """
        return Dataschema

    def get_projects(self, project_uids: Optional[List[str]] = None) -> List[Project]:
        """
        Returns projects the SESSION has access to. If uids are provided, returns only the
        project_uids that are specified.

        :param project_uids: Optional List of strings of project uids to get
        """
        if not project_uids:
            return self.session.get("/projects/").to_dataclasses(self.project_dataclass)
        else:
            return [
                self.session.get(f"/projects/{project_uid}/").to_dataclass(self.project_dataclass)
                for project_uid in project_uids
            ]


class ProjectFutureEndpoints(ProjectEndpoints):
    """
    @autoapi True
    @objname ProjectEndpoints

    Endpoints available to interact with Projects on the Rhino Platform

    Notes
    -----
    You should access these endpoints from the RhinoSession object
    """

    @property
    def project_dataclass(self):
        return FutureProject

    @property
    def workgroup_dataclass(self):
        return FutureWorkgroup

    @property
    def cohort_dataclass(self):
        return FutureCohort

    @property
    def dataschema_dataclass(self):
        return FutureDataschema

    def get_cohorts(self, project_uid: str) -> List[Cohort]:
        if not project_uid:
            raise ValueError("Must provide a project id")
        return self.session.get(f"/projects/{project_uid}/cohorts").to_dataclasses(
            self.cohort_dataclass
        )

    def get_dataschemas(self, project_uid: str) -> List[FutureDataschema]:
        if not project_uid:
            raise ValueError("Must provide a project id")
        return self.session.get(f"/projects/{project_uid}/dataschemas").to_dataclasses(
            self.cohort_dataclass
        )

    def get_collaborating_workgroups(self, project_uid: str):
        return self.session.get(f"/projects/{project_uid}/collaborators").to_dataclasses(
            self.workgroup_dataclass
        )

    def add_collaborator(self, project_uid: str, collaborating_workgroup_uid: str):
        """
        Adds COLLABORATING_WORKGROUP_UID as a collaborator to PROJECT_UID

        .. warning:: This feature is under development and the interface may change
        """
        # TODO: What should this return internally
        # TODO: Backend needs to return something sensible
        # TODO: Automatically generated swagger docs don't match with internal code
        self.session.post(
            f"/projects/{project_uid}/add_collaborator/{collaborating_workgroup_uid}", {}
        )

    def remove_collaborator(self, project_uid: str, collaborating_workgroup_uid: str):
        """
        Removes COLLABORATING_WORKGROUP_UID as a collaborator from PROJECT_UID

        .. warning:: This feature is under development and the interface may change
        """
        # TODO: What should this return internally
        # TODO: Backend needs to return something sensible
        # TODO: Automatically generated swagger docs don't match with internal code
        self.session.post(
            f"/projects/{project_uid}/remove_collaborator/{collaborating_workgroup_uid}", {}
        )

    def aggregate_cohort_metric(
        self, cohort_uids: List[str], metric_configuration
    ) -> MetricResponse:
        metric_results = [
            self.session.cohort.get_cohort_metric(cohort_uid, metric_configuration)
            for cohort_uid in cohort_uids
        ]
        return MetricResponse(
            output=calculate_aggregate_metric(
                metric_configuration, [metric_result.output for metric_result in metric_results]
            )
        )

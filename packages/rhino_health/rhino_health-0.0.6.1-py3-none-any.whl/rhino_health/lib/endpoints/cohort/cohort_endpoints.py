from rhino_health.lib.endpoints.cohort.cohort_dataclass import Cohort, FutureCohort
from rhino_health.lib.endpoints.endpoint import Endpoint
from rhino_health.lib.metrics.base_metric import MetricResponse


class CohortEndpoints(Endpoint):
    """
    @autoapi False
    """

    @property
    def cohort_data_class(self):
        return Cohort

    def get_cohort(self, cohort_uid: str):
        """
        @autoapi True
        Returns a Cohort dataclass

        Parameters
        ----------
        cohort_uid: str
            UID for the cohort

        Returns
        -------
        cohort: Cohort
            Cohort dataclass

        Examples
        --------
        >>> session.cohort.get_cohort(my_cohort_uid)
        Cohort()
        """
        return self.session.get(f"/cohorts/{cohort_uid}").to_dataclass(self.cohort_data_class)

    def get_cohort_metric(self, cohort_uid: str, metric_configuration) -> MetricResponse:
        """
        @autoapi True
        Queries the cohort with COHORT_UID on-prem and returns the result based on the METRIC_CONFIGURATION

        Parameters
        ----------
        cohort_uid: str
            UID for the cohort to query metrics against
        metric_configuration:
            Configuration for the query to run

        Returns
        -------
        metric_response: MetricResponse
            A response object containing the result of the query

        See Also
        --------
        rhino_health.lib.metrics : Dataclasses specifying possible metric configurations to send
        rhino_health.lib.metrics.base_metric.MetricResponse : Response object
        """
        return self.session.post(
            f"/cohorts/{cohort_uid}/metric/", metric_configuration.data()
        ).to_dataclass(MetricResponse)


class CohortFutureEndpoints(CohortEndpoints):
    """
    @autoapi True
    @objname CohortEndpoints

    Endpoints available to interact with Cohorts on the Rhino Platform

    Notes
    -----
    You should access these endpoints from the RhinoSession object
    """

    @property
    def cohort_data_class(self):
        """
        @autoapi False
        Dataclass to return for a cohort endpoint for backwards compatibility
        """
        return FutureCohort

    # def add_cohort(session: RhinoSession, cohort_data: CohortCreateData = None):
    #     """
    #     NOT OFFICIALLY SUPPORTED/COMPLETE YET, also no current supported way to send cohort data over remote
    #     (import location has to be on the on-prem instance)
    #     """
    #     payload_data = cohort_data.__dict__
    #     create_data = {k: v for k, v in payload_data.items() if k in []}
    #     import_data = {k: v for k, v in payload_data.items() if k in []}
    #     newly_created_cohort = session.post("/cohorts/", create_data).to_dataclass(Cohort)
    #     return session.post(f"/cohorts/{newly_created_cohort.uid}/import", import_data)

    def export_cohort(self, cohort_uid: str, output_location: str, output_format: str):
        """
        Sends a export cohort request to the ON-PREM instance holding the specified COHORT_UID.
        The file will be exported to OUTPUT_LOCATION on the on-prem instance in OUTPUT_FORMAT

        .. warning:: This feature is under development and the interface may change

        Parameters
        ----------
        cohort_uid: str
            UID for the cohort to export information on
        output_location: str
            Path to output the exported data to on the remote on-prem instance
        output_format: str
            The format to export the cohort data in
        """
        return self.session.get(
            f"/cohorts/{cohort_uid}/export",
            params={"output_location": output_location, "output_format": output_format},
        )

    def sync_cohort_info(self, cohort_uid: str):
        """
        Initializes a data sync from the relevant on-prem instance for the provided COHORT_UID

        .. warning:: This feature is under development and the interface may change

        Parameters
        ----------
        cohort_uid: str
            UID for the cohort to sync info
        """
        # TODO: what should this return value be?
        return self.session.get(f"/cohorts/{cohort_uid}/info")

    def remove_cohort(self, cohort_uid: str):
        """
        Remove a cohort with COHORT_UID from the system

        .. warning:: This feature is under development and the interface may change

        Parameters
        ----------
        cohort_uid: str
            UID for the cohort to remove
        """
        # TODO: what should this return value be?
        return self.session.post(f"/cohorts/{cohort_uid}/remove", {})

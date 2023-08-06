from rhino_health.lib.endpoints.aimodel.aimodel_dataclass import (
    AIModel,
    AIModelCreateInput,
    AIModelRunInput,
    AIModelTrainInput,
)
from rhino_health.lib.endpoints.endpoint import Endpoint


class AIModelEndpoints(Endpoint):
    """
    @autoapi True

    Rhino SDK LTS supported endpoints
    """

    @property
    def aimodel_data_class(self):
        """
        @autoapi False
        """
        return AIModel

    def get_aimodel(self, aimodel_uid: str):
        """
        Returns a AIModel dataclass

        Parameters
        ----------
        aimodel_uid: str
            UID for the aimodel

        Returns
        -------
        aimodel: AIModel
            AIModel dataclass

        Examples
        --------
        >>> session.aimodel.get_aimodel(my_aimodel_uid)
        AIModel()
        """
        result = self.session.get(f"/aimodels/{aimodel_uid}")
        return result.to_dataclass(self.aimodel_data_class)

    def create_aimodel(self, aimodel: AIModelCreateInput):
        """
        Returns a AIModel dataclass

        Parameters
        ----------
        aimodel: AIModelCreateInput
            AIModelCreateInput data class

        Returns
        -------
        aimodel: AIModel
            AIModel dataclass

        Examples
        --------
        >>> session.aimodel.create_aimodel(create_aimodel_input)
        AIModelCreateInput()
        """
        result = self.session.post(
            f"/aimodels", data=aimodel.dict(by_alias=True), adapter_kwargs={"data_as_json": True}
        )
        return result.to_dataclass(self.aimodel_data_class)

    def run_aimodel(self, aimodel: AIModelRunInput):
        """
        @autoapi True
        Returns a model_action_uid

        Parameters
        ----------
        aimodel: AIModelRunInput
            RunAIModelInput data class

        Returns
        -------
        model_action_uid: str

        Examples
        --------
        >>> session.aimodel.run_aimodel(run_aimodel_input)
        AIModelRunInput()
        """
        return self.session.post(
            f"/aimodels/{aimodel.aimodel_uid}/run",
            data=aimodel.dict(by_alias=True),
            adapter_kwargs={"data_as_json": True},
        )

    def train_aimodel(self, aimodel: AIModelTrainInput):
        """
        @autoapi True
        Returns a dict {status, d}

        Parameters
        ----------
        aimodel: AIModelTrainInput
            AIModelTrainInput data class

        Returns
        -------
        model_action_uid: str

        Examples
        --------
        >>> session.aimodel.train_aimodel(run_nvflare_aimodel_input)
        AIModelTrainInput()
        """
        return self.session.post(
            f"/aimodels/{aimodel.aimodel_uid}/train",
            data=aimodel.dict(by_alias=True),
            adapter_kwargs={"data_as_json": True},
        )

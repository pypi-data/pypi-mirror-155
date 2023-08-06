import pathlib
from typing import Dict, Any
from clients_core.service_clients import E360ServiceClient
from .models import PlotlyVisualisationModel, VisualisationModel
from .utils import VRSConverter


class PlotlyVisualizationResourceClient(E360ServiceClient):
    """
    Subclasses dataclass `clients_core.service_clients.E360ServiceClient`.

    Args:
        client (clients_core.rest_client.RestClient): an instance of a rest client
        user_id (str): the user_id guid

    """

    service_endpoint = ""
    extra_headers = {
        "accept": "application/json",
        "Content-Type": "application/json-patch+json",
    }

    def create(
        self, payload: Dict, from_plotly: bool = False, **kwargs: Any
    ) -> PlotlyVisualisationModel:
        """
        Creates a visualisation, returns a deserialised model instance.

        Args:
            payload: VRS compatible plotly payload
            from_plotly: converts from a plotly payload to a VRS payload structure, default False

        """
        if from_plotly is True:
            data = VRSConverter(payload).dump()
        else:
            data = PlotlyVisualisationModel.validate(payload).dump()

        response = self.client.post(
            "", json=data, headers=self.service_headers, raises=True, **kwargs
        )
        return PlotlyVisualisationModel.parse_obj(response.json())

    def update(
        self,
        visualisation_id: str,
        payload: Dict,
        from_plotly: bool = False,
        **kwargs: Any,
    ) -> PlotlyVisualisationModel:
        """
        Updates a visualisation by id with new payload, returns a deserialised model instance.

        Args:
            visualisation_id: visualisation id that needs updating
            payload: VRS compatible plotly payload
            from_plotly: converts from a plotly payload to a VRS payload structure, default False

        """
        if from_plotly is True:
            data = VRSConverter(payload).dump()
        else:
            data = PlotlyVisualisationModel.validate(payload).dump()

        response = self.client.put(
            str(visualisation_id),
            json=data,
            headers=self.service_headers,
            raises=True,
            **kwargs,
        )
        return PlotlyVisualisationModel.parse_obj(response.json())

    def delete_by_id(self, visualisation_id: str, **kwargs: Any) -> bool:
        """
        Delete the visualisation object by its id. Returns True when deleted successfully.
        """
        response = self.client.delete(
            str(visualisation_id), headers=self.service_headers, **kwargs
        )
        return response.ok


class VisualizationResourceClient(E360ServiceClient):
    """
    Subclasses dataclass `clients_core.service_clients.E360ServiceClient`.

    Args:
        client (clients_core.rest_client.RestClient): an instance of a rest client
        user_id (str): the user_id guid

    """

    service_endpoint = ""

    def _get_headers(
        self, auth_headers: Dict, content_type: str = "application/json-patch+json"
    ) -> dict:
        return {
            "accept": "application/json",
            "Content-Type": content_type,
            **auth_headers,
        }

    def create(self, payload: Dict, **kwargs: Any) -> VisualisationModel:
        """
        Creates a visualisation, returns a deserialised model instance.

        Args:
            payload: VRS compatible visualisation payload

        """
        # data = VisualisationModel.Schema().load(payload)  # type: ignore
        data = VisualisationModel.validate(payload).dict(by_alias=True)
        response = self.client.post(
            "",
            json=data,
            headers=self._get_headers(self.service_headers),
            raises=True,
            **kwargs,
        )

        response_json = response.json()
        return VisualisationModel.parse_obj(response_json)

    def delete_by_id(self, visualisation_id: str, **kwargs: Any) -> bool:
        """
        Delete the visualisation object by its id. Returns True when deleted successfully.
        """
        response = self.client.delete(
            str(visualisation_id),
            headers=self._get_headers(self.service_headers),
            **kwargs,
        )
        return response.ok

    def upload_file(
        self,
        visualisation_id: str,
        file_path: pathlib.Path,
        content_type: str = "text/csv",
        **kwargs: Any,
    ) -> bool:
        """
        Upload a file for an existing visualisation.

        Args:
            visualisation_id: id of an existing visualisation
            file_path: file path object which needs to be uploaded

        Kwargs:
            timeout (int): optional, maximum value in seconds for the operation to run for.

        """
        with file_path.open("rb") as file_buffer:
            response = self.client.put(
                f"{visualisation_id}/data",
                data=file_buffer,
                headers=self._get_headers(self.service_headers, content_type),
                raises=True,
                **kwargs,
            )
        return response.ok

    def create_and_upload(
        self, payload: Dict, file_path: pathlib.Path, **kwargs: Any
    ) -> VisualisationModel:
        """
        Combines creation of a visualisation and uploading of the file.
        """
        visualisation = self.create(payload, **kwargs)
        self.upload_file(visualisation.id, file_path, **kwargs)
        return visualisation

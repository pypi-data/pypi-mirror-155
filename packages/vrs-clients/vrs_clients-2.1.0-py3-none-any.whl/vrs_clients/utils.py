import json
import importlib
from typing import Dict, Any
from dataclasses import dataclass
from .models import VRSPlotlyConverterVisualisationSchema


@dataclass
class VRSConverter:
    """
    Takes a plain Plotly json payload and transforms it to a VRS payload.
    """

    payload: Dict

    _plotly_utils = "plotly.utils"
    _plotly_encoder = "PlotlyJSONEncoder"

    @classmethod
    def json_from_figure(cls, data: dict, encoder: Any = json.JSONEncoder) -> dict:
        """
        Ensures the data is serialisable to JSON.
        If plotly objects are used, they get serialised by dynamically imported plotly.utils.
        """
        try:
            serialized = json.dumps(data, cls=encoder)
            return json.loads(serialized)
        except TypeError:
            try:
                plotly_utils = importlib.import_module(cls._plotly_utils)
                plotly_encoder = getattr(plotly_utils, cls._plotly_encoder)
                return cls.json_from_figure(data, encoder=plotly_encoder)
            except ImportError:
                err_mod = ModuleNotFoundError(
                    f"Tried importing '{cls._plotly_utils}', but module was not found."
                )
                raise ValueError(
                    "Ensure the payload value is JSON serializable, or is a plotly object."
                ) from err_mod

    def dump(self) -> dict:
        data = self.json_from_figure(self.payload)
        return VRSPlotlyConverterVisualisationSchema().load(data)

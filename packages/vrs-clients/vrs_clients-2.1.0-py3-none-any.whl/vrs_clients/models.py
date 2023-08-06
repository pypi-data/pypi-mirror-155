import json
import datetime
import warnings
from typing import List, Optional, Any
import marshmallow as ma
from pydantic import BaseModel, Field


class PlotlyVisualisationModel(BaseModel):
    reports: List[dict] = Field(..., min_items=1)
    stratifications: list = Field(default_factory=list)
    id: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None
    version: Optional[int] = None
    created: Optional[datetime.datetime] = None
    updated: Optional[datetime.datetime] = None

    def dump(self) -> dict:
        return json.loads(self.json(by_alias=True))


class VisualisationModel(PlotlyVisualisationModel):
    visType: str


# --- VRS->PLOTLY CONVERTER SCHEMAS -------------------------------------------


class BaseSchema(ma.Schema):
    class Meta:
        unknown = ma.INCLUDE


class VRSPlotlyConverterChartDataSchema(BaseSchema):
    pass


class VRSPlotlyConverterLayoutSchema(BaseSchema):
    title = ma.fields.String()


class VRSPlotlyConverterChartSchema(BaseSchema):
    type = ma.fields.String()
    data = ma.fields.List(ma.fields.Nested(VRSPlotlyConverterChartDataSchema))


class VRSPlotlyConverterReportSchema(BaseSchema):
    name = ma.fields.String(required=False)
    layout = ma.fields.Nested(VRSPlotlyConverterLayoutSchema, required=False)
    charts = ma.fields.List(ma.fields.Nested(VRSPlotlyConverterChartSchema))

    @ma.pre_load
    def on_load(self, data: dict, **kwargs: Any) -> dict:
        datas = data.pop("data")
        chart_types = set(d.pop("type") for d in datas)
        data["charts"] = [{"data": datas, "type": chart_types.pop()}]
        if chart_types:
            warnings.warn(
                "\nDifferent chart types detected across multiple traces.\n"
                "VRS can only handle a single chart type for all data traces.\n"
                f"Producing a chart using `{data['charts'][0]['type']}` type only.\n"
                "Ensure the same chart type is used for all data traces.",
                UserWarning,
            )
        _title = data.get("layout", {}).pop("title", None)
        if isinstance(_title, dict):
            for key in ["text", "title_text"]:
                if key in _title:
                    _title = _title[key]
        if _title is not None:
            data["name"] = _title
        return data


class VRSPlotlyConverterVisualisationSchema(BaseSchema):
    reports = ma.fields.List(ma.fields.Nested(VRSPlotlyConverterReportSchema))

    @ma.pre_load
    def on_load(self, data: dict, **kwargs: Any) -> dict:
        return dict(reports=[data])

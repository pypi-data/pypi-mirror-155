from dataclasses import dataclass
from typing import Optional

from annotell.input_api.model.base_serializer import BaseSerializer
from annotell.input_api.model.input.resources.resource import Resource
from annotell.input_api.util import filter_none

camera_sensor_default = "CAM"


class ImageMetadata(BaseSerializer):
    shutter_time_start_ns: int
    shutter_time_end_ns: int


@dataclass
class Image(Resource):
    filename: str
    resource_id: Optional[str] = None
    sensor_name: str = camera_sensor_default
    metadata: Optional[ImageMetadata] = None

    def to_dict(self) -> dict:
        temp = {"filename": self.filename, "resourceId": self.resolve_resource_id(), "sensorName": self.sensor_name}
        if self.metadata is not None:
            temp["metadata"] = self.metadata.to_dict()

        return filter_none(temp)

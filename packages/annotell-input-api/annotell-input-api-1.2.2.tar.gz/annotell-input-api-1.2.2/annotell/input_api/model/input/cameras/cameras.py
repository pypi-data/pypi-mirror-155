from dataclasses import dataclass, field
from typing import Optional

from annotell.input_api.model.input.cameras.frame import Frame
from annotell.input_api.model.input.metadata.metadata import AllowedMetaData, metadata_to_dict
from annotell.input_api.model.input.sensor_specification import SensorSpecification


@dataclass
class Cameras:
    external_id: str
    frame: Frame
    sensor_specification: Optional[SensorSpecification] = None
    metadata: AllowedMetaData = field(default_factory=dict)

    def to_dict(self) -> dict:
        return dict(
            frame=self.frame.to_dict(),
            sensorSpecification=self.sensor_specification.to_dict() if isinstance(self.sensor_specification, SensorSpecification) else None,
            externalId=self.external_id,
            metadata=metadata_to_dict(self.metadata)
        )

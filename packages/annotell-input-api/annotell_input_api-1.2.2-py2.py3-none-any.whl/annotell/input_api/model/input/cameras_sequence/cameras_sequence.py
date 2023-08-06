from dataclasses import dataclass, field
from typing import List, Optional

from annotell.input_api.model.input.cameras_sequence.frame import Frame
from annotell.input_api.model.input.metadata.metadata import AllowedMetaData, metadata_to_dict
from annotell.input_api.model.input.sensor_specification import SensorSpecification


@dataclass
class CamerasSequence:
    external_id: str
    frames: List[Frame]
    sensor_specification: Optional[SensorSpecification] = None
    metadata: AllowedMetaData = field(default_factory=dict)

    def to_dict(self) -> dict:
        return dict(
            frames=[frame.to_dict() for frame in self.frames],
            sensorSpecification=self.sensor_specification.to_dict() if isinstance(self.sensor_specification, SensorSpecification) else None,
            externalId=self.external_id,
            metadata=metadata_to_dict(self.metadata)
        )

from dataclasses import dataclass, field
from typing import List, Optional

from annotell.input_api.model.ego.imu_data import IMUData
from annotell.input_api.model.input.lidars_and_cameras.frame import Frame
from annotell.input_api.model.input.metadata.metadata import AllowedMetaData, metadata_to_dict
from annotell.input_api.model.input.sensor_specification import SensorSpecification


@dataclass
class LidarsAndCameras:
    external_id: str
    frame: Frame
    calibration_id: str
    sensor_specification: Optional[SensorSpecification] = None
    metadata: AllowedMetaData = field(default_factory=dict)
    imu_data: List[IMUData] = field(default_factory=list)

    def to_dict(self) -> dict:
        return dict(
            frame=self.frame.to_dict(),
            sensorSpecification=self.sensor_specification.to_dict() if isinstance(self.sensor_specification, SensorSpecification) else None,
            externalId=self.external_id,
            calibrationId=self.calibration_id,
            metadata=metadata_to_dict(self.metadata)
        )

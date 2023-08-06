from dataclasses import dataclass, field
from typing import List

from annotell.input_api.model import IMUData
from annotell.input_api.model.input.lidars_and_cameras.frame import Frame
from annotell.input_api.model.input.metadata.metadata import AllowedMetaData, metadata_to_dict


@dataclass
class Lidars:
    external_id: str
    frame: Frame
    metadata: AllowedMetaData = field(default_factory=dict)
    imu_data: List[IMUData] = field(default_factory=list)

    def to_dict(self) -> dict:
        return dict(
            frame=self.frame.to_dict(),
            externalId=self.external_id,
            metadata=metadata_to_dict(self.metadata),
        )

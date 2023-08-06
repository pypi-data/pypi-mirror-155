from typing import List, Optional

from annotell.input_api.model.base_serializer import BaseSerializer


class InputFromSceneRequest(BaseSerializer):
    scene_uuid: str
    annotation_types: List[str]
    project: str
    batch: Optional[str]

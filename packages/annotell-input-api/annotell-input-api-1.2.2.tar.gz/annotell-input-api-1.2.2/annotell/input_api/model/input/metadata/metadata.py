from typing import Mapping, Optional, Union

from pydantic import BaseModel

MetaDataMapping = Mapping[str, Union[int, float, str, bool]]


class MetaData(BaseModel):
    """
    Container for metadata belonging to the input.
    The attributes of this class are reserved keywords
    with assiciated functionality in the Annotell platform.

    Attributes:
        region: A string indicating the region the data was collected in. 
            If there are annotation instructions associated with a specific
            region, talk to your contact at Annotell to sync what should be
            specified in the region attribute.
    """
    region: Optional[str]

    class Config:
        extra = "allow"


AllowedMetaData = Union[MetaDataMapping, MetaData]


def metadata_to_dict(metadata: AllowedMetaData) -> MetaDataMapping:
    if isinstance(metadata, MetaData):
        return metadata.dict()
    return metadata

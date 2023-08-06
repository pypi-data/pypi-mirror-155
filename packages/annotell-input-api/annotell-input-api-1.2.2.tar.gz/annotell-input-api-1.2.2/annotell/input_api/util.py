"""Utility functions for Input API """

from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import dateutil.parser
from PIL import Image as PILImage


def ts_to_dt(date_string: str) -> datetime:
    """
    Parse string datetime into datetime
    """
    return dateutil.parser.parse(date_string)


def filter_none(js: dict) -> dict:
    if isinstance(js, Mapping):
        return {k: filter_none(v) for k, v in js.items() if v is not None}
    else:
        return js


def get_view_links(input_uuids: List[str]) -> Dict[str, str]:
    """
        For each given input uuid returns an URL where the input can be viewed in the web app.

        :param input_uuids: List with input uuids
        :return Dict: Dictionary mapping each uuid with an URL to view the input.
        """
    view_dict = dict()
    for input_uuid in input_uuids:
        view_dict[input_uuid] = f"https://app.annotell.com/input-view/{input_uuid}"

    return view_dict

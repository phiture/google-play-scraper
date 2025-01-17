import json
from typing import Dict

from ..constants.element import ElementSpecs
from ..constants.regex import Regex
from ..constants.request import Formats
from ..utils.request import post


def permissions(app_id: str, lang: str = "en", country: str = "us") -> Dict[str, list]:
    dom = post(
        Formats.Permissions.build(lang=lang, country=country),
        Formats.Permissions.build_body(app_id),
        {"content-type": "application/x-www-form-urlencoded"},
    )

    matches = json.loads(Regex.PERMISSIONS.findall(dom)[0])
    container = json.loads(matches[0][2])

    result = {}

    for permission_items in container:
        if isinstance(permission_items, list):
            if len(permission_items[0]) == 2:
                # rearrange layout to fit ElementSpecs
                permission_items = [["Uncategorized", None, permission_items, None]]

            for permission in permission_items:
                if permission:
                    result[
                        ElementSpecs.Permission_Type.extract_content(permission)
                    ] = ElementSpecs.Permission_List.extract_content(permission)

    return result

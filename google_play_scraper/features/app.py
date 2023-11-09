import json
from typing import Any, Dict

from ..constants.element import ElementSpecs
from ..constants.regex import Regex
from ..constants.request import Formats
from ..exceptions import NotFoundError
from ..utils.request import get


def app(app_id: str, lang: str = "en", country: str = "us") -> Dict[str, Any]:
    url = Formats.Detail.build(app_id=app_id, lang=lang, country=country)

    try:
        dom = get(url)
    except NotFoundError:
        url = Formats.Detail.fallback_build(app_id=app_id, lang=lang)
        dom = get(url)
    return parse_dom(dom=dom, app_id=app_id, url=url)


def parse_dom(dom: str, app_id: str, url: str) -> Dict[str, Any]:
    matches = Regex.SCRIPT.findall(dom)

    dataset = {}
    dataset_hash = {}

    for match in matches:
        key_ds_match = Regex.KEY_DS.findall(match)
        key_hash_match = Regex.KEY_HASH.findall(match)
        value_match = Regex.VALUE.findall(match)

        if key_ds_match and key_hash_match and value_match:
            key = key_ds_match[0]
            key_hash = key_hash_match[0].replace(" ", "").replace("'", "")
            value = json.loads(value_match[0])

            dataset[key] = value
            dataset_hash[key_hash] = value

    result = {}

    ds_num = None
    for k, v in dataset.items():
        tmp_ds_num = int(k.replace("ds:", ""))
        extracted_app_id = (
            ElementSpecs(tmp_ds_num).Detail["appId"].extract_content(dataset)
        )
        extracted_title = (
            ElementSpecs(tmp_ds_num).Detail["title"].extract_content(dataset)
        )
        if extracted_app_id == app_id and extracted_title is not None:
            ds_num = tmp_ds_num
            break

    for k, spec in ElementSpecs(ds_num).Detail.items():
        if isinstance(spec, list):
            for sub_spec in spec:
                content = sub_spec.extract_content(dataset)

                if content is not None:
                    result[k] = content
                    break
        else:
            content = spec.extract_content(dataset)

            result[k] = content

    result["appId"] = app_id
    result["url"] = url

    return result

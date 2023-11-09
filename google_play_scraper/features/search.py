import json
from typing import Any, Dict, List
from urllib.parse import quote

from ..constants.element import ElementSpecs
from ..constants.regex import Regex
from ..constants.request import Formats
from ..exceptions import NotFoundError
from ..utils.request import get


def search(
    query: str, n_hits: int = 30, lang: str = "en", country: str = "us"
) -> List[Dict[str, Any]]:
    query = quote(query)
    url = Formats.Searchresults.build(query=query, lang=lang, country=country)
    try:
        dom = get(url)
    except NotFoundError:
        url = Formats.Searchresults.fallback_build(query=query, lang=lang)
        dom = get(url)

    matches = Regex.SCRIPT.findall(dom)  # take out script blocks from dom

    dataset = {
        key: json.loads(value)
        for match, key, value in zip(
            matches, Regex.KEY_DS.findall(match), Regex.VALUE.findall(match)
        )
        if key and value
    }
    """
    This is to create a dictionary "dataset" that would combine key-value pairs for each match obtained from matches under the condition that the key and value are non-empty.
    The matches variable is a list of match objects returned by the Regex.SCRIPT.findall() function. 
    """

    success = False
    # different idx for different countries and languages
    for idx in range(len(dataset["ds:4"][0][1])):
        try:
            dataset = dataset["ds:4"][0][1][idx][22][0]
            success = True
        except Exception:
            pass
    if not success:
        return []

    n_apps = min(len(dataset), n_hits)
    search_results = []
    for app_idx in range(n_apps):
        app = {}
        for k, spec in ElementSpecs.Searchresult.items():
            content = spec.extract_content(dataset[app_idx])
            app[k] = content
        search_results.append(app)

    return search_results

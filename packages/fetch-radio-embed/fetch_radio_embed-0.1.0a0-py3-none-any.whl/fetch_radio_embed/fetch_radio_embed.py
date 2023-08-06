"""Fetch embedding from hf radio-embed."""
# pylint: disable=invalid-name
import httpx
from logzero import logger

url_ = "https://hf.space/embed/mikeee/radio-embed/+/api/predict/"

# 60s timeout on connect, 300s elsewhere
timeout_ = httpx.Timeout(300, connect=60)


def fetch_radio_embed(
    text: str,
    url: str = url_,
    timeout: httpx.Timeout = timeout_,
    debug: bool = False,
):
    """Fetch embedding from hf radio-embed.

    Args:
        text: converted to list text.splitlines()
        url: dest api on hf
        timeout: httpx.Timeout format, 60 connect 5 min elsewhere
        debug: when True, fetch_radio_embed.resp = resp

    Returns:
        list of text.splitlines().__len__() x 512
    """
    text = str(text)
    data = {"data": [text]}
    try:
        resp = httpx.post(url, json=data, timeout=timeout)
        resp.raise_for_status()
        if debug:
            fetch_radio_embed.resp = resp
    except Exception as exc:
        logger.exception(exc)
        raise

    try:
        jdata = resp.json()
    except Exception as exc:
        logger.exception(exc)
        raise

    try:
        fetch_radio_embed.duraion = resp.json().get("duration")
    except Exception as exc:
        logger.warning(
            "Attach duration to fetch_radio_embed .duration unsuccessful: %s", exc
        )

    # In [11]: resp.json().keys()
    # Out[11]: dict_keys(['data', 'duration', 'average_duration'])
    try:
        res = resp.json().get("data")[0].get("data")
    except Exception as exc:
        logger.exception(exc)
        raise

    return res

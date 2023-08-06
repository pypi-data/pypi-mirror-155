"""Define fetch_radio_cmat2aset.

Input Payload
{
  "data": [
    (List[List[str | number | bool]]), // represents 2D array of str, numeric, or bool data of 'cmat' Dataframe component
    (number), // represents numeric input of 'eps' Slider component
    (number), // represents numeric input of 'min_samples' Slider component
  ]
}
Response Object
{
  "data": [
    (Dict[headers: List[str], data: List[List[str | number]]]), // represents List[str], data: List[List[str | number]]]): JSON object with key 'headers' for list of header names, 'data' for 2D array of string or numeric data of 'output' Dataframe component
  ],
  "duration": (float) // number of seconds to run function call
}

import pyperclip
from txtwrap import dedent

cmat = [[1, 0, 0], [0, 1, 0], [0, 0, ""]]

eps: float = 10
min_samples: int = 6
api_url=api_url_
timeout=timeout_

exec(dedent(pyperclip.paste()))

"""
from typing import List, Tuple, Union

import httpx
from logzero import logger

timeout_ = httpx.Timeout(None, connect=30)
api_url_ = "http://127.0.0.1:7860/api/predict"
api_url_ = "https://hf.space/embed/mikeee/radio-cmat2aset/+/api/predict"


def fetch_radio_cmat2aset(
    # cmat: Union[np.ndarray, List[List]],
    cmat: List[List],
    eps: float = 10,
    min_samples: int = 6,
    api_url=api_url_,
    timeout=timeout_,
):
    """Define fetch_radio_cmat2aset."""
    data = {"data": [cmat, eps, min_samples]}
    try:
        resp = httpx.post(
            api_url,
            json=data,
            timeout=timeout,
        )
        resp.raise_for_status()
        fetch_radio_cmat2aset.resp = resp
    except Exception as exc:
        logger.exception(exc)
        raise
    try:
        jdata = resp.json()
    except Exception as exc:
        logger.exception(exc)
        raise

    # check error message first
    try:
        err_msg = jdata.get("data")[1]
    except Exception as exc:
        logger.exception(exc)
        raise

    if err_msg:
        raise Exception(err_msg)

    try:
        res = jdata.get("data")[0].get("data")
    except Exception as exc:
        logger.exception(exc)
        raise

    return res


_ = """

jdata.get("data"): [{'data': [[[0, 0, 1.0], [1, 1, 1.0], [2, 2, 1.0]]]}, '']

jdata: {'data': [{'data': [[[0, 0, 1.0], [1, 1, 1.0], [2, 2, 1.0]]]}, ''], 'duration': 0.1540207862854004, 'average_duration': 0.1540207862854004}

[[[0, 0, 1.0], [1, 1, 1.0], [2, 2, 1.0]]]
"""

import os
from contextlib import contextmanager

import uuid
import time
import json
import requests
import streamlit as st
import streamlit.components.v1 as components
from typing import Union, Optional, Literal
from streamlit.errors import StreamlitAPIException

from streamlit_lottie.url import url as validate_url
from streamlit_lottie.utils import ValidationFailure

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = True

if not _RELEASE:
    _st_lottie = components.declare_component(
        "streamlit_lottie",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _st_lottie = components.declare_component("streamlit_lottie", path=build_dir)


class LottieDownloadFailure(StreamlitAPIException):
    pass


def _download_animation_data(url):
    request = requests.get(url)
    try:
        return request.json()
    except (json.JSONDecodeError, TypeError) as exc:
        raise LottieDownloadFailure(
            f"""Unable to download animation data from {url}  \n
* status code {request.status_code}
* JSONDecodeError {exc}
"""
        )


def download_animation_data(url):
    try:
        return _download_animation_data(url)
    except LottieDownloadFailure:
        time.sleep(1)
        return _download_animation_data(url)


def get_animation_data(animation_source: Union[bytes, str, dict]):
    if not (
        isinstance(animation_source, bytes)
        | isinstance(animation_source, str)
        | isinstance(animation_source, dict)
    ):
        raise StreamlitAPIException(
            f"""Animation data must be one of Lottie URL or loaded JSON represented by dict or string/bytes UTF-8 JSON representative.  \n
    Given type is: {type(animation_source)}"""
        )

    if isinstance(animation_source, bytes):
        animation_source = animation_source.decode("UTF-8")

    animation_data = None
    if isinstance(animation_source, dict):
        animation_data = animation_source
    elif isinstance(animation_source, str):
        try:
            if validate_url(animation_source):
                animation_data = download_animation_data(animation_source)
        except ValidationFailure:
            # Is not url try to convert it to json
            try:
                animation_data = json.loads(animation_source)
            except (json.JSONDecodeError, TypeError) as exc:
                raise StreamlitAPIException(
                    f"""Unable to load animation data as JSON {exc}"""
                )
    return animation_data


class st_lottie:
    """Creates a new instance of lottie component.

    Parameters
    ----------
    animation_source: bytes | str | dict
        Animation data as Lottie URL or loaded JSON represented by dict or string/bytes UTF-8 JSON representative
    speed: int
        Speed of animation
    reverse: bool
        Reverse animation
    quality: Literal["low", "medium", "high"]
        low, medium or high. Defaults to low.
    loop: bool | number
        Loop animation, forever if True, once if False, or 'loop' times if number
    height: Optional[int]
        Height of the animation in px
    width: Optional[int]
        Width of the animation in px

    Returns context manager, so it can be used as a spinner.
    """

    # noinspection PyTypeChecker
    def __init__(
        self,
        animation_source: Union[bytes, str, dict],
        speed: int = 1,
        reverse: bool = False,
        loop: Union[bool, int] = True,
        quality: Literal["low", "medium", "high"] = "medium",
        height: Optional[int] = None,
        width: Optional[int] = None,
        key: Optional[str] = None,
    ):
        self.animation_data = get_animation_data(animation_source)
        self.speed = speed
        self.reverse = reverse
        self.loop = loop
        self.quality = quality
        self.height = height
        self.width = width
        self.container = st.empty()
        if not key:
            key = str(uuid.uuid4().hex)
        self.key = key
        self.start(key=self.key)

    def start(self, key: str):
        with self.container:
            _st_lottie(
                animationData=self.animation_data,
                speed=self.speed,
                direction=-1 if self.reverse else 1,
                loop=self.loop,
                quality=self.quality,
                height=self.height,
                width=self.width,
                key=key,
                default=None,
            )

    def __enter__(self):
        self.container.empty()
        self.start(key=self.key or str(uuid.uuid4().hex))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.container.empty()


@contextmanager
def st_lottie_spinner(
    animation_source: Union[bytes, str, dict],
    speed: int = 1,
    reverse: bool = False,
    loop: Union[bool, int] = True,
    quality: Literal["low", "medium", "high"] = "medium",
    height: Optional[int] = None,
    width: Optional[int] = None,
    key: Optional[str] = None,
):
    if not key:
        key = str(uuid.uuid4().hex)
    animation_data = get_animation_data(animation_source)
    lottie_container = st.empty()
    try:
        with lottie_container:
            st_lottie(animation_data, speed, reverse, loop, quality, height, width, key)
        yield
    finally:
        lottie_container.empty()


st.lottie = st_lottie
st.lottie_spinner = st_lottie_spinner

import os

import streamlit.components.v1 as components


_RELEASE = False

if not _RELEASE:
    _st_lottie = components.declare_component(
        "streamlit_lottie", url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _st_lottie = components.declare_component("streamlit_lottie", path=build_dir)


def st_lottie(
    animation_data,
    speed=1,
    reverse=False,
    loop=True,
    quality="low",
    renderer="svg",
    height=None,
    width=None,
    key=None,
):
    """Create a new instance of "my_component".

    Parameters
    ----------
    animation_data: Dict
        Animation data as loaded JSON
    speed: number
        Speed of animation
    reverse: boolean
        Reverse animation
    quality: str
        low, medium or high. Defaults to low.
    loop: bool | number
        Loop animation, forever if True, once if False, or 'loop' times if number
    renderer: str
        svg (default) or canvas
    height: int
        Height of the animation in px
    width: int
        Width of the animation in px
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    is_animation_finished: Boolean
        Returns True when animation is complete, None otherwise. Similar to a st.button.
    """
    is_animation_finished = _st_lottie(
        animationData=animation_data,
        speed=speed,
        direction=-1 if reverse else 1,
        loop=loop,
        quality=quality,
        renderer=renderer,
        height=height,
        width=width,
        key=key,
        default=None,
    )
    return is_animation_finished

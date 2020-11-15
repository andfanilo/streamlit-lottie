import os

import streamlit.components.v1 as components


_RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_lottie",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_lottie", path=build_dir)


def st_lottie(animation_data, height=100, width=100, key=None):
    """Create a new instance of "my_component".

    Parameters
    ----------
    animation_data: Dict
        Animation data as loaded JSON
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    finished: bool
        Tells Streamlit when the animation is over
    """
    component_value = _component_func(animationData=animation_data, key=key, default=None)
    return component_value

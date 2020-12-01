import json
import time

import requests
import streamlit as st
from streamlit_lottie import st_lottie


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_bodymovin = load_lottiefile("./lottiefiles/16-body-movin.json")
lottie_progress = load_lottiefile("./lottiefiles/117-progress-bar.json")
lottie_success = load_lottiefile("./lottiefiles/26514-check-success-animation.json")
lottie_error = load_lottiefile("./lottiefiles/38463-error.json")

st.title("Hello Lottie!")
st.markdown(
    """
[Lottie](https://airbnb.io/lottie) is a library that parses [Adobe After Effects](http://www.adobe.com/products/aftereffects.html) animations 
exported as json with [Bodymovin](https://github.com/airbnb/lottie-web) and renders them natively on mobile and on the web!

Go look at the [awesome animations](https://lottiefiles.com/) to spice your Streamlit app!
"""
)

st.header("Infinite loop")
with st.beta_expander("Animation parameters"):
    speed = st.slider("Select speed", 0.1, 2.0, 1.0)
    reverse = st.checkbox("Reverse direction", False)
st_lottie(lottie_bodymovin, speed=speed, reverse=reverse, height=200, key="initial")

st.header("Context manager")

c_col1, colx, c_col2, coly = st.beta_columns((1, 0.1, 0.25, 1))
if c_col1.button("Run some heavy computation...for 5 seconds!"):
    time.sleep(5)
    with c_col2:
        st_lottie(lottie_success, loop=False, key="success")

st.header("Try it yourself!")
st.markdown(
    "Choose a Lottie from [the website](https://lottiefiles.com/) and paste its 'Lottie Animation URL'"
)
lottie_url = st.text_input(
    "URL", value="https://assets5.lottiefiles.com/packages/lf20_V9t630.json"
)
downloaded_url = load_lottieurl(lottie_url)

if downloaded_url is None:
    col1, col2 = st.beta_columns((2, 1))
    col1.warning(f"URL {lottie_url} does not seem like a valid lottie JSON file")
    with col2:
        st_lottie(lottie_error, height=100, key="error")
else:
    with st.echo("above"):
        st_lottie(downloaded_url, key="user")

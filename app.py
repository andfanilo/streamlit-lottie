import json

import streamlit as st
from streamlit_lottie import st_lottie


with open("./lottiefiles/success.json", "r") as f:
    success_animation = json.load(f)


st.title("Hello Lottie!")
st_lottie(success_animation, key="initial")

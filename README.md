# Streamlit Lottie

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/andfanilo/streamlit-lottie-demo/master/app.py)

Integrate [Lottie](https://lottiefiles.com/) animations inside your Streamlit app!

![](./img/demo.gif)

## Install

```
pip install streamlit-lottie
```

## Usage
* Basic usage
```python
import streamlit as st
from streamlit_lottie import st_lottie

with st.echo():
    st_lottie("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")

```

* Basic usage (with monkey patched `st.lottie` function)
```python
import streamlit as st
import streamlit_lottie

with st.echo():
    st.lottie("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")

```

* Context manager usage, using `with` notation
```python
import time

import streamlit as st
from streamlit_lottie import st_lottie

with st_lottie("https://assets5.lottiefiles.com/packages/lf20_V9t630.json"):
    time.sleep(5)

```

* Download lottie manually example
```python
import time
import requests

import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_url_hello = "https://assets5.lottiefiles.com/packages/lf20_V9t630.json"
lottie_url_download = "https://assets4.lottiefiles.com/private_files/lf30_t26law.json"
lottie_hello = load_lottieurl(lottie_url_hello)
lottie_download = load_lottieurl(lottie_url_download)


st_lottie(lottie_hello, key="hello")

if st.button("Download"):
    with st_lottie_spinner(lottie_download, key="download"):
        time.sleep(5)
    st.balloons()

```

## Development

### Install

- JS side

```shell script
cd frontend
npm install
```

- Python side

```shell script
conda create -n streamlit-lottie python=3.7
conda activate streamlit-lottie
pip install -e .
```

### Run

Both webpack dev server and Streamlit need to run for development mode.

- JS side

```shell script
cd frontend
npm run start
```

- Python side

```shell script
streamlit run app.py
```

## References

- [Lottie-web (Official)](https://github.com/airbnb/lottie-web)
- [react-lottie (chenqingspring)](https://github.com/chenqingspring/react-lottie)
- [lottie-react-web (felippenardi)](https://github.com/felippenardi/lottie-react-web)
- [lottie-react (gamote)](https://github.com/gamote/lottie-react)
- [lottie-react (LottieFiles)](https://github.com/LottieFiles/lottie-react)
- [react-lottie-player (mifi)](https://github.com/mifi/react-lottie-player)
- [lottie-interactivity](https://github.com/LottieFiles/lottie-interactivity)

# Support me

<a href="https://www.buymeacoffee.com/andfanilo" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

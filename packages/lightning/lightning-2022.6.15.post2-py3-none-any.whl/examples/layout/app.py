"""An example showcasing how `configure_layout` can be used to nest user interfaces of different flows.

Run the app:

lightning run app examples/layout/demo.py

This starts one server for each flow that returns a UI. Access the UI at the link printed in the terminal.
"""

import os
from time import sleep

from lightning_app import LightningApp, LightningFlow
from lightning_app.frontend.stream_lit import StreamlitFrontend
from lightning_app.frontend.web import StaticWebFrontend


class C11(LightningFlow):
    def __init__(self):
        super().__init__()
        self.message = "Hello Streamlit!"

    def run(self):
        pass

    def configure_layout(self):
        return StreamlitFrontend(render_fn=render_c11)


def render_c11(state):
    import streamlit as st

    st.write(state.message)


class C21(LightningFlow):
    def __init__(self):
        super().__init__()

    def run(self):
        pass

    def configure_layout(self):
        return StaticWebFrontend(os.path.join(os.path.dirname(__file__), "ui1"))


class C22(LightningFlow):
    def __init__(self):
        super().__init__()

    def run(self):
        pass

    def configure_layout(self):
        return StaticWebFrontend(os.path.join(os.path.dirname(__file__), "ui2"))


class C1(LightningFlow):
    def __init__(self):
        super().__init__()
        self.c11 = C11()

    def run(self):
        pass


class C2(LightningFlow):
    def __init__(self):
        super().__init__()
        self.c21 = C21()
        self.c22 = C22()

    def run(self):
        pass

    def configure_layout(self):
        return [
            dict(name="one", content=self.c21),
            dict(name="two", content=self.c22),
        ]


class Root(LightningFlow):
    def __init__(self):
        super().__init__()
        self.c1 = C1()
        self.c2 = C2()

    def run(self):
        sleep(10)
        self._exit("Layout End")

    def configure_layout(self):
        return [
            dict(name="one", content=self.c1.c11),
            dict(name="two", content=self.c2),
            dict(name="three", content="https://lightning.ai"),
        ]


app = LightningApp(Root())

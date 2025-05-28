import src.sly_functions as f
import src.sly_globals as g
from src.ui.projects import set_training_data_table
from src.ui.sidebar import sidebar
from supervisely.webpy.app import WebPyApplication
from supervisely.app.widgets import Container, Dialog

# from sly_sdk.webpy.app import WebPyApplication

dialog = Dialog(content=sidebar, title="New Experiment")
dialog.show()


layout = Container(widgets=[dialog])


app = WebPyApplication(layout=layout)

g.api = f._init_api(app)

# update models
set_training_data_table(g.api)

# btn = Button("Click me")
# editor = Editor(language_mode="yaml")
# card = Card(
#     content=Container(widgets=[editor, btn]),
#     title="Example Card",
#     description="This is an example card with an editor and a button.",
# )
# layout = Container(widgets=[card])
# app = WebPyApplication(layout=layout)


# @btn.click
# def on_btn_click():
#     import time

#     print("Button clicked!")
#     btn.disable()
#     time.sleep(2)  # Simulate some processing time
#     btn.enable()
#     time.sleep(1)  # Simulate some processing time
#     btn.hide()

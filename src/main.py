from supervisely.app.widgets import Button, Card, Container, Stepper, Text

from sly_sdk.webpy.app import WebPyApplication

text_info = Text(text="My info text", status="info", widget_id="info_text")
text_success = Text(text="My success text", status="success", widget_id="success_text")
text_warning = Text(text="My warning text", status="warning", widget_id="warning_text")

card_info = Card(title="Info text", content=text_info, widget_id="info_card")
card_success = Card(title="Success text", content=text_success, widget_id="success_card")
card_warning = Card(title="Warning text", content=text_warning, widget_id="warning_card")

stepper = Stepper(
    widgets=[card_info, card_success, card_warning],
    titles=["Text step", "Success step", "Warning step"],
    widget_id="stepper_widget",
)

card = Card(
    title="Stepper",
    content=stepper,
    widget_id="stepper_card",
)
button_increase = Button(text="Increase step", widget_id="increase_step_button")
button_decrease = Button(text="Decrease step", widget_id="decrease_step_button")

buttons_container = Container(
    widgets=[button_increase, button_decrease], widget_id="buttons_container"
)

buttons_card = Card(content=buttons_container, widget_id="buttons_card")
layout = Container(widgets=[card, buttons_card], widget_id="extract_layout")

app = WebPyApplication(layout=layout)


@button_increase.click
def click_button():
    curr_step = stepper.get_active_step()
    curr_step += 1
    stepper.set_active_step(curr_step)


@button_decrease.click
def click_button():
    curr_step = stepper.get_active_step()
    curr_step -= 1
    stepper.set_active_step(curr_step)


# @app.event(app.Event.FigureGeometrySaved)
# def geometry_updated(event: WebPyApplication.Event.FigureGeometrySaved):
#     figure_id = event.figure_id
#     pass


# def get_mask(force=False):
#     t = time.perf_counter()
#     pass


# @button.click
# def save_mask():
#     get_mask(force=True)

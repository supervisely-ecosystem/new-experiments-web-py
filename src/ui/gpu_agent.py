import src.sly_globals as g
from supervisely.app.widgets import (
    AgentSelector,
    Button,
    Collapse,
    Container,
    CopyToClipboard,
    Editor,
    Field,
    Text,
)
from supervisely.io.env import team_id

# gpu
info = """
    Supervisely Agent is a tool that allows you to run any Supervisely app on your local computer or server.<br>
    To train a model, you need to select one of the available GPU agents.<br>
    If you don't have a GPU agent, you can connect a new agent or rent a GPU agent for your project.<br>
"""
gpu_text = Text(status="info", widget_id="gpu_text", text=info, font_size=12)
gpu_selector = AgentSelector(
    team_id=team_id(), show_only_gpu=True, show_only_running=True, widget_id="gpu_selector"
)
no_gpu_text = Text("Don't have a GPU agent?", widget_id="no_gpu_text", font_size=12)
rent_gpu_btn = Button(text="Rent GPU", widget_id="contact_us_button", plain=True)
connnect_gpu_egitor = Editor(
    initial_text="bash <(curl -fsSLg 'https://dev.internal.supervisely.com/api/agent/7P4EK...RbRS?agentImage=supervisely/agent:6.8.49')",
    language_mode="python",
    readonly=True,
    restore_default_button=False,
    show_line_numbers=False,
    highlight_active_line=False,
    height_lines=2,
    widget_id="connect_gpu_editor",
)
connnect_gpu_copy = CopyToClipboard(content=connnect_gpu_egitor, widget_id="connect_gpu_copy")
connnect_gpu_btn = Button("Connect Agent", widget_id="connect_gpu_button", plain=True)
connnect_gpu_text = Text(
    "Click the buttom to deploy the Supervisely Agent on your computer.",
    widget_id="connect_gpu_text",
    font_size=12,
)
connnect_gpu_text_2 = Text(
    "or copy the command below to terminal and run it on your local computer or server.",
    widget_id="connect_gpu_text_2",
    font_size=12,
)
connnect_gpu_cont = Container(
    [connnect_gpu_text, connnect_gpu_btn, connnect_gpu_text_2, connnect_gpu_copy],
    widget_id="connect_gpu_container",
)

no_gpu_collapse = Collapse(
    items=[
        Collapse.Item("Connect a new agent", "Connect a new agent", content=connnect_gpu_cont),
        Collapse.Item(
            "Rent a GPU agent",
            "Rent a GPU agent",
            content=Container(
                [Text("Contact us to rent a GPU agent", font_size=12), rent_gpu_btn],
                widget_id="rent_gpu_agent",
            ),
        ),
    ],
    accordion=True,
    widget_id="no_gpu_collapse",
)
# gpu_selector_btn = Button(text="Select", widget_id="gpu_selector_button")
gpu_selector_section_cont = Container(
    [gpu_text, gpu_selector, Container([no_gpu_text, no_gpu_collapse], widget_id="no_gpu_cont")],
    gap=25,
    widget_id="gpu_selector_container",
)
gpu_selector_section = Field(
    content=gpu_selector_section_cont,
    widget_id="gpu_selector_field",
    title="GPU",
    description="Select a GPU Agent for training",
)

g.selected_gpu = gpu_selector.get_value()


@gpu_selector.value_changed
def handle_gpu_selector_change(value):
    g.selected_gpu = value

import json

import asyncio
import json
import os

from reactpy import component, html, event, use_state
from reactpy.backend.fastapi import configure, FastAPI

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = f"{HERE}/../data/data.json"
with open(DATA_PATH) as f:
    sculpture_data = json.loads(f.read())


@component
def chat():
    """Chat.

    State is a snapshot: Changing the recipient after clicking "Send"
    does not change the recipient of the message because the state is
    'snapshot' when the event is triggered.
    """
    recipient, set_recipient = use_state("Alice")
    message, set_message = use_state("")

    @event(prevent_default=True)
    async def handle_submit(event):
        set_message("")
        print("About to send message...")
        await asyncio.sleep(5)
        print(f"Sent '{message}' to {recipient}")

    return html.form(
        {"on_submit": handle_submit, "style": {"display": "inline-grid"}},
        html.label(
            {},
            "To: ",
            html.select(
                {
                    "value": recipient,
                    "on_change": lambda event: set_recipient(
                        event["target"]["value"],
                    ),
                },
                html.option({"value": "Alice"}, "Alice"),
                html.option({"value": "Bob"}, "Bob"),
            ),
        ),
        html.input(
            {
                "type": "text",
                "placeholder": "Your message...",
                "value": message,
                "on_change": lambda event: set_message(
                    event["target"]["value"],
                ),
            },
        ),
        html.button({"type": "submit"}, "Send"),
    )


@component
def gallery():
    """Manage state."""
    index, set_index = use_state(0)

    def handle_click(_event):
        set_index(index + 1)

    bounded_index = index % len(sculpture_data)
    sculpture = sculpture_data[bounded_index]
    alt = sculpture["alt"]
    artist = sculpture["artist"]
    description = sculpture["description"]
    name = sculpture["name"]
    url = sculpture["url"]

    return html.div(
        html.button({"on_click": handle_click}, "Next"),
        html.h2(name, " by ", artist),
        html.p(f"({bounded_index + 1} of {len(sculpture_data)})"),
        html.img({"src": url, "alt": alt, "style": {"height": "200px"}}),
        html.p(description),
    )


@component
def photo(alt_text, image_id):
    """Photo."""
    return html.img(
        {
            "src": f"https://picsum.photos/id/{image_id}/500/200",
            "style": {"width": "50%"},
            "alt": alt_text,
        },
    )


@component
def todo_item(attrs, name, done):
    """Item to be done."""
    return html.li(attrs, name, " ✔" if done else "")


@component
def data_list(items, filter_by_priority=None, sort_by_priority=False):
    """Manage items to be done."""
    if filter_by_priority is not None:
        items = [i for i in items if i["priority"] <= filter_by_priority]
    if sort_by_priority:
        items = sorted(items, key=lambda i: i["priority"])
    list_item_elements = [
        todo_item(
            {
                "key": i["id"],
            },
            i["text"],
            i["done"],
        )
        for i in items
    ]
    return html.ul(list_item_elements)


@component
def todo_list():
    """Items to be done."""
    tasks = [
        {"id": 0, "text": "Make breakfast", "priority": 0, "done": True},
        {"id": 1, "text": "Feed the dog", "priority": 0, "done": False},
        {"id": 2, "text": "Do laundry", "priority": 2, "done": True},
        {"id": 3, "text": "Go on a run", "priority": 1, "done": False},
        {"id": 4, "text": "Clean the house", "priority": 2, "done": True},
        {
            "id": 5, "text": "Go to the grocery store", "priority": 2,
            "done": True,
        },
        {"id": 6, "text": "Do some coding", "priority": 1, "done": True},
        {"id": 7, "text": "Read a book", "priority": 1, "done": True},
    ]
    return html.section(
        html.h1("My Todo List"),
        data_list(tasks, filter_by_priority=1, sort_by_priority=True),
    )


@component
def print_button(display_text, message_text):
    """Manage simple event."""
    def handle_event(_event):
        print(message_text)

    return html.button({"on_click": handle_event}, display_text)


@component
def main():
    """Create the app."""
    return html.div(
        html.h1("Photo Gallery"),
        html.div(
            html.div(photo("Landscape", image_id=830)),
            html.div(photo("City", image_id=274)),
            html.div(photo("Puppy", image_id=237)),
            html.div(photo("Puppy", image_id=238)),
        ),
        print_button("Play", "Playing"),
        todo_list(),
        gallery(),
        chat(),
    )


app = FastAPI()
configure(app, main)

# if __name__ == '__main__':


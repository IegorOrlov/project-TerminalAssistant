
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from prompt_toolkit.key_binding import KeyBindings


class CommandAutoSuggest(AutoSuggest):
    def __init__(self, command_names: list[str]):
        self.command_names = command_names

    def get_suggestion(self, buffer, document):
        text = document.text_before_cursor.lower()
        for cmd in self.command_names:
            if cmd.startswith(text) and cmd != text:
                return Suggestion(cmd[len(text):])
        return None


style = Style.from_dict({
    'placeholder': 'ansigray italic'
})


def get_bindings():
    bindings = KeyBindings()

    @bindings.add('tab')
    def _(event):
        buffer = event.app.current_buffer
        suggestion = buffer.suggestion
        if suggestion:
            buffer.insert_text(suggestion.text)

    return bindings


def create_prompt_session():
    return PromptSession()


def prompt_input(session, suggest, bindings):
    return session.prompt(
        '>>> ',
        auto_suggest=suggest,
        placeholder=HTML('<placeholder>Enter a command:</placeholder>'),
        style=style,
        key_bindings=bindings
    )

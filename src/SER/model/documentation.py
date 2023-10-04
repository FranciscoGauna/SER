from typing import Collection, Dict

from mistune import html

from ..interfaces import ComponentInitialization


def get_docs(components: Collection[ComponentInitialization]) -> Dict[str, Dict[str, str]]:
    result = {}
    for comp in components:
        result[comp.name] = comp.component.instrument.variable_documentation()
    return result


def get_markdown(components: Collection[ComponentInitialization]) -> str:
    docs = get_docs(components)
    text = "# Documentation\n"
    for comp in components:
        text += f"## {comp.component.__class__.__name__}: {comp.name}\n"
        for k, v in docs[comp.name].items():
            text += f"### {k}\n{v}\n"
    return text


def to_md(filename, components: Collection[ComponentInitialization]):
    with open(filename, "w+") as file:
        file.write(get_markdown(components))


def to_htm(filename, components: Collection[ComponentInitialization]):
    with open(filename, "w+") as file:
        file.write(html(get_markdown(components)))

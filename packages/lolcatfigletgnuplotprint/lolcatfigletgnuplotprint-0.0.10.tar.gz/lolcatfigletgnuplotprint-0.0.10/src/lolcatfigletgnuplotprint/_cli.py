import json
import click

from .__init__ import lolcat_figlet_print, print_example
from .utils.data_structures import snakefy_dictionary_keys


def ___parse_json_input(json_input: str):
    input_data = json.loads(json_input)
    input_data = snakefy_dictionary_keys(input_data)
    content = input_data["content"] if "content" in input_data else None
    heading_text = input_data["heading_text"] if "heading_text" in input_data else None
    description_text = input_data["description_text"] if "description_text" in input_data else None
    attachements = input_data["attachements"] if "attachements" in input_data else None
    plot_value_groups = input_data["plot_value_groups"] if "plot_value_groups" in input_data else None
    return content, heading_text, description_text, attachements, plot_value_groups


def ___parse_json_extra_arguments(attachements: str = None, plot_value_groups: str = None):
    if attachements is not None:
        if not isinstance(attachements, list):
            attachements = json.loads(attachements)
        if not isinstance(attachements, list):
            raise Exception("Bad attachements input")
        if len(attachements) > 0:
            if "message" not in attachements[0]:
                raise Exception("Bad attachements input contents")

    if plot_value_groups is not None:
        if not isinstance(plot_value_groups, list):
            plot_value_groups = json.loads(plot_value_groups)
        if not isinstance(plot_value_groups, list):
            raise Exception("Bad plot_value_groups input")
        if len(plot_value_groups) > 0:
            if "title" not in attachements[0]:
                raise Exception("Bad plot_value_groups input contents")
            if "values" not in attachements[0] or not isinstance(attachements[0]["values"], list):
                raise Exception("Bad plot_value_groups input contents")
            if "values" not in attachements[0] or not isinstance(attachements[0]["values"], list):
                raise Exception("Bad plot_value_groups input contents")
            if len(attachements[0]["values"]) > 0:
                if "value" not in attachements[0]["values"][0] or "timestamp" not in attachements[0]["values"][0]:
                    raise Exception("Bad plot_value_groups input content values")

    return attachements, plot_value_groups


@click.command()
@click.option("--print-example-output", "--example", is_flag=True, help="Print example output")
@click.option("--content", help="Content text", default=None)
@click.option("--heading-text", "--heading", help="Large heading text", default=None)
@click.option("--description-text", "--description", help="Paragraph below the heading", default=None)
@click.option("--attachements", help="attachments as json string", default=None)
@click.option("--plot-value-groups", help="plot groups as json string", default=None)
@click.option("--json-input", help="Take parts or all of input as a json string", default=None)
def _cli(
    print_example_output: bool,
    content: str,
    heading_text: str,
    description_text: str,
    attachements: str = None,
    plot_value_groups: str = None,
    json_input: str = None,
):
    if json_input is not None:
        try:
            _content, _heading_text, _description_text, _attachements, _plot_value_groups = ___parse_json_input(
                json_input
            )

            content = _content if _content is not None else content
            heading_text = _heading_text if _heading_text is not None else heading_text
            description_text = _description_text if _description_text is not None else description_text
            attachements = _attachements if _attachements is not None else attachements
            plot_value_groups = _plot_value_groups if _plot_value_groups is not None else plot_value_groups
        except Exception as err:
            print("Bad JSON received:", err)
            raise err

    if print_example_output or content is None and heading_text is None and description_text is None:
        print_example()
    else:
        # Json input parsii
        attachements, plot_value_groups = ___parse_json_extra_arguments(attachements, plot_value_groups)

        lolcat_figlet_print(
            message=content,
            heading_text=heading_text,
            description_text=description_text,
            attachements=attachements,
        )

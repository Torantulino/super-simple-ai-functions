import os
from typing import Any

import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def ai_function(
    function: str,
    args: list[str],
    description: str,
    model: str = os.getenv("OPENAI_MODEL", "gpt-4"),
    temperature: float = 0,
) -> str:
    """
    Executes a function, given the function string, arguments and description.

    Args:
        function (str): The Python function string to be executed.
        args (list[str]): A list of arguments to be passed to the function.
        description (str): A description of the function to be executed.
        model (str, optional): The model to be used. Defaults to "gpt-4".
        temperature (float, optional): The temperature to be used. Defaults to 0.
    """
    args_str: str = ", ".join(args)
    content: tuple[str, ...] = (
        f"You are now the following python function: ```# {description}\n{function}```",
        "\n\nOnly respond with your `return` value. Do not include any other explanatory text in your response.",
    )

    messages: list[dict[str, str]] = [
        {"role": "system", "content": "".join(content)},
        {"role": "user", "content": args_str},
    ]

    response: Any = openai.ChatCompletion.create(
        model=model, messages=messages, temperature=temperature
    )

    return response.choices[0].message["content"]

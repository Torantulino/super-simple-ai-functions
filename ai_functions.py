import openai
from util import exec_with_return, getSmallTrace


def ai_function(
    function: str,
    args,
    description: str,
    model="gpt-4",
    error_correction=False
):
    VERBOSE=False
    MAX_ERROR_CORRECTION_RETRY = 5
    # parse args to comma separated string
    args = ", ".join(args)
    system_prompt = f"""You are now coding the following python function: \n\n# {description}\n{function}\n\n
    In the last line of your output, call the function with the given argument.
    Only respond with python code. Do not include any other explanatory text in your response and do not format as markdown.
    Do not use the print() function anywhere in your code. Only use standard python library in your import statements as dependencies."
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args},
    ]
    code = callOpenAI(messages, model)

    if VERBOSE:
        print(f"CODE:\n{code}")

    if not error_correction:
        try:
            result = exec_with_return(code)
        except Exception:
            result = ""
    else:
        for i in range(MAX_ERROR_CORRECTION_RETRY):
            try:
                result = exec_with_return(code)
                break
            except Exception:
                broken_code = code
                code = fix_code(code, messages, VERBOSE, model)
                result = ""

                # If there are no further improvements, then stop error correcting
                if broken_code == code:
                    break

    if not result:
        return ai_function_without_code(function, args, description)

    return result


def ai_function_without_code(
    function: str,
    args,
    description: str,
    model="gpt-4",
):
    messages = [
        {
            "role": "system",
            "content": f"You are now the following python function: ```# {description}\n{function}```\n\nOnly respond with your `return` value. Do not include any other explanatory text in your response.",
        },
        {"role": "user", "content": args},
    ]

    response = openai.ChatCompletion.create(
        model=model, messages=messages, temperature=0
    )

    result = response.choices[0].message["content"]

    # If result is enclosed in quotes, then strip quotes
    if (
        isinstance(result, str)
        and result[0] == result[-1]
        and (result[0] == '"' or result[0] == "'")
    ):
        result = result.strip("'\"")
    return result


def fix_code(broken_code: str, messages: list[dict], verbose: bool, model):
    error_trace = getSmallTrace()
    if verbose:
        print(f"ERROR:\n{error_trace}")
    error_correction_prompt = f"""
        Unfortunately, when executing the code the following error happens. Can you fix the code?
        Remember, only respond output executable python code. Do not include any other explanatory text in your response.
        Do not use the print() function anywhere in your code.
        Only use standard python library in your import statements as dependencies.
        Here is the error: {error_trace}
    """

    messages.extend(
        [
            {"role": "assistant", "content": broken_code},
            {"role": "user", "content": error_correction_prompt},
        ]
    )
    if verbose:
        print(f"ERROR CORRECTION PROMPT:\n{messages}")
    result = callOpenAI(messages, model)
    if verbose:
        print(f"IMPROVED CODE:\n{code}")
    return result


def callOpenAI(messages: list[dict], model="gpt-4") -> str:
    response = openai.ChatCompletion.create(
        model=model, messages=messages, temperature=0
    )
    return response.choices[0].message["content"]

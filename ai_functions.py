import openai


def ai_function(function, args, description, model="gpt-4"):
    # parse args to comma separated string
    args = ", ".join(args)
    messages = [
        {
            "role": "system",
            "content": "You are now the following python function: "
            + f"```# {description}\n{function}```\n\nOnly respond with your "
            + "`return` value. Do not include any other explanatory text in your response.",
        },
        {"role": "user", "content": args},
    ]

    response = openai.ChatCompletion.create(model=model, messages=messages, temperature=0)

    return response.choices[0].message["content"]

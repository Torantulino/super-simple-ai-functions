import openai


def ai_function(function, args, description, model="gpt-4"):
    # parse args to comma separated string
    args = ", ".join(args)
    messages = [{"role": "system", "content": f"You are now the following python function: ```# {description}\n{function}```\n\nOnly respond with your `return` value. Do not include any other explanatory text in your response."}, {"role": "user", "content": args}]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0
    )

    return response.choices[0].message["content"]


def optimize_function(function, args, model="gpt-4"):
    # Generate a prompt to optimize the function
    prompt = f"Optimize the following Python function:\n\n{function.__name__}({', '.join(args)})\n\nThe function's purpose is to {function.__doc__}\n\noptimize the function's time and space complexity.\n\nDo not include any other explanatory text in your response."
    messages = [
        {"role": "system",
         "content": "You are a code optimizer and refactor. Just give only output not extra text with that."},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the suggested optimizations from the GPT response
    optimized_code = response.choices[0]['message']['content']
    print(
        f"Here is the optimized function in terms of time and space complexity:\n{optimized_code}")

    # Compile the optimized function code into a function object
    optimized_function = None
    exec(optimized_code, globals(), locals())
    for var in locals():
        if var != '__builtins__':
            optimized_function = locals()[var]
            break

    return optimized_function

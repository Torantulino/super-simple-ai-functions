from ai_functions import optimize_function
import openai
import keys

# Initialize the OpenAI API client
openai.api_key = keys.OPENAI_API_KEY


def test_optimized_function_returns_correct_result(model):
    def calculate_square(x):
        """
        This function returns the square of its input.
        """
        n = x
        res = 0
        while n > 0:
            res += x
            n -= 1
        return res

    optimized_function = optimize_function(calculate_square, ["x"], model)
    assert optimized_function(2) == 4
    assert optimized_function(3) == 9
    assert optimized_function(4) == 16


# test_optimized_function_returns_correct_result("gpt-3.5-turbo")
test_optimized_function_returns_correct_result("gpt-4")

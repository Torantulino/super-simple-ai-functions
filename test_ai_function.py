import ast
import json
import time
import ai_functions
import pytest
import openai
import keys

# Initialize the OpenAI API client
openai.api_key = keys.OPENAI_API_KEY


# Run all tests, print the results, and return the number of failed tests
def run_tests(model):
    test_functions = [test_1, test_2, test_3, test_4, test_5, test_6]
    test_names = [
        "Generate fake people",
        "Generate Random Password",
        "Calculate area of triangle",
        "Calculate the nth prime number",
        "Encrypt text",
        "Find missing numbers",
    ]
    failed_tests = []

    i = 0
    for test in test_functions:
        print(
            f"=-=-=- Running test: {test.__name__} - {test_names[i]} with model {model} -=-=-="
        )
        i += 1
        try:
            test(model)
            print(f"{test.__name__}: PASSED")
        except AssertionError as e:
            print(f"{test.__name__}: FAILED - {e}")
            failed_tests.append(test)
        # Wait so as not to exceed the API rate limit
        time.sleep(1)

    # Print the total number of tests
    print(f"Total tests: {len(test_functions)}")

    # Print the number of failed tests
    print(
        f"Success Rate: {len(test_functions) - len(failed_tests)}/{len(test_functions)}"
    )


# Ai function test 1
def test_1(model):
    function_string = "def fake_people(n: int) -> list[dict]:"
    args = ["4"]
    description_string = """Generates n examples of fake data representing people, 
            each with a name and an age."""

    result_string = ai_functions.ai_function(
        function_string, args, description_string, model
    )

    print(f"Output: {result_string}")

    if isinstance(result_string, list):
        result = result_string
    else:
        # Assert the result can be parsed as is a list of dictionaries
        print("Testing if result is a a string...")
        assert isinstance(result_string, str)
        result = None
        try:
            print("Testing if result can be parsed as a list of dictionaries...")
            # Parse the result as a list of dictionaries
            result = json.loads(result_string)
        except Exception as e:
            # If the result can't be parsed as a list of dictionaries, the test fails
            assert False

    # Assert the length of the result is equal to the number of people requested
    print(
        "Testing if the length of the result is equal to the number of people requested..."
    )
    if result:
        assert len(result) == int(args[0])
    else:
        assert False


# Ai function test 2
def test_2(model):
    function_string = (
        "def random_password_generator(length: int, special_chars: bool) -> str:"
    )
    args = ["12", "True"]
    description_string = """Generates a random password of given length with or without special characters."""

    result_string = ai_functions.ai_function(
        function_string, args, description_string, model
    )

    print(f"Output: {result_string}")

    # Assert the length of the result is equal to the length requested
    print("Testing if the length of the result is equal to the length requested...")
    assert len(result_string) == int(args[0])


# Ai function test 3
def test_3(model):
    function_string = (
        "def calculate_area_of_triangle(base: float, height: float) -> float:"
    )
    args = ["15", "6.5"]
    description_string = (
        """Calculates the area of a triangle given its base and height."""
    )

    result_string = ai_functions.ai_function(
        function_string, args, description_string, model
    )
    print(f"Output: {result_string}")

    # Assert the result can be parsed as a float
    print("Testing if result is a a float...")
    try:
        assert isinstance(float(result_string), float)
    except Exception as e:
        print(e)
        assert False

    # Assert the result is equal to the expected area of the triangle
    expected_area = (float(args[0]) * float(args[1])) / 2
    print(
        "Testing if the result is equal to the expected area of the triangle, which is: "
        + str(expected_area)
    )
    assert float(result_string) == pytest.approx(expected_area)


# Ai function test 4
def test_4(model):
    function_string = "def get_nth_prime_number(n: int) -> int:"
    args = ["10"]
    description_string = """Finds and returns the nth prime number."""

    result_string = ai_functions.ai_function(
        function_string, args, description_string, model
    )

    print(f"Output: {result_string}")

    # Assert the result can be parsed as an integer
    print("Testing if result is a a integer...")
    try:
        assert isinstance(int(result_string), int)
    except Exception as e:
        print(e)
        assert False

    # Assert the result is equal to the expected nth prime number
    expected_prime_number = 29
    print(
        "Testing if the result is equal to the expected nth prime number, which is: "
        + str(expected_prime_number)
    )
    assert int(result_string) == expected_prime_number


# Ai function test 5
def test_5(model):
    function_string = "def encrypt_text(text: str, key: str) -> str:"
    plain_text = "Hello, World!"
    key = "abc123"
    args = [f"'{plain_text}'", f"'{key}'"]
    description_string = """Encrypts the given text using a simple character substitution based on the provided key."""

    cipher = ai_functions.ai_function(function_string, args, description_string, model)

    print(f"Output: {cipher}")

    # Assert the result has the same length as the input text
    print("Testing if the result has the same length as the input text...")
    assert len(cipher) == len(plain_text)


# Ai function test 6
def test_6(model):
    function_string = (
        "def find_missing_numbers_in_list(numbers: list[int]) -> list[int]:"
    )
    args = ["[3, 5, 8, 15, 16]"]
    description_string = (
        """Finds and returns a list of missing numbers in a given sorted list."""
    )

    result_string = ai_functions.ai_function(
        function_string, args, description_string, model
    )

    print(f"Output: {result_string}")

    if isinstance(result_string, list):
        result_list = result_string
    else:
        # Assert the result can be parsed as a list
        try:
            result_list = ast.literal_eval(result_string)
            print("Testing if result is a a list...")
            assert isinstance(result_list, list)
        except Exception as e:
            print(e)
            assert False

    # Assert the result list contains the expected missing numbers
    expected_missing_numbers = [4, 6, 7, 9, 10, 11, 12, 13, 14]
    print("Testing if the result list contains the expected missing numbers...")
    assert result_list == expected_missing_numbers
    
# Ai function test 7
def test_7(model):
    function_string = "def calculate_factorial(n: int) -> int:"
    args = ["5"]
    description_string = """Calculates and returns the factorial of a given non-negative integer n."""

    result_string = ai_functions.ai_function(function_string, args, description_string, model)

    print(f"Output: {result_string}")

    # Assert the result can be parsed as an integer
    print("Testing if result is an integer...")
    try:
        assert isinstance(int(result_string), int)
    except Exception as e:
        print(e)
        assert False

    # Assert the result is equal to the expected factorial value
    expected_factorial = 120
    print("Testing if the result is equal to the expected factorial, which is: " + str(expected_factorial))
    assert int(result_string) == expected_factorial


# Ai function test 8
def test_8(model):
    function_string = "def generate_fibonacci_sequence(n: int) -> list[int]:"
    args = ["10"]
    description_string = """Generates and returns the first n numbers in the Fibonacci sequence."""

    result_string = ai_functions.ai_function(function_string, args, description_string, model)

    print(f"Output: {result_string}")

    # Assert the result can be parsed as a list of integers
    try:
        result_list = ast.literal_eval(result_string)
        print("Testing if result is a list of integers...")
        assert isinstance(result_list, list) and all(isinstance(x, int) for x in result_list)
    except Exception as e:
        print(e)
        assert False

    # Assert the result list contains the expected Fibonacci sequence
    expected_fibonacci_sequence = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    print("Testing if the result list contains the expected Fibonacci sequence...")
    assert result_list == expected_fibonacci_sequence


# Ai function test 9
def test_9(model):
    function_string = "def reverse_words_in_string(s: str) -> str:"
    args = ["'Hello, World!'"]
    description_string = """Reverses the words in a given string and returns the result."""

    result_string = ai_functions.ai_function(function_string, args, description_string, model)

    print(f"Output: {result_string}")

    # Assert the result has the same length as the input string
    print("Testing if the result has the same length as the input string...")
    assert len(result_string) == len(args[0])

    # Assert the result is the expected reversed words string
    expected_reversed_words_string = "World! Hello,"
    print("Testing if the result is the expected reversed words string...")
    assert result_string == expected_reversed_words_string



run_tests("gpt-4")
run_tests("gpt-3.5-turbo")

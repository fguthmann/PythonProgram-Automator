from openai import OpenAI
import subprocess
import random

client = OpenAI(api_key='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')

PROGRAMS_LIST = [
    '''Given two strings str1 and str2, print all interleavings of the given two strings. You may assume that all 
    characters in both strings are different. Input: str1 = "AB", str2 = "CD" Output: ABCD ACBD ACDB CABD CADB CDAB 
    Input: str1 = "AB", str2 = "C" Output: ABC ACB CAB''',
    "a program that checks if a number is a palindrome",
    "A program that finds the kth smallest element in a given binary search tree.",
    "A program that optimally parenthesizes a matrix chain multiplication. Given a sequence of matrices, "
    "the program should print the most efficient way to multiply these matrices together.",
    "A program that solves the N-Queens problem. The task is to place N chess queens on an N×N chessboard so that no "
    "two queens threaten each other.",
    "A dynamic programming solution for the 0/1 Knapsack problem. Given weights and values of n items, "
    "put these items in a knapsack of a specific capacity to get the maximum total value in the knapsack.",
    "A program that implements a graph coloring algorithm. Given an undirected graph, assign colors to the vertices "
    "such that no two adjacent vertices share the same color.",
    "A program that solves a Sudoku puzzle. The program should take a partially filled-in grid and attempt to assign "
    "values to all empty cells in such a way that each row, column, and subgrid contains all the digits from 1 to 9 "
    "exactly once."
]


def generate_code(user_input):
    enhanced_prompt = user_input + " The program use runs in python3. Please include 5 unit tests such that if the " \
                                   "expected answer is not the one the program give, I want to return an error"
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[
                                                  {"role": "system", "content": "Tell me, which program would you like "
                                                                                "me to code for you? If you don't have "
                                                                                "an idea, just press enter and I will "
                                                                                "choose a random program to code"},
                                                  {"role": "user", "content": enhanced_prompt}
                                              ])
    return response.choices[0].message.content


def extract_code_block(prime_code, marker="```"):
    parts = prime_code.split(marker)
    code = parts[1].replace('python\n', '')
    return code


def run_script_and_handle_exceptions(user_input, max_attempts=5):
    script_path = "generatedcode.py"

    for attempt in range(max_attempts):
        print(attempt)
        try:
            # Generate and write the code
            prime_code = generate_code(user_input)
            extracted_code = extract_code_block(prime_code)
            with open(script_path, 'w') as file:
                file.write(extracted_code)

            # Attempt to run the script
            subprocess.call(["open", script_path])
            break  # Break the loop if successful
        except subprocess.CalledProcessError as e:
            print(f"Error encountered: {e}")
            if attempt < max_attempts - 1:
                print(f"Retrying... Attempt {attempt + 2}/{max_attempts}")
                user_input = "Error: " + str(e)
            else:
                print("Maximum attempts reached. Last error:")
                print(e)
                return
        finally:
            attempt += 1


def create_code_file():
    # System message and user input
    print("Tell me, which program would you like me to code for you? If you don't have an idea, just press enter and I "
          "will choose a random program to code.")
    user_input = input()

    # Choose a random program if no input is given
    if not user_input.strip():
        user_input = random.choice(PROGRAMS_LIST)
        print(user_input)

    # Generate code based on user input
    code = generate_code(user_input)

    # Extract the code block between markers
    extracted_code = extract_code_block(code)
    with open('generatedcode.py', 'w') as file:
        file.write(extracted_code)

    # Define the path to the Python interpreter and the script you want to run
    python_interpreter = "python3"
    script_path = "generatedcode.py"

    # Run the script
    subprocess.run([python_interpreter, script_path])
    run_script_and_handle_exceptions(user_input)


if __name__ == "__main__":
    create_code_file()

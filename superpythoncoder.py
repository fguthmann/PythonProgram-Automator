from openai import OpenAI
import subprocess
import random
from colorama import init, Fore
from tqdm import tqdm


client = OpenAI(api_key='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')

PROGRAMS_LIST = [
    '''Given two strings str1 and str2, print all interleavings of the given two strings. You may assume that all 
    characters in both strings are different. Input: str1 = "AB", str2 = "CD" Output: ABCD ACBD ACDB CABD CADB CDAB 
    Input: str1 = "AB", str2 = "C" Output: ABC ACB CAB''',
    "a program that checks if a number is a palindrome",
    "A program that finds the kth smallest element in a given binary search tree.",
    '''A program that optimally parenthesizes a matrix chain multiplication. Given a sequence of matrices,
    the program should print the most efficient way to multiply these matrices together ''',
    "Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be validated according to the following"
    " rules: Each row must contain the digits 1-9 without repetition. Each column must contain the digits 1-9 without "
    "repetition. Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition."
]


def extract_code_block(prime_code, conversation_history, marker="```"):
    parts = prime_code.split(marker)
    word_to_replace = 'python\n'
    if word_to_replace in parts[1]:
        code = parts[1].replace(word_to_replace, '')
    else:
        conversation_history.append({"role": "user", "content": "please return a code and 5 unity test that answered "
                                                                "the problem"})
        new_code = generate_code(conversation_history)
        code = extract_code_block(new_code, conversation_history)
    return code


def generate_code(conversation_history):
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=conversation_history)
    return response.choices[0].message.content


def create_code_file(file_path = "generatedcode.py", max_attempts = 5):
    conversation_history = [
        {"role": "system", "content": "Tell me, which program would you like me to code for you? If you don't have "
                                      "an idea, just press enter and I will choose a random program to code"}
    ]

    user_input = communicate_api_first_connection()
    conversation_history.append({"role": "user", "content": user_input})

    for attempt in tqdm(range(max_attempts), desc="Generating code"):
        try:
            code = generate_code(conversation_history)
            extracted_code = extract_code_block(code, conversation_history)
            with open(file_path, 'w') as file:
                file.write(extracted_code)
            subprocess.run(['black', file_path], check=True, capture_output=True, text=True)
            result = subprocess.run(['python', file_path], capture_output=True, text=True)
            if result.returncode == 0:
                print(Fore.LIGHTGREEN_EX + "Code creation completed successfully !")
                subprocess.call(["open", file_path])
                return
            else:
                error = result.stderr
                if attempt == max_attempts - 1:
                    print(Fore.LIGHTRED_EX + "Maximum attempts reached. Last error:")
                    print(Fore.LIGHTRED_EX + error)
                    return
                else:
                    print(Fore.LIGHTRED_EX + "Error running generated code! Error: " + error)
                    code_with_error = extracted_code + "\nThis is he old code you gave me, please fix it and returned" \
                                                       " me the new code with 5 unity tests such that following error" \
                                                       " is fixed\n\n" + error
                    conversation_history.append({"role": "user", "content": code_with_error})

        except subprocess.CalledProcessError as e:
            print(e)
            return


def communicate_api_first_connection():
    # System message and user input
    print(Fore.LIGHTBLUE_EX + "Tell me, which program would you like me to code for you? If you don't have an idea,"
                              "just press enter and I will choose a random program to code.")
    user_input = input()

    # Choose a random program if no input is given
    if not user_input.strip():
        # user_input = PROGRAMS_LIST[-1]
        user_input = random.choice(PROGRAMS_LIST)
        print(user_input)
    enhanced_prompt = user_input + " The program use runs in python3. Please include 5 unit tests such that if the " \
                                   "expected answer is not the one the program give, I want to return an error"
    return enhanced_prompt


if __name__ == "__main__":
    init(autoreset=True)
    create_code_file()


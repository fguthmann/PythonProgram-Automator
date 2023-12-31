from openai import OpenAI
import subprocess

client = OpenAI(api_key='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')


def generate_code(user_input):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[
                                                  {"role": "system", "content": "Tell me, which program would you like "
                                                                                "me to code for you? If you don't have "
                                                                                "an idea, just press enter and I will "
                                                                                "choose a random program to code"},
                                                  {"role": "user", "content": user_input}
                                              ])
    return response.choices[0].message.content


def extract_code_block(prime_code, marker="```"):
    parts = prime_code.split(marker)
    code = parts[1].replace('python\n', '')
    return code


def create_prime_code_file():
    # System message and user input
    print("Tell me, which program would you like me to code for you? If you don't have an idea, just press enter and "
          "I will choose a random program to code.")
    user_input = input()

    # Generate code based on user input
    prime_code = generate_code(user_input if user_input else "Create a Python program that checks if a number is prime,"
                                                             " please add 5 unity tests that main function will run. "
                                                             "Please don't add any comments or explanation. I want to "
                                                             "be able to run this function directly without adding "
                                                             "anything by hand. Please give me the main function to run"
                                                             " the code directly")

    # Extract the code block between markers
    extracted_code = extract_code_block(prime_code)
    with open('generatedcode.py', 'w') as file:
        file.write(extracted_code)

    # Define the path to the Python interpreter and the script you want to run
    python_interpreter = "python"  # or "python3" depending on your environment
    script_path = "generatedcode.py"  # Update this to the actual path

    # Run the script
    subprocess.run([python_interpreter, script_path])


if __name__ == "__main__":
    create_prime_code_file()

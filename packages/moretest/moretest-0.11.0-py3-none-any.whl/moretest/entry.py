import inquirer
import os

def main():
    print(os.getcwd())
    questions = [
        inquirer.List(
            "type",
            message="Choose a Parameter-Type!",
            choices=['float', 'int', 'string'],
        ),
    ]
    answers = inquirer.prompt(questions)
    print(answers)
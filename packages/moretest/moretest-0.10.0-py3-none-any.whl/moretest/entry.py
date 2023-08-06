import inquirer

def main():
    questions = [
        inquirer.List(
            "type",
            message="Choose a Parameter-Type!",
            choices=['float', 'int', 'string'],
        ),
    ]
    answers = inquirer.prompt(questions)
    print(answers)
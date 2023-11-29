# Developed by **Amanuel Mihiret (Aman)**
# Import required dependencies
from __future__ import annotations
import json
from difflib import get_close_matches


# Load the knowledge base from JSON file
def load_knowledge_bas(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data


# Function to save the old knowledge as it is
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


# Function to find out the best match from the dictionary
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


# Function get the answer for each questions
def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base['questions']:
        if q["question"] == question:
            return q["answer"]

# Define the chatbot
def chat_bot():
    knowledge_base: dict = load_knowledge_bas('knowledge_base.json')

    while True:
        user_input: str = input("You: ")
        if user_input.lower() == 'quit':
            print("Quitting! nice to chat with you, thank you!")
            break
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Sanita: {answer}')

        else:
            print("Sanita: Sorry, I don't know the answer. Can you teach me? please")
            new_answer: str = input("Type the answer or write 'Skip' to skip: ")

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print("Sanita: Thank you, I have learned a new response!")


if __name__ == '__main__':
    chat_bot()

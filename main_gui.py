# Developed by **Amanuel Mihiret (Aman)**
# Import required dependencies
from __future__ import annotations
import json
from difflib import get_close_matches
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, END
# Import the correct module for simpledialog
try:
    import tkinter.simpledialog as simpledialog
except ImportError:
    # For Python 2.x
    import tkSimpleDialog as simpledialog

# Load the knowledge base from JSON file
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# Function to save the knowledge base
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Function to find out the best match from the dictionary
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Function to get the answer for each question
def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base['questions']:
        if q["question"] == question:
            return q.get("answer",
                         "No answer found")  # Use get method to provide a default value if 'answer' is not present
    return "No answer found"  # Return a default value if the question is not found in the knowledge base


# Function to update or add a new question-answer pair
def update_answer(knowledge_base: dict, user_input: str, new_answer: str):
    for q in knowledge_base["questions"]:
        if q["question"] == user_input:
            q["answer"] = new_answer
            return
    knowledge_base["questions"].append({"question": user_input, "answer": new_answer})


# Function to handle user input and update the chat area
def handle_user_input():
    user_input = user_entry.get()
    chat_area.insert(tk.END, f'You: {user_input}\n')
    user_entry.delete(0, END)

    if user_input.lower() == 'quit':
        chat_area.insert(tk.END, "Sanita: Quitting! Nice to chat with you, thank you!\n")
        window.quit()
        return

    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        chat_area.insert(tk.END, f'Sanita: {answer}\n')
        correction_option = tk.simpledialog.askstring("Correction",
                                                      "Would you like to correct/update this answer? (yes/no)")
        if correction_option and correction_option.lower() == 'yes':
            new_answer = tk.simpledialog.askstring("Correction", "Type the corrected/update answer:")
            update_answer(knowledge_base, best_match, new_answer)
            save_knowledge_base('knowledge_base.json', knowledge_base)
            chat_area.insert(tk.END, "Sanita: Thank you, I have updated the response!\n")

    else:
        chat_area.insert(tk.END, "Sanita: Sorry, I don't know the answer. Can you teach me? please\n")
        new_answer = tk.simpledialog.askstring("Teach Me", "Type the answer or write 'Skip' to skip:")
        if new_answer and new_answer.lower() != 'skip':
            knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
            save_knowledge_base('knowledge_base.json', knowledge_base)
            chat_area.insert(tk.END, "Sanita: Thank you, I have learned a new response!\n")

# Define the chatbot
def chat_bot():
    global knowledge_base
    knowledge_base = load_knowledge_base('knowledge_base.json')

    # Create the main window
    global window
    window = tk.Tk()
    window.title("Sanita ChatBot ")

    # Create the chat area
    global chat_area
    chat_area = scrolledtext.ScrolledText(window, width=40, height=10)
    chat_area.pack(padx=10, pady=10)

    # Create the user entry field
    global user_entry
    user_entry = Entry(window, width=40)
    user_entry.pack(padx=10, pady=5)

    # Create the send button
    send_button = Button(window, text="Send", command=handle_user_input)
    send_button.pack(pady=10)

    window.mainloop()

if __name__ == '__main__':
    chat_bot()
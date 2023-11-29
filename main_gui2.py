# Developed by **Amanuel Mihiret (Aman)**
# Import required dependencies
from __future__ import annotations
import json
from difflib import get_close_matches
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, simpledialog, END
# Import the correct module for simpledialog
try:
    import tkinter.simpledialog as simpledialog
except ImportError:
    # For Python 2.x
    import tkSimpleDialog as simpledialog

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base['questions']:
        if q["question"] == question:
            return q.get("answer", "No answer found")
    return "No answer found"

def update_answer(knowledge_base: dict, user_input: str, new_answer: str):
    for q in knowledge_base["questions"]:
        if q["question"] == user_input:
            q["answer"] = new_answer
            return
    knowledge_base["questions"].append({"question": user_input, "answer": new_answer})

def handle_user_input():
    global best_match
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

        # Display correction messages in the same window
        correction_text.insert(tk.END, "Sanita: Would you like to correct/update this answer?\n")


def handle_correction_option(choice: str):
    correction_text.insert(tk.END, f'You: {choice}\n')

    if choice.lower() == 'yes' and best_match:
        new_answer = simpledialog.askstring("Correction", "Type the corrected/update answer for :")
        update_answer(knowledge_base, best_match, new_answer)
        save_knowledge_base('knowledge_base.json', knowledge_base)
        correction_text.insert(tk.END, "Sanita: Thank you, I have updated the response!\n")


def chat_bot():
    global knowledge_base
    knowledge_base = load_knowledge_base('knowledge_base.json')

    global window
    window = tk.Tk()
    window.title("Sanita ChatBot")

    global chat_area
    chat_area = scrolledtext.ScrolledText(window, width=40, height=10)
    chat_area.pack(padx=10, pady=10)

    global user_entry
    user_entry = Entry(window, width=40)
    user_entry.pack(padx=10, pady=5)

    global send_button
    send_button = Button(window, text="Send", command=handle_user_input)
    send_button.pack(pady=10)

    # Add Text widget for correction messages
    global correction_text
    correction_text = scrolledtext.ScrolledText(window, width=40, height=5)
    correction_text.pack(padx=10, pady=10)

    # Add Yes/No buttons for correction option
    correction_yes_button = Button(window, text="Yes", command=lambda: handle_correction_option('yes'))
    correction_yes_button.pack(side=tk.LEFT, padx=5)

    correction_no_button = Button(window, text="No", command=lambda: handle_correction_option('no'))
    correction_no_button.pack(side=tk.LEFT, padx=5)

    window.mainloop()

if __name__ == '__main__':
    chat_bot()

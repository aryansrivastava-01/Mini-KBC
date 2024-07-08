import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import random
import pygame

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KBC Quiz")
        self.root.geometry("800x600")
        pygame.mixer.init()
        self.sounds = {
            "start": "start_sound.mp3",
            "correct": "correct_answer.mp3",
            "wrong": "wrong_answer.mp3",
            "lock": "lock_answer.mp3"
        }
        self.load_questions()
        self.current_score = 0
        self.highest_score = 0
        self.question_index = 0
        self.max_questions = 10
        self.selected_option = tk.IntVar()
        self.create_main_menu()

    def load_questions(self):
        with open("questions.json", "r") as file:
            self.questions = json.load(file)

    def create_main_menu(self):
        self.clear_widgets()
        
        self.title_label = tk.Label(self.root, text="KBC Quiz", font=("Arial", 24))
        self.title_label.pack(pady=20)

        self.easy_button = tk.Button(self.root, text="Easy", font=("Arial", 18), command=lambda: self.start_quiz("easy"))
        self.easy_button.pack(pady=10)

        self.medium_button = tk.Button(self.root, text="Medium", font=("Arial", 18), command=lambda: self.start_quiz("medium"))
        self.medium_button.pack(pady=10)

        self.hard_button = tk.Button(self.root, text="Hard", font=("Arial", 18), command=lambda: self.start_quiz("hard"))
        self.hard_button.pack(pady=10)

    def start_quiz(self, difficulty):
        self.clear_widgets()
        self.difficulty = difficulty
        self.current_score = 0
        self.question_index = 0
        self.play_sound("start")

        # Shuffle and select questions for the chosen difficulty
        self.questions[difficulty] = random.sample(self.questions[difficulty], len(self.questions[difficulty]))
        self.questions[difficulty] = self.questions[difficulty][:self.max_questions]

        self.create_quiz_widgets()
        self.next_question()

    def create_quiz_widgets(self):
        self.score_label = tk.Label(self.root, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(pady=10)

        self.question_label = tk.Label(self.root, text="", font=("Arial", 18), wraplength=600, justify="center")
        self.question_label.pack(pady=20)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Radiobutton(self.root, text="", font=("Arial", 14), variable=self.selected_option, value=i, indicatoron=0, width=30)
            btn.pack(pady=5)
            btn.bind("<Button-1>", lambda event, idx=i: self.play_sound("lock"))  # Bind sound to each option button
            self.option_buttons.append(btn)

        self.submit_button = tk.Button(self.root, text="Submit Answer", font=("Arial", 14), command=self.submit_answer)
        self.submit_button.pack(pady=10)

        self.helpline_button = tk.Button(self.root, text="50-50", font=("Arial", 14), command=self.use_helpline)
        self.helpline_button.pack(pady=10)

        self.switch_button = tk.Button(self.root, text="Switch Question", font=("Arial", 14), command=self.switch_question)
        self.switch_button.pack(pady=10)

    def next_question(self):
        if self.question_index < len(self.questions[self.difficulty]):
            question_data = self.questions[self.difficulty][self.question_index]
            self.question_label.config(text=question_data["question"])
            for i, option in enumerate(question_data["options"]):
                self.option_buttons[i].config(text=option, state=tk.NORMAL)
            self.selected_option.set(-1)  # Deselect any previously selected option
        else:
            self.end_game()

    def submit_answer(self):
        selected_index = self.selected_option.get()
        if selected_index == -1:
            messagebox.showwarning("Warning", "Please select an option before submitting.")
        else:
            self.check_answer(selected_index)

    def check_answer(self, index):
        self.play_sound("lock")
        question_data = self.questions[self.difficulty][self.question_index]
        selected_answer = question_data["options"][index]
        if selected_answer == question_data["answer"]:
            self.current_score += 1
            self.play_sound("correct")
            self.update_score()
            self.question_index += 1
            self.next_question()
        else:
            self.play_sound("wrong")
            self.end_game()

    def update_score(self):
        self.score_label.config(text=f"Score: {self.current_score}")

    def use_helpline(self):
        self.play_sound("lock")
        question_data = self.questions[self.difficulty][self.question_index]
        correct_answer = question_data["answer"]
        incorrect_options = [opt for opt in question_data["options"] if opt != correct_answer]
        incorrect_options = random.sample(incorrect_options, 2)
        for btn in self.option_buttons:
            if btn.cget("text") in incorrect_options:
                btn.config(state=tk.DISABLED)
        self.helpline_button.config(state=tk.DISABLED)

    def switch_question(self):
        self.play_sound("lock")
        self.question_index += 1
        self.next_question()
        self.switch_button.config(state=tk.DISABLED)

    def play_sound(self, sound_key):
        pygame.mixer.music.load(self.sounds[sound_key])
        pygame.mixer.music.play()

    def end_game(self):
        messagebox.showinfo("Game Over", f"Your final score is: {self.current_score}")
        if self.current_score > self.highest_score:
            self.highest_score = self.current_score
            messagebox.showinfo("New High Score", f"Congratulations! New High Score: {self.highest_score}")
        self.create_main_menu()

    def win_game(self):
        messagebox.showinfo("Congratulations!", "You won 7 Crores!")
        self.create_main_menu()

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

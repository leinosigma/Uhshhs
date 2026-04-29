import tkinter as tk
import random
import time
import os

# =========================
# FRAGEN + FLAGGEN
# =========================
QUESTIONS = [
    {
        "country": "Deutschland",
        "img": "assets/flags/de.png",
        "options": ["Deutschland", "Frankreich", "Italien", "Spanien"],
        "answer": "Deutschland"
    },
    {
        "country": "Frankreich",
        "img": "assets/flags/fr.png",
        "options": ["Frankreich", "Deutschland", "Belgien", "Kanada"],
        "answer": "Frankreich"
    },
    {
        "country": "Japan",
        "img": "assets/flags/jp.png",
        "options": ["Japan", "China", "Korea", "Vietnam"],
        "answer": "Japan"
    },
    {
        "country": "Brasilien",
        "img": "assets/flags/br.png",
        "options": ["Brasilien", "Argentinien", "Chile", "Mexiko"],
        "answer": "Brasilien"
    }
]

# =========================
# SPIELVARIABLEN
# =========================
score = 0
highscore = 0
current = None
mode = "classic"
start_time = 0

# =========================
# WINDOW
# =========================
root = tk.Tk()
root.title("🌍 Flaggen Quiz")
root.geometry("500x600")

img_label = tk.Label(root)
img_label.pack(pady=10)

question_label = tk.Label(root, text="", font=("Arial", 16))
question_label.pack(pady=10)

info_label = tk.Label(root, text="Score: 0 | Highscore: 0")
info_label.pack()

frame = tk.Frame(root)
frame.pack(pady=20)

buttons = []

# =========================
# HIGH SCORE
# =========================
def load_highscore():
    global highscore
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            highscore = int(f.read())

def save_highscore():
    global score, highscore
    if score > highscore:
        highscore = score
        with open("highscore.txt", "w") as f:
            f.write(str(highscore))

# =========================
# NÄCHSTE FRAGE
# =========================
def next_question():
    global current, start_time

    current = random.choice(QUESTIONS)

    question_label.config(text="Welche Flagge ist das?")
    info_label.config(text=f"Score: {score} | Highscore: {highscore}")

    # Bild laden
    try:
        img = tk.PhotoImage(file=current["img"])
        img_label.config(image=img)
        img_label.image = img
    except:
        img_label.config(text="Bild fehlt")

    options = current["options"][:]
    random.shuffle(options)

    for b in buttons:
        b.destroy()
    buttons.clear()

    start_time = time.time()

    for opt in options:
        b = tk.Button(frame, text=opt, width=20,
                      command=lambda o=opt: check(o))
        b.pack(pady=5)
        buttons.append(b)

# =========================
# CHECK
# =========================
def check(ans):
    global score

    if mode == "timed":
        if time.time() - start_time > 7:
            question_label.config(text="⏰ Zu langsam!")
            return

    if ans == current["answer"]:
        score += 1
        question_label.config(text="✔ Richtig!")
    else:
        question_label.config(text=f"❌ Falsch! ({current['answer']})")
        end_game()
        return

    info_label.config(text=f"Score: {score} | Highscore: {highscore}")
    root.after(800, next_question)

# =========================
# GAME END
# =========================
def end_game():
    save_highscore()
    question_label.config(text=f"Game Over!\nScore: {score}")
    info_label.config(text=f"Highscore: {highscore}")

# =========================
# MODI
# =========================
def classic():
    global score, mode
    score = 0
    mode = "classic"
    next_question()

def endless():
    global score, mode
    score = 0
    mode = "endless"
    next_question()

def timed():
    global score, mode
    score = 0
    mode = "timed"
    next_question()

# =========================
# MENU
# =========================
def menu():
    load_highscore()

    menu_frame = tk.Frame(root)
    menu_frame.pack(pady=10)

    tk.Label(menu_frame, text="🌍 FLAGGEN QUIZ", font=("Arial", 20)).pack(pady=10)

    tk.Button(menu_frame, text="🎮 Klassisch", width=25,
              command=classic).pack(pady=5)

    tk.Button(menu_frame, text="♾ Endlos", width=25,
              command=endless).pack(pady=5)

    tk.Button(menu_frame, text="⏱ Zeitmodus", width=25,
              command=timed).pack(pady=5)

    tk.Button(menu_frame, text="❌ Exit", width=25,
              command=root.destroy).pack(pady=10)

# =========================
# START
# =========================
menu()
root.mainloop()

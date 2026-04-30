import tkinter as tk
from tkinter import messagebox, Listbox, END, StringVar, OptionMenu
import json
import random

QUOTES_FILE = "quotes.json"
HISTORY_FILE = "history.json"

# --- Загрузка данных ---
def load_quotes():
    try:
        with open(QUOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# --- Логика приложения ---
def generate_quote():
    quotes = load_quotes()
    if not quotes:
        messagebox.showwarning("Нет данных", "Список цитат пуст.")
        return

    quote = random.choice(quotes)
    
    # Добавляем в историю (без дубликатов)
    history = load_history()
    if quote not in history:
        history.append(quote)
        save_history(history)

    # Отображаем цитату
    text_quote.config(state="normal")
    text_quote.delete(1.0, tk.END)
    text_quote.insert(tk.END, f'"{quote["text"]}"\n\n— {quote["author"]}')
    text_quote.config(state="disabled")

def filter_history():
    author = entry_author_filter.get().strip().lower()
    topic = selected_topic.get()
    
    history = load_history()
    
    filtered = history
    
    if author:
        filtered = [q for q in filtered if author in q["author"].lower()]
    
    if topic and topic != "Все":
        filtered = [q for q in filtered if q["topic"] == topic]
    
    listbox_history.delete(0, END)
    for q in filtered:
        listbox_history.insert(END, f'{q["author"]} — {q["topic"]}')

# --- GUI ---
root = tk.Tk()
root.title("Генератор случайных цитат")
root.geometry("600x500")

# Блок генерации цитаты
frame_quote = tk.Frame(root)
frame_quote.pack(pady=10, fill=tk.X)

btn_generate = tk.Button(frame_quote, text="Сгенерировать цитату", command=generate_quote)
btn_generate.pack(side=tk.LEFT)

text_quote = tk.Text(root, height=4, width=70, wrap=tk.WORD, state="disabled")
text_quote.pack(pady=10)

# Блок фильтрации истории
frame_filter = tk.Frame(root)
frame_filter.pack(pady=10, fill=tk.X)

tk.Label(frame_filter, text="Фильтр по автору:").pack(side=tk.LEFT)
entry_author_filter = tk.Entry(frame_filter)
entry_author_filter.pack(side=tk.LEFT, expand=True, fill=tk.X)

# Получаем уникальные темы для фильтра
topics = ["Все"] + sorted({q["topic"] for q in load_quotes()})
selected_topic = StringVar(value=topics[0])
topic_menu = OptionMenu(frame_filter, selected_topic, *topics)
topic_menu.pack(side=tk.LEFT, padx=5)

btn_filter = tk.Button(frame_filter, text="Фильтровать", command=filter_history)
btn_filter.pack(side=tk.LEFT)

# Блок истории
frame_history = tk.Frame(root)
frame_history.pack(pady=10, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame_history)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox_history = Listbox(frame_history, yscrollcommand=scrollbar.set, width=70, height=10)
listbox_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=listbox_history.yview)

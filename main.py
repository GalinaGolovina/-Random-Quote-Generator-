import tkinter as tk
from tkinter import messagebox, Listbox, END, StringVar, OptionMenu
import json
import random

QUOTES_FILE = "quotes.json"
HISTORY_FILE = "history.json"

# --- Функции работы с данными ---
def load_quotes():
    """Загружает список цитат из файла."""
    try:
        with open(QUOTES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_history():
    """Загружает историю сгенерированных цитат."""
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_history(history):
    """Сохраняет историю в файл."""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# --- Логика приложения ---
def generate_quote():
    """Генерирует случайную цитату и обновляет историю."""
    quotes = load_quotes()
    if not quotes:
        messagebox.showwarning("Ошибка", "Файл с цитатами пуст или отсутствует.")
        return

    quote = random.choice(quotes)
    
    # Обновление истории (без дубликатов)
    history = load_history()
    if quote not in history:
        history.append(quote)
        save_history(history)
    
    # Отображение цитаты в интерфейсе
    quote_text_display.config(state="normal")
    quote_text_display.delete(1.0, tk.END)
    quote_text_display.insert(tk.END, f'"{quote["text"]}"\n\n— {quote["author"]}')
    quote_text_display.config(state="disabled")

def filter_history():
    """Фильтрует историю по автору и теме."""
    author_filter = entry_author.get().strip().lower()
    
    history = load_history()
    
    filtered_history = history.copy()
    
    # Фильтр по автору
    if author_filter:
        filtered_history = [q for q in filtered_history if author_filter in q["author"].lower()]
    
    # Фильтр по теме
    selected_topic_value = selected_topic.get()
    if selected_topic_value != "Все":
        filtered_history = [q for q in filtered_history if q["topic"] == selected_topic_value]
    
    # Обновление списка в GUI
    listbox_history.delete(0, END)
    for q in filtered_history:
        listbox_history.insert(END, f'{q["author"]} — {q["topic"]}')

# --- Создание графического интерфейса ---
root = tk.Tk()
root.title("Генератор случайных цитат")
root.geometry("650x500")

# Блок генерации цитаты
frame_quote = tk.Frame(root)
frame_quote.pack(pady=10)

btn_generate = tk.Button(frame_quote, text="Сгенерировать цитату", command=generate_quote)
btn_generate.pack(side=tk.LEFT, padx=5)

quote_text_display = tk.Text(root, height=4, width=70, wrap=tk.WORD, state="disabled")
quote_text_display.pack(pady=10)

# Блок фильтрации истории
frame_filter = tk.Frame(root)
frame_filter.pack(pady=10)

tk.Label(frame_filter, text="Фильтр по автору:").pack(side=tk.LEFT)
entry_author = tk.Entry(frame_filter)
entry_author.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

# Создание выпадающего списка тем (берем уникальные из файла)
all_quotes = load_quotes()
unique_topics = ["Все"] + sorted({q["topic"] for q in all_quotes})
selected_topic = StringVar(value=unique_topics[0])
topic_menu = OptionMenu(frame_filter, selected_topic, *unique_topics)
topic_menu.pack(side=tk.LEFT, padx=5)

btn_filter = tk.Button(frame_filter, text="Фильтровать", command=filter_history)
btn_filter.pack(side=tk.LEFT)

# Блок истории с прокруткой
frame_history = tk.Frame(root)
frame_history.pack(pady=10, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame_history)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox_history = Listbox(frame_history, yscrollcommand=scrollbar.set, width=70, height=10)
listbox_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=listbox_history.yview)

root.mainloop()

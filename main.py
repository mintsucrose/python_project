import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime


# ========== Загрузка данных ==========
def load_weather():
    try:
        with open("weather.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# ========== Сохранение данных ==========
def save_weather(data):
    with open("weather.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# ========== Валидация даты ==========
def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# ========== Добавление записи ==========
def add_record():
    date = date_entry.get().strip()
    temp = temp_entry.get().strip()
    desc = desc_entry.get().strip()
    precip = precip_var.get()

    # Валидация
    if not validate_date(date):
        messagebox.showwarning("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД (например: 2026-05-15)")
        return

    try:
        temp = float(temp)
    except ValueError:
        messagebox.showwarning("Ошибка", "Температура должна быть числом!")
        return

    if not desc:
        messagebox.showwarning("Ошибка", "Описание погоды не может быть пустым!")
        return

    # Добавление записи
    record = {
        "date": date,
        "temperature": temp,
        "description": desc,
        "precipitation": "Да" if precip else "Нет"
    }

    weather_data.append(record)
    save_weather(weather_data)
    update_table(weather_data)
    clear_fields()
    status_label.config(text=f"✅ Запись за {date} добавлена", fg="#2e7d32")


# ========== Обновление таблицы ==========
def update_table(data):
    table.delete(*table.get_children())
    for i, record in enumerate(data, 1):
        table.insert("", "end", values=(
            i,
            record["date"],
            record["temperature"],
            record["description"],
            record["precipitation"]
        ))


# ========== Фильтрация по дате ==========
def filter_by_date():
    date_filter = filter_date_entry.get().strip()

    if not date_filter:
        update_table(weather_data)
        status_label.config(text="📋 Показаны все записи", fg="#1565c0")
        return

    if not validate_date(date_filter):
        messagebox.showwarning("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД")
        return

    filtered = [r for r in weather_data if r["date"] == date_filter]

    if filtered:
        update_table(filtered)
        status_label.config(text=f"🔍 Найдено записей: {len(filtered)}", fg="#1565c0")
    else:
        update_table([])
        status_label.config(text="❌ Записи не найдены", fg="#c62828")


# ========== Фильтрация по температуре ==========
def filter_by_temp():
    temp_filter = filter_temp_entry.get().strip()

    if not temp_filter:
        update_table(weather_data)
        status_label.config(text="📋 Показаны все записи", fg="#1565c0")
        return

    try:
        temp_filter = float(temp_filter)
    except ValueError:
        messagebox.showwarning("Ошибка", "Температура должна быть числом!")
        return

    filtered = [r for r in weather_data if r["temperature"] >= temp_filter]

    if filtered:
        update_table(filtered)
        status_label.config(text=f"🔍 Найдено записей: {len(filtered)} (≥ {temp_filter}°C)", fg="#1565c0")
    else:
        update_table([])
        status_label.config(text="❌ Записи не найдены", fg="#c62828")


# ========== Сброс фильтров ==========
def reset_filters():
    filter_date_entry.delete(0, tk.END)
    filter_temp_entry.delete(0, tk.END)
    update_table(weather_data)
    status_label.config(text="📋 Показаны все записи", fg="#1565c0")


# ========== Удаление записи ==========
def delete_record():
    selected = table.selection()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите запись для удаления!")
        return

    index = table.index(selected[0])
    record = weather_data[index]

    confirm = messagebox.askyesno("Подтверждение", f"Удалить запись за {record['date']}?")
    if confirm:
        del weather_data[index]
        save_weather(weather_data)
        update_table(weather_data)
        status_label.config(text=f"🗑 Запись за {record['date']} удалена", fg="#c62828")


# ========== Очистка полей ввода ==========
def clear_fields():
    date_entry.delete(0, tk.END)
    temp_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    precip_var.set(False)
    date_entry.focus_set()


# ========== Главное окно ==========
window = tk.Tk()
window.title("🌤 Weather Diary — Дневник погоды")
window.geometry("700x550")
window.resizable(False, False)
window.configure(bg="#e3f2fd")

# ========== Заголовок ==========
tk.Label(
    window,
    text="🌤 Weather Diary — Дневник погоды",
    font=("Arial", 16, "bold"),
    bg="#e3f2fd",
    fg="#0d47a1"
).pack(pady=(15, 10))

# ========== Фрейм ввода данных ==========
input_frame = tk.LabelFrame(
    window,
    text="📝 Добавить запись",
    font=("Arial", 11, "bold"),
    bg="#ffffff",
    fg="#333333",
    padx=10,
    pady=10
)
input_frame.pack(pady=5, padx=15, fill="x")

# Дата
tk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):", bg="#ffffff", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=3)
date_entry = tk.Entry(input_frame, font=("Arial", 10), width=20, relief="solid", borderwidth=1)
date_entry.grid(row=0, column=1, pady=3, padx=5)

# Температура
tk.Label(input_frame, text="Температура (°C):", bg="#ffffff", font=("Arial", 10)).grid(row=0, column=2, sticky="w", pady=3)
temp_entry = tk.Entry(input_frame, font=("Arial", 10), width=10, relief="solid", borderwidth=1)
temp_entry.grid(row=0, column=3, pady=3, padx=5)

# Описание
tk.Label(input_frame, text="Описание:", bg="#ffffff", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=3)
desc_entry = tk.Entry(input_frame, font=("Arial", 10), width=45, relief="solid", borderwidth=1)
desc_entry.grid(row=1, column=1, columnspan=3, pady=3, padx=5, sticky="w")

# Осадки
precip_var = tk.BooleanVar()
tk.Checkbutton(
    input_frame,
    text="Осадки",
    variable=precip_var,
    bg="#ffffff",
    font=("Arial", 10)
).grid(row=2, column=0, sticky="w", pady=5)

# Кнопки
tk.Button(
    input_frame,
    text="➕ Добавить запись",
    command=add_record,
    font=("Arial", 10, "bold"),
    bg="#4CAF50",
    fg="white",
    activebackground="#388E3C",
    activeforeground="white",
    cursor="hand2",
    relief="flat",
    padx=15,
    pady=5
).grid(row=2, column=1, pady=5, sticky="w")

tk.Button(
    input_frame,
    text="🗑 Удалить",
    command=delete_record,
    font=("Arial", 10, "bold"),
    bg="#d32f2f",
    fg="white",
    activebackground="#c62828",
    activeforeground="white",
    cursor="hand2",
    relief="flat",
    padx=15,
    pady=5
).grid(row=2, column=2, pady=5, sticky="w")

# ========== Фрейм фильтрации ==========
filter_frame = tk.LabelFrame(
    window,
    text="🔍 Фильтрация",
    font=("Arial", 11, "bold"),
    bg="#ffffff",
    fg="#333333",
    padx=10,
    pady=10
)
filter_frame.pack(pady=5, padx=15, fill="x")

tk.Label(filter_frame, text="По дате:", bg="#ffffff", font=("Arial", 10)).grid(row=0, column=0, pady=3)
filter_date_entry = tk.Entry(filter_frame, font=("Arial", 10), width=15, relief="solid", borderwidth=1)
filter_date_entry.grid(row=0, column=1, pady=3, padx=5)

tk.Button(
    filter_frame,
    text="🔍 Фильтр по дате",
    command=filter_by_date,
    font=("Arial", 10, "bold"),
    bg="#1976d2",
    fg="white",
    activebackground="#1565c0",
    cursor="hand2",
    relief="flat",
    padx=10,
    pady=3
).grid(row=0, column=2, pady=3, padx=5)

tk.Label(filter_frame, text="По температуре ≥ :", bg="#ffffff", font=("Arial", 10)).grid(row=0, column=3, pady=3)
filter_temp_entry = tk.Entry(filter_frame, font=("Arial", 10), width=8, relief="solid", borderwidth=1)
filter_temp_entry.grid(row=0, column=4, pady=3, padx=5)

tk.Button(
    filter_frame,
    text="🔍 Фильтр по t°C",
    command=filter_by_temp,
    font=("Arial", 10, "bold"),
    bg="#1976d2",
    fg="white",
    activebackground="#1565c0",
    cursor="hand2",
    relief="flat",
    padx=10,
    pady=3
).grid(row=0, column=5, pady=3, padx=5)

tk.Button(
    filter_frame,
    text="🔄 Сброс",
    command=reset_filters,
    font=("Arial", 10, "bold"),
    bg="#ff9800",
    fg="white",
    activebackground="#f57c00",
    cursor="hand2",
    relief="flat",
    padx=10,
    pady=3
).grid(row=0, column=6, pady=3, padx=5)

# ========== Таблица записей ==========
table_frame = tk.Frame(window, bg="#e3f2fd")
table_frame.pack(pady=10, padx=15, fill="both", expand=True)

columns = ("#", "Дата", "t°C", "Описание", "Осадки")
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

table.heading("#", text="№")
table.heading("Дата", text="Дата")
table.heading("t°C", text="t°C")
table.heading("Описание", text="Описание")
table.heading("Осадки", text="Осадки")

table.column("#", width=40)
table.column("Дата", width=100)
table.column("t°C", width=60)
table.column("Описание", width=250)
table.column("Осадки", width=60)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)

table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ========== Статусная строка ==========
status_label = tk.Label(
    window,
    text="📋 Готов к работе",
    font=("Arial", 9, "italic"),
    bg="#e3f2fd",
    fg="#757575"
)
status_label.pack(pady=(0, 10))

# ========== Инициализация ==========
weather_data = load_weather()
update_table(weather_data)
date_entry.focus_set()

window.mainloop()
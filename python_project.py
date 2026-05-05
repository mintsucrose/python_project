import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from datetime import datetime


# ========== Загрузка заметок из файла ==========
def load_notes():
    try:
        with open("notes.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# ========== Сохранение заметок в файл ==========
def save_notes(notes_list):
    with open("notes.json", "w", encoding="utf-8") as file:
        json.dump(notes_list, file, ensure_ascii=False, indent=4)


# ========== Обновление Listbox ==========
def update_notes_listbox():
    notes_listbox.delete(0, tk.END)
    for i, note in enumerate(notes, 1):
        # Показываем заголовок и дату в списке
        display_text = f"{i}. {note['title']} ({note['date']})"
        notes_listbox.insert(tk.END, display_text)


# ========== Отображение содержимого заметки ==========
def show_note_content(event=None):
    selected = notes_listbox.curselection()
    if selected:
        index = selected[0]
        note = notes[index]
        content_text.config(state=tk.NORMAL)
        content_text.delete(1.0, tk.END)
        content_text.insert(tk.END, f"Заголовок: {note['title']}\n")
        content_text.insert(tk.END, f"Дата: {note['date']}\n")
        content_text.insert(tk.END, "-" * 40 + "\n\n")
        content_text.insert(tk.END, note['content'])
        content_text.config(state=tk.DISABLED)


# ========== Добавление заметки ==========
def add_note():
    title = title_entry.get().strip()
    content = text_entry.get("1.0", tk.END).strip()
    
    if not title:
        messagebox.showwarning("Предупреждение", "Введите заголовок заметки!")
        title_entry.focus_set()
        return
    
    if not content:
        messagebox.showwarning("Предупреждение", "Введите текст заметки!")
        text_entry.focus_set()
        return
    
    # Создание заметки с датой
    note = {
        "title": title,
        "content": content,
        "date": datetime.now().strftime("%d.%m.%Y %H:%M")
    }
    
    notes.append(note)
    save_notes(notes)
    update_notes_listbox()
    clear_fields()
    status_label.config(text=f"✅ Заметка «{title}» добавлена", fg="#2e7d32")


# ========== Редактирование заметки ==========
def edit_note():
    selected = notes_listbox.curselection()
    if not selected:
        messagebox.showwarning("Предупреждение", "Выберите заметку для редактирования!")
        return
    
    index = selected[0]
    note = notes[index]
    
    # Заполняем поля текущими данными
    title_entry.delete(0, tk.END)
    title_entry.insert(0, note['title'])
    text_entry.delete("1.0", tk.END)
    text_entry.insert("1.0", note['content'])
    
    # Меняем кнопку сохранения на обновление
    save_button.config(
        text="🔄 Обновить",
        command=lambda: update_note(index)
    )
    status_label.config(text=f"✏️ Редактирование: {note['title']}", fg="#1565c0")


# ========== Обновление заметки ==========
def update_note(index):
    title = title_entry.get().strip()
    content = text_entry.get("1.0", tk.END).strip()
    
    if not title or not content:
        messagebox.showwarning("Предупреждение", "Заполните все поля!")
        return
    
    notes[index]['title'] = title
    notes[index]['content'] = content
    notes[index]['date'] = datetime.now().strftime("%d.%m.%Y %H:%M") + " (изм.)"
    
    save_notes(notes)
    update_notes_listbox()
    clear_fields()
    reset_save_button()
    status_label.config(text=f"✅ Заметка «{title}» обновлена", fg="#2e7d32")


# ========== Удаление заметки ==========
def delete_note():
    selected = notes_listbox.curselection()
    if not selected:
        messagebox.showwarning("Предупреждение", "Выберите заметку для удаления!")
        return
    
    index = selected[0]
    title = notes[index]['title']
    
    confirm = messagebox.askyesno(
        "Подтверждение",
        f"Вы уверены, что хотите удалить заметку «{title}»?"
    )
    
    if confirm:
        del notes[index]
        save_notes(notes)
        update_notes_listbox()
        content_text.config(state=tk.NORMAL)
        content_text.delete(1.0, tk.END)
        content_text.config(state=tk.DISABLED)
        status_label.config(text=f"🗑 Заметка «{title}» удалена", fg="#c62828")


# ========== Очистка полей ввода ==========
def clear_fields():
    title_entry.delete(0, tk.END)
    text_entry.delete("1.0", tk.END)
    title_entry.focus_set()


# ========== Сброс кнопки сохранения ==========
def reset_save_button():
    save_button.config(
        text="💾 Сохранить",
        command=add_note
    )


# ========== Создание главного окна ==========
window = tk.Tk()
window.title("📒 Заметки")
window.geometry("650x500")
window.resizable(False, False)
window.configure(bg="#f5f5f5")

# ========== Верхний фрейм — ввод данных ==========
input_frame = tk.LabelFrame(
    window,
    text="📝 Новая заметка",
    font=("Arial", 11, "bold"),
    bg="#ffffff",
    fg="#333333",
    padx=10,
    pady=10
)
input_frame.pack(pady=(10, 5), padx=10, fill="x")

# Поле заголовка
tk.Label(
    input_frame,
    text="Заголовок:",
    font=("Arial", 10),
    bg="#ffffff"
).grid(row=0, column=0, sticky="w", pady=(0, 3))

title_entry = tk.Entry(
    input_frame,
    font=("Arial", 11),
    width=50,
    relief="solid",
    borderwidth=1
)
title_entry.grid(row=1, column=0, pady=(0, 10))

# Поле текста
tk.Label(
    input_frame,
    text="Текст заметки:",
    font=("Arial", 10),
    bg="#ffffff"
).grid(row=2, column=0, sticky="w", pady=(0, 3))

text_entry = tk.Text(
    input_frame,
    font=("Arial", 11),
    width=50,
    height=4,
    relief="solid",
    borderwidth=1,
    wrap="word"
)
text_entry.grid(row=3, column=0, pady=(0, 10))

# Кнопки
button_frame = tk.Frame(input_frame, bg="#ffffff")
button_frame.grid(row=4, column=0, pady=5)

save_button = tk.Button(
    button_frame,
    text="💾 Сохранить",
    command=add_note,
    font=("Arial", 10, "bold"),
    bg="#4CAF50",
    fg="white",
    activebackground="#388E3C",
    activeforeground="white",
    cursor="hand2",
    relief="flat",
    padx=15,
    pady=5
)
save_button.pack(side=tk.LEFT, padx=5)

tk.Button(
    button_frame,
    text="🧹 Очистить",
    command=clear_fields,
    font=("Arial", 10, "bold"),
    bg="#ff9800",
    fg="white",
    activebackground="#f57c00",
    activeforeground="white",
    cursor="hand2",
    relief="flat",
    padx=15,
    pady=5
).pack(side=tk.LEFT, padx=5)

# ========== Нижний фрейм — список и просмотр ==========
bottom_frame = tk.Frame(window, bg="#f5f5f5")
bottom_frame.pack(pady=5, padx=10, fill="both", expand=True)

# Левый фрейм — список заметок
left_frame = tk.LabelFrame(
    bottom_frame,
    text="📋 Список заметок",
    font=("Arial", 11, "bold"),
    bg="#ffffff",
    width=300,
    height=250
)
left_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 5))
left_frame.pack_propagate(False)

notes_listbox = tk.Listbox(
    left_frame,
    font=("Arial", 10),
    bg="#ffffff",
    fg="#333333",
    selectbackground="#bbdefb",
    selectforeground="#0d47a1",
    relief="flat",
    activestyle="none"
)
notes_listbox.pack(fill="both", expand=True, padx=5, pady=5)
notes_listbox.bind('<<ListboxSelect>>', show_note_content)

# Правый фрейм — просмотр заметки
right_frame = tk.LabelFrame(
    bottom_frame,
    text="📄 Содержимое",
    font=("Arial", 11, "bold"),
    bg="#ffffff",
    width=300,
    height=250
)
right_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=(5, 0))
right_frame.pack_propagate(False)

content_text = tk.Text(
    right_frame,
    font=("Arial", 10),
    bg="#fafafa",
    fg="#333333",
    wrap="word",
    relief="flat",
    state=tk.DISABLED
)
content_text.pack(fill="both", expand=True, padx=5, pady=5)

# ========== Кнопки управления ==========
control_frame = tk.Frame(window, bg="#f5f5f5")
control_frame.pack(pady=5)

tk.Button(
    control_frame,
    text="✏️ Редактировать",
    command=edit_note,
    font=("Arial", 10, "bold"),
    bg="#1976d2",
    fg="white",
    activebackground="#1565c0",
    activeforeground="white",
    cursor="hand2",
    relief="flat",
    padx=15,
    pady=5
).pack(side=tk.LEFT, padx=5)

tk.Button(
    control_frame,
    text="🗑 Удалить",
    command=delete_note,
    font=("Arial", 10, "bold"),
    bg="#d32f2f",
    fg="white",
    activebackground="#c62828",
    activeforeground="white",
    cursor="hand2",
    relief="flat",
    padx=15,
    pady=5
).pack(side=tk.LEFT, padx=5)

# ========== Статусная строка ==========
status_label = tk.Label(
    window,
    text="Готов к работе",
    font=("Arial", 9, "italic"),
    bg="#f5f5f5",
    fg="#9e9e9e"
)
status_label.pack(pady=(0, 10))

# ========== Инициализация ==========
notes = load_notes()
update_notes_listbox()
title_entry.focus_set()

# Привязка горячих клавиш
window.bind('<Control-s>', lambda event: add_note())
window.bind('<Control-n>', lambda event: clear_fields())

# ========== Запуск ==========
window.mainloop()
import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
import json
import os

# Файл для избранных
FAVORITES_FILE = 'favorites.json'

# Загрузка избранных
def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Сохранение избранных
def save_favorites(favorites):
    with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
        json.dump(favorites, f, ensure_ascii=False, indent=2)

# Инициализация списка избранных
favorites = load_favorites()

# Основное окно
root = tk.Tk()
root.title("GitHub User Finder")

# Поле поиска
search_var = tk.StringVar()
entry_search = tk.Entry(root, textvariable=search_var, width=40)
entry_search.pack(padx=10, pady=5)

# Результаты поиска
results_listbox = tk.Listbox(root, width=60, height=10)
results_listbox.pack(padx=10, pady=5)

# Функция поиска пользователя
def search_user():
    username = search_var.get().strip()
    if not username:
        messagebox.showwarning("Ошибка", "Пожалуйста, введите имя пользователя.")
        return
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        user_data = response.json()
        display_user(user_data)
    else:
        messagebox.showerror("Ошибка", f"Пользователь '{username}' не найден.")

# Отобразить пользователя в списке
def display_user(user_data):
    results_listbox.delete(0, tk.END)
    display_text = f"{user_data['login']} - {user_data.get('name', 'Нет имени')}"
    results_listbox.insert(tk.END, display_text)
    # Можно добавить больше информации или детализацию

# Добавить в избранное
def add_to_favorites():
    selected_idx = results_listbox.curselection()
    if not selected_idx:
        messagebox.showwarning("Ошибка", "Выберите пользователя из списка.")
        return
    selected_text = results_listbox.get(selected_idx)
    login = selected_text.split(' - ')[0]  # извлечь логин
    # Получить данные пользователя по логину
    url = f"https://api.github.com/users/{login}"
    response = requests.get(url)
    if response.status_code == 200:
        user_data = response.json()
        # Проверка на дубли
        if any(u['login'] == login for u in favorites):
            messagebox.showinfo("Информация", "Этот пользователь уже в избранных.")
            return
        favorites.append(user_data)
        save_favorites(favorites)
        messagebox.showinfo("Успех", f"Пользователь {login} добавлен в избранные.")
    else:
        messagebox.showerror("Ошибка", "Не удалось получить данные пользователя.")

# Просмотр избранных
def show_favorites():
    fav_window = tk.Toplevel(root)
    fav_window.title("Избранные пользователи")
    listbox = tk.Listbox(fav_window, width=60, height=15)
    listbox.pack(padx=10, pady=10)
    for user in favorites:
        listbox.insert(tk.END, f"{user['login']} - {user.get('name', 'Нет имени')}")

    def remove_from_favorites():
        idx = listbox.curselection()
        if not idx:
            messagebox.showwarning("Ошибка", "Выберите пользователя для удаления.")
            return
        user_obj = favorites.pop(idx[0])
        save_favorites(favorites)
        listbox.delete(idx)
        messagebox.showinfo("Удалено", f"Пользователь {user_obj['login']} удалён из избранных.")

    btn_remove = tk.Button(fav_window, text="Удалить из избранных", command=remove_from_favorites)
    btn_remove.pack(pady=5)

# Кнопки управления
btn_search = tk.Button(root, text="Поиск", command=search_user)
btn_search.pack(pady=5)

btn_add_fav = tk.Button(root, text="Добавить в избранное", command=add_to_favorites)
btn_add_fav.pack(pady=5)

btn_show_fav = tk.Button(root, text="Показать избранных", command=show_favorites)
btn_show_fav.pack(pady=5)

root.mainloop()

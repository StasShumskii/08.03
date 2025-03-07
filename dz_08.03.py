import customtkinter as ctk
from tkinter import messagebox

prices = {
    "Борщ": 90, "Пельмені": 75, "Вареники": 80, "Салат Олів'є": 110,
    "Картопля фрі": 65, "Чай": 40, "Кава": 40, "Тістечко": 50
}

def update_selection():
    selected = [dish for dish, var in checkboxes.items() if var.get()]
    label.configure(text=f"Обрано: {', '.join(selected)}")
    with open("selected_dishes.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(selected))

def show_menu(menu_name):
    for frame in frames.values():
        frame.pack_forget()
    frames[menu_name].pack(fill="both", expand=True, padx=10, pady=10)

def change_theme():
    selected_theme = theme_var.get()
    ctk.set_appearance_mode(selected_theme)

def calculate_total():
    total = sum(prices[dish] for dish, var in checkboxes.items() if var.get())
    total_label.configure(text=f"Сума замовлення: {total} грн")
    return total

def confirm_order():
    total = calculate_total()
    if total > 0:
        messagebox.showinfo("Замовлення підтверджено", f"✅ З вашої карти знято {total} грн.\nОчікуйте прибуття замовлення!")
    else:
        messagebox.showwarning("Помилка", "Ви не вибрали жодної страви!")

ctk.set_appearance_mode('light')
app = ctk.CTk()
app.title("Меню кафе")
app.geometry("715x300")
app.resizable(False, False)

sidebar = ctk.CTkFrame(app, width=150, corner_radius=0)
sidebar.pack(side="left", fill="y")

buttons = [
    ("Вибрати страви", lambda: show_menu("menu")),
    ("Ціни на страви", lambda: show_menu("price")),
    ("Переглянути суму", lambda: [show_menu("order_summary"), calculate_total()]),
    ("Налаштування програми", lambda: show_menu("settings")),
    ("Про ресторан", lambda: show_menu("about"))
]

for text, command in buttons:
    btn = ctk.CTkButton(sidebar, text=text, command=command)
    btn.pack(fill="x", pady=5, padx=5)

frames = {
    "menu": ctk.CTkFrame(app),
    "price": ctk.CTkFrame(app),
    "order_summary": ctk.CTkFrame(app),  # Додано
    "settings": ctk.CTkFrame(app),
    "about": ctk.CTkFrame(app)
}

label = ctk.CTkLabel(frames["menu"], text="Обрано: ")
label.pack(pady=10)

menu_items = list(prices.keys())
checkboxes = {}

for item in menu_items:
    var = ctk.BooleanVar()
    checkbox = ctk.CTkCheckBox(frames["menu"], text=item, variable=var, command=update_selection)
    checkbox.pack(anchor='w')
    checkboxes[item] = var

price_label = ctk.CTkLabel(frames["price"], text="\n".join([f"{dish} - {price} грн" for dish, price in prices.items()]))
price_label.pack(pady=15)

total_label = ctk.CTkLabel(frames["order_summary"], text="Сума замовлення: 0 грн")
total_label.pack(pady=10)

order_button = ctk.CTkButton(frames["order_summary"], text="Замовити", command=confirm_order)
order_button.pack(pady=5)

continue_button = ctk.CTkButton(frames["order_summary"], text="Продовжити покупки", command=lambda: show_menu("menu"))
continue_button.pack(pady=5)

theme_var = ctk.StringVar(value="light")
settings_label = ctk.CTkLabel(frames["settings"], text="Колір фону програми")
settings_label.pack(pady=10)

light_button = ctk.CTkRadioButton(frames["settings"], text="Світлий", variable=theme_var, value="light", command=change_theme)
dark_button = ctk.CTkRadioButton(frames["settings"], text="Темний", variable=theme_var, value="dark", command=change_theme)

light_button.pack(pady=5)
dark_button.pack(pady=5)

about_label = ctk.CTkLabel(frames["about"], text="Цей ресторан розробив Шумський Станіслав 08.03.2025")
about_label.pack(pady=10)

show_menu("menu")

app.mainloop()

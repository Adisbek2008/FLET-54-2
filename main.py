import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "Мое первое приложение на Flet"

    page.theme_mode = ft.ThemeMode.DARK

    greeting_text = ft.Text("Привет, мир")

    greeting_history = []
    history_text = ft.Text("История приветствий")



    def on_button_click(e):
        name = name_input.value.strip()

        if name:
            # greeting_text.value = f"Hello", name
            name_input.value = ""
            greeting_button.text = "Поздороваться еще раз"

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            greeting_history.append(f"{timestamp} - {name}")
            history_text.value = "История приветствий:\n" + "\n".join(greeting_history)
            if timestamp >= "6:00:00" and timestamp <= "12:00:00":
                greeting_text.value = f"Доброе утро, {name}"
            elif timestamp >= "12:00:00" and timestamp <= "18:00:00":
                greeting_text.value = f"Добрый день, {name}"
            elif timestamp >= "18:00:00" and timestamp <= "24:00:00":
                greeting_text.value = f"Добрый вечер, {name}"
            elif timestamp >= "24:00:00" and timestamp <= "6:00:00":
                greeting_text.value = f"Добрый ночи, {name}"
        else:
            greeting_text.value = "Пожалуйста, введите ваше имя"
        page.update()


    def on_button_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode =  ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK

        page.update()


    def clear_history(_):
        greeting_history.clear()
        greeting_text.value = "История приветствий:"
        page.update()

    def copy_greeting(_):
        page.set_clipboard(greeting_text.value)

    clear_button = ft.ElevatedButton("Очистить историю", icon=ft.Icons.DELETE, on_click=clear_history)

    name_input = ft.TextField(label='Введите ваше имя', autofocus=True, on_submit=on_button_click)

    theme_button = ft.IconButton(icon=ft.Icons.BRIGHTNESS_6, tooltip="Сменить тему", on_click=on_button_theme)

    greeting_button = ft.ElevatedButton("Поздороваться", icon=ft.Icons.HANDSHAKE, on_click=on_button_click)

    copy_button = ft.IconButton(icon=ft.Icons.COPY, tooltip="Скопироавть приветсвие", on_click=copy_greeting)


    # page.add(greeting_text, name_input, greeting_button, theme_button, clear_button, history_text)

    page.add(
        # ft.Row([theme_button, clear_button], alignment=ft.MainAxisAlignment.CENTER),
             ft.Row([greeting_text, copy_button], alignment=ft.MainAxisAlignment.CENTER),
             ft.Row([name_input, greeting_button, theme_button, clear_button], alignment=ft.MainAxisAlignment.CENTER),
             history_text)

ft.app(main)
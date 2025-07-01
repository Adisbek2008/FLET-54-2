from db import main_db
from datetime import datetime, date
import flet as ft

def main(page: ft.Page):
    page.title = 'toDo App'
    page.theme_mode = ft.ThemeMode.DARK

    task_list = ft.Column(spacing=10)
    filter_type = 'all'

    # Предупреждение об ограничении длины
    warning_text = ft.Text("", color=ft.Colors.RED_400, size=12)

    def get_deadline_color(deadline_str):
        if not deadline_str:
            return ft.Colors.WHITE
        deadline_date = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        today = date.today()
        if deadline_date < today:
            return ft.Colors.RED_500
        days_left = (deadline_date - today).days
        if days_left < 3:
            return ft.Colors.ORANGE
        elif days_left <= 7:
            return ft.Colors.YELLOW
        else:
            return ft.Colors.GREEN

    def get_deadline_text(deadline_str):
        if not deadline_str:
            return "Нет срока"
        deadline_date = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        today = date.today()
        if deadline_date < today:
            return f"Просрочено ({deadline_str})"
        days_left = (deadline_date - today).days
        if days_left == 0:
            return "Сегодня"
        elif days_left == 1:
            return "Завтра"
        elif days_left < 3:
            return f'Очень срочно! ({deadline_str})'
        else:
            return f'До срока: {days_left} дней ({deadline_str})'

    def load_task():
        task_list.controls.clear()
        all_tasks = main_db.get_tasks()
        if filter_type == 'completed':
            tasks = [t for t in all_tasks if t[2]]
        elif filter_type == 'uncompleted':
            tasks = [t for t in all_tasks if not t[2]]
        else:
            tasks = all_tasks
        for task_id, task_text, completed, deadline in tasks:
            task_list.controls.append(create_task_row(task_id, task_text, completed, deadline))
        page.update()

    def create_task_row(task_id, task_text, completed, deadline):
        task_field = ft.TextField(value=task_text, expand=True, read_only=True)

        task_checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )

        deadline_text = ft.Text(
            value=get_deadline_text(deadline),
            color=get_deadline_color(deadline),
            size=12,
            weight=ft.FontWeight.BOLD if deadline and datetime.strptime(deadline, '%Y-%m-%d').date() < date.today() else ft.FontWeight.NORMAL
        )

        def enable_edit(e):
            task_field.read_only = False 
            task_field.update()

        def handler_date_picked(e):
            if e.control.value:
                selected_date = e.control.value
                update_deadline(task_id, selected_date.strftime('%Y-%m-%d'))

        def pick_date(e):
            date_picker = ft.DatePicker(
                on_change=handler_date_picked,
                open=True
            )
            page.overlay.append(date_picker)
            page.update()

        def update_deadline(task_id, new_deadline):
            main_db.update_task(task_id, deadline=new_deadline)
            load_task()

        def save_task(e):
            main_db.update_task(task_id, task_field.value)
            page.update()

        return ft.Row([
            task_checkbox,
            task_field, 
            deadline_text,
            ft.IconButton(ft.Icons.CALENDAR_TODAY, icon_color=ft.Colors.BLUE, on_click=pick_date), 
            ft.IconButton(ft.Icons.EDIT, on_click=enable_edit, tooltip='Редактировать', icon_color=ft.Colors.YELLOW_500),
            ft.IconButton(ft.Icons.SAVE_ALT_ROUNDED, on_click=save_task, tooltip='Сохранить', icon_color=ft.Colors.GREEN_500),
            ft.IconButton(ft.Icons.DELETE, on_click=lambda e: delete_task(task_id), icon_color=ft.Colors.RED_500, tooltip='Удалить')
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def check_length():
        if len(task_input.value.strip()) > 100:
            warning_text.value = "Максимум 100 символов!"
        else:
            warning_text.value = ""
        page.update()

    def add_task(e):
        text = task_input.value.strip()
        if not text or len(text) > 100:
            check_length()
            return
        task_id = main_db.add_task(text)
        task_list.controls.append(create_task_row(task_id, text, False, None))
        task_input.value = ''
        check_length()
        page.update()

    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id, completed=int(is_completed))
        load_task()

    def delete_task(task_id):
        main_db.delete_task(task_id)
        load_task()

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_task()

    task_input = ft.TextField(
        label='Введите задачу',
        expand=True,
        on_change=lambda e: check_length()
    )

    add_button = ft.ElevatedButton("Добавить задачу", on_click=add_task)

    filter_buttons = ft.Row(
        controls = [
            ft.ElevatedButton("Все", on_click=lambda e: set_filter('all')),
            ft.ElevatedButton("Завершенные", on_click=lambda e: set_filter('completed')),
            ft.ElevatedButton("Незавершенные", on_click=lambda e: set_filter('uncompleted'))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[task_input, add_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                warning_text,
                filter_buttons,
                task_list
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=20,
        alignment=ft.alignment.center,
    )

    background_image = ft.Image(
        src="/Users/kurmanbek/Desktop/Geeks/Groups_flet/group_flet_54_2_to_di_list/image.jpeg",
        fit=ft.ImageFit.FILL,
        width=page.width,
        height=page.height,
    )

    background = ft.Stack(controls=[background_image, content])

    def on_resize(e):
        background_image.width = page.width
        background_image.height = page.height
        page.update()

    page.add(background)
    page.on_resize = on_resize

    load_task()

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)

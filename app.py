import flet as ft
from main import start

def main(page: ft.Page):
    page.title = "File Picker Example"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Поля ввода для выбора файлов
    folder_picker_1 = ft.TextField(label="Выберите папку", width=800)
    file_picker_2 = ft.TextField(label="Выберите промежуточный файл", width=800)
    file_picker_3 = ft.TextField(label="Выберите сводную таблицу", width=800)
    
    def pick_folder_result(e: ft.FilePickerResultEvent):
        folder_picker_1.value = e.path if e.path else "Cancelled!"
        folder_picker_1.update()

    # Функция для обработки результата выбора файлов
    def pick_files_result(text_field):
        def handler(e: ft.FilePickerResultEvent):
            text_field.value = (
                ", ".join(map(lambda f: f.path, e.files)) if e.files else "Cancelled!"
            )
            text_field.update()
        return handler

    # Создание диалогов для выбора файлов
    pick_folder_dialog_1 = ft.FilePicker(on_result=pick_folder_result)
    pick_files_dialog_2 = ft.FilePicker(on_result=pick_files_result(file_picker_2))
    pick_files_dialog_3 = ft.FilePicker(on_result=pick_files_result(file_picker_3))

    page.overlay.extend([pick_folder_dialog_1, pick_files_dialog_2, pick_files_dialog_3])

    # Кнопки выбора папки и файлов
    button_pick_1 = ft.ElevatedButton(
        text="Выбрать папку...",
        on_click=lambda _: pick_folder_dialog_1.get_directory_path()
    )
    button_pick_2 = ft.ElevatedButton(
        text="Выбрать файл...",
        on_click=lambda _: pick_files_dialog_2.pick_files(allow_multiple=False)
    )
    button_pick_3 = ft.ElevatedButton(
        text="Выбрать файл...",
        on_click=lambda _: pick_files_dialog_3.pick_files(allow_multiple=False)
    )

    # Прогресс-бар для анимации работы
    progress_bar = ft.ProgressBar(width=400, height=10, visible=False)

    # Функция для запуска программы
    def start_program(e):
        
        progress_bar.visible = True
        page.update()
        start(folder_picker_1.value, file_picker_2.value, file_picker_3.value)
        progress_bar.visible = False
        progress_bar.value = 0
        page.update()

    # Кнопка запуска программы
    start_button = ft.ElevatedButton(text="Запустить программу", on_click=start_program)

    # Размещение элементов на странице
    page.add(
        ft.Column([
            ft.Row([folder_picker_1, button_pick_1], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([file_picker_2, button_pick_2], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([file_picker_3, button_pick_3], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([start_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([progress_bar], alignment=ft.MainAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

# Запуск приложения
ft.app(target=main)

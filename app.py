import flet as ft
from main import start

def main(page: ft.Page):
    page.window_width = 500
    page.window_height = 500
    page.theme_mode = ft.ThemeMode.DARK
    
    page.title = "Сборщик Excel"
    
    def button_clicked(e):
        current_text.value = "Сборка началась"
        page.update()
        
    current_text = ft.Text()
        
    page.add(ft.TextField(hint_text="Путь до файлов", border=ft.InputBorder.UNDERLINE))
    page.add(ft.TextField(hint_text="Путь для сохранения промежуточного файла", border=ft.InputBorder.UNDERLINE))
    page.add(ft.ElevatedButton(text="Начать сборку", on_click=button_clicked, bgcolor=ft.colors.GREEN, color=ft.colors.WHITE))
    page.add(current_text)
    
ft.app(main)
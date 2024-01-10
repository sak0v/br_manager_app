import flet as ft
import requests

def main(page: ft.Page):
    page.title = 'Weather APP'
    page.theme_mode = 'Dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    user_data = ft.TextField(label = 'Укажите город', width=400)
    weather_data = ft.Text('')

    def get_info(e):
        if len(user_data.value) < 2:
            return
        
        API_KEY = '0805e2f2bc976fc60b3f59d16dfad85c'
        URL = f'https://api.openweathermap.org/data/2.5/weather?q={user_data.value}&appid={API_KEY}&units=metric'
        res = requests.get(URL).json()
        temp = res['main']['temp']
        weather_data.value = f'Погода в {user_data.value} :' + str(temp)
        page.update()
        

    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        page.update()
    
    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.SUNNY,on_click=change_theme),
                ft.Text("Погодная программа")
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row([user_data],alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([weather_data],alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([ft.ElevatedButton(text="Получить",on_click=get_info )],alignment=ft.MainAxisAlignment.CENTER),
    )


ft.app(target=main)

import flet as ft
import asyncio
from flet import AppBar, ElevatedButton, Page, Text, View, colors,IconButton,icons,alignment,Row,CrossAxisAlignment,MainAxisAlignment
from dotenv import load_dotenv
load_dotenv()
import os
import telebot
from datetime import datetime
import pytz
from supabase import create_client


#1
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client (url, key)
bot = telebot.TeleBot("6561602243:AAHvhoS37axZdYv7pdUJeDxQfQfK4CEm-xU")
api_id = 22597634
api_hash = '76dc5110a9692018ba07ee781bce3a36'


#client.start()


def main(page: Page):
    page.title = "Manager | Console"
    page.theme_mode = 'light'
    page.scroll = "adaptive"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
     
    def send_message_tg(user_id,username):
        bot.send_message(user_id,f"Кто-то зашел на страничку пользователя - {username}")
    
    def select_user():
        response = supabase.table("users").select("nickname").execute()
        data = response.data
        result = data[0]
        user = result['nickname']    
        
        return user
   
    def get_nickname(user_id):
        request = supabase.table("users").select("nickname").eq('user_id',user_id).execute()
        data = request.data
        
        if data:
            result = data[0]
            nickname = result['nickname']
            return nickname

    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        page.update()

    #not used anymore
    def go_to_user(user):
        return lambda e: page.go(f"/users/{user}")

    def user_on_route(username):
        user_id = 716255074
        send_message_tg(user_id, username)
    
       
    def validate(e):
        if all([user_login.value,user_pass.value]):
            btn_auth.disabled = False
        else:
            btn_auth.disabled = True

        page.update()

    def auth_user(e):
        request = supabase.table("users").select("*",count='exact').eq('nickname',user_login.value).execute()
        count = request.count
        if count:
            password = get_user_password(user_login.value)

            if user_pass.value == password:
                page.client_storage.set("loggedin", True)
                page.client_storage.set("nickname", f"{user_login.value}")
                page.go("/")
            else:
                page.snack_bar = ft.SnackBar(ft.Text('Вы указали неккоректный пароль!'),bgcolor=ft.colors.RED)
                page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(ft.Text('Неверно введеные данные!'),bgcolor=ft.colors.RED)
            page.snack_bar.open = True
        page.update()
    
    def get_user_password(nickname):
        request = supabase.table("users").select("admin_pass").eq('nickname',nickname).execute()
        data = request.data
    
        if data:
            result = data[0]
            password = result['admin_pass']

            return password
        
    
    user_login = ft.TextField(label='Nickname',width=200,on_change=validate)
    user_pass = ft.TextField(label='Password',password=True,width=200,on_change=validate)
    btn_auth = ft.OutlinedButton(text='Войти',width=200,on_click=auth_user,disabled=True)
    
 

    def route_change(e):
        if page.route == '/':
            page.views.clear()
            logged_in = page.client_storage.contains_key("loggedin")
            if logged_in:
                username = page.client_storage.get("nickname")
                print(username)
                page.views.append(
                    View(
                        "/",
                        [   
                        AppBar(
                            center_title = True,
                            title=Text("Admin Dashboard"),
                            bgcolor=colors.SURFACE_VARIANT,
                            actions=[
                                ft.IconButton(ft.icons.SUNNY, on_click=change_theme),
                            ],
                        ),
                            ft.Row([
                                ElevatedButton("login", on_click=lambda _: page.go(f"/login")),
                            ]),
                            ft.Row([]),
                            ft.Row([]),
                           
                        ],
                    )
                ) 
            else:
                page.go("/login")
            
        page.update()
        if page.route == '/login':
            logged_in = page.client_storage.contains_key("loggedin")
            if not logged_in:
                page.views.clear()
                page.views.append(
                    View("/login",[
                        AppBar(
                            center_title=True,
                            title=ft.Text("Вход в панель управления"),
                            bgcolor= colors.SURFACE_VARIANT,
                            actions=[
                                ft.IconButton(ft.icons.SUNNY,on_click=change_theme),
                            ],
                        ),
                        ft.Row([
                            ft.Column(
                                [
                                    user_login,
                                    user_pass,
                                    btn_auth,
                                    
                                ],
                            )
                        ],alignment=ft.MainAxisAlignment.CENTER,
                        ),
                            
                        ],
                        ),
                    )
            else:
                page.go("/")
                
        
        page.update()
        if page.route == "/users":
            logged_in = page.client_storage.contains_key("loggedin")
            if logged_in:
                page.views.clear()
                response = supabase.table("users").select("nickname").execute()
                data = response.data
                users = []
                for result in data:
                    users.append(result['nickname'])
                
                
                
                page.update()
                grid_view = ft.GridView(
                    expand=True,
                    runs_count=5,
                    max_extent=200, 
                    child_aspect_ratio=1.0,
                    spacing=5,
                    run_spacing=5,
                    auto_scroll=True
                    
                )   
                

                page.views.append(
                    ft.View("/users", [
                        ft.AppBar(
                            leading=ft.IconButton(ft.icons.HOME,on_click=lambda _: page.go("/")),
                            title=ft.Text("Все пользователи"),
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            actions=[
                                ft.IconButton(ft.icons.SUNNY, on_click=change_theme),
                                
                                
                            ],
                        ),

                        grid_view,
                        
                    ])
                )

                for user in users:
                    btn = ft.TextButton(user, width=200, height=50,icon="person", on_click=lambda e, user=user: go_to_user(user)(e))
                    grid_view.controls.append(btn)  
            else:
                page.go("/login")
        page.update()

                    
        if page.route.startswith("/users/"):
            logged_in = page.client_storage.contains_key("loggedin")
            if logged_in:
                page.views.clear()
                username = page.route.split("/users/")[1]
                username = username.capitalize()  
                user_id = 716255074
                send_message_tg(user_id, username)
                page.views.append(
                    View(
                        "/users/",
                        [
                            AppBar(
                                leading=ft.IconButton(ft.icons.HOME,on_click=lambda _: page.go("/")),
                                title=Text(f"Статистика пользователя: {username}"), bgcolor=colors.SURFACE_VARIANT,
                                actions=[
                            ft.IconButton(ft.icons.SUNNY, on_click=change_theme),
                        ],
                        ),
                            ElevatedButton("Перейти обратно к списку", on_click=lambda _: page.go("/users")),   
                            ft.Row([
                                ft.Text(f"Nickname: {username}",weight=ft.FontWeight.BOLD,size=24),
                                
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                            )
                        ],
                    )
                )
            else:
                page.go("/login")
            
        page.update()

        

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    
    page.on_route_change = route_change
    page.on_view_pop =  view_pop

    page.go(page.route)
   

ft.app(target=main,assets_dir="assets")
#ft.app(target=main, view=ft.AppView.WEB_BROWSER,assets_dir="./app/assets")

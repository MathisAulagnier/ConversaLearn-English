import time
import flet as ft
from com2LLM_Offline import send2Friend, loadModel
from utils import load_json


def send_message(page, message_list, message_input, model, json):
    # Affichage du message
    q = str(message_input.value)
    message_list.controls.append(ft.Row([
        ft.Container(content=ft.Text(message_input.value), bgcolor=ft.colors.LIGHT_BLUE, padding=10, border_radius=10),
        ft.Container(content=ft.Text("You"), bgcolor=ft.colors.LIGHT_BLUE_ACCENT, padding=5, border_radius=5, margin=ft.margin.only(left=10))
    ], alignment=ft.MainAxisAlignment.END))
    # Réponse du modèle
    # repMax = send2Friend(model, json, q)
    repMax = "read"
    message_list.controls.append(ft.Row([
        ft.Container(content=ft.Image("static/images/max.png", width=25,height=25,fit=ft.ImageFit.CONTAIN,), bgcolor=ft.colors.WHITE, padding=5, border_radius=5, margin=ft.margin.only(left=10)),
        ft.Container(content=ft.Text(repMax), bgcolor=ft.colors.GREY, padding=10, border_radius=10),
    ], alignment=ft.MainAxisAlignment.START))
    # Mise à jour de la page
    message_input.value = ""
    message_input.update()
    page.update()


def switch_theme(page: ft.Page, ):
    # SWITCH THE THEME
    page.theme_mode = "light" if page.theme_mode =="dark" else "dark"
    page.update()
    time.sleep(0.5)
    # AND PAGE UPDATE FOR CHANGE STATE
    page.update()




def main(page: ft.Page):
    page.title = "ConversaLearn"
    page.icon = "static/images/max.png"
    page.theme_mode = "light"
    page.splash = ft.ProgressBar(visible=False)
    
    # Chat interface

    #######################
    ####### Objects #######
    #######################

    message_list = ft.Column(expand=1, wrap=False, scroll="always")
    message_input = ft.TextField(hint_text="Type a message...", on_submit=lambda e: send_message(page, message_list, message_input, model, json))
    send_button = ft.ElevatedButton("Send", on_click=lambda e: send_message(page, message_list, message_input, model, json))    
    
    theme = ft.IconButton(ft.icons.WB_SUNNY, on_click=lambda e: switch_theme(page,),)
    head= ft.AppBar(
        
        leading=ft.Image(src=f"logo.png",
                width=40,
                height=40,
                fit=ft.ImageFit.NONE,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(5),),
        title=ft.Text("The CHAT"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[theme],
    )

    navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.CHAT, label="Chat"),
            ft.NavigationDestination(icon=ft.icons.MUSIC_NOTE, label="Singer"),
            ft.NavigationDestination(icon=ft.icons.BOOK_SHARP,label="Lessons",),
        ]
    )

    #######################

    page.add(head, message_list, message_input, send_button, navigation_bar)
    page.update()


# model = loadModel("/Users/mathisaulagnier/Library/Application Support/nomic.ai/GPT4All/mistral-7b-instruct-v0.1.Q4_0.gguf")
model = True
json = load_json("static/prompts.json")
# # Chat loop
# with model.chat_session():
#     model.generate(prompt=json["StartPrompt"], temp=0)
#     print(model.generate("Are you ready to start?", temp=0))

#     ft.app(target=main,)

# ft.app(target=main, view=ft.AppView.WEB_BROWSER,)
ft.app(target=main, view=ft.AppView.FLET_APP)
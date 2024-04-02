import time
import flet as ft

### Variables ###
indexe = 0

def switch_theme(page: ft.Page):
    # SWITCH THE THEME
    page.theme_mode = "light" if page.theme_mode =="dark" else "dark"
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

    profil = ft.CircleAvatar(foreground_image_url="https://media.licdn.com/dms/image/D4E03AQEXTy2eNrOWoQ/profile-displayphoto-shrink_400_400/0/1695153733199?e=1717632000&v=beta&t=S_YTA9qASE8Z20jLNCekoKRlRFcGu8L4Hi8806icuUI")
    
    message_list = ft.Column(expand=1, wrap=False, scroll="always")
    message_input = ft.TextField(hint_text="Type a message...", )
    send_button = ft.ElevatedButton("Send",)

    # Mettre message_list, message_input, send_button dans une colonne
    chat = ft.Column(
        controls=[message_list, message_input, send_button],
        expand=1,
        wrap=False,
    )


    theme = ft.IconButton(ft.icons.WB_SUNNY, on_click=lambda e: switch_theme(page,),)

    head = ft.AppBar(
        # Ajouter le logo de l'application
        leading_width=40,
        title=ft.Text("ConversaLearn", size=20, weight="bold", color="black"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[profil, theme,],
    )

    navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=ft.colors.AMBER_100,
        inactive_color=ft.colors.GREY,
        active_color=ft.colors.BLACK,
        on_change=lambda e: selected_tab(e),
        destinations=[
            ft.NavigationDestination(icon=ft.icons.CHAT_BUBBLE, label="Chat", selected_icon=ft.icons.CHAT_BUBBLE_OUTLINE),
            ft.NavigationDestination(icon=ft.icons.BOOK, label="Lessons", selected_icon=ft.icons.BOOK_OUTLINED),
            ft.NavigationDestination(icon=ft.icons.MENU_BOOK, label="Exercices", selected_icon=ft.icons.MENU_BOOK_OUTLINED),
        ]
    )

    


    #######################
    ###### Fonctions ######
    #######################

    def selected_tab(e):
        global indexe
        if indexe == e.control.selected_index:
            return  # Do nothing
        indexe = e.control.selected_index
    
        if indexe == 0:
            page.controls.pop(1)
            page.insert(1, chat)
        elif indexe == 1:
            page.controls.pop(1)
            page.insert(1, ft.Text("Lessons"))
        elif indexe == 2:
            page.controls.pop(1)
            page.insert(1, ft.Text("Exercices"))
        else:
            print("Unknown")

    page.add(head, chat, navigation_bar,)
    page.update()


ft.app(target=main, view=ft.AppView.FLET_APP)
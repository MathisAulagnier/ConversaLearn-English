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
    bot_profil = ft.CircleAvatar(foreground_image_url="https://img.freepik.com/photos-gratuite/vue-du-robot-graphique-3d_23-2150849173.jpg")
    
    message_list = ft.Column(expand=1, wrap=False, scroll="always", auto_scroll=True,)
    message_input = ft.TextField(hint_text="Type a message...", )
    send_button = ft.ElevatedButton("Send", on_click=lambda e: send_message(e))

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

    
    exercise_data = ["This is a text with {} and {}.", "a", "b"]

    #######################
    ###### Fonctions ######
    #######################

    ### Chat ###

    def send_message(e):
        sent_message = ft.Container(ft.Text(message_input.value, size=16, color="white"),padding=3, margin=3, bgcolor=ft.colors.BLUE_500 , border_radius=5)

        received_message = ft.Text("vu", size=16) # Modifier par la réponse du LLM

        # Ajouter une bulle de message
        sent_row = ft.Row([sent_message, profil], alignment=ft.MainAxisAlignment.END)
        received_row = ft.Row([bot_profil, received_message], alignment=ft.MainAxisAlignment.START)
        message_list.controls.append(sent_row)
        message_list.controls.append(received_row)
        message_list.update() 

        # Réinitialiser le champ de texte
        message_input.value = ""
        message_input.update()
        page.update()

    ### Exercices ###

    def generate_clicked(exercise_data) -> ft.Column:
        text_exo = exercise_data[0].split("{}")
        exercise_field = ft.Column()

        for i in range(len(text_exo)):
            exercise_field.controls.append(ft.Text(text_exo[i]))
            if i < len(text_exo) - 1:
                exercise_field.controls.append(ft.TextField(hint_text='..............'))
        exercise_field.controls.append(ft.ElevatedButton("Valider", on_click=lambda e : get_and_reset_values(exercise_field, exercise_data)))
        
        # Ajout d'un bouton de génération de l'exercice
        exercise_field.controls.append(ft.ElevatedButton("New exercice", on_click=lambda e : new_exercices_data(exercise_field)))

        return exercise_field
    
    def new_exercices_data(exercise_field):
        global exercise_data 
        exercise_data = ["AAAAAAAAAAA {} BBBBBBBB {}.", "c", "d"] # Changer pour interroger le LLM et qu'il interroge le modèle
        print("Mise à jour des données")
        page.controls.pop(1)
        print(exercise_data)
        page.insert(1, generate_clicked(exercise_data))
        print("Données mises à jour")
        page.update()

    def get_and_reset_values(exercice_field: ft.Column, exercise_data=exercise_data):
        i = 0
        for text_field in exercice_field.controls:
            if i % 2 == 1 and i < len(exercice_field.controls) - 2:
                value = text_field.value
                if value == exercise_data[i//2 + 1]:
                    print("Correct")
                    text_field.bgcolor = ft.colors.GREEN_200
                else:
                    text_field.bgcolor = ft.colors.RED
                    text_field.value = exercise_data[i//2 + 1]
            i += 1
        exercice_field.update()

    ### Navigation ###
        
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
            page.insert(1, generate_clicked(exercise_data))
        else:
            print("Unknown")

    page.add(head, chat, navigation_bar,)
    page.update()


ft.app(target=main, view=ft.AppView.FLET_APP)
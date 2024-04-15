import time
import random as rd
import json
import flet as ft
from LLM_control import *

### Variables ###
indexe = 0
lecon_str = "lesson"

json_exercices = json.load(open("static/exercices_data.json"))
json_irregular_verbs = json.load(open("static/Verbs.json"))

Score = 0
Best_Score = json_irregular_verbs["Score"]
verb = json_irregular_verbs["verbs"][rd.randint(0, len(json_irregular_verbs["verbs"]))]

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
    bot_teacher = ft.CircleAvatar(foreground_image_url="https://www.educol.net/image-professeur-dl30229.jpg")

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
            #ft.NavigationDestination(icon=ft.icons.BOOK, label="Lessons", selected_icon=ft.icons.BOOK_OUTLINED),
            ft.NavigationDestination(icon=ft.icons.MENU_BOOK, label="Exercices", selected_icon=ft.icons.MENU_BOOK_OUTLINED),
            ft.NavigationDestination(icon=ft.icons.SPORTS_SCORE, label="IrregularVerbs", selected_icon=ft.icons.SPORTS_SCORE_OUTLINED),
        ]
    )

    
    exercise_data = ["This is a text with {} and {}.", "a", "b"]

    #######################
    ###### Fonctions ######
    #######################

    ### Chat ###

    def send_message(e):
        if message_input.value == "":
            pass
        else:
            str_message_user = message_input.value
            sent_message = ft.Container(ft.Text(str_message_user, size=16, color="white"),padding=3, margin=3, bgcolor=ft.colors.BLUE_500 , border_radius=5)
            correction_button = ft.IconButton(ft.icons.CHECK, on_click=lambda e: bouton_correction(e, str_message_user))

            global msg_LLM
            received_message = ft.Text(last_respond_LLM(msg_LLM, str_message_user), size=16) # Modifier par la réponse du LLM

            # Ajouter une bulle de message
            sent_row = ft.Row([sent_message, correction_button, profil], alignment=ft.MainAxisAlignment.END)
            received_row = ft.Row([bot_profil, received_message], alignment=ft.MainAxisAlignment.START)
            message_list.controls.append(sent_row)
            message_list.controls.append(received_row)
            message_list.update() 

            # Réinitialiser le champ de texte
            message_input.value = ""
            message_input.update()
            page.update()

    def go_to_page_correction(e, message):
        print(message)
        print("####")
        lecon_str = gene_message_lecon(message)
        print(lecon_str)
        print("####")
        page.controls.pop(1)
        page.insert(1, ft.Text(lecon_str))
        page.update()

    def bouton_correction(e, message):
        # en cas d'appuie sur le bouton correction, on doit alors apeler l'agent correction pour qu'il arrive dans la conv et fasse la correction
        msg_correction = init_message_agent_correction() # on initialise la conversation avec un agent de correction
        rajout_message_user(msg_correction, message) # on rajout dans cette conv le message que l'on veut corriger
        message_de_correction = gene_message_correction(msg_correction)

        correction_gene_lecon = ft.IconButton(ft.icons.CHECK, on_click=lambda e: go_to_page_correction(e, message_de_correction))
        response = ft.Text(message_de_correction, size=16)
        received_row = ft.Row([bot_teacher, correction_gene_lecon, response], alignment=ft.MainAxisAlignment.START)
        message_list.controls.append(received_row)
        print(response)
        message_list.update()

    def generate_clicked(exercise_data) -> ft.Column:
        text_exo = exercise_data[0].split("{}")
        exercise_field = ft.Column()

        for i in range(len(text_exo)):
            exercise_field.controls.append(ft.Text(text_exo[i]))
            if i < len(text_exo) - 1:
                exercise_field.controls.append(ft.TextField(hint_text='__________'))
        exercise_field.controls.append(ft.ElevatedButton("Valider", on_click=lambda e : get_and_reset_values(exercise_field, exercise_data)))
        
        # Ajout d'un bouton de génération de l'exercice
        exercise_field.controls.append(ft.ElevatedButton("New exercice", on_click=lambda e : new_exercices_data(exercise_field)))

        return exercise_field
    
    def generate_irregulard() -> ft.Column:
        global verb
        verb = json_irregular_verbs["verbs"][rd.randint(0, len(json_irregular_verbs["verbs"]))]
        verb_field = ft.Column()
        entete = ft.Container(ft.Text("Score : " + str(Score) + "   Best score : " + str(Best_Score)), padding=3, margin=3, bgcolor=ft.colors.BLUE_500, border_radius=5)
        verb_field.controls.append(entete)
        choix = ["Base", "Past-simple", "Past-Participle"]
        j = rd.choice(choix)
        for k, v in verb.items():
            if k == j:
                verb_field.controls.append(ft.TextField(hint_text= k))
            else:
                verb_field.controls.append(ft.Text(v))
        verb_field.controls.append(ft.ElevatedButton("Valider", on_click=lambda e : correct_irregular(verb_field, verb)))
        return verb_field

    def correct_irregular(verb_field, verb):
        global Score
        global Best_Score
        for text_field in verb_field.controls:
            if type(text_field) == ft.TextField:
                value = text_field.value
                if value == verb[text_field.hint_text]:
                    print("Correct")
                    text_field.bgcolor = ft.colors.GREEN_200
                    Score += 1
                    if Score > Best_Score:
                        Best_Score = Score
                else:
                    text_field.bgcolor = ft.colors.RED
                    text_field.value = verb[text_field.hint_text]
                    Score = 0
                    json_irregular_verbs["Score"] = Best_Score
                    with open("static/Verbs.json", "w") as f:
                        json.dump(json_irregular_verbs, f)
        page.splash.visible = True
        page.update()
        time.sleep(3)
        page.splash.visible = False
        page.controls.pop(1)
        page.insert(1, generate_irregulard())
        page.update()
        

    def new_exercices_data(exercise_field):
        if rd.randint(1, 3) > 1:
            global exercise_data 
            exercise_data = json_exercices[str(rd.randint(1, 10))] # Changer pour interroger le LLM et qu'il interroge le modèle ou compléter ce JSON
            print("Mise à jour des données")
            page.controls.pop(1)
            print(exercise_data)
            page.insert(1, generate_clicked(exercise_data))
            print("Données mises à jour")
        else:
            print("Données non mises à jour")
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
        global lecon_str
        if indexe == e.control.selected_index:
            return  # Do nothing
        indexe = e.control.selected_index
    
        if indexe == 0:
            page.controls.pop(1)
            page.insert(1, chat)

        elif indexe == 1:
            page.controls.pop(1)
            page.insert(1, generate_clicked(exercise_data))
        elif indexe == 2:
            page.controls.pop(1)
            page.insert(1, generate_irregulard())
        else:
            print("Unknown")

    page.add(head, chat, navigation_bar,)
    page.update()

msg_LLM = init_message_user()
ft.app(target=main, view=ft.AppView.FLET_APP)
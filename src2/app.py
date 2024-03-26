import ollama

model_name = 'neural-chat'

# Définir les rôles et les invites système correspondantes
roles = {
    'Max' : "You are Max, a college student and friend of the user. Your goal is to help the user improve their English by discussing a specified topic or continuing the current conversation. Encourage the user to engage in the conversation and reply to their message as an AI friend.",
    'Teacher' : "You are an English teacher. Your goal is to correct the errors in the user-provided message list and generate code for a Markdown file that will display the corrected messages and a short lesson about the errors the student made. Respond as a Mentor AI.",
    'Moderator' : "You are an AI moderator. Your goal is to moderate the user-provided message and respond YES only if the message can be sent or NO only if the message is vulgar or inappropriate.",
}

def send_message(role, message):
    # Sélectionner l'invite système en fonction du rôle
    system_prompt = roles[role]
    messages=[
            {
                'role': 'system',
                'content': system_prompt,
            },
            {
                'role': 'user',
                'content': message,
            },
        ],
    for part in ollama.chat('neural-chat', messages=messages, stream=True):
        response = part['message']['content']
    
    print(response)
    return response['message']['content']


# Boucle de conversation
while True:
    # Demander à l'utilisateur de saisir un rôle
    role = input("Quel rôle voulez-vous donner au bot ? ")

    # Vérifier que le rôle est valide
    if role not in roles:
        print("Rôle inconnu. Veuillez choisir parmi les rôles suivants : assistant, tutor, friend.")
        continue

    # Demander à l'utilisateur de saisir un message
    user_message = input("You : ")

    # Envoyer le message au modèle et obtenir une réponse
    bot_response = send_message(role, user_message)

    # Afficher la réponse du modèle
    print("Bot : " + bot_response)
import ollama

def init_message_user():
    """
        fonction initialiser la lister des messages
    """
    return  [
    {
        "role": "system",
        "content" : """You are a friendly AI name Kléo assistant living in an English-speaking country.  The user you're interacting with is French. Your respons are in English only and should not exceed 30 words approximatly. No french will be tolereted. You sould respond like the user is your friend not just like an assistant.
        """
    }
    ]
    
def init_message_agent_correction():
    """
        fonction initialiser l'egant qui se charge de corriger les phrases
    """
    return  [
    {
        "role": "system",
        "content" : """You are an automatic English grammar corrector. Your task is to identify and correct grammatical errors in the sentences given by users, who are French learners of English. You must provide a clear and concise explanation of each grammatical error and how to correct it. Your responses should be factual and should not exceed 40 words.

Here are some examples of how you should respond:

User: I likes to play soccer.
System: The correct sentence is 'I like to play soccer.' The verb 'like' does not need an 's' after 'I' in the present simple tense.

User: She don't have a car.
System: The correct sentence is 'She doesn't have a car.' The contraction of 'does not' is 'doesn't' in the present simple tense.

User: I am going to the zoo this afternoon, have you ever been to the zoo?
System: Your sentence is grammatically correct. However, in informal English, 'Have you ever been to the zoo?' can be shortened to 'Have you been to the zoo?' when asking if someone has visited the zoo before.
        """
    }
    ]

def init_message_agent_exercice():
    """
        fonction initialiser l'agent qui va faire les exercices
    """
    return  [
    {
        """You are an automatic English exercise generator. Your task is to create a fill-in-the-blank exercise based on the grammatical errors identified and corrected by the previous agent. The exercise should be related to the errors and should help reinforce the correct usage. Each exercise should consist of 5 sentences. You should provide clear and concise instructions for the exercise, and the exercise should not exceed 100 words.

Here are some examples of how you should respond:

Correction: The correct sentence is 'I like to play soccer.' The verb 'like' does not need an 's' after 'I' in the present simple tense.
Exercise: Fill in the blank with the correct form of the verb:

    I [like] to play soccer.
    She [likes] to watch movies.
    They [like] to go swimming.
    He [likes] to read books.
    We [like] to listen to music.

Correction: The correct sentence is 'She doesn't have a car.' The contraction of 'does not' is 'doesn't' in the present simple tense.
Exercise: Fill in the blank with the correct contraction:

    She [doesn't] have a car.
    He [doesn't] like coffee.
    They [don't] live here.
    We [don't] want to go.
    I [don't] know the answer.

Correction: The correct sentence is 'Have you been to the zoo?' In informal English, 'Have you ever been to the zoo?' can be shortened to 'Have you been to the zoo?' when asking if someone has visited the zoo before.
Exercise: Fill in the blank with the correct form of the question:

    Have you [been] to the zoo?
    Have they [gone] to the store?
    Has she [eaten] breakfast yet?
    Have we [seen] that movie before?
    Has he [finished] his homework?"
"""
    }
    ] 
    

def rajout_message_user(msg, msg_user):
    """
        fonction rajouter un message utilisateur à msg
    """

    msg.append({"role": "user",
            "content": msg_user})
    return msg
    

def gene_message_suivant(msg):
    """
        fonction générer un message suivant
    """
    output = ollama.chat(
    model='mistral',
    messages=msg
    )
    msg.append({"role": "system",
            "content": output['message']['content']})
    
def last_respond_LLM(msg,user_msg):
    """
        on lance la génération du message par le LLM et on le retourne sous forme d'un string directement utilisable
    """
    msg = rajout_message_user(msg, user_msg)
    gene_message_suivant(msg)

    liste_mot = msg[len(msg) - 1]["content"].split(" ")
    liste_mot.insert(20, "\n")
    if len(liste_mot)>40:
        liste_mot.insert(40,"\n")
    if len(liste_mot)>60:
        liste_mot.insert(60,"\n") # flemme de faire une boucle
    new_sentance = ""
    for mot in liste_mot:
        new_sentance += mot + " "
    return  new_sentance



def print_conv(msg):
    """
        fonction afficher la conversation
    """
    for m in msg:
        print(m['role'], ":", m['content'])
    print("\n")


def sauv_message_user(msg, nom_fichier):
    """
        fonction sauvegarder la conversation
    """
    with open(nom_fichier, 'w') as f:
        len_msg = len(msg)
        f.write(f"{len_msg//2} : {msg[len_msg - 2]["content"]}\n")

def reset_fichier_sauv(nom_fichier):
    """
        fonction réinitialiser le fichier de sauvegarde
    """
    with open(nom_fichier, 'w') as f:
        f.write("")


    
def gene_message_suivant_correction(msg):
    """
        fonction générer un message suivant
    """
    output = ollama.chat(
    model='mistral',
    messages=msg
    )
    msg.append({"role": "system",
            "content": output['message']['content']})
    

def mise_en_forme_sentence(message):
    liste = message.split(" ")
    for  i in range(len(liste)//20):
        liste.insert(20*(i+1), "\n")
    new_sentance = ""
    for mot in liste:
        new_sentance += mot + " "
    return new_sentance


def gene_message_correction(msg):
    """
        fonction générer un message suivant
    """
    gene_message_suivant_correction(msg)

    return mise_en_forme_sentence(msg[len(msg) - 1]["content"])
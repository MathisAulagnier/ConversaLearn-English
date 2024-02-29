from gpt4all import GPT4All
from utils import replaceMSG

# def loadModel(model_name = "mpt-7b-chat-newbpe-q4_0.gguf"):
def loadModel(model_name = "mistral-7b-instruct-v0.1.Q4_0.gguf"):
    model = GPT4All(model_name)
    return model


def question_answer(prompt, model, temp = 0):
    response = model.generate(prompt, temp=temp) 
    return response

def verbose(q):
    print("Question: ")
    print(q)
    print("Answer:")

def sendableMsg(model, json, msg):
    q = json["toModerator"]
    q = replaceMSG(q, msg)
    verbose(q)
    r = question_answer(q, model)
    if "yes" in r.lower() or "sure" in r.lower():
        return  True
    return False

def send2Friend(model, json, msg):
    q = json["toFriend"]
    q = replaceMSG(q, msg)
    verbose(q)
    print(question_answer(q, model, 0.5))

def send2Teacher(model, json, messages):
    q = json["toTeacher"]
    for msg in messages:
        msg += ", {}"
        q = replaceMSG(q, msg)
    print(messages)
    verbose(q)
    print(question_answer(q, model))



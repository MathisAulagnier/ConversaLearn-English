from com2LLM_Offline import *
from utils import load_json



def main(model_name = "mistral-7b-instruct-v0.1.Q4_0.gguf"):

    model = loadModel("/Users/mathisaulagnier/Library/Application Support/nomic.ai/GPT4All/" + model_name)
    json = load_json("data/prompts.json")
    messages = []
    
    with model.chat_session():
        model.generate(prompt=json["StartPrompt"], temp=0)
        print(model.generate("Are you ready to start?", temp=0))
        while True:
            input_text = input("Say something: ")
            if input_text.lower() == "exit":
                break
            messages.append(input_text)
            send2Friend(model, json, input_text)        
        send2Teacher(model, json, messages)
        



if __name__ == "__main__":
    main()



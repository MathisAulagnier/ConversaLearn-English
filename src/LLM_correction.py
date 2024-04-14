import ollama

def init_message_agent_correction():
    """
        fonction initialiser la lister des messages
    """
    return  [
    {
        "role": "system",
        "content" : """You are agent which sould correct sentance in english. Juste repond the correction of the sentence that the user gives woth an explenation woth it false and how correct it
        """
    }
    ]
    
    


from google import genai

api_key =  input("Please enter the API key: ")

client = genai.Client(api_key = api_key) # Instantiates the client
chat = client.chats.create(model="gemma-4-26b-a4b-it") # Creates the chat for

response = chat.send_message("Who is the president of America?")    # Test prompt

print(response.text)

#introduce characters to give chatbot context, turn based game where the ai responds to the option that the player chooses.

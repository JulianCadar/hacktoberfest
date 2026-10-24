from google import genai

class Player:
    def __init__(self, name, health):
        self.name = name
        self.health = health
if __name__ =="__main__":
    api_key = input("Please enter the API key: ")
    print("\033c")  # Clears the screen

    client = genai.Client(api_key = api_key) # Instantiates the client
    chat = client.chats.create(model="gemma-4-26b-a4b-it") # Creates the chat

    response = chat.send_message("You are operating a DND-like, turn-based game where you are the game master")

    print(response.text)

    # Introduce characters to give chatbot context, turn based game where the ai responds to the option that the player chooses.

    def update_health(players: list[Player]):
        response = chat.send_message(f"""Here are the players in order:
    {"\n".join(player.name for player in players)}
    What is the health of all the characters? (please return a list of integers like this:)
    1
    3
    5
    for 1st player has 1 heart, 2nd has 3 hearts and 3rd player has 5 hearts.""")

        response = response.strip()
        for i in range(len(response)):
            players[i].health = int(response[i])
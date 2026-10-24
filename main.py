from typing import List
from google import genai
from google.genai import types
from pydantic import BaseModel

# --- Pydantic Models ---

class Player(BaseModel):
    name: str
    hearts: int
    max_hearts: int
    is_alive: bool
    weapon: str
    item: str
class Choice(BaseModel):
    id: str
    description: str

class CurrentTurn(BaseModel):
    player_index: int
    player_name: str
    narrative_resolution: str
    current_situation: str
    choices: List[Choice]

class GameState(BaseModel):
    round_number: int
    game_over: bool
    party: List[Player]
    current_turn: CurrentTurn

def get_config():
    players = int(input("How many players? "))
    player_names = []
    for i in range(players):
        player_name = input(f"Name for player {i + 1}: ")
        player_names.append(player_name)

    genre = input("Genre? ")
    difficulty = input("How difficult? ")
    return player_names, genre, difficulty

def run():
    api_key = input("Please enter the API key: ").strip()
    print("\033c", end="")  # Clears the screen

    client = genai.Client(api_key=api_key)

    # Use a Gemini model that supports thinking_config and response_schema
    chat = client.chats.create(
        model="gemma-4-26b-a4b-it",
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_level=types.ThinkingLevel("minimal")
            )
        )
    )

    with open("init_prompt.txt", "r", encoding="utf-8") as f:
        init_prompt = f.read()

    player_names, genre, difficulty = get_config()

    init_prompt = f"""{init_prompt}

Game Configuration:
- players: {player_names}
- genre: {genre}
- difficulty: {difficulty}"""

    print("\nInitializing survival session...\n")

    initial_response = chat.send_message(init_prompt)
    state = GameState.model_validate_json(initial_response.text)

    while not state.game_over:
        turn = state.current_turn

        print(f"\n--- Round {state.round_number} ---")
        for p in state.party:
            status = f"{p.hearts}/{p.max_hearts} HP" if p.is_alive else "DEAD"
            print(f"• {p.name}: {status} \n  Weapon: {p.weapon} \n  Item: {p.item}")
        print()

        if turn.narrative_resolution:
            print(f"[Outcome]: {turn.narrative_resolution}\n")
        print(f"[Turn: {turn.player_name}]")
        print(f"{turn.current_situation}\n")

        for choice in turn.choices:
            print(f"[{choice.id}] {choice.description}")

        selected = ""
        valid_ids = [c.id.upper() for c in turn.choices]
        while selected not in valid_ids:
            selected = input(f"\nSelect choice for {turn.player_name} ({'/'.join(valid_ids)}): ").strip().upper()

        response = chat.send_message(f"Player {turn.player_name} chose: {selected}")
        state = GameState.model_validate_json(response.text)

    print("\n--- GAME OVER ---")
    print("All party members have fallen.")

if __name__ == "__main__":
    run()
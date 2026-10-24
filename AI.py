from typing import List
from google import genai
from google.genai import types
from pydantic import BaseModel
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

api_key = input("Please enter the API key: ").strip()
client = genai.Client(api_key=api_key)
chat = client.chats.create(
        model="gemma-4-26b-a4b-it",
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_level=types.ThinkingLevel("minimal")
            )
        )
    )

def gen_game(players: List[str]):
    global chat
    with open("init_prompt.txt", "r", encoding="utf-8") as f:
        init_prompt = f.read()
    init_prompt = f"""{init_prompt}
    Game Configuration:
    - players: {players}
    - genre: Sci-Fi
    - difficulty: medium"""
    initial_response = chat.send_message(init_prompt)
    return initial_response

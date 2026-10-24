def heal_player(players, target): #target a specifc player in array players
   
    if target not in players: 
        print("Player does not exist.")
        return # checks if the target is in the players array

    if players[target] == 0:
        print("Cannot heal an eliminated player.") #cant heal a player that is dead
    
    elif players[target] < 5:
        players[target] += 1
        print(target, "has been healed!") #heals a player if they are alive and less than 5 hearts
    
    else:
        print(target, "already has full health.") #doesnt heal a player if they are already full health
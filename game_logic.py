import time
import random
import asyncio
import data_handler
import webapp

class Game_logic:

    def __init__(self):
        self.players = {}
        self.bets = {
            1 : [],
            2 : [],
            3 : [],
            4 : [],
            5 : []
        }
        # asyncio.run(better(self))
        # asyncio.run(self.game_loop())
        

    async def game_loop(self):

        while True:
            winning_number = random.randint(1,5)
            winning_number = 4
            data_handler.add_history(winning_number)


            print("Winners :", end = " ")
            # discord_bot.message_winners(self.bets[winning_number])
            for player in self.bets[winning_number]:
                data_handler.add_score(str(player))
                print(player, end = ", ")
                # increase players score in scoreboard
            print("")
        
            self.players = {}
            self.bets = {
                1 : [],
                2 : [],
                3 : [],
                4 : [],
                5 : []
            }   
            await asyncio.sleep(10)

        

    def bet(self, player, num):
        match num:
            case "one" : num = 1
            case "two" : num =2
            case "three" : num = 3
            case "four" : num = 4
            case "five" : num = 5

        if self.players.get(player) == None:
            self.players[player] = num
            self.bets[int(num)].append(player)
            return True
        
        return False


    def countdown(t):
    
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1
        
        print('Fire in the hole!!')

async def better(z):
    while True:
        n,m = input().split(" ")
        z.bet(n,m)
  
  
async def start():
    game_logic = Game_logic()

    game_logic.bet("zaza", 4)
    
    await asyncio.gather(game_logic.game_loop())

    # t2 = asyncio.create_task(better(game_logic))
    # t1 = asyncio.create_task(game_logic.game_loop())

    # await asyncio.gather(t1, t2)

        

if __name__ == "__main__":

    asyncio.run(start())


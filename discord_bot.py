import discord
import os
import logging
import openai
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from game_logic import Game_logic
import asyncio
import typing

# create logger
def init_logging(logger):
    # logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    log_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')

    handler_rot_file = RotatingFileHandler(filename='discord-bot.log', encoding='utf-8', mode='a')
    handler_rot_file.setLevel(logging.DEBUG)
    handler_rot_file.setFormatter(log_formatter)

    handler_console = logging.StreamHandler()
    handler_console.setLevel(logging.DEBUG)
    handler_console.setFormatter(log_formatter)

    logger.addHandler(handler_rot_file)
    logger.addHandler(handler_console)

    return logger

class MyClient(discord.Client):
    # def __init__(self, *, intents: discord.Intents, **options: typing.Any) -> None:
    #     super().__init__(intents=intents, **options)
        

    async def on_ready(self):
        print('Logged on as', self.user)

        
        # await self.game_logic.game_loop

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if self.user.mentioned_in(message):
            
            try:
                comm = classify(message.content, "command")

                if comm == "bet":
                    logging.info("Classified as bet... Checking value...")
                    bet_number = classify(message.content, "bet")
                    logging.info("Got bet number %s", bet_number)
                    
                    
                    logger.info(f"{message.author} bet on {bet_number}")

                    if self.game_logic.bet(message.author, bet_number):
                        await message.channel.send(f"{message.author} bet on {bet_number}") 
                    else:
                        await message.channel.send(f"You already betted on {self.game_logic.players[message.author]}, wait for next spin to bet again")
                    # self.game_logic.game_loop()

                else:
                    logger.info(f"Classified as an unknown command: {comm}")
                    await message.channel.send("other")
                    logger.info(comm)
            except Exception as e:
                logging.error("Exception in classify!")
                

def classify(prompt, class_type):
    model_engine = "text-davinci-002"  # or any other OpenAI model that suits your use case
    
    # define the prompt to use for classification

    if class_type == "bet":
        prompt = (f"Please classify the following user input into one of the following categories: "
                f"1. one\n2. two\n3. three \n4. four \n5. five \n\n"
                f"User Input: {prompt}\nCategory:")
    elif class_type == "command":
        prompt = (f"Please classify the following user input into one of the following categories: "
                f"1. bet\n2. other \n\n"
                f"User Input: {prompt}\nCategory:")

    try:
        # send prompt to OpenAI's API for classification
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1,
            n=1,
            stop=None,
            temperature=0,
        )

        # retrieve the predicted intent code from the response
        predicted_intent = response.choices[0].text.strip().lower()

        # return the predicted intent code
        logger.info("openAI: %s", predicted_intent)
        return predicted_intent
    except:
        logging.warn("AAAAAAAAAAAAAAAAAAAAAAAAAAA")
        return "zz"

async def start():
    intents = discord.Intents.default()
    intents.message_content = True

    game_logic = Game_logic()
    client = MyClient(intents=intents)

    task2 = client.start(os.getenv('DISCORD_BOT_TOKEN'), reconnect = True)
    # asyncio.run(task2)
    client.game_logic = game_logic

    t2 = asyncio.create_task(task2)
    t1 = asyncio.create_task(game_logic.game_loop())

    await asyncio.gather(t1, t2)

        

if __name__ == "__main__":
    load_dotenv()

    logger = init_logging(logging.root)
    
    openai.api_key = (os.getenv('OPENAI_KEY'))
    
    asyncio.run(start())
    # load_dotenv()

    # logger = init_logging(logging.root)
    # openai.api_key = (os.getenv('OPENAI_KEY'))


    # intents = discord.Intents.default()
    # intents.message_content = True

    # game_logic = Game_logic()
    # client = MyClient(intents=intents)

    # task2 = client.start(os.getenv('DISCORD_BOT_TOKEN'), reconnect = True)
    # # asyncio.run(task2)

    # t2 = asyncio.create_task(task2)
    # t1 = asyncio.create_task(game_logic.game_loop())

    # asyncio.run(asyncio.gather(t1, t2))

    # # loop = asyncio.get_event_loop()

    # try:
    #     loop.run_until_complete(asyncio.gather(t1,t2))
    # except KeyboardInterrupt:
    #     pass

    # client.run(os.getenv('DISCORD_BOT_TOKEN'))
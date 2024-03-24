# ***DISCORD GUESSING GAME***

Welcome to the Discord Guessing Game Bot!

### **How to setup**

1.  Clone repository
`git clone https://github.com/ooDIAX/Discord-Guessing-BOT.git`

2. Install all the required dependencies from /requirements.txt 
`pip install -r requirements.txt`
3.  Accuire API keys from [Discord](https://discord.com/developers/docs "Discord") and [OPENAI](https://platform.openai.com/docs/overview "OPENAI") from the following websites
4. Create /.env file according to /.env.dist format. Fill in all the required fields including the API keys

### **How to run**

Considering you've done all the work for setting up

1. Start the Docker container using command
`docker-compose up`
2. Create a [Discord bot ](https://discord.com/developers/applications "Discord bot ")  from developer portal
3. Add bot to the Discord server where you want to test it
4. Finally interact with the bot, Since bot has NLP capabilities theres no need to use any commands just use plain English
5. If you want to see live draw of number along with the leaderboard host the /webapp.py on you local machine or web service




### **Features**

User-Friendly Web Interface: Created using HTML, CSS, and Python's Flask library, the interface showcases the leaderboard and presents random numbers for the guessing game.

Natural Language Processing (NLP): Implemented NLP capabilities using OPENAI's text-davinci-3, allowing users to interact with the game using plain English commands.

Discord Integration: Leveraged Discord's Python library to effectively engage and interact with users on Discord servers, enhancing the overall user experience.

Persistent Data Storage: Leaderboard and number history data are persistently stored in a PostgreSQL database, ensuring accurate tracking and historical analysis.

Deployment: Successfully deployed the application on an AWS server, utilizing Docker for streamlined management and scalability.

### **Usage**

To start playing the guessing game on your Discord server, simply invite the bot and follow the instructions in the README!

Feel free to customize the sections, add links, or provide more detailed instructions based on your project's specifics and preferences!

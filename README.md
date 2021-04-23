# Bot Code

This repo contains the necessary files that are required for the sucessfull integration of the bot to Telegram and Database

# Description of each file:
actions/actions.py: All the custom actions that are required for the bot to connect to external world for API Integration and Database<br>
data/nlu.yml: The intents and their examples.<br>
data/rules.yml: The rules which are to be at any cost what ever the situation of the bot is. <br>
data/stories.yml: The file in which the intents are mapped with their responses<br>
domain.yml: The heart of the bot. All the necassary information to train the model is defined here.




## General Work flow of the Bot

The bot initially Authenticates the user whenever the user asks a query.
Then the bot classifies the request that is asked by the user and then responds accordingly
For storing information like Harassment Isuues, Resign Issues forms will be activated and asks all the necessary slots and send to a database

When ever the user says GoodBye the bot clears it memory.

import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person/bot!",
  "Let your unique awesomeness and positive energy inspire confidence in others."
  "Don't give up"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

def ez_command():
  messages = ["Wait... This isn't what I typed!", "Anyone else really like Rick Astley?", "Hey helper, how play game?", "Sometimes I sing soppy, love songs in the car.", "I like long walks on the beach and playing Hypixel", "Please go easy on me, this is my first game!", "You're a great person! Do you want to play some Hypixel games with me?", "In my free time I like to watch cat videos on Youtube", "When I saw the witch with the potion, I knew there was trouble brewing.", "If the Minecraft world is infinite, how is the sun spinning around it?", "Hello everyone! I am an innocent player who loves everything Hypixel.", "Plz give me doggo memes!", "I heard you like Minecraft, so I built a computer in Minecraft in your Minecraft so you can Minecraft while you Minecraft", "Why can't the Ender Dragon read a book? Because he always starts at the End.", "Maybe we can have a rematch?", "I sometimes try to say bad things then this happens :(", "Behold, the great and powerful, my magnificent and almighty nemisis!", "Doin a bamboozle fren.", "Your clicks per second are godly. :eek:", "What happens if I add chocolate milk to macaroni and cheese?", "Can you paint with all the colors of the wind", "Blue is greener than purple for sure", "I had something to say, then I forgot it.", "When nothing is right, go left.", "I need help, teach me how to play!", "Your personality shines brighter than the sun.", "You are very good at the game friend.", "I like pineapple on my pizza", "I like pasta, do you prefer nachos?", "I like Minecraft pvp but you are truly better than me!", "I have really enjoyed playing with you! <3", "ILY <3", "Pineapple doesn't go on pizza!", "Lets be friends instead of fighting okay?"]
  return(random.choice(messages))

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content
  
  if msg.startswith('-ez'):
    command = ez_command()
    await message.channel.send(command)

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")
  

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.key():
      index = int(msg.split("-del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channgel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
  
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv('TOKEN'))
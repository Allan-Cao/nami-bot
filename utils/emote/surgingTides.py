import discord
from discord.ext import commands
from discord.utils import get

from ebb import productionToken, sussy_kittens
import time

import sqlite3
connection = sqlite3.connect("kittens.db")
cursor = connection.cursor()

intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents = intents)
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    print("[Warning] This is the setup program and WILL override any current databases.")
    time.sleep(1)
    input("If this is what you would like to do, press [enter] to continue. Otherwise, exit the program.")
    cursor.execute("CREATE TABLE kitten (name TEXT, id INTEGER, kitten_number INTEGER)")
)
#import string
#letters = string.ascii_lowercase

@bot.event
async def on_message(message):
    await bot.process_commands(message)

##################### KITTEN COMMANDS #############################

@bot.event
async def on_member_join(member):

    if len(open_kittens.all()) == 0:
        n = len(kittens.all()) + starting_number
        try:
            await member.edit(nick="Kitten #" + str(n))
            print(f"{member.name} was renamed Kitten #{n}")
            kittens.insert({'id': member.id, 'name': member.name, 'number': n})
            n +=1
        except:
            print(f"{member.name} was unable to be renamed!")
    else:
        new_kitten = open_kittens.all()[0]
        cat = Query()
        try:
            await member.edit(nick="Kitten #" + str(new_kitten['number']))
            print(f"New kitten with id {member.id} will be assigned kitten #{new_kitten['number']}")
            kittens.insert({'id': member.id, 'name': member.name, 'number': new_kitten['number']})
            print(f"[Debug] {open_kittens.all()}")
            open_kittens.remove(cat.id == new_kitten['id'])
            print(f"[Debug] {open_kittens.all()}")
        except:
            print(f"{member.name} was unable to be renamed!")


@bot.event
async def on_member_remove(member):
    print(f"{member.name} has left the server! They were kitten #{n}")
    cursor.execute(
        "DELETE FROM kitten WHERE id = ?",
        (member.id,)
    )
"""
@bot.event
async def on_member_update(before, after):
    if str(before.name) != str(after.name):
        print("update before: " + before.name)
        print("update after: " + after.name)
"""

@bot.command(
    name="kitten",
    brief="Meow!",
    pass_context=True,
)
async def kitten(ctx):
    if ctx.author.id == 645940845245104130:
        sussy_kitten_n_values = []
        crewmate_kittens = ctx.message.guild.members
        crewmate_kittens = [i for i in crewmate_kittens if i.id not in sussy_kittens.keys()] # remove sussy kittens
        for sus_kitten_id in sussy_kittens.keys():
            try:
                n = sussy_kittens[sus_kitten_id]
                sus_kitten = ctx.message.guild.get_member(sus_kitten_id)
                await sus_kitten.edit(nick="Kitten #" + str(n))
                print(f"{sus_kitten.name} was renamed Kitten #{n}")
                kittens.insert({'id': sus_kitten.id, 'name': sus_kitten.name, 'number': n})
                sussy_kitten_n_values.append(n)
            except:
                print(f"{kitten.name} could not be renamed!")
        n = starting_number
        for member in crewmate_kittens:
            while n in sussy_kitten_n_values:
                n+=1
            cat = Query()
            if(len(kittens.search(cat.id == member.id)) == 0):
                try:
                    await member.edit(nick="Kitten #" + str(n))
                    print(f"{member.name} was renamed Kitten #{n}")
                    kittens.insert({'id': member.id, 'name': member.name, 'number': n})
                    n +=1
                except:
                    print(f"{member.name} was unable to be renamed!")
            else:
                if (member.nick == ("Kitten #" + str(kittens.search(cat.id == member.id)[0]['number']))):
                    print(f"{member.name} is already a kitten!")
                else:
                    await member.edit(nick="Kitten #" + str(kittens.search(cat.id == member.id)[0]['number']))
                    print(f"{member.name} was renamed Kitten #{str(kittens.search(cat.id == member.id)[0]['number'])}")
                
    else:
        await ctx.send("FAKE KITTEN DETECTED MEOW!")

@bot.command(
    name="unkitten",
    brief="Meow!",
    pass_context=True,
)
async def unkitten(ctx):
    if ctx.author.id == 645940845245104130:
        for member in ctx.message.guild.members:
            try:
                await member.edit(nick=member.name)
            except:
                print(f"{member.name} could not be unkittened!")
    else:
        await ctx.send("FAKE KITTY RAWRRRRRR!")

###################### END KITTEN COMMANDS #############################

"""
@bot.command(
    name="reset",
    pass_context=True,
)
async def reset(ctx):
    for member in ctx.message.guild.members:
            try:
                # print(member.display_name)
                await member.edit(nick=''.join(random.choice(letters) for i in range(10)))
            except:
                continue
"""
bot.run(productionToken)
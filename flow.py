import discord
from discord.ext import commands
from discord.utils import get

from ebb import productionToken, sussy_kittens, testToken

import sqlite3
connection = sqlite3.connect("kittens.db", isolation_level=None)
cursor = connection.cursor()

intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents = intents)
bot = commands.Bot(command_prefix="!", intents=intents)
##################### UTILITY COMMANDS #############################

def next_kitten_number():
    rows = cursor.execute("SELECT kitten_number FROM kitten").fetchall()
    all_kitten_numbers = [i[0] for i in rows]
    max_kitten_numbers = list(range(min(all_kitten_numbers),max(all_kitten_numbers)+2))
    return min(list(set(max_kitten_numbers) - set(all_kitten_numbers)))
    # surely it isn't that computationally expensive
    # surely there is a better way to do this :3

##################### DISCORD COMMANDS #############################
@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("I still hear the song of the sea."),
)

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    """
        On member join, first check if the member id is already in the database
        If it is,
            Give them back their kitten number
        Otherwise,
            Use the next_kitten_number() to find the next available kitten number
    """
    try:
        kitten = cursor.execute("SELECT name, id, kitten_number FROM kitten WHERE id == ?",
                                (member.id,)).fetchone()
        if kitten == None:
            kitten_name = member.name
            kitten_id = member.id
            kitten_number = next_kitten_number()
            await member.edit(nick="Kitten #" + str(kitten_number))
            cursor.execute("INSERT INTO kitten VALUES (?, ?, ?)",
                        (kitten_name, kitten_id, kitten_number)
            )
            print(f"{member.name} was renamed Kitten #{kitten_number}")
        else:
            kitten_number = kitten[2]
            await member.edit(nick="Kitten #" + str(kitten_number))
            print(f"{member.name} was renamed Kitten #{kitten_number}")
    except:
        print(f"{member.name} was unable to be renamed!")


@bot.event
async def on_member_remove(member):
    """
        Since we have an algorithm to deal with newly assigned numbers, why not just keep the number people had :3
    """
    n = cursor.execute("SELECT name, id, kitten_number FROM kitten WHERE id == ?",
                        (member.id,)).fetchone()
    print(f"{member.name} has left the server! They were kitten #{n} and was last named {member.nick}")
"""
@bot.event
async def on_member_update(before, after):
    if str(before.name) != str(after.name):
        print("update before: " + before.name)
        print("update after: " + after.name)
"""
@bot.command(
    name="createDB",
    brief="Creates new database",
    pass_context=True,
)
async def createDB(ctx):
    if ctx.author.id == 645940845245104130:
        try:
            cursor.execute("CREATE TABLE kitten (name TEXT, id INTEGER, kitten_number INTEGER)")
            cursor.execute("INSERT INTO kitten VALUES (?, ?, ?)",
                                    ("TauPiPhi", 645940845245104130, 0)
                        )
            cursor.execute("INSERT INTO kitten VALUES (?, ?, ?)",
                                    ("Jopee", 218843524748148736, 1)
                        )
            cursor.execute("INSERT INTO kitten VALUES (?, ?, ?)",
                                    ("Milk Loaf", 243537427162071040, 2)
                        )
        except:
            await ctx.send("Database has already been created bozo...")
    else:
        await ctx.send("meow :3")

@bot.command(
    name="kitten",
    brief="Meow!",
    pass_context=True,
)

#crewmate_kittens = [i for i in crewmate_kittens if i.id not in sussy_kittens.keys()] # remove sussy kittens
#        for sus_kitten_id in sussy_kittens.keys():
#
async def kitten(ctx):
    if ctx.author.id == 645940845245104130:
        for sus_kitten in ctx.message.guild.members:
            if sus_kitten.id in sussy_kittens.keys():
                try:
                    print(sus_kitten)
                    kitten_name = sus_kitten.name
                    kitten_id = sus_kitten.id
                    kitten_number = sussy_kittens[sus_kitten.id]
                    await sus_kitten.edit(nick="Kitten #" + str(kitten_number))
                    print(f"By coincidence, {sus_kitten.name} was renamed Kitten #{kitten_number}")
                    kitten = cursor.execute("SELECT name, id, kitten_number FROM kitten WHERE id == ?",
                                            (sus_kitten.id,)).fetchone()
                    if kitten == None:
                        cursor.execute("INSERT INTO kitten VALUES (?, ?, ?)",
                                    (kitten_name, kitten_id, kitten_number)
                        )
                except:
                    print(f"{kitten_name} could not be renamed!")
            else:
                try:
                    current_kitten = cursor.execute("SELECT name, id, kitten_number FROM kitten WHERE id == ?",
                                            (sus_kitten.id,)).fetchone()
                    if current_kitten == None:
                        kitten_name = sus_kitten.name
                        kitten_id = sus_kitten.id
                        kitten_number = next_kitten_number()
                        await sus_kitten.edit(nick="Kitten #" + str(kitten_number))
                        cursor.execute("INSERT INTO kitten VALUES (?, ?, ?)",
                                    (kitten_name, kitten_id, kitten_number)
                        )
                        print(f"{sus_kitten.name} was renamed Kitten #{kitten_number}")
                    else:
                        kitten_number = current_kitten[2]
                        await sus_kitten.edit(nick="Kitten #" + str(kitten_number))
                except:
                    print(f"{sus_kitten.name} was unable to be renamed!") 
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
        await ctx.send("nyaaaaa :3")

###################### END KITTEN COMMANDS #############################

bot.run(testToken)
import discord
from discord.ext import commands
from ebb import productionToken, sussy_kittens, testToken, admin
import sqlite3
connection = sqlite3.connect("userbase.db", isolation_level=None)
cursor = connection.cursor()

intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents = intents)
bot = commands.Bot(command_prefix="!", intents=intents)

is_debug = False

activity_name = "I still hear the song of the sea."
admin_error = "meow :3"
db_error = "Database error..."

##################### UTILITY COMMANDS #############################

def generate_name(n):
    return("Kitten #" + str(n))

def get_next_number():
    rows = cursor.execute("SELECT kitten_number FROM kitten").fetchall()
    all_kitten_numbers = [i[0] for i in rows] + list(sussy_kittens.values())
    distinct = {*all_kitten_numbers}
    index = 1
    while True:
        if index not in distinct:
            return index
        index += 1
    # btw this is a leetcode hard question lol
    # https://leetcode.com/problems/first-missing-positive/

##################### DISCORD COMMANDS #############################
@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(activity_name),
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
        user = cursor.execute("SELECT name, id, kitten_number FROM kitten WHERE id == ?",
                                (member.id,)).fetchone()
        if user == None:
        # If member could not be found
            user_name = member.name
            user_id = member.id
            user_number = get_next_number() 
            await member.edit(nick=generate_name(user_number))
            cursor.execute("INSERT INTO kitten VALUES (?, ?, ?, ?)",
                        (user_name, user_id, user_number, True)
            )
            print(f"{member.name} was renamed {generate_name(user_number)}")
        else:
        # Otherwise, give them back their number
            user_number = user[2]
            await member.edit(nick=generate_name(user_number))
            print(f"{member.name} was renamed {generate_name(user_number)}")
    except:
        if is_debug:
            raise
        print(f"{member.name} was unable to be renamed!")

@bot.event
async def on_member_remove(member):
    """
        Since we have an algorithm to deal with newly assigned numbers, people will keep their number!
    """
    cursor.execute(
        "UPDATE kitten SET active = ? WHERE id = ?",
        (False, member.id)
    )
    n = cursor.execute("SELECT name, id, kitten_number FROM kitten WHERE id == ?",
                        (member.id,)).fetchone()
    print(f"{member.name} has left the server! They were {generate_name(n[2])} and was last named {member.nick}")

##################### DATABASE COMMANDS #############################

@bot.command(
    name="create",
    brief="Creates new database",
    pass_context=True,
)
async def createDB(ctx):
    if ctx.author.id in admin:
        try:
            cursor.execute("CREATE TABLE kitten (name TEXT, id INTEGER, kitten_number INTEGER, active BOOLEAN)")
        except:
            if is_debug:
                raise
            await ctx.send(db_error)
    else:
        await ctx.send(admin_error)

@bot.command(
    name="list",
    brief="Prints out the entire database",
    pass_context=True,
)
async def list(ctx):
    if ctx.author.id in admin:
        try:
            inactive = list(cursor.execute("SELECT * FROM kitten WHERE active == false").fetchall())
            embed=discord.Embed(title="Inactive Users")
            for user in inactive:
                embed.add_field(name=generate_name(user[2]), value=user[1], inline=True)
            await ctx.send(embed=embed)

            active = list(cursor.execute("SELECT * FROM kitten WHERE active == true").fetchall())
            embed=discord.Embed(title="Active Users")
            for user in active:
                embed.add_field(name=generate_name(user[2]), value=user[1], inline=True)
            await ctx.send(embed=embed)
        except:
            if is_debug:
                raise
            await ctx.send(db_error)
    else:
        await ctx.send(admin_error)

@bot.command(
    name="remove",
    brief="Removes a member from the database",
    pass_context=True,
)
async def remove(ctx, arg):
    if ctx.author.id in admin:
        try:
            user_number, is_active = cursor.execute("SELECT kitten_number, active FROM kitten WHERE id == ?",
                        (arg,)).fetchone()
            if is_active == False:
                cursor.execute(
                    "DELETE FROM kitten WHERE id = ?",
                    (arg,)
                )
                await ctx.send(f"Removed {generate_name(user_number)} from the database!")
            else:
                await ctx.send(f"Unable to remove user {arg} due to them being active!")
        except:
            if is_debug:
                raise
            await ctx.send("An error occured trying to remove that user from the db. Try removeDB {user id}")
    else:
        await ctx.send(admin_error)

@bot.command(
    name="rename",
    brief="Renames all users",
    pass_context=True,
)
async def rename(ctx):
    if ctx.author.id in admin:
        for sus_kitten in ctx.message.guild.members:
            if sus_kitten.id in sussy_kittens.keys():
                try:
                    kitten_name = sus_kitten.name
                    kitten_id = sus_kitten.id
                    kitten_number = sussy_kittens[sus_kitten.id]
                    await sus_kitten.edit(nick="Kitten #" + str(kitten_number))
                    print(f"By coincidence, {sus_kitten.name} was renamed Kitten #{kitten_number}")
                    kitten = cursor.execute("SELECT name, id, kitten_number FROM kitten WHERE id == ?",
                                            (sus_kitten.id,)).fetchone()
                    if kitten == None:
                        cursor.execute("INSERT INTO kitten VALUES (?, ?, ?, ?)",
                                    (kitten_name, kitten_id, kitten_number, True)
                        )
                except:
                    if is_debug:
                        raise
                    print(f"{kitten_name} could not be renamed!")
                    await ctx.send(print(f"{kitten_name} could not be renamed!"))
            else:
                try:
                    current_kitten = cursor.execute("SELECT name, id, kitten_number FROM kitten WHERE id == ?",
                                            (sus_kitten.id,)).fetchone()
                    if current_kitten == None:
                        kitten_name = sus_kitten.name
                        kitten_id = sus_kitten.id
                        kitten_number = get_next_number()
                        await sus_kitten.edit(nick="Kitten #" + str(kitten_number))
                        cursor.execute("INSERT INTO kitten VALUES (?, ?, ?, ?)",
                                    (kitten_name, kitten_id, kitten_number, True)
                        )
                        print(f"{sus_kitten.name} was renamed Kitten #{kitten_number}")
                    else:
                        kitten_number = current_kitten[2]
                        await sus_kitten.edit(nick="Kitten #" + str(kitten_number))
                except:
                    if is_debug:
                        raise
                    print(f"{sus_kitten.name} was unable to be renamed!")
                    await ctx.send(f"{sus_kitten.name} was unable to be renamed!")
    else:
        await ctx.send(admin_error)

@bot.command(
    name="reset",
    brief="Resets all user names",
    pass_context=True,
)
async def reset(ctx):
    if ctx.author.id == 645940845245104130:
        for member in ctx.message.guild.members:
            try:
                await member.edit(nick=member.name)
            except:
                if is_debug:
                    raise
                print(f"{member.name}'s nickname could not be reset.")
                await ctx.send(f"{member.name}'s nickname could not be reset.")
    else:
        await ctx.send(admin_error)

###################### END KITTEN COMMANDS #############################

bot.run(testToken)
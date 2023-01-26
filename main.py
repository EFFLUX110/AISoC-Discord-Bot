import discord
from discord.ext import commands
import os
import asyncio

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="%",intents=discord.Intents.all() )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.name == "google-form-logs":
        ID= message.embeds[0].fields[1].value 
        
        await message.channel.send(f"This is new member's ID: {ID}")

        member = bot.get_user(ID)
        member.add_roles("Verified")

message=None

@bot.event
async def on_ready():
    
    global message
    
    print(f"{bot.user} has connected to Discord!")
    
    # Create the interactive button
    button = discord.Embed(title="Get your Discord USER ID", color=0x00FF00)
    button.add_field(name="👇|Press the blue circle", value="\u200b")
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
            await message.remove_reaction(payload.emoji, user)
            await asyncio.sleep(15)
            await id_msg.delete()
            await id.delete()

bot.run(DISCORD_TOKEN)
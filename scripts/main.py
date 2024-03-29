import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import functions
from io import StringIO
import json
import cm2image
import cm2video
import io

load_dotenv()

TOKEN = os.environ['TOKEN']
NAME = os.environ['name']

bot = commands.Bot(command_prefix="", intents = discord.Intents.all())

converting_video = False
hi_lastuser = None

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Bot ID: {bot.user.id}")
    game = discord.Game("Circuit Maker π")
    await bot.change_presence(activity=game)
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.event
async def on_message(message):
    global NAME, hi_lastuser
    lowered_content = str(message.content).lower()
    if lowered_content == "hi" or "<@1213876646315171841>" in lowered_content: 
        if str(message.author) != "ASTRO#8574" and hi_lastuser != str(message.author):
            hi_lastuser = str(message.author)
            await message.channel.send("hi")

    content = message.content
    command, inputs = functions.get_command(content)
    joinedinputs = " ".join(inputs)
    if command != "":
        if "@here" in content or "@everyone" in content:
                pass
        elif command[0] == "$" and str(message.author) != "ASTRO#8574":
            action = command[1:]

            extracmds = []

            commands = json.load(open(f"/home/{NAME}/workspace/ASTRO/commands.json", "r"))
            cmd_list = commands["commands"]
            for i in range(len(cmd_list)):
                extracmds.append(cmd_list[i]['command'])

            commands = ["praise", "binary", "integer", "ascii", "pop"]

            all_commands = commands + extracmds

            if action == "help":
                output = f"'$' commands: {', '.join(all_commands)}"
            elif action == "poll":
                numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"] 
                # color = functions.rgb_hex(0, 0, 255)
                try:
                    name = joinedinputs.split(",")[0]
                    options = joinedinputs.split(",")[1:]
                    if len(options) > 10:
                        await message.channel.send("Maximum 10 options.")
                        return
                    
                    embed = discord.Embed(title=name, description=f"Poll created by {message.author.display_name}({message.author})", color=0x0000ff)
                    for i, option in enumerate(options):
                        embed.add_field(name="",value=f"{numbers[i]} {option}", inline=False)

                    poll = await message.channel.send(embed=embed)
                    for j, option in enumerate(options):
                        await poll.add_reaction(numbers[j])
                    return
                except Exception:
                    output = "Invalid, $poll {title}, {options}, {more options} (use ',' as a separator))"
            elif action == "say" and str(message.author) == "gaming4cats":
                await message.delete()
                output = joinedinputs
            elif action == "praise":
                thing = joinedinputs
                praise1 = f"{thing} is the best, everybody should pray to {thing}"
                praise2 = f"We all live to love {thing}"
                praise3 = f"We must all pray to {thing}"
                praise4 = f"Nobody should disrespect {thing}"
                praise5 = f"ALL HAIL {thing.upper()}"
                praises = [praise1, praise2, praise3, praise4, praise5]
                output = random.choice(praises)
            elif action == "pop":
                try:
                    x = int(inputs[0])
                    y = int(inputs[1])
                    
                    matrix = []

                    for i in range(y):
                        matrix.append("||pop||" * x)

                    output = "\n".join(matrix)
                except Exception:
                    output = "$pop {x} {y}"
            elif action == "binary":
                try:
                    value = int("".join(inputs))
                    output = f"Integer to binary:\n```{bin(value)[2:]}```"
                except Exception:
                    ascii_val = []
                    value = " ".join(inputs)
                    for c in value:
                        val = bin(ord(c))
                        ascii_val.append(val[2:])
                    ascii_joined = " ".join(ascii_val)
                    output = f"Ascii to binary:\n```{ascii_joined}```"
            elif action == "integer":
                try:
                    value = "".join(inputs)
                    output = f"Binary to integer:\n```{int(value, 2)}```"
                except Exception:
                    output = "Must be binary."
            elif action == "ascii":
                try:
                    characters = []
                    for c in inputs:
                        characters.append(chr(int(c, 2)))
                    chars_joined = "".join(characters)
                    if '`' in chars_joined:
                        output = "nuh uh dont even try"
                    else:
                        output = f"Binary to ascii:\n```{chars_joined}```"
                except Exception:
                    output = "Must be binary."
            elif action == "add" and str(message.author) == "gaming4cats":
                name = inputs[0]
                out = inputs[1:]
                data = {
                    "command":name,
                    "output": " ".join(out)
                }
                functions.json_add(data, f"/home/{NAME}/workspace/ASTRO/")
                output = f"Created command: {name}\nOutput: {' '.join(out)}"
            elif action == "log" and str(message.author) == "gaming4cats":
                with open(f"/home/{NAME}/workspace/ASTRO/dollarLog.txt", "r+") as log:
                    output = "Recent $ commands\n" + "".join(log.readlines()[-5:])
            elif action == "reboot" and str(message.author) == "gaming4cats":
                await message.channel.send("Rebooting...")
                os.system("rebootbot")
            else:
                if action in extracmds:
                    output = cmd_list[extracmds.index(action)]['output']
                else:
                    output = "Invalid command, see $help."

            with open(f"/home/{NAME}/workspace/ASTRO/dollarLog.txt", "a+") as log:
                if joinedinputs == '':
                    log.write(f"{message.author} did command ``{action}``\n")
                else:
                    log.write(f"{message.author} did command ``{action}``, inputs: ``{joinedinputs}``\n")

            try:
                await message.channel.send(output)
            except discord.errors.HTTPException:
                await message.channel.send("Message over character limit")

@bot.tree.command(name="dpaste", description="get a raw dpaste link")
@app_commands.describe(input="text you want to send to dpaste")
async def dpaste(message: discord.Interaction, input: str):
    link = functions.dpaste(input)
    await message.response.send_message(link)
    
@bot.tree.command(name="textcm2", description="create text in cm2")
@app_commands.describe(text="text to convert", step="space between text, default:0.5")
async def textcm2(message: discord.Interaction, text: str, step: float=0.5):
    output = f"{functions.make_text(text, step)}"
    if len(output) > 1000:
        buffer = StringIO(output)
        f = discord.File(buffer, filename="output.txt")
        await message.response.send_message(file=f)
    await message.response.send_message(f"```{output}```")

@bot.tree.command(name="decoder_generator", description="generate a decoder")
@app_commands.describe(inputs="amount of inputs")
async def decoder_generator(message: discord.Interaction, inputs: int):
    if inputs > 10:
        await message.response.send_message("too much")
    else:
        output = f"{functions.generate_decoder(inputs)}"
        if len(output) > 1000:
            buffer = StringIO(output)
            f = discord.File(buffer, filename="output.txt")
            await message.response.send_message(file=f)
        else:
            await message.response.send_message(f"```{output}```")

@bot.tree.command(name="suggest", description="suggest an idea for the bot")
@app_commands.describe(topic="what do you want to suggest")
async def suggest(message: discord.Interaction, topic: str):
    global NAME
    with open(f"/home/{NAME}/workspace/ASTRO/suggestions.txt", "a+") as s:
        s.write(f"Name: {message.user}, Suggestion: {topic}\n")
    await message.response.send_message("Added suggestion")

@bot.tree.command(name="imagecm2", description="Convert an Image to a CM2 save string.")
@app_commands.describe(image="Image to convert", maxraw="Maximum raw size")
async def imagecm2(message: discord.Interaction, image: discord.Attachment, maxraw: int=200_000):
    await message.response.send_message("Converting...")
    imBytes = await image.read()
    save = cm2image.convert_image(io.BytesIO(imBytes), maxraw)
    await message.edit_original_response(content=save)

@bot.tree.command(name="videocm2", description="Convert a video to a CM2 save string.")
@app_commands.describe(video="Video to convert", fps="Frames per second", tps="Ticks between frames, 2+ recommended", height="Height of the video", threshold="Pixel brightness to choose black or white")
async def videocm2(message: discord.Interaction, video: discord.Attachment, fps: int=2, tps: int=2, height: int=16, threshold: int=200):
    global NAME, converting_video

    if converting_video:
        await message.response.send_message("Currently converting video, please wait and try again.")
        return
    
    converting_video = True

    if video.content_type.startswith("video"):
        integers = [fps, tps, height, threshold]
        names = ["fps", "tps", "height", "threshold"]
        errors = []
        if height > 32:
            errors.append("height over 32")
        if threshold > 255:
            errors.append("threshold over 255")
        for i, integer in enumerate(integers):
            if integer < 1:
                errors.append(f"{names[i]} under 1")

        if errors != []:
            await message.response.send_message("ERROR: " + ", ".join(errors))
            converting_video = False
            return
        
        await message.response.send_message("Converting...")

        await video.save(f"/home/{NAME}/workspace/ASTRO/frames/" + video.filename)
        path = f"/home/{NAME}/workspace/ASTRO/frames/" + video.filename
        save = cm2video.convertvideo(path, fps=fps, tps=tps, height=height, threshold=threshold)
        await message.edit_original_response(content=save)
    else:
        await message.response.send_message("Must be a video file.")  

    converting_video = False

bot.run(TOKEN)

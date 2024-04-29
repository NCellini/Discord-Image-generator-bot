import time
from Classes.ViewClasses import *
from Classes.ButtonClasses import *

load_dotenv()  # load all the variables from the .env file
intents = discord.Intents.default()
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="create", description="Create a image from text")
async def create(interaction, prompt):
    """Generate an image from a text prompt using the stable-diffusion model"""
    await interaction.response.send_message("**" + prompt + "** - " +
                                            f"{interaction.author.mention} (in process)")
    response = text2img_call(prompt)
    if response['status'] == 'failed':
        await interaction.delete()
        await interaction.send("Api call failed, please try again later")
    elif response['status'] == 'error':
        await interaction.delete()
        await interaction.send(f"Api call error: {response['message']}")
    else:
        create_image_collage(response['output'], f"{interaction.user.id}")
        view = ButtonsView(prompt, response['output'], f"{interaction.user.id}")

        for number in range(1, len(response['output']) + 1):
            view.add_item(UpscaleButton(number=number))
            view.add_item(VariationButton(number=number))

        await interaction.delete()
        await interaction.send("**" + prompt + "** - " + f"{interaction.author.mention}",
                               file=discord.File(f"./images/{interaction.user.id}/img_collage.png"), view=view)


@bot.slash_command(name="test", description="test command")
async def test(interaction):
    response = create_test_response()
    await interaction.response.send_message("**" + response['meta']['prompt'] + "** - " +
                                            f"{interaction.author.mention} (in process)")
    create_image_collage(response['output'], f"{interaction.user.id}")
    view = ButtonsView(response['meta']['prompt'], response['output'], f"{interaction.user.id}")

    for number in range(1, len(response['output']) + 1):
        view.add_item(UpscaleButton(number=number))
        view.add_item(VariationButton(number=number))

    time.sleep(4)
    await interaction.delete()
    await interaction.send("**" + response['meta']['prompt'] + "** - " + f"{interaction.author.mention}",
                           file=discord.File(f"./images/{interaction.user.id}/img_collage.png"), view=view)


bot.run(os.getenv('DISCORD_TOKEN'))  # run the bot with the token

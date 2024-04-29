import discord
from Classes.ViewClasses import UpscaledView, VariationsView
from functions import *


class UpscaleButton(discord.ui.Button):
    def __init__(self, number):
        super().__init__(label=f" Upscale {number}  ", style=discord.ButtonStyle.gray, row=0)
        self.number = number

    async def callback(self, interaction: discord.Interaction):
        view = UpscaledView(self.view.prompt, self.view.relative_path, self.view.images_urls[self.number - 1])

        self.style = discord.ButtonStyle.blurple
        await interaction.response.edit_message(view=self.view)

        await interaction.followup.send(
            "**" + self.view.prompt + "** - Upscaled by " + f"{interaction.user.mention}",
            file=discord.File(
                f"./images/{self.view.relative_path}/img{self.number}.png"),
            view=view)


class VariationButton(discord.ui.Button):
    def __init__(self, number):
        super().__init__(label=f"Variations {number}", style=discord.ButtonStyle.gray, row=1)
        self.number = number

    async def callback(self, interaction: discord.Interaction):
        self.style = discord.ButtonStyle.blurple
        await interaction.response.edit_message(view=self.view)
        msg = await interaction.followup.send(f"Making variations for image#{self.number} with prompt **" + self.view.prompt
                                        + "** - " + f"{interaction.user.mention} (in process)")
        response = img2img_call(self.view.prompt, self.view.images_urls[self.number - 1])
        if response['status'] == 'failed' or response['status'] == 'error':
            await interaction.followup.send("Api call failed, please try again later")
        else:
            self.view.relative_path = f"{interaction.user.id}/variations{self.number}"

            create_image_collage(response['output'], f"{interaction.user.id}/variations{self.number}")

            view = VariationsView(self.view.prompt, response['output'],
                                  f"{interaction.user.id}/variations{self.number}",
                                  self.view.images_urls[self.number - 1])

            for number in range(1, len(response['output']) + 1):
                view.add_item(UpscaleButton(number=number))
                view.add_item(VariationButton(number=number))

            await msg.delete()
            await interaction.followup.send(
                "**" + self.view.prompt + "** - Variations by " + f"{interaction.user.mention}",
                file=discord.File(f"./images/{interaction.user.id}/variations{self.number}"
                                  f"/img_collage.png"),
                view=view)

import discord
from functions import *


class ButtonsView(discord.ui.View):
    def __init__(self, prompt, images_urls, relative_path):
        super().__init__()
        self.relative_path = relative_path
        self.prompt = prompt
        self.images_urls = images_urls

    @discord.ui.button(label="Try Again",
                       style=discord.ButtonStyle.gray,
                       row=4)
    async def try_again(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.prompt is None:
            await interaction.response.send_message("Error in the prompt")
            return

        await interaction.response.send_message("**" + self.prompt + "** - " +
                                                f"{interaction.user.mention} (in process)")
        response = text2img_call(self.prompt)
        if response['status'] == 'failed':
            await interaction.followup.send("Api call failed, please try again later")
        else:
            create_image_collage(response['output'], f"{interaction.user.id}")
            view = ButtonsView(self.prompt, response['output'], f"{interaction.user.id}")

            from Classes.ButtonClasses import UpscaleButton, VariationButton
            for number in range(1, len(response['output']) + 1):
                view.add_item(UpscaleButton(number=number))
                view.add_item(VariationButton(number=number))

            await interaction.delete_original_response()
            await interaction.followup.send("**" + self.prompt + "** - " + f"{interaction.user.mention}",
                                            file=discord.File(f"./images/{interaction.user.id}/img_collage.png"),
                                            view=view)


class VariationsView(discord.ui.View):
    def __init__(self, prompt, images_urls, relative_path, init_img):
        super().__init__()
        self.relative_path = relative_path
        self.prompt = prompt
        self.images_urls = images_urls
        self.init_img = init_img

    @discord.ui.button(label="Try Again",
                       style=discord.ButtonStyle.gray,
                       row=4)
    async def try_again(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("**" + self.prompt + "** - " +
                                                f"{interaction.user.mention} (in process)")
        response = img2img_call(self.prompt, self.init_img)
        if response['status'] == 'failed':
            await interaction.followup.send("Api call failed, please try again later")
        else:
            create_image_collage(response['output'], f"{interaction.user.id}")
            view = VariationsView(self.prompt, response['output'], f"{interaction.user.id}", self.init_img)

            from Classes.ButtonClasses import UpscaleButton, VariationButton
            for number in range(1, len(response['output']) + 1):
                view.add_item(UpscaleButton(number=number))
                view.add_item(VariationButton(number=number))

            await interaction.delete_original_response()
            await interaction.followup.send("**" + self.prompt + "** - " + f"{interaction.user.mention}",
                                            file=discord.File(f"./images/{interaction.user.id}/img_collage.png"),
                                            view=view)


class UpscaledView(discord.ui.View):
    def __init__(self, prompt, relative_path, init_img):
        super().__init__()
        self.relative_path = relative_path
        self.prompt = prompt
        self.init_img = init_img

    @discord.ui.button(label="Create variations",
                       style=discord.ButtonStyle.blurple)
    async def create_variations(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("**" + self.prompt + "** - Creating variations by" +
                                                f"{interaction.user.mention} (in process)")
        response = img2img_call(self.prompt, self.init_img)
        if response['status'] == 'failed' or response['status'] == 'error':
            await interaction.followup.send("Api call failed, please try again later")
        else:
            self.relative_path = f"{interaction.user.id}/variations"
            create_image_collage(response['output'], f"{interaction.user.id}/variations")
            view = VariationsView(self.prompt, response['output'],
                                  f"{interaction.user.id}/variations",
                                  self.init_img)

            from Classes.ButtonClasses import UpscaleButton, VariationButton
            for number in range(1, len(response['output']) + 1):
                view.add_item(UpscaleButton(number=number))
                view.add_item(VariationButton(number=number))

            await interaction.delete_original_response()
            await interaction.followup.send(
                "**" + self.prompt + "** - Variations by " + f"{interaction.user.mention}",
                file=discord.File(f"./images/{interaction.user.id}/variations"
                                  f"/img_collage.png"),
                view=view)

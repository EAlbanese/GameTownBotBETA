from discord import ui, ButtonStyle, InputTextStyle, Interaction, Embed, PermissionOverwrite, Client, ChannelType, SelectOption

# Buttons


class ChannelSettingsButtonView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ ui.button(emoji="🔐", style=ButtonStyle.primary)
    async def private_button_callback(self, button, interaction: Interaction):
        await interaction.response.defer()
        voicechannel = interaction.user.voice.channel
        overwrite = PermissionOverwrite()
        overwrite.connect = False
        await voicechannel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        embed = Embed(
            title=f"✅ Voice Channel wurde auf 🔐 PRIVAT 🔐 gesetzt")
        await interaction.followup.send(embed=embed, ephemeral=True)

    @ ui.button(emoji="🔓", style=ButtonStyle.primary)
    async def public_button_callback(self, button, interaction: Interaction):
        await interaction.response.defer()
        voicechannel = interaction.user.voice.channel
        overwrite = PermissionOverwrite()
        overwrite.connect = True
        await voicechannel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        embed = Embed(
            title=f"✅ Voice Channel wurde auf 🔓 ÖFFENTLICH 🔓 gesetzt")
        await interaction.followup.send(embed=embed, ephemeral=True)

    @ ui.button(emoji="👥", style=ButtonStyle.primary)
    async def limit_button_callback(self, button, interaction):
        await interaction.response.send_modal(LimitModal(title="Limit"))

    @ ui.button(emoji="📝", style=ButtonStyle.primary)
    async def edit_button_callback(self, button, interaction):
        await interaction.response.send_modal(EditModal(title="Umbenennen"))

    @ ui.button(emoji="🦶", style=ButtonStyle.primary)
    async def kick_button_callback(self, button, interaction):
        await interaction.response.send_modal(KickModal(title="Kick"))


# Modal
class LimitModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=None)

        self.add_item(ui.InputText(
            label="Voice Channel Limit setzen", style=InputTextStyle.short))

    async def callback(self, interaction: Interaction):

        voicechannel = interaction.user.voice.channel
        await voicechannel.edit(user_limit=self.children[0].value)

        embed = Embed(
            title=f"✅ Channel Limit wurde auf {self.children[0].value} Member gesetzt.")
        channel = await interaction.guild.fetch_channel(1087350554977640508)

        await interaction.response.send_message(f"Voice Channel wurde erfolgreich bearbeitet", ephemeral=True)
        await channel.send(embed=embed)


class EditModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=None)

        self.add_item(ui.InputText(
            label="Voice Channel Umbenennen", style=InputTextStyle.short))

    async def callback(self, interaction: Interaction):

        voicechannel = interaction.user.voice.channel
        await voicechannel.edit(name=self.children[0].value)

        embed = Embed(
            title=f"✅ Channel wurde zu {self.children[0].value} umbenannt.")
        channel = await interaction.guild.fetch_channel(1087350554977640508)

        await interaction.response.send_message(f"Voice Channel wurde erfolgreich bearbeitet", ephemeral=True)
        await channel.send(embed=embed)


class KickModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=None)

        self.add_item(ui.InputText(
            label="Wen möchtest du kicken", style=InputTextStyle.short))

    async def callback(self, interaction: Interaction):

        voicechannel = interaction.user.voice.channel
        for member in voicechannel.members:
            if member.name == self.children[0].value:
                await member.move_to(None)

        embed = Embed(
            title=f"✅ {self.children[0].value} wurde aus dem Channel gekickt.")
        channel = await interaction.guild.fetch_channel(1087350554977640508)

        await interaction.response.send_message(f"Voice Channel wurde erfolgreich bearbeitet", ephemeral=True)
        await channel.send(embed=embed)

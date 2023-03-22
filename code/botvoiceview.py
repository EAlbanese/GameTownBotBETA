from discord import ui, ButtonStyle, InputTextStyle, Interaction, Embed, PermissionOverwrite, Client, ChannelType, SelectOption

# Buttons


class ChannelSettingsView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.select(
        placeholder="Einstellungen für deinen Voice Channel",
        min_values=1,
        max_values=1,
        options=[
            SelectOption(
                label="🔐 Privat",
                value='1'
            ),
            SelectOption(
                label="🔓 Öffentlich",
                value='2'
            ),
            SelectOption(
                label="👥 Limit",
                value='3'
            ),
            SelectOption(
                label="📝 Umbenennen",
                value='4'
            ),
            SelectOption(
                label="🦶 Kick",
                value='5'
            ),
        ]
    )
    async def tempvoice_select_callback(self, select, interaction: Interaction):
        await interaction.response.defer()

        if select.values[0] == "1":
            voicechannel = interaction.user.voice.channel
            await interaction.followup.send(f"✅ Voice Channel wurde auf **PRIVAT** gesetzt", ephemeral=True)
        if select.values[0] == "2":
            await interaction.followup.send(f"✅ Voice Channel wurde auf **ÖFFENTLICH** gesetzt", ephemeral=True)
        if select.values[0] == "3":
            await interaction.response.send_modal(LimitModal(title="Voice Channel Limit setzen"))
        if select.values[0] == "4":
            voicechannel = interaction.user.voice.channel
            await voicechannel.edit(name="test")
            # await interaction.response.send_modal(EditModal(title="Voice Channel Umbenennen"))
        if select.values[0] == "5":
            await interaction.response.send_modal(KickModal(title="Member Kicken"))


# Modal
class LimitModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=None)

        self.add_item(ui.InputText(
            label="Voice Channel Limit setzen", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(
            title=f"✅ Channel Limit wurde auf {self.children[0].value} Member gesetzt.")
        channel = await interaction.guild.fetch_channel(1087350554977640508)

        await channel.send(embed=embed, ephemeral=True)


class EditModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=None)

        self.add_item(ui.InputText(
            label="Voice Channel Umbenennen", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(
            title=f"✅ Channel wurde zu {self.children[0].value} umbenannt.")
        channel = await interaction.guild.fetch_channel(1087350554977640508)

        await channel.send(embed=embed, ephemeral=True)


class KickModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=None)

        self.add_item(ui.InputText(
            label="Wen möchtest du kicken", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(
            title=f"✅ {self.children[0].value} wurde aus dem Channel gekickt.")
        channel = await interaction.guild.fetch_channel(1087350554977640508)

        await channel.send(embed=embed, ephemeral=True)

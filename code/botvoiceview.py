from discord import ui, ButtonStyle, InputTextStyle, Interaction, Embed, PermissionOverwrite, Client, ChannelType, SelectOption


class variableManager(ui.View):
    voice_channel = 0
    voice_member = []
    user_count = []


# Buttons
class ChannelSettingsButtonView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ ui.button(emoji="🔐", style=ButtonStyle.gray)
    async def private_button_callback(self, button, interaction: Interaction):
        await interaction.response.defer()
        voicechannel = interaction.user.voice.channel
        overwrite = PermissionOverwrite()
        overwrite.connect = False
        await voicechannel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        embed = Embed(
            title=f"✅ Voice Channel wurde geschlossen")
        await interaction.followup.send(embed=embed, ephemeral=True)

    @ ui.button(emoji="🔓", style=ButtonStyle.gray)
    async def public_button_callback(self, button, interaction: Interaction):
        await interaction.response.defer()
        voicechannel = interaction.user.voice.channel
        overwrite = PermissionOverwrite()
        overwrite.connect = True
        await voicechannel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        embed = Embed(
            title=f"✅ Voice Channel wurde geöffnet")
        await interaction.followup.send(embed=embed, ephemeral=True)

    @ ui.button(emoji="👥", style=ButtonStyle.gray)
    async def limit_button_callback(self, button, interaction):
        await interaction.response.send_modal(LimitModal(title="Limit"))

    @ ui.button(emoji="📝", style=ButtonStyle.gray)
    async def edit_button_callback(self, button, interaction):
        await interaction.response.send_modal(EditModal(title="Umbenennen"))

    @ ui.button(emoji="🦶", style=ButtonStyle.gray)
    async def kick_button_callback(self, button, interaction: Interaction):
        embed = Embed(
            title=f'Member kicken',
            description='Wähle mindestens einen Member, welchen du aus dem Channel kicken möchtest.',
        )

        await interaction.channel.send(embed=embed, view=KickMemberView())

        # await interaction.response.send_modal(KickModal(title="Kick"))
        # @ui.select(
        #     placeholder="Wähle mind. einen User",
        #     min_values=1,
        #     max_values=len(user_count),
        #     options=[
        #         SelectOption(f"{i+1} user{'s' if i != 0 else ''} in VC", value=f"{i+1}") for i in range(user_count)
        #     ]
        # )
        # await ctx.send("Select the number of users in the voice channel:",
        #                components=[create_select(options=options, placeholder="Select a number", min_values=1, max_values=1)])


# Kick Dropdown
class KickMemberView(ui.View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=None)

    async def kickmembers(interaction: Interaction):
        # Get the voice channel the user is in
        voice_channel = interaction.user.voice.channel

        # Get all members in the voice channel
        members = voice_channel.members

        # Create the select dropdown with options for each member
        dropdown = SelectOption(
            placeholder="Wähle mind. einen Member aus",
            min_values=1,
            max_values=len(members),
            options=[
                SelectOption(
                    label=member.display_name,
                    value=str(member.id)
                ) for member in members
            ]
        )

        # Send the select dropdown to the user
        message = await interaction.channel.send("Kick members from voice channel:", view=dropdown)

        # Define a callback function for when the user clicks the "Kick" button
        async def callback(interaction):
            selected_members = [member for member in members if str(
                member.id) in interaction.values]
            for member in selected_members:
                await member.move_to(None)
            await interaction.response.edit_message(content="Selected members have been kicked from the voice channel.")

        # Add the callback function to the select dropdown
        dropdown.callback = callback


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

        await interaction.response.send_message(embed=embed, ephemeral=True)


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

        await interaction.response.send_message(embed=embed, ephemeral=True)


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

        await interaction.response.send_message(embed=embed, ephemeral=True)

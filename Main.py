import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# Load config from data.txt
def load_config():
    config = {}
    with open("data.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                config[k] = v.strip()
    return config

config = load_config()

bot_token = config.get("bot_token")
support_role_id = config.get("support_role_id")
support_role_id = int(support_role_id) if support_role_id and support_role_id.lower() != "none" else None

panel_channel_id = int(config["ticket_panel_channel_id"])
ticket_logs_channel_id = config.get("ticket_logs_channel_id")
ticket_logs_channel_id = int(ticket_logs_channel_id) if ticket_logs_channel_id and ticket_logs_channel_id.lower() != "none" else None

category_id = int(config["category_id"])
ticket_name_template = config["ticket_name"]
panel_message = config["panel_message"]
button_color = config.get("button_color", "gray").lower()

style_map = {
    "blurple": discord.ButtonStyle.blurple,
    "gray": discord.ButtonStyle.gray,
    "green": discord.ButtonStyle.green,
    "red": discord.ButtonStyle.red,
}
button_style = style_map.get(button_color, discord.ButtonStyle.gray)

# Load ticket options from config (up to 5)
ticket_options = []
for i in range(1, 6):
    label = config.get(f"option_{i}_label", "none")
    msg = config.get(f"option_{i}_message", "none")
    if label.lower() != "none":
        ticket_options.append({
            "label": label,
            "message": msg
        })

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        if support_role_id:
            support_role = interaction.guild.get_role(support_role_id)
            if not support_role or support_role not in member.roles:
                await interaction.response.send_message("❌ Only support staff can close tickets.", ephemeral=True)
                return

        await interaction.response.send_message("📦 Closing ticket and sending transcript...", ephemeral=True)

        messages = []
        async for msg in interaction.channel.history(limit=None, oldest_first=True):
            timestamp = msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
            content = msg.content.replace("\n", " ")
            messages.append(f"[{timestamp}] {msg.author}: {content}")

        transcript_text = "\n".join(messages)
        filename = f"transcript-{interaction.channel.id}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(transcript_text)

        if ticket_logs_channel_id:
            logs_channel = interaction.guild.get_channel(ticket_logs_channel_id)
            if logs_channel:
                await logs_channel.send(
                    content=f"📄 Transcript from {interaction.channel.name}",
                    file=discord.File(filename)
                )

        os.remove(filename)
        await interaction.channel.send("✅ Transcript sent to logs. Deleting channel in 5 seconds.")
        await asyncio.sleep(5)
        await interaction.channel.delete()

class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=opt["label"], value=str(idx))
            for idx, opt in enumerate(ticket_options)
        ]
        super().__init__(placeholder="Select a ticket reason...", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.guild
        category = discord.utils.get(guild.categories, id=category_id)

        # Prevent multiple tickets per user in the category
        for channel in guild.text_channels:
            if channel.category_id == category_id and channel.topic == str(user.id):
                await interaction.response.send_message("❌ You already have an open ticket.", ephemeral=True)
                return

        ticket_index = int(self.values[0])
        option = ticket_options[ticket_index]

        channel_name = ticket_name_template.replace("{username}", user.name.lower())

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        }
        if support_role_id:
            role = guild.get_role(support_role_id)
            if role:
                overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        ticket_channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites,
            topic=str(user.id)
        )

        # Use option message or default if "none"
        message = option["message"]
        if not message or message.lower() == "none":
            message = f"🎫 Hello {user.mention}, your ticket has been created."

        message = message.replace("{user}", user.mention)

        await ticket_channel.send(message, view=CloseTicketView())
        await interaction.response.send_message(f"✅ Ticket created: {ticket_channel.mention}", ephemeral=True)

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await tree.sync()
        print(f"🔧 Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

    panel_channel = bot.get_channel(panel_channel_id)
    if panel_channel:
        try:
            await panel_channel.purge(limit=100)
        except Exception as e:
            print(f"⚠️ Could not purge messages: {e}")
        await panel_channel.send(panel_message, view=TicketView())
    else:
        print("❌ Panel channel not found!")

@tree.command(name="close", description="Close the current ticket (support role only)")
async def close_command(interaction: discord.Interaction):
    member = interaction.user
    if support_role_id:
        support_role = interaction.guild.get_role(support_role_id)
        if not support_role or support_role not in member.roles:
            await interaction.response.send_message("❌ Only support staff can close tickets.", ephemeral=True)
            return
    await CloseTicketView().children[0].callback(interaction)

bot.run(bot_token)

# 🎟️ Ticket-Bot-Discord

A simple, easy-to-configure Ticket Bot for Discord servers.  
Quick setup. Clean design. Private and self-hosted.

---

## Project Structure

```
Ticket-bot/
├── Requirements.txt       # Python dependencies
├── Main.py                # Ticket Bot main code
├── data.txt               # Configuration data for the Ticket Bot
```

---

## Description

Ticket Bot is a straightforward private Discord bot designed to streamline the management of support tickets on your server.

---

## How to Configure It

Edit the `data.txt` file to customize your bot’s behavior.

### Required settings:

- `bot_token`: Your Discord bot token.
- `support_role_id`: The Discord Role ID for your support team. Only users with this role can close tickets.
- `ticket_panel_channel_id`: Channel ID where the ticket panel message with buttons will be posted.
- `ticket_logs_channel_id`: Channel ID where ticket transcripts will be sent. Set to `none` to disable.
- `category_id`: The category ID under which new tickets will be created.
- `ticket_name`: Template for naming ticket channels. Use `{username}` to insert the user's name.
- `panel_message`: Message shown above the ticket selection dropdown.
- `button_color`: Button color. Options: `green`, `blurple`, `red`, `gray`.

### Ticket Options (up to 5):

Each option requires:

- `option_X_label`: The label in the dropdown. Use `none` to disable.
- `option_X_message`: Message sent when the ticket is created. Use `{user}` to mention the creator.

**Example:**

```
option_1_label=Support
option_1_message=Hello {user}, how can we help you with support?

option_2_label=Report
option_2_message=Please describe what you're reporting, {user}.
```

Set unused options’ label/message to `none`.

---

## Usage

1. Install Python
   ```
   i dont know what os your running so you need to find it yourself python
   ```

2. Install dependencies:

    ```
    pip install -r Requirements.txt
    ```

3. Configure your settings in `data.txt`.

4. Run the bot:

    ```
    python Main.py
    ```

---

## Example `data.txt`

```
support_role_id=Your-Ticket-Role-Id
ticket_panel_channel_id=Your-Ticket-Channel
panel_message=🎫 Click below to open a support ticket.
button_color=green
ticket_name=ticket-{username}
category_id=Your-Tickets-Category
ticket_logs_channel_id=Your-Ticket-Logs-Channel-Id
bot_token=Your-Bot-Token

option_1_label=Support
option_1_message=Hello {user}, how can we help you with support?

option_2_label=Report
option_2_message=Please describe what you're reporting, {user}.

option_3_label=Partnership
option_3_message=Thank you for your interest in partnering, {user}! A Staff Member will be with you shortly.

option_4_label=Other
option_4_message=none

option_5_label=none
option_5_message=none
```

---

## Notes

- Make sure your bot has permission to create/manage channels, send messages, and manage embeds.
- Users cannot open multiple tickets simultaneously.
- Only users with the support role can close tickets.
- Ticket transcripts are saved and sent to your logs channel.
- Customize everything via `data.txt`.
- For the bot to work you need to setup The Required Settings

---


Thank you for using Ticket Bot! 🎟️

Made With ❤️ By Pontikaki34

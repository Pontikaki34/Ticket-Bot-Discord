# Ticket-Bot-Discord

**Your simple, easy-to-configure Ticket Bot for Discord**

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

Ticket-Bot-Discord is a straightforward, easy-to-use Discord bot designed to help you manage support tickets efficiently. The bot is highly customizable through a simple `data.txt` configuration file, so you can tailor it to your server’s needs without fuss.

---

## Usage

1. Install dependencies:

```bash
pip install -r Requirements.txt
```

2. Configure your bot settings in `data.txt`.

3. Run the bot:

```bash
python Main.py
```

---

## Configuration (`data.txt` example)

```txt
bot_token=YOUR_BOT_TOKEN
support_role_id=123456789012345678
ticket_panel_channel_id=123456789012345679
ticket_logs_channel_id=123456789012345680
category_id=123456789012345681
ticket_name=ticket-{username}
panel_message=🎟️ Please select a reason to open a ticket:
button_color=blurple

option_1_label=Support
option_1_message=Hello {user}, how can we help you with support?

option_2_label=Report
option_2_message=Please describe what you're reporting, {user}.

option_3_label=Partnership
option_3_message=Thank you for your interest in partnering, {user}!

option_4_label=Other
option_4_message=none

option_5_label=none
option_5_message=none
```

---

Feel free to ask if you want me to help with the actual bot code or anything else!

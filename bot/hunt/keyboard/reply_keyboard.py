from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

info_btn = KeyboardButton("🔎 Info")
cancel_btn = KeyboardButton("🚫 Cancel")
support_btn = KeyboardButton("🆘 Support")
map_btn = KeyboardButton("🗺️ Map")
create_team_btn = KeyboardButton("🤝🏻 Create team")
join_team_btn = KeyboardButton("🤝🏿 Join team")
score_btn = KeyboardButton("💯 Score")
team_info_btn = KeyboardButton("🔎 My Team")
leaderboard_btn = KeyboardButton("🏆 Scoreboard")
tasks_btn = KeyboardButton("✔ Tasks")
flag_btn = KeyboardButton("🤘 Flag")
casino_btn = KeyboardButton("🔞 Casino")


start_markup = (
    ReplyKeyboardMarkup(resize_keyboard=True)
    .add(join_team_btn)
    .row(info_btn, support_btn)
)

team_markup = (
    ReplyKeyboardMarkup(resize_keyboard=True)
    .row(team_info_btn, map_btn)
    .row(tasks_btn, flag_btn)
    .add(leaderboard_btn)
    .row(info_btn, support_btn)
)

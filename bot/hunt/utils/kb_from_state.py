from sqlalchemy.orm import Session

from hunt.db import get_db
from hunt.db.models import User
from hunt.keyboard.reply_keyboard import start_markup, team_markup, admin_markup


def kb_from_state(db: Session, chat_id):
    user = User.get(db, chat_id=chat_id)
    if user is None:
        return start_markup
    if user.role == "admin":
        return admin_markup
    if user.team_id is None:
        return start_markup
    return team_markup

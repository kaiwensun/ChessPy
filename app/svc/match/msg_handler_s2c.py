from flask_login import current_user

from app.svc.match.match_db import MatchDB
from app.svc.match import driver as match_driver


def handle_s2c():
    match = match_driver.get_match(current_user.user_id)
    message = match.receive_message_to(current_user.user_id)
    return message

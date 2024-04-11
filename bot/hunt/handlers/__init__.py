from hunt.handlers.admin import register_handlers_admin
from hunt.handlers.common import register_handlers_common
from hunt.handlers.task import register_handlers_task
from hunt.handlers.team import register_handlers_team
from hunt.handlers.test import register_handlers_test
from hunt.handlers.casino import register_handlers_casino
from hunt.handlers.quiz import register_handlers_quiz

__all__ = [
    "register_handlers_admin",
    "register_handlers_test",
    "register_handlers_team",
    "register_handlers_task",
    "register_handlers_common",
    "register_handlers_casino",
    "register_handlers_quiz",
]

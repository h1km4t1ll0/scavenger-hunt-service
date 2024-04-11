
# Usage:
* src/ for your tasks and photos
* results/ to store the results.xlsx and json
* hunt/ is the bot logic
* Makefile is the way to rule the bot
* PgAdmin - to rule the database

# Commands for admins:
## To join admin team:
* type /admin
* pass secret admin token
## Commands:
* /create_team (gives you a token)
* invite_tokens (to receive tokens for all teams)
* /add_task (adding a task with dialogue)
* /get_tasks
* /remove_task (Pass the name of the task to delete it)
* /get_teams
* /get_users
* /manager (choosing a task to become manager of)
* /build_results
* /mailing_all
* /mailing_team

# For users:
* One of the users
* /join_team
* /leave_team
* some other commands idc


# Known problems:
* If a team has a name with "_" symbols, it will be impossible to send messages to this team and give points as a manager. (give_money_from_solution_callback in admin.py has a parsing by _)
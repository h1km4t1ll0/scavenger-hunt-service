from sqlalchemy import select

from service.database import Database
from service.environment import environmental_variables


def get_leaderboard():
    database = Database(environmental_variables.DATABASE_URL)
    table = database.get_table('team')
    results = database.execute_query(
        select(
            table.columns.name,
            table.columns.amount
        )
    )

    return [{'team': row[0], 'points': row[1]} for row in results]

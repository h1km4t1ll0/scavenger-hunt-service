from sqlalchemy import select

from server.service.database import Database
from server.service.environment import env




def get_leaderboard():
    database = Database(env.DATABASE_URL)
    table = database.get_table('team')
    results = database.execute_query(
        select(
            table.columns.name,
            table.columns.amount
        )
    )

    return [{'team': row[0], 'points': row[1]} for row in results]

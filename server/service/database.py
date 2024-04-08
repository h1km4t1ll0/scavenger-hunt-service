from sqlalchemy import create_engine, MetaData, Table, Select


class Database:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.connection = self.engine.connect()

    def get_table(self, table_name: str):
        metadata = MetaData()
        return Table(
            table_name,
            metadata,
            autoload_with=self.engine
        )

    def execute_query(self, query: Select):
        return self.connection.execute(
            query
        ).fetchall()

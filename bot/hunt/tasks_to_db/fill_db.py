import json

import sqlalchemy.exc

from hunt.config import get_settings
from hunt.db.connection.session import get_db
from hunt.db.models import Task


def fill_database():
    with get_db() as db:
        # try:
        #     db.flush()
        # except PendingRollbackError:
        #     db.rollback()

        print("CREATING TASKS STARTED\n")
        print("CREATING ONLINE TASKS:")
        with open(get_settings().SRC_PREFIX + 'tasks/online_tasks.json', 'r') as online_tasks_file:
            online_tasks = json.loads(online_tasks_file.read())
            for task in online_tasks:
                try:
                    new_task = Task(**task)
                    db.add(new_task)
                    db.commit()
                    db.refresh(new_task)
                    print(f"Task with flag {new_task.flag} created")
                except sqlalchemy.exc.IntegrityError as e:
                    db.rollback()
                    print(f'Task with flag {task["flag"]} already exists, skipped')
        db.close()
        print()

        print("CREATING OFFLINE TASKS:")
        with open(get_settings().SRC_PREFIX + 'tasks/offline_tasks.json', 'r') as offline_tasks_file:
            offline_tasks = json.loads(offline_tasks_file.read())
            for task in offline_tasks:
                try:
                    new_task = Task(**task)
                    db.add(new_task)
                    db.commit()
                    db.refresh(new_task)
                    print(f"Task with flag {new_task.flag} created")
                except sqlalchemy.exc.IntegrityError as e:
                    db.rollback()
                    print(f'Task with flag {task["flag"]} already exists, skipped')
        db.close()
        print()

        print("CREATING COSPLAY TASKS:")
        with open(get_settings().SRC_PREFIX + 'tasks/cosplay_tasks.json', 'r') as offline_tasks_file:
            offline_tasks = json.loads(offline_tasks_file.read())
            for task in offline_tasks:
                try:
                    new_task = Task(**task)
                    db.add(new_task)
                    db.commit()
                    db.refresh(new_task)
                    print(f"Task with flag {new_task.flag} created")
                except sqlalchemy.exc.IntegrityError as e:
                    db.rollback()
                    print(f'Task with flag {task["flag"]} already exists, skipped')
        db.close()
        print()

        print("CREATING SECRET TASKS:")
        with open(get_settings().SRC_PREFIX + 'tasks/secret_tasks.json', 'r') as offline_tasks_file:
            offline_tasks = json.loads(offline_tasks_file.read())
            for task in offline_tasks:
                try:
                    new_task = Task(**task)
                    db.add(new_task)
                    db.commit()
                    db.refresh(new_task)
                    print(f"Task with flag {new_task.flag} created")
                except sqlalchemy.exc.IntegrityError as e:
                    db.rollback()
                    print(f'Task with flag {task["flag"]} already exists, skipped')
        db.close()
        print()

        print("CREATING SONG SUMMARIZATION TASKS:")
        with open(get_settings().SRC_PREFIX + 'tasks/songs_tasks.json', 'r') as offline_tasks_file:
            offline_tasks = json.loads(offline_tasks_file.read())
            for task in offline_tasks:
                try:
                    new_task = Task(**task)
                    db.add(new_task)
                    db.commit()
                    db.refresh(new_task)
                    print(f"Task with flag {new_task.flag} created")
                except sqlalchemy.exc.IntegrityError as e:
                    db.rollback()
                    print(f'Task with flag {task["flag"]} already exists, skipped')
        db.close()
        print()

        print("CREATING RHYMES TASKS:")
        with open(get_settings().SRC_PREFIX + 'tasks/rhymes_tasks.json', 'r') as offline_tasks_file:
            offline_tasks = json.loads(offline_tasks_file.read())
            for task in offline_tasks:
                try:
                    new_task = Task(**task)
                    db.add(new_task)
                    db.commit()
                    db.refresh(new_task)
                    print(f"Task with flag {new_task.flag} created")
                except sqlalchemy.exc.IntegrityError as e:
                    db.rollback()
                    print(f'Task with flag {task["flag"]} already exists, skipped')
        db.close()
        print()


if __name__ == "__main__":
    fill_database()

import json
from datetime import datetime
from typing import List

from hunt.config import get_settings
from hunt.db.connection.session import get_db
from hunt.db.models import Results, Team, Task, SolvedQuiz
import pandas as pd


def build_results():
    results = []
    with get_db() as db:
        cur_result = {}
        tasks: List[Task] = db.query(Task).all()
        teams: List[Team] = db.query(Team).all()
        for team in teams:
            cur_result['Team'] = team.name
            cur_result['Score'] = team.amount
            for task in tasks:
                db_res: Results = db.query(Results).filter_by(team_id=team.id, task_id=task.id).first()
                if db_res is None:
                    amount = 0
                else:
                    amount = db_res.amount
                    print()
                if task.type == 'offline' or task.type == 'online':
                    cur_result[task.name] = amount
                elif task.type == 'cosplay':
                    cur_result['Cosplay'] = cur_result.get("Cosplay", 0) + amount
                elif task.type == 'secret':
                    cur_result['Secret'] = cur_result.get("Secret", 0) + amount
                elif task.type == 'song summarization':
                    cur_result['Song summarization'] = cur_result.get("song summarization", 0) + amount
                elif task.type == 'rhymes':
                    cur_result['Rhymes'] = cur_result.get("rhymes", 0) + amount
            # cur_result["Quiz"] = SolvedQuiz.query(team_id=team.id)['points']
            results.append(cur_result)
            cur_result = {}
    results.sort(key=lambda x: x['Score'], reverse=True)
    res_name = str(datetime.now().strftime("Results %H-%M %d.%m"))
    with open(f"./results/{res_name}.json", "w") as f:
        f.write(json.dumps(results))

    df = pd.read_json(f"./results/{res_name}.json")
    df.to_excel(f"./results/{res_name}.xlsx", "w")
    return res_name


if __name__ == "__main__":
    build_results()

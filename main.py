from datetime import datetime, timedelta
import os

def main():
    today = datetime.today()
    past_year = today - timedelta(days=365)
    days_until_sunday = 6 - past_year.weekday()
    if days_until_sunday == 0:
        days_until_sunday = 7

    start_date = past_year + timedelta(days=days_until_sunday)
    today_formatted = today.strftime('%b.%d.').upper()

    create_repo(build_matrix(today_formatted, load_chars()), start_date)

def get_date(begin_date: datetime, i: int, j: int) -> datetime:
    return begin_date + timedelta(days=j * 7 + i)

def load_chars() -> dict[str, list[list[bool]]]:
    result: dict[str, list[list[bool]]] = dict()
    with open('chars.txt', 'rt', encoding='utf-8') as f:
        order = f.readline().strip()
        order_index = -1
        for _ in range(5):
            lines = []
            for _ in range(7):
                lines.append(f.readline().strip())
            for i in range(len(lines[0])):
                if i % 5 == 0:
                    order_index += 1
                    if order_index == len(order):
                        break
                    result[order[order_index]] = [ [] for _ in range(7) ]
                for j in range(7):
                    result[order[order_index]][j].append(bool(int(lines[j][i])))
    return result

def build_matrix(text: str, char_table: dict[str, list[list[bool]]]):
    matrix = [ [ False for _ in range(51) ] for _ in range(7) ]
    offset = (51 - (len(text) * 5 + len(text) - 1)) // 2
    for i in text:
        for j in range(7):
            for k in range(5):
                matrix[j][k + offset] = char_table[i][j][k]
        offset += 6
    return matrix

def create_repo(matrix: dict[str, list[list[bool]]], start_date: datetime):
    if os.path.exists('.git'):
        if os.name == 'nt':
            os.system('rd /s /q .git')
        else:
            os.system('rm -rf .git')
    os.system('git init')
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j]:
                date = get_date(start_date, i, j)
                for _ in range(15):
                    os.system(f'git commit --date={date.isoformat()} --allow-empty --allow-empty-message -m \"\"')

    os.system('gh repo delete ... --yes')
    os.system('gh repo create ... --private --push --source=.')

main()
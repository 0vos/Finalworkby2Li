import json

def load_data_from_json(path, data_name):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        stuff = data.get(data_name)
        if not stuff:
            raise ValueError(f"JSON 文件中不包含 '{data_name}' 字段")
        return stuff

def save_maze_result_2(filename, maze, max_resource, optimal_path):
    result = {
        "maze": maze,
        "max_resource": max_resource,
        "optimal_path": [[x, y] for x, y in optimal_path]
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

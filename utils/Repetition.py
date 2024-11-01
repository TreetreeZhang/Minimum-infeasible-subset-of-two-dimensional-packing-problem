import json
import os
from FeasibilityCheck import *

def json_read(json_path):
    '''
    :param json_path:json数据的路径
    :return:
    machines_count：机器的数量,
    machines_info:[(id, L, W)],
    parts_info:[(id,[(L, W, H)])],
    bins_info:{id:[L, W]}
    '''
    with open(json_path, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error in {json_path}: {e}")
            return None

    # 读取 machines 字段的数量
    machines_count = len(data.get('machines', []))

    # 获取每个 machine_id 对应的 L 和 W
    machines_info = []
    for machine in data.get('machines', []):
        machine_id = machine.get('machine_id')
        L = machine.get('L')
        W = machine.get('W')
        machines_info.append((machine_id, L, W))

    # 获取 parts 字段中的每个 part_id，并根据 num_part 重复每个零件的 l、w 和 h，且对重复的 part_id 进行重新命名
    parts_info = []
    part_id_counts = {}
    bins_info = {}
    for part in data.get('parts', []):
        part_id = part.get('part_id')
        num_part = part.get('num_part')
        orientations = part.get('orientations', [])
        lwh_triplets = [(orientation.get('l'), orientation.get('w'), orientation.get('h')) for orientation in
                        orientations]

        if part_id not in part_id_counts:
            part_id_counts[part_id] = 0

        for i in range(num_part):
            part_id_counts[part_id] += 1
            unique_part_id = f"{part_id}-{part_id_counts[part_id]}"
            parts_info.append((unique_part_id, lwh_triplets))
            if orientations:
                bins_info[unique_part_id] = (orientations[0].get('l'), orientations[0].get('w'))

    return machines_count, machines_info, bins_info



def Check_grid_Feasibility(input_folder, grid_size=1):
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.json'):
            input_json_path = os.path.join(input_folder, file_name)
            result = json_read(input_json_path)
            if result is None:
                raise ValueError(f"文件{file_name}.json读取为空")
                continue
            machines_count, machines_info, bins_info = result
            #print(f"文件 {file_name} 读取成功，机器数量: {machines_count}, 零件数量: {len(bins_info)}")
            for machine in machines_info:
                L = machine[1]
                W = machine[2]

            bins = []
            for value in bins_info.values():
                bins.append(value)












if __name__ == '__main__':
    input_folder = '../TestInstances/json'
    json_test = '../TestInstances/json/ht1_1.json'
    a,b,c = json_read(json_test)
    print(a)
    print(b)
    print(c)
    Check_grid_Feasibility(input_folder)


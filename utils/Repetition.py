import json
import os
import itertools
from FeasibilityCheck import *

def json_read(json_path):
    '''
    :param json_path: json数据的路径
    :return:
    machines_count：机器的数量,
    machines_info:[(id, L, W)],
    parts_info:[(id,[(L, W, H)])],
    bins_info:{id:[L, W]}
    '''
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error in {json_path}: {e}")
        return None

    # 读取 machines 字段的数量
    machines_count = len(data.get('machines', []))

    # 获取每个 machine_id 对应的 L 和 W
    machines_info = [(machine.get('machine_id'), machine.get('L'), machine.get('W')) for machine in data.get('machines', [])]

    # 获取 parts 字段中的每个 part_id，并根据 num_part 重复每个零件的 l、w 和 h，且对重复的 part_id 进行重新命名
    part_id_counts = {}
    bins_info = {}
    for part in data.get('parts', []):
        part_id = part.get('part_id')
        num_part = part.get('num_part')
        orientations = part.get('orientations', [])
        lwh_triplets = [(orientation.get('l'), orientation.get('w'), orientation.get('h')) for orientation in orientations]

        if part_id not in part_id_counts:
            part_id_counts[part_id] = 0

        for i in range(num_part):
            part_id_counts[part_id] += 1
            unique_part_id = f"{part_id}-{part_id_counts[part_id]}"
            if orientations:
                bins_info[unique_part_id] = (orientations[0].get('l'), orientations[0].get('w'))

    return machines_count, machines_info, bins_info

def Check_grid_Feasibility(input_folder):
    resolution = [5, 2, 1, 0.5]
    for grid_size in resolution:

        for file_name in os.listdir(input_folder):
            print(file_name)
            if file_name.endswith('.json'):
                input_json_path = os.path.join(input_folder, file_name)
                result = json_read(input_json_path)

                if result is None:
                    print(f"文件{file_name}.json读取为空")
                    continue
                machines_count, machines_info, bins_info = result

                for machine in machines_info:
                    L = machine[1]
                    W = machine[2]

                    # 设置保存路径并清空原有内容
                    output_folder = f'../output/repetition/{file_name.split('.')[0]}/{machine[0]}/{grid_size}'
                    # if not os.path.exists(output_folder):
                    #     os.makedirs(output_folder)
                    # 清空原有内容因为写入txt时为a模式
                    if os.path.exists(output_folder):
                        for file in os.listdir(output_folder):
                            os.remove(os.path.join(output_folder, file))
                    else:
                        os.makedirs(output_folder)

                    # 获取所有可能的组合
                    for i in range(2, len(bins_info) + 1):
                        for combination in itertools.combinations(bins_info.keys(), i):
                            bins = [bins_info[key] for key in combination]
                            check_feasi(L, W, grid_size, bins, output_folder)

if __name__ == '__main__':
    input_folder = '../TestInstances/json'
    json_test = '../TestInstances/json/ht1_1.json'
    a, b, c = json_read(json_test)
    # print(a)
    # print(b)
    # print(c)
    Check_grid_Feasibility(input_folder)

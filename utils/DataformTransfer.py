import json
import os

def convert_txt_to_json(input_txt_path, output_json_path):
    # 读取输入文件内容
    with open(input_txt_path, 'r') as file:
        lines = file.readlines()

    # 移除空行或仅包含换行符的行
    lines = [line.strip() for line in lines if line.strip()]

    # 解析数据
    data = {
        "machines": [],
        "parts": []
    }

    line_index = 0

    # 获取 types_machine 和 types_parts
    if line_index >= len(lines):
        raise ValueError("输入文件格式错误：缺少 types_machine 和 types_parts 数据。")

    types_machine, types_parts = map(int, lines[line_index].split())
    line_index += 1
    data["types_machine"] = types_machine
    data["types_parts"] = types_parts

    # 获取 num_machine 和 num_parts
    if line_index >= len(lines):
        raise ValueError("输入文件格式错误：缺少 num_machine 和 num_parts 数据。")

    num_machine, num_parts = map(int, lines[line_index].split())
    line_index += 1
    data["num_machine"] = num_machine
    data["num_parts"] = num_parts

    # 获取 machine 数据
    for machine_index in range(types_machine):
        if line_index >= len(lines):
            raise ValueError(
                f"输入文件格式错误：缺少机器数据（machine 数据），当前行索引：{line_index}, 当前机器序号：{machine_index + 1}")

        parts = lines[line_index].split()
        if len(parts) < 8:
            raise ValueError(f"输入文件格式错误：机器数据行格式错误，行索引：{line_index}, 行内容：{lines[line_index]}")

        machine_id = int(parts[0])
        num_machine = int(parts[1])
        V, U, S, L, W, H = map(float, parts[2:])
        machine = {
            "machine_id": machine_id,
            "num_machine": num_machine,
            "V": V,
            "U": U,
            "S": S,
            "L": L,
            "W": W,
            "H": H
        }
        data["machines"].append(machine)
        line_index += 1

    # 获取 part 数据
    for part_index in range(types_parts):
        if line_index >= len(lines):
            raise ValueError(
                f"输入文件格式错误：缺少零件数据（part 数据），当前行索引：{line_index}, 当前零件序号：{part_index + 1}")

        parts = lines[line_index].split()
        if len(parts) < 4:
            raise ValueError(f"输入文件格式错误：零件数据行格式错误，行索引：{line_index}, 行内容：{lines[line_index]}")

        part_id = int(parts[0])
        num_part = int(parts[1])
        num_orientation = int(parts[2])
        volume = float(parts[3])
        orientations = []
        line_index += 1

        for orientation_index in range(num_orientation):
            if line_index >= len(lines):
                raise ValueError(
                    f"输入文件格式错误：缺少 orientation 数据，当前行索引：{line_index}, 当前零件序号：{part_index + 1}, 当前 orientation 序号：{orientation_index + 1}")

            orientation_data = list(map(float, lines[line_index].split()))
            if len(orientation_data) < 4:
                raise ValueError(
                    f"输入文件格式错误：orientation 数据行格式错误，行索引：{line_index}, 行内容：{lines[line_index]}")

            orientations.append({
                "l": orientation_data[0],
                "w": orientation_data[1],
                "h": orientation_data[2],
                "support": orientation_data[3]
            })
            line_index += 1

        part = {
            "part_id": part_id,
            "num_part": num_part,
            "num_orientation": num_orientation,
            "volume": volume,
            "orientations": orientations
        }
        data["parts"].append(part)

    # 转换为 JSON 格式
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    # 将 JSON 数据写入文件
    with open(output_json_path, 'w') as json_file:
        json_file.write(json_data)

    print(f"转换完成，JSON 数据已保存为 {output_json_path}")

def convert_all_txt_in_folder(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有 txt 文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_txt_path = os.path.join(input_folder, filename)
            output_json_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.json")

            try:
                convert_txt_to_json(input_txt_path, output_json_path)
            except ValueError as e:
                print(f"处理文件 {filename} 时出错：{e}")

# 使用示例
convert_all_txt_in_folder('../TestInstances/txt', '../TestInstances/json')

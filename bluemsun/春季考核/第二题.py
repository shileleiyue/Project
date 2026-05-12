# 第二题：处理学生文件，计算平均分，写入新文件


def process_students(input_file: str, output_file: str):
    """
    读取学生文件，计算平均分，将结果写入输出文件
    :param input_file: 输入文件名（students.txt）
    :param output_file: 输出文件名（summary.txt）
    """
    students = []      # 存放学生字典的列表
    total_score = 0    # 总分

    try:
        # 1. 读取文件，每行转换为字典
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:          # 跳过空行
                    continue
                parts = line.split('，')
                if len(parts) != 3:
                    print(f"警告：格式错误行已跳过 -> {line}")
                    continue
                name, age_str, score_str = parts
                try:
                    age = int(age_str)
                    score = float(score_str)
                except ValueError:
                    print(f"警告：年龄或分数非数字，跳过 -> {line}")
                    continue
                student = {"name": name, "age": age, "score": score}
                students.append(student)
                total_score += score

        if not students:
            raise RuntimeError("没有有效的学生数据")

        average_score = total_score / len(students)

        # 2. 写入 summary.txt
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"平均分：{average_score:.2f}\n")
            f.write("学生信息：\n")
            for stu in students:
                f.write(f"姓名：{stu['name']}，年龄：{stu['age']}，分数：{stu['score']}\n")

        print(f"处理完成！共 {len(students)} 名学生，平均分 {average_score:.2f}，结果已写入 {output_file}")

    except FileNotFoundError:
        print(f"错误：文件 {input_file} 不存在，请检查文件路径")
    except PermissionError:
        print(f"错误：没有权限读取 {input_file} 或写入 {output_file}")
    except Exception as e:
        print(f"发生未知错误：{e}")

if __name__ == "__main__":
    process_students("students.txt", "summary.txt")

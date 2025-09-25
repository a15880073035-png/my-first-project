"""
封装JSON文件操作（读写/校验/转换）

"""
import json
import os
from datetime import datetime
import jsonpath
#读取json 文件

class JsonHandler:

    def read_json(file_path:str)->dict:
        # 1. 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            # 2. 解析JSON
            data = json.load(f)
        return data

    def validate_json(file_path:str)->bool:
        """验证文件是否为有效json"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            return True
        except(json.JSONDecodeError,FileNotFoundError):
            return False

    def write_json(output_file_path:str,new_json):
        with open(output_file_path, "w", encoding="utf-8") as f:
            json.dump(new_json, f, ensure_ascii=False, indent=4)  # ensure_ascii=False 支持中文




# 使用示例
if __name__ == "__main__":
    # 读取
    data = JsonHandler.read_json("D:/Downloads/在场景中唱歌（情感抒发型） (8).json")
    # new_list = jsonpath.jsonpath(data, "$..aimv_script")   #返回值是个list
    # new_json = json.dumps(new_list,indent=4)
    # 1. 定义目标目录（相对路径）
    target_dir = "../data/output/"  # 当前项目下的 data/output 目录
    # 2. 创建目录（如果不存在）
    os.makedirs(target_dir, exist_ok=True)  # exist_ok=True 避免目录已存在时报错

    #3、取出脚本中的数据，生成带时间戳的文件名
    new_json = data["json"][0]["aimv_script"]
    file_name = new_json["title"]

    # 获取当前日期和时间（格式：YYYY-MM-DD_HH-MM-SS）
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_file_name = file_name+"_"+current_time+".json"

    # 4. 拼接完整文件路径
    output_file_path = os.path.join(target_dir, new_file_name)  # 跨平台兼容路径拼接

    #写入json
    with open(output_file_path,"w",encoding="utf-8") as f:
        json.dump(new_json, f , ensure_ascii=False, indent=4) # ensure_ascii=False 支持中文

    print(f"文件已保存到：{os.path.abspath(output_file_path)}")

    # 校验
    print(JsonHandler.validate_json("F:/test_data/在场景中唱歌（情感抒发型） (1).json"))  # False
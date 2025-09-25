"""
#common/BaseExcel
封装对excel的操作
读取excle数据
pandas 依赖一些其他库，如果不下载，会报错，需要多下载 fsspec，openpyxl 这两个库
"""

import pandas as pd


class BaseExcel:

    def read_excel(file_path,sheet_name):
        # 读取 Excel 文件
        df = pd.read_excel(file_path, sheet_name)

        # 转换为list格式，然后作为用例循环导入
        excel_list = df.to_dict(orient='records')
        return excel_list



# 使用示例
if __name__ == "__main__":
    file_path = "F://0507check.xlsx"
    sheet_name = "Sheet1"
    data_list = BaseExcel.read_excel(file_path=file_path,sheet_name=sheet_name)
    for data in data_list:
        print(data["歌曲"])
    # 校验
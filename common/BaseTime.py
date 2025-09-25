"""
这里是提供时间转换的方法
这里统一描述时间相关的方法，比如时间转换，时间段判重等
"""
from typing import List,Dict
import re
from datetime import timedelta,datetime
class BaseTime:
    """将时间字符串（格式为HH:MM:SS.ss）转换为秒数"""
    def change_to_seconds(self,time_str):
        # minutes, seconds = time_str.split(':')  这个无法识别HH:MM:SS的情况
        parts = time_str.split(':')
        # 处理秒和小数部分
        seconds = float(parts[-1])
        # 根据冒号数量判断格式
        if len(parts) == 3:  # HH:MM:SS.SS 格式
            hours = int(parts[0])
            minutes = int(parts[1])
            return hours * 3600 + minutes * 60 + seconds
        elif len(parts) == 2:  # MM:SS.ss 格式
            minutes = int(parts[0])
            return minutes * 60 + seconds
        else:
            raise ValueError(f"无效的时间格式: {time_str}")


    """将 MM:SS.ss 时间字符串转换为秒数（float）,这个是不支持有HH的情况"""
    def time_str_to_seconds(self, time_str: str) -> float:
        count = time_str.count(":")
        if count == 1:
            mm, ss = time_str.split(":")
            second = int(mm) * 60 + float(ss)
        elif count == 2:
            hh, mm, ss = time_str.split(":")
            second = int(hh) * 3600 + int(mm) * 60 + float(ss)
        return second

    """检查时间区间是否有重叠"""
    def check_time_overlap(self,segments : List[Dict])->bool:
        intervals = []
        for seg in segments:
            time = self.time_str_to_seconds(seg["time"])
            end_time = self.time_str_to_seconds(seg["end_time"])
            intervals.append((time,end_time))
        # 按开始时间排序
        intervals.sort()
        #检查是否有重叠
        for i  in range(1,len(intervals)):
            prev_end = intervals[i-1][1]
            curr_start = intervals[i][0]
            if curr_start<prev_end:
                print(f"⚠️ 时间区间重叠：{intervals[i - 1]} 和 {intervals[i]}")
                return True
        return False

    """检查时间字符串是否符合 MM:SS.ss 格式"""

    def is_valid_time_format(self, time_str: str) -> bool:
        pattern = r'^\d{2}:\d{2}\.\d{2}$'
        if not re.fullmatch(pattern, time_str):
            return False
        print(re.fullmatch(pattern, time_str))
        mm, ss = time_str.split(":")[0:2]
        ss = float(ss.split(".")[0])
        return int(mm) >= 0 and 0 <= float(ss) < 60

    def parse_time(self,time_str):
        """将 mm:ss.sss 格式的时间字符串转换为 timedelta 对象"""
        minutes, rest = time_str.split(':')
        seconds = rest.split('.')[0]
        milliseconds = rest.split('.')[1] if '.' in rest else '0'

        return timedelta(
            minutes=int(minutes),
            seconds=int(seconds),
            milliseconds=int(milliseconds)
        )
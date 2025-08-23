# 何限が何時から始まって何時終了なのか判定する、時間に多少余裕を持たせています

from datetime import datetime, time, date

def JudgePeriod():
    now_time = datetime.now()
    day_of_week = date(now_time.year, now_time.month, now_time.day).weekday()
    tmp_list = [0, 1, 2, 3, 4]
    if day_of_week in tmp_list:
        now_time = now_time.time()
        period_list = [
            [time(9, 20), time(11, 0)],
            [time(11, 0), time(12, 40)],
            [time(13, 30), time(15, 10)],
            [time(15, 10), time(16, 50)],
        ]
        for i in range(0, 4):
            start = period_list[i][0]
            end = period_list[i][1]
            if start <= now_time and now_time <= end:
                return (day_of_week, i)
    
    return None
                
    
if __name__ == '__main__':
    JudgePeriod()
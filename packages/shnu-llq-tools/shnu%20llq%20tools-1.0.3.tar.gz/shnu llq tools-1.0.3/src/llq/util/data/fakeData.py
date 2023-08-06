import numpy as np
import pandas as pd

def create_name(name='姓名', rows=40):
    xing = '赵钱孙李周吴郑王冯陈褚蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏窦章苏潘葛奚范彭郎鲁韦昌马苗方俞任袁柳'
    ming = "群平风华正茂仁义礼智媛强天霸红和丽平世莉界中华正义伟岸茂盛繁圆一懿贵妃彭习嬴政不韦近荣群智慧睿兴平风清扬自成世民嬴旺品网红丽文天学与翔斌霸学花文教学忠谋书"
    x = np.random.choice(list(xing), (rows, 1))
    m = np.random.choice(list(ming), (rows, 2))
    nm = np.hstack((x, m))
    df = pd.DataFrame(nm)
    dff = pd.DataFrame()
    df[2] = df[2].apply(lambda x: ('', x)[np.random.randint(0, 2)])
    dff[name] = df[0] + df[1] + df[2]

    return dff[name]


def create_columns(column_list, value_list, rows=40):
    size = (rows, len(column_list))
    if type(value_list[0]) == int and len(value_list) == 2:
        return pd.DataFrame(np.random.randint(*value_list, size=size), columns=column_list)
    else:
        return pd.DataFrame(np.random.choice(value_list, size=size), columns=column_list)




def generate(rows=40):
    return pd.concat([
        create_name('姓名', rows),
        create_columns(['性别'], ['男', '女'], rows),
        create_columns(['学校'], ['清华大学', '北京大学', '复旦大学', '上海师大', '上海交大'], rows),
        create_columns(['班级'], ['计算机科学与技术', '人工智能', '数据科学'], rows),
        create_columns(['英语', '政治','线代', '概率'], [20, 100], rows),
        create_columns(['高数', '专业课', '表达能力','面试'], [30, 150], rows)],
        axis=1)


if __name__ == '__main__':
    print(generate(100))

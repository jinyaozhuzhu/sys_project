# -*- coding: utf-8 -*-
"""
对矩阵的计算以及聚类
"""
from sys_project.func import reachable_matrix

course_name_num = dict()
course_name_num['管理学'] = 1
course_name_num['信息技术基础'] = 2
course_name_num['经济学'] = 3
course_name_num['高级语言程序设计'] = 4
course_name_num['数据结构'] = 5
course_name_num['计算机网络'] = 6
course_name_num['信息管理学'] = 7
course_name_num['数据库系统原理'] = 8
course_name_num['管理运筹学'] = 9
course_name_num['管理信息系统'] = 10
course_name_num['面向对象程序设计'] = 11
course_name_num['信息系统项目管理'] = 12
course_name_num['信息系统分析与设计'] = 13
course_name_num['数据挖掘技术'] = 14
course_name_num['管理统计学'] = 15
course_name_num['信息系统测试与维护'] = 16
course_name_num['信息分析与预测'] = 17
course_name_num['生产与运作管理'] = 18
course_name_num['系统工程'] = 19

import networkx as nx

course_di_net = nx.MultiDiGraph()
"""
有向图构建邻接矩阵
"""
course_di_net.add_edge(1, 3)
course_di_net.add_edge(1, 7)
course_di_net.add_edge(2, 4)
course_di_net.add_edge(2, 6)
course_di_net.add_edge(2, 8)
course_di_net.add_edge(4, 5)
course_di_net.add_edge(5, 10)
course_di_net.add_edge(5, 11)
course_di_net.add_edge(6, 10)
course_di_net.add_edge(7, 17)
course_di_net.add_edge(8, 10)
course_di_net.add_edge(9, 18)
course_di_net.add_edge(10, 13)
course_di_net.add_edge(10, 12)
course_di_net.add_edge(11, 13)
course_di_net.add_edge(11, 14)
course_di_net.add_edge(13, 16)
course_di_net.add_edge(14, 17)
course_di_net.add_edge(15, 14)
course_di_net.add_node(19)

# 邻接矩阵
neighbor_matrix = nx.to_numpy_matrix(course_di_net)
index_columns = [i for i in range(1, 20)]
import pandas as pd

df_neighbor = pd.DataFrame(neighbor_matrix, index=index_columns, columns=index_columns)
df_neighbor.to_csv("/Users/jinyao/Desktop/neighbor_matrix.csv", sep=",", float_format='%d')

# 可达矩阵 并生成可达矩阵文件 reachable_matrix.csv
reachable_ma = reachable_matrix(neighbor_matrix)
df_reachable = pd.DataFrame(reachable_ma,
                            index=index_columns, columns=index_columns)
df_reachable.to_csv("/Users/jinyao/Desktop/reachable_matrix.csv", sep=",", float_format='%d')

"""
无向图用于聚类
"""
course_net = nx.Graph()
import community

course_net.add_edge(1, 3)
course_net.add_edge(1, 7)
course_net.add_edge(2, 4)
course_net.add_edge(2, 6)
course_net.add_edge(2, 8)
course_net.add_edge(4, 5)
course_net.add_edge(5, 10)
course_net.add_edge(5, 11)
course_net.add_edge(6, 10)
course_net.add_edge(7, 17)
course_net.add_edge(8, 10)
course_net.add_edge(9, 18)
course_net.add_edge(10, 13)
course_net.add_edge(10, 12)
course_net.add_edge(11, 13)
course_net.add_edge(11, 14)
course_net.add_edge(13, 16)
course_net.add_edge(14, 17)
course_net.add_edge(15, 14)
course_net.add_node(19)

# 聚类 并获取每一类别的课程名称
classification = community.best_partition(course_net)
classification_num_name = dict()
for key, val in classification.items():
    if val not in classification_num_name.keys():
        values = list()
        values.append(key)
        classification_num_name[val] = values
    else:
        values = classification_num_name.get(val)
        values.append(key)

course_num_name = {num: course for course, num in course_name_num.items()}
classification_course_name = list()  # 存放最终的信息
for k1, v1 in classification_num_name.items():
    new_v1 = [course_num_name.get(v11) for v11 in v1]
    new_v1_str = ' '.join(new_v1)
    l = [k1, new_v1_str, len(new_v1)]
    classification_course_name.append(l)
classification_df = pd.DataFrame(classification_course_name,
                                 columns=['类别', '课程名', '数量'])
classification_df.to_csv('/Users/jinyao/Desktop/classification.csv',
                         index=False, encoding='UTF-8', sep=",", float_format='%d')

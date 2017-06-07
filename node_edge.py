# -*- coding: utf-8 -*-


"""
生成节点文件以及边文件
"""
import networkx as nx
import pandas as pd

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

# 生成节点文件 nodes.csv
course_num_name = {num: course for course, num in course_name_num.items()}  # 转换数字->课程名
id_label = [[num, course_name] for course_name, num in course_name_num.items()]
df_id_label = pd.DataFrame(id_label, columns=['id', 'label'])
df_id_label.to_csv('/Users/jinyao/Desktop/nodes.csv', sep=',', float_format='%d', index=False,
                   encoding='UTF-8')

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

# 生成边文件 edges.csv
source_target = pd.DataFrame(course_di_net.edges(), columns=['source', 'target']
                             ).sort_values(by='source')
source_target.to_csv('/Users/jinyao/Desktop/edges.csv', sep=',', float_format='%d',
                     index=False, encoding='UTF-8')

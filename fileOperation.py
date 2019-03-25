# -*-coding:utf-8-*-
import cx_Oracle
import pymysql
import  pymysql.cursors

def read_network_policy(table_name):
    # 从数据库中获取当前存在的策略
    conn = cx_Oracle.connect('SYSTEM', 'cmtk1234', 'localhost:1521/xe')
    cursor = conn.cursor()
    sql = "select * from "+table_name
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return rows

def read_network_policy1(table_name):
    # 从数据库中获取当前存在的策略
    conn = pymysql.connect(host='localhost', port=3306, user='root',passwd='root',db='network_control')
    cursor = conn.cursor()
    sql = "select * from "+table_name
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return rows


def split_policy_str(str_policy):
    if str_policy == None:
        return 0
    else:
        sps = str_policy.split(",")
        policy_type_id = 0
        if sps[0] == '1':
            policy_type_id = 1
        elif sps[0] == '2':
            policy_type_id = 2
        elif sps[0] == '3':
            policy_type_id = 3
        else:
            print("无该类型的策略")
        # print(policy_type_id)
        return policy_type_id

def select_policy_table(table_name,src,dst):
    conn = cx_Oracle.connect('SYSTEM', 'cmtk1234', 'localhost:1521/xe')
    cursor = conn.cursor()
    sql = "select * from " + table_name +" where nw_src=\'{}\' and nw_dst=\'{}\' " .format(src,dst)
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return rows
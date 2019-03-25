# -*-coding:utf-8-*-

from fileOperation import *
import operator

class PolicyConflict(object):

    def __init__(self):
        # 获取 set_field策略的源和目的地址的集合
        #self.SRC_TUPLE, self.DST_TUPLE = self.read_policy_translate()
        pass

    def single_policy_conflict(self,new_policy):
        """
           先判断新策略与当前策略是否存在直接冲突
        :param new_policy:
        :return:
        """
        flag = 0
        print("判断是否与某一条直接策略冲突")
        # 若下发的策略为安全或普通策略时
        if new_policy['policy_type_id'] == 1 or new_policy['policy_type_id'] == 3:
            rows = select_policy_table('comm_policys', new_policy['src'], new_policy['dst'])
            if len(rows) == 0 :
                print("当前系统不存在与之相同条件的策略，不冲突")
                flag = 0
            else:
                for row in rows:
                    exist_policy = self.list_trans_policys(row)
                    if exist_policy['action'] == 'drop' and new_policy['action'] == 'forward':
                        print('该策略与现存策略冲突')
                        flag=1
                    elif exist_policy['action'] == 'forward' and new_policy['action'] == 'drop':
                        print('该策略与现存策略冲突')
                        flag = 1
                    else:
                        print("不存在单独冲突的情况")
        elif new_policy['policy_type_id'] == 2:
            # self.combined_policy_conflict(new_policy)
            print('不存在单独冲突的情况')
            flag = 0
        else:
            flag = 0
        return flag

    def combined_policy_conflict(self,new_policy):
        """
            判断是否存在组合冲突的情况
            接受新的策略
            1、安全策略  2、set_field策略 3、普通策略:
            当有set_field动作或者存在防火墙安全策略时，触发该函数
        """
        # 读取目前存在的set_fields动作的策略
        print('判断是否存在组合冲突的情况')
        if new_policy['policy_type_id'] == 1:

            # 当新添加的策略的动作为安全动作时
            policy_list = []  # 用于存储src/set_src 为 nw_src的策略
            # set_fields策略库中读取相关的策略
            rows = read_network_policy('set_field_policys')
            for row in rows:
                exit_policy = self.list_trans_policys(row)
                if exit_policy['src'] == new_policy['src'] or exit_policy['set_src'] == new_policy['src'] or \
                        exit_policy['dst'] == new_policy['dst'] or exit_policy['set_dst'] == new_policy['dst']:
                    policy_list.append(exit_policy)
            combined_set_policys = self.combined_set_policy(policy_list)
            if len(combined_set_policys) == 0:
                print('不存在组合策略冲突的情况')
            else:
                for csp in combined_set_policys:
                    src_tuple, dst_tuple = self.translate_alias_set(csp)
                    print(src_tuple)
                    print(dst_tuple)
                    if new_policy['src'] in src_tuple and new_policy['dst'] in dst_tuple:
                        print('存在冲突')
                    else:
                        print('不存在策略')
        elif new_policy['policy_type_id'] == 2:
            # 当新添加的策略的动作为set_field
            # 从set_field_policys策略集中获取以这条策略存在交集的策略
            rows = read_network_policy('set_field_policys')
            for row in rows:
                exist_policy = self.list_trans_policys(row)
                combined_set_policys=[]
                combined_set_policys.append(exist_policy)
                combined_set_policys.append(new_policy)
                src_tuple,dst_tuple = self.translate_alias_set(combined_set_policys)
                # 获取存在交集的安全策略
                print(src_tuple,dst_tuple)
                actions = []
                for src in src_tuple:
                    for dst in dst_tuple:
                        rows = select_policy_table('comm_policys',src,dst)
                        for row in rows:
                            policy = self.list_trans_policys(row)
                            print(policy)
                            if policy['action'] not in actions:
                                actions.append(policy['action'])
                if 'drop' in actions and 'forward' in actions:
                    print('存在冲突')
                else:
                    print('不存在冲突')
        elif new_policy['policy_type_id'] == 3:
            policy_list = []   # 用于存储src/set_src 为 nw_src的策略
            # set_fields策略库中读取相关的策略
            rows = read_network_policy('set_field_policys')
            for row in rows:
                exit_policy = self.list_trans_policys(row)
                if exit_policy['src'] == new_policy['src'] or exit_policy['set_src'] == new_policy['src'] or \
                        exit_policy['dst'] == new_policy['dst'] or exit_policy['set_dst'] == new_policy['dst']:
                    policy_list.append(exit_policy)
            combined_set_policys = self.combined_set_policy(policy_list)
            for csp in combined_set_policys:
                src_tuple, dst_tuple = self.translate_alias_set(csp)
                print(src_tuple)
                print(dst_tuple)
                if new_policy['src'] in src_tuple and new_policy['dst'] in dst_tuple:
                    print('存在冲突')
                else:
                    print('不存在策略')

    def combined_set_policy(self,policy_list):
        # 对满足条件的set_filed 策略两两组合
        combined_set_policys = []
        for i in range(len(policy_list)-1):
            combined_set_policy = []
            combined_set_policy.append(policy_list[i])
            combined_set_policy.append(policy_list[i+1])
            combined_set_policys.append(combined_set_policy)
        return combined_set_policys

    def translate_alias_set(self,set_field_policys):
        """
        将set_fields策略转换为别名集
        :return:
        """
        src_tuple = []
        dst_tuple = []
        for sfp in set_field_policys:
            nw_src = sfp['src']
            nw_dst = sfp['dst']
            set_src = sfp['set_src']
            set_dst = sfp['set_dst']
            if nw_src not in src_tuple:
                if nw_src is not None:
                    src_tuple.append(nw_src)
            if nw_dst not in dst_tuple:
                if nw_dst is not None:
                    dst_tuple.append(nw_dst)
            if set_src not in src_tuple:
                if set_src is not None:
                    src_tuple.append(set_src)
            if set_dst not in dst_tuple:
                if set_dst is not None:
                    dst_tuple.append(set_dst)
        return src_tuple,dst_tuple

    def read_policy_translate(self):
        set_field_policys = read_network_policy("set_field_policys")
        src_tuple, dst_tuple = self.translate_alias_set(set_field_policys)
        return src_tuple,dst_tuple

    def list_trans_policys(self,exist_policy):
        already_exist_policy={}
        if exist_policy[3] == 1 or exist_policy[3] == 3:
            already_exist_policy['policy_type_id'] = exist_policy[3]
            already_exist_policy['src'] = exist_policy[1]
            already_exist_policy['dst'] = exist_policy[2]
            already_exist_policy['action'] = exist_policy[4]
        elif exist_policy[3] == 2:
            already_exist_policy['policy_type_id'] = exist_policy[3]
            already_exist_policy['src'] = exist_policy[1]
            already_exist_policy['dst'] = exist_policy[2]
            already_exist_policy['set_src'] = exist_policy[4]
            already_exist_policy['set_dst'] = exist_policy[5]
        return already_exist_policy


if __name__ == '__main__':
    pc = PolicyConflict()
    # src,dst = pc.read_policy_translate()
    # print(src,dst)
    new_policy={'policy_type_id': 1, 'src': '10.0.0.1', 'dst': '10.0.0.4', 'action': 'drop'}
    # nw_policy = {'policy_type_id': 3, 'src': '10.0.0.1', 'dst': '10.0.0.2', 'action': 'forward'}
    set_policy = {'policy_type_id': 2, 'src': '10.0.0.2', 'dst': '10.0.0.3', 'set_src': None, 'set_dst': '10.0.0.4'}
    # pc.single_policy_conflict(new_policy)
    # pc.single_policy_conflict(nw_policy)
    # src,dst = pc.combined_policy_conflict()
    # print(select_policy_table('comm_policys','10.0.0.1','10.0.0.2'))
    #pc.combined_policy_conflict({'policy_type_id': 3, 'src': '10.0.0.1', 'dst': '10.0.0.3', 'action': 'forward'})
    # pc.combined_policy_conflict(new_policy)
    pc.combined_policy_conflict(set_policy)








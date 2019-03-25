# -*-coding:utf-8-*-

class Formulat_Policy(object):
    def __init__(self):
        pass

    def making_policy(self):
        policy_type = input("请选择您要制定的策略类型:1、安全策略  2、set_field策略 3、普通策略: ")
        my_policy = ''
        my_policys = {}
        while policy_type != 'exit':
            if policy_type == '1':
                policy = self.security_policy()
                policy = '1,'+policy
                my_policys = self.formulat_policy(policy)
                break
            elif policy_type == '2':
                policy = self.set_field_policy()
                policy = '2,' + policy
                print(policy)
                my_policys = self.formulat_policy(policy)
                break
            elif policy_type == '3':
                policy = self.common_policy()
                policy = '3,' + policy
                my_policys = self.formulat_policy(policy)
                break
            else:
                policy_type = input("请重新输入您要制定的策略类型:")
                continue
        return my_policys

    def security_policy(self):
        policy = input("请按照相应格式输入（src,dest,action）:")
        print(policy)
        return policy

    def set_field_policy(self):
        policy = input("请按照相应格式输入（src,dest,set_src,set_dst）:")
        print(policy)
        return policy

    def common_policy(self):
        policy = input("请按照相应格式输入（src,dest,action）:")
        print(policy)
        return policy

    def formulat_policy(self,policy):
        my_policy={}
        policy_fields = policy.split(",")
        policy_type = policy_fields[0]
        if policy_type == '1':
            my_policy['policy_type_id'] = 1
            my_policy['src'] = policy_fields[1]
            my_policy['dst'] = policy_fields[2]
            my_policy['action'] = policy_fields[3]
        elif policy_type == '2':
            my_policy['policy_type_id'] = 2
            my_policy['src'] = policy_fields[1]
            my_policy['dst'] = policy_fields[2]
            if len(policy_fields[3]) == 0:
                my_policy['set_src'] = None
            else:
                my_policy['set_src'] = policy_fields[3]
            if len(policy_fields[4])==0:
                my_policy['set_dst'] = None
            else:
                my_policy['set_dst'] = policy_fields[4]
        elif policy_type == '3':
            my_policy['policy_type_id'] = 3
            my_policy['src'] = policy_fields[1]
            my_policy['dst'] = policy_fields[2]
            my_policy['action'] = policy_fields[3]
        return my_policy

if __name__ == "__main__":
    fp = Formulat_Policy()
    print(fp.making_policy())
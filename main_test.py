from formulat_policy import *
from policyConflict import *
from fileOperation import *

if __name__ == "__main__":
    fp = Formulat_Policy()
    policy = fp.making_policy()
    print("******************对策略进行冲突检测*********************")
    pc = PolicyConflict()
    print(policy)
    flag = pc.single_policy_conflict(policy)
    print(flag)

    pc.combined_policy_conflict(policy)





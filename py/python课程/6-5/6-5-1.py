import random
candidates = ['A','B','C','D']
votes=[random.choice(candidates) for _ in range(20)]
print("投票结果列表：", votes)
print("\n得票统计：")
for c in candidates:
    count = votes.count(c)
    print(f"候选人 {c} 得票数：{count}")
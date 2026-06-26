set={0,10}
tuple=(3,2)
list=[4,5]
dict={6:'d',7:'e'}

# 通用
print(len(set),len(tuple),len(list),len(dict),sep='-',end='\n')
print(max(set),max(tuple),max(list),max(dict),sep='-',end='\n')
print(min(set),min(tuple),min(list),min(dict),sep='-',end='\n')
print(sum(set),sum(tuple),sum(list),sum(dict),sep='-',end='\n')
print(0 in set,1 in tuple,4 in list,'e' in dict)

# 集合
print(set.add(5),set.remove(0),set.pop(),set.clear(),set,sep='-',end='\n')
# 元组
print(tuple.count(2),tuple.index(3),tuple,sep='-',end='\n')
# 列表
print(list.append(6),list.insert(3,0),list.pop(2),list.remove(4),list.reverse(),list.sort(),list,sep='-',end='\n')
# 字典

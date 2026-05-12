a=b=c=1
x,y,z=1,2,3
name,age,score=["hanlei",18,100]
print(a,b,c,sep=' ',end="\n")
print(x,y,z,sep='-',end='\n')
print(name,age,score,sep=';')


lst=[1,2,3,4,5]
first,*middle,last=lst
print(first,middle,last,sep=' ')

x,y=y,x
print(x,y)

from pprint import pprint
f=open('太乙金华宗旨.txt',encoding='utf-8').read().splitlines()
pprint(f)
print(len(f))
ff=[i.replace('\u3000\u3000','') for i in f]
pprint(ff)
pprint(len(ff))
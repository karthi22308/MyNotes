



# lst = list(map(str,input().split(',')))

# print(lst[0])
# for c in lst:
#     print(c)

#dictionary sample
def findpair(lst, sum):
    dict = {}
    for i in lst:
        y = sum-i
        if(y in lst):
            return [i,y]
        else:
            dict[i]=True
    return[]





sum = 8
#print(findpair(lst,sum))


#2d arrays

def arrays():
    mat = []
    n = int(input())
    for i in range(n):
        t = list(map(int,input().split(',')))
        mat.append(t)

    print(mat[1][0])






dic ={}

dic["pair"]=5

if "pair" in dic:
    print(dic["pair"])


lst = [1,8,9,9,9,9,6,7,4,3,10]
#s = set(lst)

s = set()

for i in lst:
    s.add(i)


print(s)
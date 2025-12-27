


lst = [1,2,3,4,5,[1,44,55,65,67,[88,90],45,[56,99,98],47],876]



def fetchnum(lst):
    retlst = []
    for i in lst:
        if type(i) is int:
            retlst.append(i)
        else:
            con = fetchnum(i)
            for j in con:
                retlst.append(j)
    return retlst


#newlst = fetchnum(lst)


newlst = []

for i in lst:
    if type(i) is int:
        newlst.append(i)
    else:
        newlst.extend(i)

print(newlst)






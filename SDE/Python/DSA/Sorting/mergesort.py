


def merge(lst,s,e):
    m= (s+e)//2
    i,j=s,m+1
    ls = []
    while i<=m and j<=e:
        if lst[i]<lst[j]:
            ls.append(lst[i])
            i+=1
        else:
            ls.append(lst[j])
            j+=1
    while i<=m:
        ls.append(lst[i])
        i+=1
    while j<=e:
        ls.append(lst[j])
        j+=1
    lst[s:e+1] = ls



def mergesot(lst,s,e):
    if s>=e:
        return
    m= (s+e)//2
    mergesot(lst, s,m)
    mergesot(lst,m+1,e)
    merge(lst,s,e)
    


input = list(map(str,input().split(',')))
mergesot(input,0,len(input)-1 )

print(",".join(map(str, input)))

class Solution:
    def climbStairs(self, n: int) -> int:
        if n==0 or n==1:
            return 1
        dic = {}
        dic[0]=1
        dic[1]=1
        for i in range(2,n+1):
            dic[i]=dic[i-1]+dic[i-2]
        return dic[n]

        
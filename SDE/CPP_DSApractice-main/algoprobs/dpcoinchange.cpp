

#include <iostream>
#include <climits>
#include<vector>
using namespace std;
//bottom up
int minchange(int target, vector<int> denoms){
    vector<int> dp(target,0);
    for(int i=1;i<=target;i++){
        dp[i]=INT_MAX;
        for(int c : denoms){
            if(i-c>=0 and dp[i-c]!=INT_MAX){
                dp[i]=min(dp[i],dp[i-c]+1);
            }
        }
    }
    return dp[target];
    
    
    
}
//top down
int mintd(int t, vector<int> denoms){
    if (t==0){
        return 0;
    }
    int mini = INT_MAX;
    for(int c : denoms){
        if(t-c>=0){
           mini = min( mintd(t-c , denoms),mini);
        }
    }
    if(mini==INT_MAX){
        return -1;
    }
    else {
        return mini+1;
    }
    
    
    
    
}

int main()
{
    vector<int> denoms ={1,3,7,10};
    int target = 40;
    
    cout<< minchange(target,denoms)<<endl;
    cout<< mintd(target,denoms);
    

    return 0;
}

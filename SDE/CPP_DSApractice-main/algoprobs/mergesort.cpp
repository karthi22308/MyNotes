

#include <iostream>
#include<vector>
using namespace std;
void merge(vector<int> &a, int s,int e){
    int m= (s+e)/2;
    int i=s;
    int j=m+1;
    vector<int> temp;
    while(i<=m && j<=e){
        if(a[i]<a[j]){
            temp.push_back(a[i]);
            i++;
        }
        else{
            temp.push_back(a[j]);
            j++;
        }
    }
    
    while(i<=m){
        temp.push_back(a[i]);
            i++;
    }
    while(j<=e){
         temp.push_back(a[j]);
            j++;
    }
    int x=s;
    for(int i : temp){
        a[x++]=i;
    }
    
}

void mergesort(vector<int> & a, int s, int e){
    if(s>=e)return;
    int m= (s+e)/2;
    mergesort(a,s,m);
    mergesort(a,m+1,e);
    merge(a,s,e);
}

int main()
{
    vector<int> a ={9,8,7,6,5,4,3,2,1};
    mergesort(a,0,a.size()-1);
    for(int i: a){
        cout<< i <<" ";
    }

    return 0;
}

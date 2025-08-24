

#include <iostream>
using namespace std;
void printboard(int a[][20],int n){
    for (int i = 0;i<n;i++){
        for(int j=0;j<n;j++){
            if(a[i][j]==1){
                cout<<"Q"<<" ";
            }
            else{
                cout<<"0"<<" ";
            }
        }
        cout<<endl;
    }
}
bool canplace(int a[][20],int n,int i,int j){
    //check up
    for(int x=i;x>=0;x--){
        if(a[x][j]==1){
            return false;
        }
    }
    
    //check diagonal left
    for(int x=i,y=j;x>=0 && y>=0;x--,y--){
        if(a[x][y]==1){
            return false;
        }
    }
    
    //check diagonal right
    for(int x=i,y=j;x>=0 && y<n;x--,y++){
        if(a[x][y]==1){
            return false;
        }
    }
    return true;
    
}
bool solvenqueens(int a[][20],int n,int i){
    //base case
    if(i==n){
        return true;
    }
    
    //rec case
    for(int x=0;x<n;x++){
        if(canplace(a,n,i,x)){
            a[i][x]=1;
            if(solvenqueens(a,n,i+1)){
                return true;
            }
            a[i][x]=0;
            
        }
    }
    return false;
}


int main()
{
    int n;
    cin>>n;
    int a[20][20]={0};
    if(solvenqueens(a,n,0)){
    printboard(a,n);
    }
    else{
        cout<<"no solution exists"<<endl;
    }
    return 0;
}

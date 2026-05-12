// 输入
// 输入的第一行有两个整数L（1 <= L <= 10000）和 M（1 <= M <= 100），L代表马路的长度，M代表区域的数目，L和M之间用一个空格隔开。接下来的M行每行包含两个不同的整数，用一个空格隔开，表示一个区域的起始点和终止点的坐标。注意输入数据可能有很多组。
// 输出
// 输出包括一行，这一行只包含一个整数，表示马路上剩余的树的数目。
#include<stdio.h>
int main(){
    int L,M,tree[10001]={0},start,end;
    while(scanf("%d %d",&L,&M)!=EOF){
        for(int i=0;i<M;i++){
            scanf("%d %d",&start,&end);
            for(int j=start;j<end;j++){
                tree[j]=1;
            }
        }
        int count=0;
        for(int i=0;i<L;i++){
            if(tree[i]==0){
                count++;
            }
        }
        printf("%d\n",count-1);
    }
    return 0;
}
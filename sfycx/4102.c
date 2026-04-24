#include<stdio.h>
#include<string.h>

int main(){
    int n,i,j,p,q,num[1001];
    char color[1001][16],temp[16];
    scanf("%d",&n);
    while (n!=0){
        p=0;
        memset(num, 0, sizeof(num));
        for(i=0;i<n;i++){
            scanf("%s",temp);
            if(p==0){
                strcpy(color[p],temp);
                p++;
            }
            for(j=0;j<p;j++){
                if(strcmp(temp,color[j])==0){
                    num[j]++;
                }
                else {
                    strcpy(color[p],temp);
                    num[p]++;
                    p++;
                }
            }
        }
        q=0;
        for(j=0;j<p;j++){
            if(num[j]>num[q])q=j;
        }
        printf("%s\n",color[q]);
        scanf("%d",&n);
    }
    
    return 0;
}
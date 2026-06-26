#include<stdio.h>
int main(){
    int n,r,i;
    int sr[32];
    while(scanf("%d %d",&n,&r)!=EOF){
        if (n<0)
        {
            n=-n;
            printf("-");
        }
        i=0;
        for(;n!=0;i++){
            sr[i]=n%r;
            n=n/r;
        }
        for (int j = i-1; j >=0; j--)
        {
            if(sr[j]>9){
                printf("%c",sr[j]-10+'A');
                }
                else{
                    printf("%d",sr[j]);
                }
        }
        
        printf("\n");
        
    }
    
    return 0;
}
#include<stdio.h>

int main()
{
    int n;
    int s8[32];
    int i;
    while(scanf("%d",&n)!=EOF){
        if (n<0)
        {
            n=-n;
            printf("-");
        }
        i=0;
        for(;n!=0;i++){
            s8[i]=n%8;
            n=n/8;
        }
        for (int j = i-1; j >=0; j--)
        {
            if(s8[j]>9){
                printf("%c",s8[j]-10+'A');
                }
                else{
                    printf("%d",s8[j]);
                }
        }
        printf("\n");
    }
    return 0;
}
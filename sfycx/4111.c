#include<stdio.h>

int main(){
    int n,t,i,j,l,li,p=0,q=0;
    char num[10000][50];

    scanf("%d",&n);
    for ( i = 0; i < n; i++)
    {
        scanf("%lf",&num[i]);
    }
    for ( i = 0; i < n; i++)
    {
        if(num[i]>0){
             if (num[i]>num[p])p=i;
        }
        else   {
            if (num[i]<num[q])q=i;
        }
    }
    if(num[p]>-num[q]){
        l=0;
    }
    else{
        l=1;
        p=q;
    }
    for (t=(int)num[p]/10; t!=0; t=t/10)
    {
        l++;
    }
    for ( i = 0; i < n; i++)
    {
        li=0;
        for (t=(int)num[i]/10; t!=0; t=t/10)
        {
            li++;
        }
        if(num[i]>=0){
            for(j=0;j<l-li;j++)
                printf(" ");
            printf("%.10g\n",num[i]);
        }
        else{
            for(j=0;j<l-li-1;j++)
                printf(" ");
            printf("%.10g\n",num[i]);
        }
    }
    return 0;
}
#include<stdio.h>
int main()
{
    int i,n;
    long long plus=1,sum=0;
    scanf("%d",&n);
    for(i=1;i<=n;i++){
        plus*=i;
        sum+=plus;
    }
    printf("%lld",sum);
    return 0;
}

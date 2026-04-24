#include<stdio.h>
int main(){
    int a,b;
    // scanf("%d %d",&a,&b);
    // while(a!=0&&b!=0){
    //     printf("%d\n",a+b);
    //     scanf("%d %d",&a,&b);
    // }
    // for(scanf("%d %d",&a,&b);a!=0&&b!=0;
    //     scanf("%d %d",&a,&b);){
    //     printf("%d\n",a+b);
    // }
    // while (1)
    // {
    //     scanf("%d %d",&a,&b);
    //     if(a==0&&b==0) break;
    //     printf("%d\n",a+b);
    // }
     for(;;){
        scanf("%d %d",&a,&b);
        if(a==0&&b==0) break;
        printf("%d\n",a+b);
    }
    
    return 0;
}
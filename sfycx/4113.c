#include<stdio.h>
#include<string.h>

int main(){
    int n;
    scanf("%d",&n);
    for(int i=0;i<n;i++){
        int t,time,direct=0;
        char tru[81],fls[81];
        scanf("%d",&t);
        scanf("%s",tru);
        scanf("%s",fls);
        for (int j = 0; j < strlen(tru); j++)
        {
            if(tru[j] == fls[j]){
                direct++;
            }
            else break;
        }
        time = t*(strlen(tru)+strlen(fls)-2*direct);
        printf("%d\n",time);
    }
    return 0;
}
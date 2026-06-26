#include<stdio.h>
#include<string.h>

int main(){
    int m,n;
    char str[81];
    scanf("%d",&m);
    for(int i=0;i<m;i++){
        scanf("%d",&n);
        getchar();
        for(int j=0;j<n;j++){
            
            while(scanf("%s",str)!=EOF){
                for (int k = strlen(str)-1; k >= 0; k--)
                {
                    printf("%c",str[k]);
                }
                if (getchar()=='\n')
                {
                    printf("\n");
                    break;
                }
                else
                {
                    printf("%c",32);
                }
            }
            
        }
    }
    return 0;
}
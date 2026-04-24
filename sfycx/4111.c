#include<stdio.h>
#include<string.h>

int flt_len(char *flt){
    int len = 0;
    while(flt[len] != '.'){
        len++;
    }
    return len;
}
int maxlen(int *fltlen,int n){
    int max = 0;
    for(int i=0;i<n;i++){
        if(fltlen[i] > max){
            max = fltlen[i];
        }
    }
    return max;
}
int main(){
    int n;
    char flt[10000][51];
    int fltlen[10000];
    scanf("%d",&n);
    for(int i=0;i<n;i++){
        scanf("%s",flt[i]);
        fltlen[i] = flt_len(flt[i]);
    }
    int max = maxlen(fltlen,n);
    for (int i = 0; i < n; i++)
    {
        for(int j=0;j<max-fltlen[i];j++)
        printf(" ");
        printf("%s\n",flt[i]);
    }
    

    return 0;
}
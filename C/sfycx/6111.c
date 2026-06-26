//一种细菌的繁殖速度是每天成倍增长。
#include <stdio.h>
int main(){
    int n;
    scanf("%d",&n);
    while(n--){
        int m,d,x,m2,d2;
        scanf("%d %d %d %d %d",&m,&d,&x,&m2,&d2);
        int day=0;
        for (int i = m; i < m2; i++)
        {
            switch (i)
            {
            case 1:case 3:case 5:case 7:case 8:case 10:case 12:
                day+=31;
                break;
            case 4:case 6:case 9:case 11:
                day+=30;
                break;
            case 2:
                day+=28;
                break;
            }
        }
        for(int i=0;i<d2-d+day;i++){
            x*=2;
        }
        printf("%d\n",x);
    }
    return 0;
}
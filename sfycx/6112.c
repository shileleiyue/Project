//已知某年的一月一日是星期w，并且这一年一定不是闰年，求出这一年所有13号那天是星期5的月份，按从小到大的顺序输出月份数字（w=1~7）
#include <stdio.h>
int main(){
    int w;
    while(scanf("%d",&w)!=EOF){
        for(int i=1;i<=12;i++){
            int day=0;
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
            for(int j=0;j<day;j++){
                if(w==7){
                    w=0;
                }
                if(j==12&&w==5){
                    printf("%d\n",i);
                }
                w++;
            }
        }
    }
    return 0;
}
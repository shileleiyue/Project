#include <stdio.h>
#include <string.h>
#include <ctype.h>

void remove_whitespace(const char *src, char *dst) {
    while (*src) {
        if (!isspace((unsigned char)*src)) {
            *dst++ = *src;
        }
        src++;
    }
    *dst = '\0';
}

int main() {
    int T;
    scanf("%d", &T);
    getchar();

    while (T--) {
        char line[5000];
        char correct[5000] = {0};
        char user[5000] = {0};
        fgets(line, sizeof(line), stdin);
        if (strcmp(line, "START\n") == 0) {
            while (1) {
                fgets(line, sizeof(line), stdin);
                if (strcmp(line, "END\n") == 0) break;
                strcat(correct, line);
            }
        }

        fgets(line, sizeof(line), stdin);
        if (strcmp(line, "START\n") == 0) {
            while (1) {
                fgets(line, sizeof(line), stdin);
                if (strcmp(line, "END\n") == 0) break;
                strcat(user, line);
            }
        }

        if (strcmp(correct, user) == 0) {
            printf("Accepted\n");
        } else {
            char clean_correct[5000], clean_user[5000];
            remove_whitespace(correct, clean_correct);
            remove_whitespace(user, clean_user);
            if (strcmp(clean_correct, clean_user) == 0) {
                printf("Presentation Error\n");
            } else {
                printf("Wrong Answer\n");
            }
        }
    }
    return 0;
}
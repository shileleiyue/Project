#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main() {
    char line[210];
    while (1) {
        if (fgets(line, sizeof(line), stdin) == NULL) break;
        line[strcspn(line, "\n")] = '\0';
        if (strcmp(line, "ENDOFINPUT") == 0) break;
        if (strcmp(line, "START") != 0) continue;
        if (fgets(line, sizeof(line), stdin) == NULL) break;
        line[strcspn(line, "\n")] = '\0';
        for (int i = 0; line[i]; i++) {
            if (line[i] >= 'A' && line[i] <= 'Z') {
                line[i] = ((line[i] - 'A' - 5 + 26) % 26) + 'A';
            }
        }
        printf("%s\n", line);
        if (fgets(line, sizeof(line), stdin) == NULL) break;
    }
    return 0;
}
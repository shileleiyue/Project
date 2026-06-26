/* Minimal syscalls for newlib - no actual file I/O needed */
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>

int _close(int file) { (void)file; return -1; }
int _fstat(int file, struct stat *st) { (void)file; st->st_mode = S_IFCHR; return 0; }
int _isatty(int file) { (void)file; return 1; }
int _lseek(int file, int ptr, int dir) { (void)file; (void)ptr; (void)dir; return 0; }
int _open(const char *name, int flags, int mode) { (void)name; (void)flags; (void)mode; return -1; }
int _read(int file, char *ptr, int len) { (void)file; (void)ptr; (void)len; return 0; }
void _exit(int status) { (void)status; while(1); }
int _kill(int pid, int sig) { (void)pid; (void)sig; errno = EINVAL; return -1; }
int _getpid(void) { return 1; }

caddr_t _sbrk(int incr) {
    extern char __HeapBase, __HeapLimit;
    static char *heap_end;
    char *prev_heap_end;

    if (heap_end == 0) heap_end = &__HeapBase;
    prev_heap_end = heap_end;

    if (heap_end + incr > &__HeapLimit) {
        errno = ENOMEM;
        return (caddr_t)-1;
    }

    heap_end += incr;
    return (caddr_t)prev_heap_end;
}
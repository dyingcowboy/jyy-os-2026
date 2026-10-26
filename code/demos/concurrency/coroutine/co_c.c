#include <stdio.h>
#include <stdlib.h>
#include <setjmp.h>
#include <string.h>
#include <time.h>

#define THREADS  100000
#define COUNT    10000000
#define STACK_SZ 4096

enum { INIT, YIELD, DONE };

struct coroutine {
    jmp_buf ctx;          /* caller context */
    jmp_buf coro_ctx;     /* coroutine context */
    char *stack;
    int state;
    int name;
    int i;
    char buf[128];
};

__attribute__((noinline)) static void coro_entry(struct coroutine *c);

/* Reserve stack space with a volatile barrier */
static char *alloc_stack(void) {
    char *mem = malloc(STACK_SZ);
    if (!mem) { perror("malloc"); exit(1); }
    /* touch the top page to force allocation */
    volatile char touch = mem[0];
    (void)touch;
    return mem;
}

/* Initialize a coroutine */
static void coro_create(struct coroutine *c, int name) {
    c->state = INIT;
    c->name = name;
    c->i = 0;
    c->stack = alloc_stack();

    if (setjmp(c->ctx) == 0) {
        /* Switch to a new stack and jump to entry */
        void *new_sp = (char *)c->stack + STACK_SZ;
#if defined(__x86_64__)
        __asm__ volatile (
            "mov %0, %%rsp"
            :: "r"(new_sp)
        );
#elif defined(__aarch64__)
        __asm__ volatile (
            "mov sp, %0"
            :: "r"(new_sp)
        );
#else
        /* Portable fallback using longjmp trick — less reliable */
        memcpy((char *)c->stack + STACK_SZ - sizeof(jmp_buf), &c->ctx, sizeof(jmp_buf));
#endif
        coro_entry(c);
    }
}

/* Yield back to caller, returning current buffer */
__attribute__((noinline))
static const char *coro_yield(struct coroutine *c) {
    c->state = YIELD;
    if (setjmp(c->coro_ctx) == 0) {
        longjmp(c->ctx, 1);
    }
    return c->buf; /* resumed here */
}

/* Resume a coroutine */
static const char *coro_resume(struct coroutine *c) {
    if (setjmp(c->ctx) == 0) {
        longjmp(c->coro_ctx, 1);
    }
    return c->buf;
}

/* Coroutine body — mimics T_worker */
static void coro_entry(struct coroutine *c) {
    while (1) {
        c->i++;
        snprintf(c->buf, sizeof(c->buf), "[%d] i = %d", c->name, c->i);
        coro_yield(c);
    }
}

int main(void) {
    struct coroutine *threads = calloc(THREADS, sizeof(struct coroutine));
    if (!threads) { perror("calloc"); return 1; }

    /* Create all coroutines */
    for (int i = 0; i < THREADS; i++)
        coro_create(&threads[i], i);

    /* Random scheduling */
    srand(42);
    for (int count = 0; count < COUNT; count++) {
        int idx = rand() % THREADS;
        const char *res = coro_resume(&threads[idx]);
        printf("%s\n", res);
    }

    /* Cleanup */
    for (int i = 0; i < THREADS; i++)
        free(threads[i].stack);
    free(threads);

    return 0;
}

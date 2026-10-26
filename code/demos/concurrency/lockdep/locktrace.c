#define _GNU_SOURCE
#include <dlfcn.h>
#include <pthread.h>
#include <stdio.h>

static int (*real_lock)(pthread_mutex_t *);
static int (*real_unlock)(pthread_mutex_t *);
static volatile int resolving;

static void resolve_real(void) {
    if (real_lock) return;
    if (__atomic_exchange_n(&resolving, 1, __ATOMIC_ACQ_REL)) return;
    real_lock   = dlsym(RTLD_NEXT, "pthread_mutex_lock");
    real_unlock = dlsym(RTLD_NEXT, "pthread_mutex_unlock");
    __atomic_store_n(&resolving, 0, __ATOMIC_RELEASE);
}

static __thread int in_trace;

int pthread_mutex_lock(pthread_mutex_t *m) {
    resolve_real();
    if (!real_lock || in_trace)
        return real_lock ? real_lock(m) : 0;

    in_trace = 1;
    fprintf(stderr, "[trace] thread %lu: acquire  %p\n",
            (unsigned long)pthread_self(), (void *)m);
    in_trace = 0;

    int ret = real_lock(m);

    in_trace = 1;
    fprintf(stderr, "[trace] thread %lu: acquired %p\n",
            (unsigned long)pthread_self(), (void *)m);
    in_trace = 0;

    return ret;
}

int pthread_mutex_unlock(pthread_mutex_t *m) {
    resolve_real();
    if (!real_unlock || in_trace)
        return real_unlock ? real_unlock(m) : 0;

    in_trace = 1;
    fprintf(stderr, "[trace] thread %lu: release  %p\n",
            (unsigned long)pthread_self(), (void *)m);
    in_trace = 0;

    return real_unlock(m);
}

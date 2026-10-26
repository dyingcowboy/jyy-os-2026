#include <coroutine>
#include <cstdio>
#include <cstdlib>
#include <random>
#include <vector>
#include <cstring>

#define THREADS 1000000
#define COUNT   10000000

struct Coroutine {
    struct promise_type {
        const char* value = nullptr;

        Coroutine get_return_object() {
            return Coroutine{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        void return_void() {}
        void unhandled_exception() { abort(); }

        struct yield_value_awaiter {
            const char* value;
            bool await_ready() { return false; }
            void await_suspend(std::coroutine_handle<>) {}
            void await_resume() {}
        };

        yield_value_awaiter yield_value(const char* v) {
            value = v;
            return {v};
        }
    };

    std::coroutine_handle<promise_type> handle = nullptr;

    Coroutine(std::coroutine_handle<promise_type> h = nullptr) : handle(h) {}
    Coroutine(Coroutine&& o) noexcept : handle(o.handle) { o.handle = nullptr; }
    Coroutine& operator=(Coroutine&& o) noexcept {
        if (this != &o) {
            if (handle && !handle.done()) handle.destroy();
            handle = o.handle;
            o.handle = nullptr;
        }
        return *this;
    }
    Coroutine(const Coroutine&) = delete;
    Coroutine& operator=(const Coroutine&) = delete;

    ~Coroutine() {
        if (handle && !handle.done())
            handle.destroy();
    }

    const char* next() {
        handle.resume();
        return handle.promise().value;
    }
};

static char buf[128];

Coroutine T_worker(int name) {
    int i = 0;
    while (true) {
        i++;
        snprintf(buf, sizeof(buf), "[%d] i = %d", name, i);
        co_yield buf;
    }
}

int main() {
    std::vector<Coroutine> threads;
    threads.reserve(THREADS);

    for (int i = 0; i < THREADS; i++)
        threads.emplace_back(T_worker(i));

    std::mt19937 rng(42);
    for (int count = 0; count < COUNT; count++) {
        int idx = rng() % THREADS;
        const char* res = threads[idx].next();
        printf("%s\n", res);
    }

    return 0;
}

#include <thread.h>
#include <thread-sync.h>

thread_local int x = 100;

void T_worker(int tid) {
  // thread_local int y;  <- Not compile.

  x++;
  printf("Thread %d: %p = %d\n", tid, &x, x);
}

int main() {
    for (int i = 0; i < 4; i++) {
        spawn(T_worker);
    }
}

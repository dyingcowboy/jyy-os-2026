/*
 * 教务系统 — mmap 持久化学生数据库
 *
 * jw.db 通过 MAP_FIXED 映射到固定地址，superblock 里的指针直接写入文件，
 * 跨进程重启仍然有效。msync + fdatasync 保证落盘。
 *
 * 编译: gcc -O2 -Wall -o jw jw.c
 */

#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

#define DB_FILE   "jw.db"
#define DB_SIZE   (64 << 10)             /* 64 KiB */
#define BASE      ((void *)0x100000000000UL)
#define MAX_NAME  48
#define MAGIC     0x4A574442u            /* "JWDB" */

/* ---- 数据结构：真实指针直接持久化 ---- */

typedef struct student {
    int             id;
    char            name[MAX_NAME];
    struct student *next;
} student_t;

typedef struct superblock {
    unsigned    magic;
    char        wal[252];      /* 前 4B: "WAL:" / 全零=空 */
    int         count;
    student_t  *head;          /* 学生链表头 */
    student_t  *free_head;     /* 空闲链表头 */
    char       *slab_next;     /* 下一次分配位置 */
} superblock_t;

#define SB ((superblock_t *)BASE)

/* ---- 自定义分配器 (slab + free list) ---- */

static student_t *alloc_student(void) {
    if (SB->free_head) {
        student_t *s = SB->free_head;
        SB->free_head = s->next;
        memset(s, 0, sizeof(*s));
        return s;
    }
    if (SB->slab_next + sizeof(student_t) >= (char *)BASE + DB_SIZE)
        return NULL;
    student_t *s = (student_t *)SB->slab_next;
    SB->slab_next += sizeof(student_t);
    memset(s, 0, sizeof(*s));
    return s;
}

static void free_student(student_t *s) {
    s->next = SB->free_head;
    SB->free_head = s;
}

/* ---- 持久化 ---- */

static int g_fd;

static void db_sync(void) {
    msync(BASE, DB_SIZE, MS_SYNC);
    fdatasync(g_fd);
}

static int db_open(void) {
    g_fd = open(DB_FILE, O_RDWR | O_CREAT, 0644);
    if (g_fd < 0) return -1;

    struct stat st;
    fstat(g_fd, &st);
    int new_db = st.st_size < (off_t)sizeof(superblock_t);
    ftruncate(g_fd, DB_SIZE);

    void *p = mmap(BASE, DB_SIZE, PROT_READ | PROT_WRITE,
                   MAP_SHARED | MAP_FIXED, g_fd, 0);
    if (p == MAP_FAILED) return -1;

    if (new_db) {
        memset(SB, 0, sizeof(*SB));
        SB->magic     = MAGIC;
        SB->slab_next = (char *)BASE + sizeof(superblock_t);
        db_sync();
    } else if (SB->magic != MAGIC) {
        fprintf(stderr, "数据库文件格式错误\n");
        return -1;
    }
    return 0;
}

static void db_close(void) {
    db_sync();
    munmap(BASE, DB_SIZE);
    close(g_fd);
}

/* ---- 增删改查 ---- */

static student_t *find(int id, student_t **prev) {
    student_t *cur = SB->head, *p = NULL;
    for (; cur; p = cur, cur = cur->next)
        if (cur->id == id) {
            if (prev) *prev = p;
            return cur;
        }
    return NULL;
}

static void do_add(int id, const char *name) {
    if (find(id, NULL)) {
        printf("  学号 %d 已存在\n", id);
        return;
    }
    student_t *s = alloc_student();
    if (!s) { printf("  数据库已满\n"); return; }
    s->id = id;
    strncpy(s->name, name, MAX_NAME - 1);
    s->next  = SB->head;
    SB->head = s;
    SB->count++;
    db_sync();
    printf("  已添加: %d %s\n", id, name);
}

static void do_del(int id) {
    student_t *prev;
    student_t *s = find(id, &prev);
    if (!s) { printf("  学号 %d 不存在\n", id); return; }
    if (prev) prev->next = s->next;
    else      SB->head   = s->next;
    SB->count--;
    free_student(s);
    db_sync();
    printf("  已删除: %d\n", id);
}

static void do_upd(int id, const char *name) {
    student_t *s = find(id, NULL);
    if (!s) { printf("  学号 %d 不存在\n", id); return; }
    strncpy(s->name, name, MAX_NAME - 1);
    db_sync();
    printf("  已更新: %d -> %s\n", id, name);
}

static void do_get(int id) {
    student_t *s = find(id, NULL);
    if (!s) { printf("  学号 %d 不存在\n", id); return; }
    printf("  %d %s\n", s->id, s->name);
}

static void do_list(void) {
    printf("  共 %d 名学生\n", SB->count);
    int n = 0;
    for (student_t *s = SB->head; s; s = s->next)
        printf("  [%d] %d\t%s\n", ++n, s->id, s->name);
}

/* ---- Crash recovery: rebuild invariants from slab ---- */

static void db_rebuild(void) {
    /* Recount linked list */
    int count = 0;
    for (student_t *s = SB->head; s; s = s->next)
        count++;
    SB->count = count;

    /* Rebuild free list: all slab slots not in linked list */
    SB->free_head = NULL;
    for (char *p = (char *)BASE + sizeof(superblock_t);
         p + sizeof(student_t) <= SB->slab_next;
         p += sizeof(student_t)) {
        student_t *s = (student_t *)p;
        int in_use = 0;
        for (student_t *t = SB->head; t; t = t->next)
            if (t == s) { in_use = 1; break; }
        if (!in_use) {
            s->next = SB->free_head;
            SB->free_head = s;
        }
    }
    db_sync();
}

/* ---- WAL (Write-Ahead Log, 1 slot) ---- */

static void wal_write(const char *cmd) {
    char tmp[sizeof(SB->wal) - 4];
    strncpy(tmp, cmd, sizeof(tmp) - 1);
    tmp[sizeof(tmp) - 1] = '\0';
    memcpy(SB->wal, "WAL:", 4);
    memcpy(SB->wal + 4, tmp, sizeof(tmp));
    SB->wal[sizeof(SB->wal) - 1] = '\0';
    db_sync();
}

static void wal_clear(void) {
    memcpy(SB->wal, "WAL:", 4);
    memset(SB->wal + 4, 0, sizeof(SB->wal) - 4);
    db_sync();
}

/* ---- 命令执行 ---- */

/* 返回值: <0 退出, 0 未知命令, 1 已执行 */
static int execute(const char *cmd) {
    char buf[256];
    strncpy(buf, cmd, sizeof(buf) - 1);
    buf[sizeof(buf) - 1] = '\0';

    char *av[4] = {0};
    int ac = 0;
    for (char *p = strtok(buf, " \t"); p && ac < 4; p = strtok(NULL, " \t"))
        av[ac++] = p;
    if (!ac) return 0;

    if (!strcmp(av[0], "quit") || !strcmp(av[0], "q")) return -1;

    if (!strcmp(av[0], "ls"))              { do_list();          return 1; }
    if (!strcmp(av[0], "get") && ac >= 2)  { do_get(atoi(av[1])); return 1; }

    /* 修改操作: WAL -> 执行 -> 清 WAL */
    if (!strcmp(av[0], "add") && ac >= 3) {
        wal_write(cmd);
        do_add(atoi(av[1]), av[2]);
        wal_clear();
        return 1;
    }
    if ((!strcmp(av[0], "del") || !strcmp(av[0], "rm")) && ac >= 2) {
        wal_write(cmd);
        do_del(atoi(av[1]));
        wal_clear();
        return 1;
    }
    if (!strcmp(av[0], "upd") && ac >= 3) {
        wal_write(cmd);
        do_upd(atoi(av[1]), av[2]);
        wal_clear();
        return 1;
    }

    return 0;
}

static void wal_replay(void) {
    if (memcmp(SB->wal, "WAL:", 4) || SB->wal[4] == '\0') return;
    printf("  [WAL 重放] %s\n", SB->wal + 4);
    execute(SB->wal + 4);
    wal_clear();
}

/* ---- 命令行 ---- */

int main(void) {
    printf("教务系统 (mmap 持久化数据库)\n");
    if (db_open() < 0) return 1;
    printf("数据库已加载 地址=%p 学生数=%d\n", BASE, SB->count);
    wal_replay();
    db_rebuild();
    printf("命令:\n");
    printf("  add <学号> <姓名>  添加学生\n");
    printf("  del <学号>         删除学生 (也可用 rm)\n");
    printf("  upd <学号> <姓名>  修改姓名\n");
    printf("  get <学号>         查询学生\n");
    printf("  ls                 列出所有学生\n");
    printf("  quit               退出\n\n");

    char line[256];
    while (printf("jw> "), fflush(stdout), fgets(line, sizeof line, stdin)) {
        line[strcspn(line, "\n")] = '\0';
        int r = execute(line);
        if (r < 0) break;
        if (r == 0) printf("  未知命令，试试 add/del/upd/get/ls/quit\n");
    }

    db_close();
    printf("已退出，数据已落盘。\n");
}

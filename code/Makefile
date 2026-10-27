# =============================================================================
#  JYY《操作系统原理》2026 课堂 demo —— 批量构建入口
# -----------------------------------------------------------------------------
#    make            构建所有能在当前平台构建的 demo
#    make -j8        并行构建
#    make status     查看每个 demo 在本机的构建状态
#    make clean      清理全部构建产物
#    make <demo>     只构建指定 demo，例如 make concurrency/peterson
#    make help       显示这段帮助
#
#  每个 demo 目录里也可以单独 make；统一配置见 mk/demo.mk。
#  在 macOS 上无法构建的 demo（Linux 专属 / 其他架构 / 外部工具）会打印
#  [跳过] 说明并以成功状态退出，不计入失败。
# =============================================================================

ROOT       := $(CURDIR)
STATUS_DIR := $(ROOT)/.make-status

# 收集带 Makefile 的 demo 目录：
#   demos/<topic>/<demo>/         例如 demos/concurrency/peterson
#   demos/<topic>/<sub>/<demo>/   例如 demos/intro/cpu-reset/x86
DEMO_MAKEFILES := $(sort \
	$(wildcard demos/*/*/Makefile) \
	$(wildcard demos/*/*/*/Makefile))
DEMOS := $(patsubst demos/%/Makefile,%,$(DEMO_MAKEFILES))

.PHONY: all help status clean $(DEMOS)

# -----------------------------------------------------------------------------
# 构建
# -----------------------------------------------------------------------------
all: $(DEMOS)
	@printf '\n'
	@total=$(words $(DEMOS)); \
	 fails=$$(ls $(STATUS_DIR)/*.fail 2>/dev/null | wc -l | tr -d ' '); \
	 if [ "$$fails" -eq 0 ]; then \
	   printf '  共 %s 个 demo：可构建的已构建完成，无法在本机构建的已跳过。\n\n' "$$total"; \
	 else \
	   printf '  共 %s 个 demo，其中 %s 个构建失败：\n' "$$total" "$$fails"; \
	   sed 's/^/    - /' $(STATUS_DIR)/*.fail; \
	   printf '\n'; \
	   exit 1; \
	 fi

# 每个 demo 单独一次递归 make：失败只记录、不中断其它 demo 的构建。
$(DEMOS):
	@mkdir -p $(STATUS_DIR); rm -f $(STATUS_DIR)/$(subst /,_,$@).fail
	@$(MAKE) -C demos/$@ --no-print-directory \
	  || { echo '$@' > $(STATUS_DIR)/$(subst /,_,$@).fail; \
	       printf '\n  \033[31m✗ %s 构建失败\033[0m\n\n' '$@'; }

# -----------------------------------------------------------------------------
# 状态 / 清理 / 帮助
# -----------------------------------------------------------------------------
status:
	@printf '%-46s %s\n' 'DEMO' 'STATUS'
	@printf '%-46s %s\n' '----------------------------------------------' '------'
	@for d in $(DEMOS); do $(MAKE) -C demos/$$d --no-print-directory status; done

clean:
	@for d in $(DEMOS); do \
	   $(MAKE) -C demos/$$d --no-print-directory clean >/dev/null 2>&1 \
	     || echo "  clean 失败: $$d"; \
	 done
	@rm -rf $(STATUS_DIR)
	@printf '  已清理全部 demo。\n'

help:
	@printf '\n用法：\n'
	@printf '  make            构建所有能在本机构建的 demo\n'
	@printf '  make -j8        并行构建\n'
	@printf '  make status     查看每个 demo 在本机的构建状态\n'
	@printf '  make clean      清理全部构建产物\n'
	@printf '  make <demo>     只构建指定 demo，例如 make concurrency/peterson\n\n'
	@printf '单独构建某个 demo：cd demos/concurrency/peterson && make\n\n'

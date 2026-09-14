# verl 中文文档构建入口
# 用法：
#   make env     —— 首次：创建虚拟环境并安装依赖
#   make html    —— 构建 HTML 文档（输出到 build/html）
#   make serve   —— 构建并启动本地预览服务器（http://localhost:8000）
#   make clean   —— 清理构建产物

SPHINXBUILD = LC_ALL=C.UTF-8 LANG=C.UTF-8 .venv/bin/sphinx-build
SOURCEDIR   = docs
BUILDDIR    = build

.PHONY: env html serve clean

env:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

html:
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html"
	@echo ""
	@echo "构建完成！打开 $(BUILDDIR)/html/index.html 查看"

serve: html
	@echo "启动本地预览服务器：http://localhost:8000"
	cd "$(BUILDDIR)/html" && python3 -m http.server 8000

clean:
	rm -rf "$(BUILDDIR)"

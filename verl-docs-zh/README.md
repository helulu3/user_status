# verl 中文文档（社区翻译版）

本目录是 [verl 官方文档](https://verl.readthedocs.io/en/latest/) 的中文翻译项目，使用 **Sphinx + ReadTheDocs 主题** 构建，页面形式与官方文档一致（左侧导航树 + 右侧页面目录 + 全文搜索）。

## 目录结构

```
verl-docs-zh/
├── docs/                  # 文档源文件（Markdown）
│   ├── conf.py            # Sphinx 配置
│   ├── index.md           # 主页（含完整目录导航）
│   └── start/             # 快速开始
│       ├── install.md     # 安装指南 ✅ 已翻译
│       └── quickstart.md  # PPO 快速入门 ✅ 已翻译
├── Makefile               # 构建入口
├── requirements.txt       # 构建依赖
├── .venv/                 # 构建虚拟环境（不入库）
└── build/                 # 构建产物（不入库）
```

## 本地构建与预览

```bash
cd verl-docs-zh

# 首次：创建虚拟环境并安装依赖
make env

# 构建 HTML（输出到 build/html/）
make html

# 构建并启动本地预览（http://localhost:8000）
make serve
```

## 部署方式

构建产物是纯静态 HTML（`build/html/`），可部署到任何静态托管平台：

### GitHub Pages

```bash
# 方式一：gh-pages 分支
git subtree push --prefix verl-docs-zh/build/html origin gh-pages

# 方式二：使用 GitHub Actions 自动构建部署（推荐）
# 在仓库根目录添加 .github/workflows/docs.yml，参考：
# https://docs.github.com/en/pages/getting-started-with-github-pages
```

### ReadTheDocs

在仓库根目录添加 `.readthedocs.yaml`：

```yaml
version: 2
build:
  os: ubuntu-24.04
  tools:
    python: "3.12"
sphinx:
  configuration: verl-docs-zh/docs/conf.py
python:
  install:
    - requirements: verl-docs-zh/requirements.txt
```

然后在 [readthedocs.org](https://readthedocs.org) 导入仓库即可自动构建。

## 翻译进度

| 章节 | 页面 | 状态 |
| --- | --- | --- |
| 快速开始 | 安装 | ✅ 已翻译 |
| 快速开始 | 快速入门：GSM8K 上的 PPO 训练 | ✅ 已翻译 |
| 其他章节 | —— | 🔗 导航至英文原文 |

## 如何贡献翻译

1. 在 `docs/` 下对应目录新建 `.md` 文件（参考 `docs/start/install.md` 的翻译风格）；
2. 在 `docs/index.md` 的相应 `{toctree}` 块中，把原来的英文外链条目替换为本地文档条目，例如：

   ```diff
   - 多节点训练（英文） <https://verl.readthedocs.io/en/latest/start/multinode.html>
   + 多节点训练 <start/multinode>
   ```

3. `make html` 构建确认无警告后提交。

### 翻译约定

* 技术术语保留英文并附中文注释，如「单控制器（single-controller）」；
* 专有名词不译：FSDP、Megatron-LM、vLLM、SGLang、Ray、uv 等；
* 代码块、命令行、配置参数保持原样；
* 每个页面顶部标注原文档地址。

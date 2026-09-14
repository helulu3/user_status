# 安装

> 原文档地址：https://verl.readthedocs.io/en/latest/start/install.html

## 环境要求

* **Python**：版本 >= 3.10
* **CUDA**：版本 >= 12.8

verl 支持多种后端。目前可用的配置如下：

* 训练后端：**FSDP** 和 **Megatron-LM**（可选）。
* Rollout 生成后端：**SGLang**、**vLLM** 和 **TGI**。

## 后端引擎的选择

### 1. 训练

我们推荐使用 **FSDP / FSDP2** 后端来研究、探索和原型化不同的模型、数据集和 RL 算法。对于追求更好可扩展性的用户，我们推荐 **Megatron-LM** 后端。目前我们支持 [Megatron-LM v0.13.1](https://github.com/NVIDIA/Megatron-LM/tree/core_v0.13.1)。两种后端都通过统一 worker 层提供服务——worker 级 API 请参阅 [Engine Workers](https://verl.readthedocs.io/en/latest/workers/engine_workers.html)，引擎级设计请参阅 [Model Engine](https://verl.readthedocs.io/en/latest/workers/model_engine.html)。

### 2. 推理

推理方面，支持 vllm 0.18.0 及更高版本；旧版本已不再与 verl 兼容。

关于 SGLang，详细安装和使用说明请参阅 [SGLang 后端](https://verl.readthedocs.io/en/latest/workers/sglang_worker.html)。SGLang rollout 正在大量开发中，提供了许多高级特性和优化。我们鼓励用户通过 [SGLang Issue Tracker](https://github.com/zhaochenyang20/Awesome-ML-SYS-Tutorial/issues/106) 报告任何问题或提供反馈。

对于 huggingface TGI 集成，通常用于调试和单 GPU 探索。

## 使用 uv 安装

verl 的 Python 环境由 [uv](https://docs.astral.sh/uv/) 驱动：一个提交的 `uv.lock` 覆盖所有后端，您可以针对特定运行以 **extras** 的方式选择后端：

* 推理：`vllm` 或 `sglang`。
* 训练：`fsdp` 或 `megatron`。
* `cpu`：无 GPU，用于 CI / 快速检查。

**没有安装步骤**。`uv run --extra ...` 在首次使用时从 `uv.lock` 构建项目虚拟环境（`.venv`），之后复用它，因此无论环境是否已存在，启动任务的命令都是相同的——这就是 `examples/` 脚本和 CI 的做法。`uv sync` 和 `manage_envs.py` 用于 `uv run` 无法覆盖的场景（重新生成 lockfile、并存多个环境、激活的 shell、Docker 缓存烘焙）；请参阅[显式管理环境](#显式管理环境)。

> **注意**
>
> uv 工作流面向 **Linux，Python 3.12，x86_64 和 aarch64**（GH200 / GB200）。两种架构都在 `[tool.uv].environments` 中声明，因此提交的 `uv.lock` 同时携带两者，下面每条命令在任一机器上的写法完全相同——uv 会根据主机自身的平台标签选择每个 wheel。架构永远不是一个 extra：没有 `vllm-aarch64`，只有 `vllm`。昇腾 NPU 和 AMD ROCm 仍在 uv 工作流之外；请使用专用镜像。

> **注意**
>
> uv 从不从源码编译原生包。`apex`、`transformer-engine` 和 `flash-attn`——以及纯 Python 的 `megatron-bridge`——都从 verl wheelhouse 索引（[verl-project.github.io/verl-wheelhouse](https://verl-project.github.io/verl-wheelhouse/simple/)，在 `pyproject.toml` 的 `[tool.uv.index]` / `[tool.uv.sources]` 中配置）拉取**预构建**版本；这些 wheel 是为 cu130 / torch 2.11 / CPython 3.12 构建的，同时支持 `linux_x86_64` 和 `linux_aarch64`（aarch64 构建针对 `TORCH_CUDA_ARCH_LIST` `9.0;10.0`，这是 arm64 主机仅有的 CUDA 部件）。推理引擎（`vllm`、`sglang`、`sglang-kernel`）直接来自 PyPI，其固定版本的 wheel 已经是 cu130 / torch-2.11 构建。只有 git 来源的 `megatron-core`（`core_v0.18.0`，搭配 `megatron-bridge` 0.5.2）和 `mbridge` 会在环境首次构建时编译。

### 运行任务或测试

从 verl 仓库根目录运行——uv 在那里找到 `pyproject.toml` 和 `uv.lock`。`examples/` 下的脚本已经携带 uv 配置，因此测试运行无需任何准备：

```bash
bash examples/grpo_trainer/run_qwen3_8b_fsdp.sh

# 脚本会选择与您请求的引擎匹配的 extras
INFER_BACKEND=sglang bash examples/grpo_trainer/run_qwen3_8b_fsdp.sh
```

每个脚本在末尾的短代码块中组装其启动命令，例如 `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`：

```bash
LAUNCH=(python3)
RAY=(ray_kwargs.ray_init.runtime_env.py_executable=null)
if [ "${VERL_USE_UV:-1}" != 0 ] && [ "${DEVICE:-gpu}" = gpu ] && { [ "${INFER_BACKEND}" = vllm ] || [ "${INFER_BACKEND}" = sglang ]; }; then
    LAUNCH=(uv run --frozen --all-packages --extra "${INFER_BACKEND}" --extra fsdp python3)
    RAY=(ray_kwargs.ray_init.runtime_env.py_executable="uv -v run --frozen --all-packages --extra ${INFER_BACKEND} --extra fsdp")
fi
"${LAUNCH[@]}" -m verl.trainer.main_ppo "${DATA[@]}" ... "${RAY[@]}"
```

驱动程序在 `uv run` 下运行，Ray 通过 `ray_kwargs.ray_init.runtime_env.py_executable` 用相同的命令启动 TaskRunner 和每个 worker actor，因此任务中的每个进程都解析相同的环境。这些标志：

* `--frozen` —— 按原样使用提交的 `uv.lock`，永不重新解析。
* `--all-packages` —— 安装 uv 工作区的每个包。
* `--extra <engine> --extra <trainer>` —— 本次运行的后端组合。

您想运行的任何其他内容——pytest、数据预处理、您自己的入口点——都使用相同的前缀。CI 就是这样运行的（见 `.github/workflows/`）：

```bash
UV_RUN="uv run --frozen --all-packages --extra vllm --extra megatron"
$UV_RUN uv pip list                        # 该组合解析出了什么
$UV_RUN python3 examples/data_preprocess/gsm8k.py --local_save_dir ~/data/gsm8k
$UV_RUN pytest -s tests/experimental/agent_loop
$UV_RUN python3 -m verl.trainer.main_ppo trainer.n_gpus_per_node=8 ...
```

在同一任务的各条命令之间保持 extras 一致：`uv run` 会将 `.venv` 精确同步到给定的 extras，因此交替使用组合每次都会重新安装 torch。

> **注意**
>
> Ray >= 2.47 有自己的 `uv run` runtime-env 钩子，会重写 `runtime_env["working_dir"]`，并在 verl 传入的显式 `working_dir=None` 上崩溃，因此 `verl/__init__.py` 设置了 `RAY_ENABLE_UV_RUN_RUNTIME_ENV=0`——uv 环境已经通过 `py_executable` 到达 worker。如果启动器在 `ray.init()` 之前重新定位了工作目录（导致 worker cwd 没有可解析的项目），请将 `py_executable` 设置为解释器路径，例如 `/abs/path/verl/.venv/bin/python3`，而不是 `uv run` 前缀。

### 回退到系统 Python

设置 `VERL_USE_UV=0` 改用环境解释器启动；这也会让 `py_executable` 保持其 `null` 默认值：

```bash
# 默认：驱动程序和 Ray workers 都在 uv 下
bash examples/grpo_trainer/run_qwen3_8b_fsdp.sh

# 过渡回退：系统 Python，无 uv
VERL_USE_UV=0 bash examples/grpo_trainer/run_qwen3_8b_fsdp.sh
```

无论 `VERL_USE_UV` 如何设置，NPU / trtllm 和其他非 uv 后端都已经回退到系统 Python：每个 uv 分支都额外受 `[ "${DEVICE:-gpu}" = gpu ]` 门控，因此 `DEVICE=npu` 永远不会进入 uv（lockfile 只解析 CUDA 后端），昇腾运行保持使用环境解释器，包括 Ray workers。`tests/special_sanity/check_uv_gpu_only.py`（一个 pre-commit 钩子）强制执行这一点：uv 命令必须位于该门控内，而仅 NPU 的目录树（如 `examples/ascend_extras/` 和 `tests/special_npu/`）必须完全不引用 uv。

### 有效的后端组合

典型运行组合**一个推理引擎**与**一个训练后端**，例如 `--extra vllm --extra fsdp`。规则：

* 最多选择一个推理引擎：`vllm` **或** `sglang`（不能同时选）。
* 添加一个训练后端：`fsdp`（默认）或 `megatron`。
* `cpu` 是无 GPU 的，单独使用。

互斥集合在 `[tool.uv].conflicts` 中声明，因此 uv 会拒绝不可能的组合，而不是解析出一个。当您想查看时，`python manage_envs.py list` 会打印 extras、冲突规则以及您的 `.venv` 状态。

### 从 uv Docker 镜像运行

`docker/Dockerfile.uv.cu130` 将每个后端的 uv **包缓存**烘焙到镜像中，但没有固定的 `.venv`。构建一次，然后在运行时选择组合——第一次 `uv run` 会从烘焙的缓存离线构建 `.venv`：

```bash
DOCKER_BUILDKIT=1 docker build -f docker/Dockerfile.uv.cu130 -t verl:uv-cu130 .

docker run --rm -it --gpus all verl:uv-cu130 bash
# 容器内（workdir /workspace/verl，其 .venv 已在 PATH 上）：
bash examples/grpo_trainer/run_qwen3_8b_fsdp.sh
# ... 或自己驱动：
uv run --frozen --all-packages --extra sglang --extra megatron \
    python3 -m verl.trainer.main_ppo trainer.n_gpus_per_node=8 ...
```

### 其他后端

昇腾 NPU、AMD ROCm 和 `trtllm` 在 uv 工作流之外。请使用独立的 Dockerfile——例如 `docker/ascend/`（昇腾）、`docker/rocm/Dockerfile.rocm`（AMD）或 `docker/Dockerfile.stable.trtllm`（TensorRT-LLM）。

aarch64 GPU **不在**此列表中：它们是 uv 工作流的一等公民，与 x86_64 共享相同的 extras 和相同的 `uv.lock`。在 arm64 主机上构建 `docker/Dockerfile.uv.cu130` 并完全按上述方式使用。

### 升级或修改依赖

要升级、降级或固定一个包（例如 `vllm`），请在 `pyproject.toml` 中编辑其版本，刷新 lockfile，然后验证：

```bash
# 1. 编辑 pyproject.toml —— 例如在 [vllm] extra 中提升 vllm 的固定版本
# 2. 刷新 lockfile 并检查组合是否可解析：
python manage_envs.py lock                                        # 重新生成 uv.lock
uv run --frozen --all-packages --extra vllm --extra fsdp uv pip list   # 安装 + 验证
# 3. 将清单和 lockfile 一起提交：
git add pyproject.toml uv.lock
```

包版本位于 `pyproject.toml` 的 `[project.optional-dependencies]` 下（每个后端一个块）；少数项目级固定（`numpy`、`kernels`）和每个引擎的 `transformers` 固定位于 `[tool.uv].override-dependencies` 下。请更新包出现的每个位置。

`transformers` 跟随推理引擎（其版本必须与引擎所需的匹配）：`vllm` 固定 `5.5.3`，而 `sglang` 和 `cpu` 开发切片固定 `5.3.0`。训练后端（`fsdp` / `megatron`）自己不携带 `transformers` 固定，因此运行继承所选引擎的版本（`--extra vllm --extra megatron` -> `5.5.3`；`--extra sglang --extra fsdp` -> `5.3.0`）；仅训练的组合回退到 `5.3.0`。每个引擎的固定使用 `override-dependencies` 中的 `extra` 冲突标记，uv 按解析分支求值。

要在不提交的情况下尝试某个版本，将其安装到现有的 `.venv` 中（会被下一次 `uv run` / `uv sync` 还原）：

```bash
source .venv/bin/activate
uv pip install -U vllm        # 或：uv pip install vllm==<version>
```

> **注意**
>
> 升级 `vllm` / `sglang` 可能需要匹配的 `torch`（所有 GPU 后端共享同一个 `torch`），而大的 `torch` / CUDA 升级可能需要不同的 Docker 基础镜像。

## 在自定义环境中使用 uv 安装

如果您不使用 Docker 镜像，请在您自己的主机或基础镜像上运行。uv 只安装 Python 包，因此请携带一个 CUDA 运行时与您选择的 GPU 后端匹配的基础环境。

### 选择基础镜像

| Extra(s) | 推荐基础镜像 |
| --- | --- |
| `vllm` / `fsdp` / `megatron` | `nvidia/cuda:13.0.2-devel-ubuntu24.04`（与 `docker/Dockerfile.uv.cu130` 匹配） |
| `sglang` | `lmsysorg/sglang:v0.5.12` 或 `nvidia/cuda:13.0.2-cudnn-devel-ubuntu24.04` |
| `cpu`（CI / 健全性检查） | 任何带有 Python 3.12 的 x86_64 或 aarch64 Linux 主机；无需 GPU |

### 设置

```bash
# 一次性：安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

git clone https://github.com/verl-project/verl.git
cd verl

# 没有安装步骤：第一次 uv run 会从提交的 uv.lock 构建 .venv
uv run --frozen --all-packages --extra vllm --extra fsdp uv pip list
```

然后按[运行任务或测试](#运行任务或测试)中所述启动——使用 `examples/` 脚本，或您自己的 `uv run --frozen --all-packages --extra <engine> --extra <trainer> ...`。

## 显式管理环境

`uv run` 覆盖常规运行。`manage_envs.py`——验证 extra 组合并向 `uv` 传递正确标志的驱动程序——用于它未覆盖的场景。在 `lock` / `sync` / `prefetch` 上，`--` 之后的任何内容都会转发给底层 `uv` 命令（在 `run` 上它是要执行的命令）；`python manage_envs.py --help` 列出所有内容。

**编辑 `pyproject.toml` 后重新生成 lockfile**（见[升级或修改依赖](#升级或修改依赖)）：

```bash
python manage_envs.py lock
```

**并存多个环境。** 默认情况下每个组合都复用 `.venv`，因此切换组合会重新同步它。`--name NAME`（或 `VERL_VENV_NAME`）将环境放在 `.venv-<name>` 中，而 `.venv` 成为指向您最近同步的那个的符号链接：

```bash
python manage_envs.py sync --name vllm-mega vllm megatron
python manage_envs.py sync --name sglang-fsdp sglang fsdp
source .venv/bin/activate                 # = sglang-fsdp 环境
```

相同的 `--name` 适用于 `run` / `shell` / `clean` / `list`（对于 `sync` / `run` 请将其放在 extras 之前）。要让普通的 `uv run` 指向命名环境，请导出 `UV_PROJECT_ENVIRONMENT=.venv-vllm-mega`。

**在激活的环境中工作**（交互式调试、编辑器、期望 venv 在 `PATH` 上的工具）：

```bash
python manage_envs.py shell vllm fsdp     # 同步，然后启动一个 .venv 已激活的 shell
python manage_envs.py clean               # 删除 .venv 并重新开始
```

**保留您自己构建的包。** 如果内部构建（比如自定义的 `ray` 或 `wandb`）不能被覆盖，请将其列在 `VERL_UV_NO_INSTALL` 中，然后自己安装；`sync` 随后会向 uv 传递 `--no-install-package` 和 `--inexact`，使其既不被替换也不被移除：

```bash
export VERL_UV_NO_INSTALL="ray wandb"
python manage_envs.py sync vllm fsdp      # 除 ray / wandb 之外的所有内容
uv pip install <您的 ray / wandb wheels>
```

请注意，普通的 `uv run` 会精确同步，这会撤销这种精心策划的环境；请改用 `python manage_envs.py run vllm fsdp -- <cmd>`（它会添加 `--no-sync`）或激活的 shell。

**预热 Docker 镜像的缓存。** `prefetch` 将每个后端的依赖下载并构建到 `UV_CACHE_DIR` 中，而不生成可用的 `.venv`，因此后续运行可以离线解析。它是构建时辅助工具（见 `docker/Dockerfile.uv.cu130`），永远不是运行时命令：

```bash
python manage_envs.py prefetch cu130 dev -- --frozen
```

## uv 故障排查

* **`uv: command not found`** —— 运行 `curl -LsSf https://astral.sh/uv/install.sh | sh`。

* **组合被拒绝** —— 您选择了两个推理引擎；请选择 `vllm` **或** `sglang`。

* **每次运行都重新安装 torch** —— 同一任务中的两条命令请求了不同的 extras。每个任务保持一个组合。

* **`apex` / `transformer-engine` / `flash-attn` 出现 `No solution found`** —— 这些是从 verl wheelhouse 拉取的预构建包（见*使用 uv 安装*下的说明）。这意味着解析器没有找到匹配您平台的 wheel，或者 wheelhouse 无法访问；uv 流程仅支持 Linux x86_64 或 aarch64 上的 cu130 / torch 2.11 / CPython 3.12。

* **`vllm` / `sglang` / `sglang-kernel` 出现 `No solution found`** —— 这些来自 PyPI，PyPI 仅为 Linux x86_64 和 aarch64 发布它们（且 `sglang` 仅支持 glibc >= 2.34），因此适用相同的平台限制。

* **uv 在 macOS 上失败** —— uv 工作流仅限 Linux（任一架构）；请使用 Linux 主机或 Docker 镜像。`python manage_envs.py list` 会打印它检测到的主机以及 `uv.lock` 是否覆盖该主机。

* **重新开始** —— `python manage_envs.py clean`，然后再次运行。

一些系统级组件完全不由 uv 处理（Dockerfile 会设置它们）：系统 apt 包、用于 MoE all-to-all 的 GDRCopy + DeepEP、用于 SGLang KV-cache 传输的 Mooncake、flashinfer JIT 缓存和 sgl-router。请参考 `docker/Dockerfile.stable.{vllm,sglang}`。

## 使用 Docker 镜像安装

预构建的稳定镜像是上述 uv 工作流的替代方案：每个标签附带一个固定的引擎 + 训练栈，依赖已安装好，因此在镜像内您用 `pip` 安装 verl 本身，并用环境 `python3` 启动（对于 `examples/` 脚本，设置 `VERL_USE_UV=0`）。

从 v0.6.0 开始，我们使用 vllm 和 sglang 的发布镜像作为基础镜像。

### 基础镜像

* vLLM：[https://hub.docker.com/r/vllm/vllm-openai](https://hub.docker.com/r/vllm/vllm-openai)
* SGLang：[https://hub.docker.com/r/lmsysorg/sglang](https://hub.docker.com/r/lmsysorg/sglang)

### 应用镜像

在基础镜像之上，添加了以下包：

* flash_attn
* Megatron-LM
* Apex
* TransformerEngine
* DeepEP

最新的 docker 文件：

* [Dockerfile.stable.vllm](https://github.com/verl-project/verl/blob/main/docker/Dockerfile.stable.vllm)
* [Dockerfile.stable.sglang](https://github.com/verl-project/verl/blob/main/docker/Dockerfile.stable.sglang)

所有预构建镜像都可以在 dockerhub 上找到：[verlai/verl](https://hub.docker.com/r/verlai/verl)。例如 `verlai/verl:sgl055.latest`、`verlai/verl:vllm011.latest`。

您可以在我们的 github workflows 中找到用于开发和 CI 的最新镜像：

* [.github/workflows/vllm.yml](https://github.com/verl-project/verl/blob/main/.github/workflows/vllm.yml)
* [.github/workflows/sgl.yml](https://github.com/verl-project/verl/blob/main/.github/workflows/sgl.yml)

### 从 Docker 安装

拉取所需的 Docker 镜像并安装所需的推理和训练框架后，您可以按以下步骤运行：

1. 启动所需的 Docker 镜像并进入：

```bash
docker create --runtime=nvidia --gpus all --net=host --shm-size="10g" --cap-add=SYS_ADMIN -v .:/workspace/verl --name verl <image:tag> sleep infinity
docker start verl
docker exec -it verl bash
```

2. 如果您使用提供的镜像，则只需安装 verl 本身（不带依赖）：

```bash
# 安装 nightly 版本（推荐）
git clone https://github.com/verl-project/verl && cd verl
pip3 install --no-deps -e .
```

【可选】如果您希望在不同框架之间切换，可以使用以下命令安装 verl：

```bash
# 安装 nightly 版本（推荐）
git clone https://github.com/verl-project/verl && cd verl
pip3 install -e ".[vllm]"
pip3 install -e ".[sglang]"
```

## 使用 AMD GPU 安装 - ROCm 内核支持

当您在 ROCm 平台上使用 AMD GPU（MI300）运行时，不能使用前面的快速开始来运行 verl。您应该按照以下步骤构建 docker 并运行它。如果您在使用 AMD GPU 运行 verl 时遇到任何问题，请随时联系我 - [Yusheng Su](https://yushengsu-thu.github.io/)。

### 找到 AMD ROCm 的 docker：[docker/rocm/Dockerfile.rocm](https://github.com/verl-project/verl/blob/main/docker/rocm/Dockerfile.rocm)

```dockerfile
#  在仓库目录中构建 docker：
# docker build -f docker/rocm/Dockerfile.rocm -t verl-rocm:03.04.2015 .
# docker images # 您可以找到构建的 docker
FROM rocm/vllm:rocm6.2_mi300_ubuntu20.04_py3.9_vllm_0.6.4

# 设置工作目录
# WORKDIR $PWD/app

# 设置环境变量
ENV PYTORCH_ROCM_ARCH="gfx90a;gfx942"

# 安装 vllm
RUN pip uninstall -y vllm && \
    rm -rf vllm && \
    git clone -b v0.6.3 https://github.com/vllm-project/vllm.git && \
    cd vllm && \
    MAX_JOBS=$(nproc) python3 setup.py install && \
    cd .. && \
    rm -rf vllm

# 复制整个项目目录
COPY . .

# 安装依赖
RUN pip install "tensordict<0.6" --no-deps && \
    pip install accelerate \
    codetiming \
    datasets \
    dill \
    hydra-core \
    "liger-kernel>=0.8.2" \
    numpy \
    pandas \
    datasets \
    peft \
    "pyarrow>=15.0.0" \
    pylatexenc \
    "ray[data,train,tune,serve]" \
    torchdata \
    transformers \
    wandb \
    orjson \
    pybind11 && \
    pip install -e . --no-deps
```

### 构建镜像

```bash
docker build -t verl-rocm .
```

### 启动容器

```bash
docker run --rm -it \
  --device /dev/dri \
  --device /dev/kfd \
  -p 8265:8265 \
  --group-add video \
  --cap-add SYS_PTRACE \
  --security-opt seccomp=unconfined \
  --privileged \
  -v $HOME/.ssh:/root/.ssh \
  -v $HOME:$HOME \
  --shm-size 128G \
  -w $PWD \
  verl-rocm \
  /bin/bash
```

如果您不想使用 root 模式并要求将自己指定为用户，请在上述 docker 启动脚本中添加 `-e HOST_UID=$(id -u)` 和 `-e HOST_GID=$(id -g)`。

verl 在 AMD GPU 上目前支持 FSDP 作为训练引擎，vLLM 和 SGLang 作为推理引擎。我们将来会支持 Megatron。

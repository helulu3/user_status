# 欢迎使用 verl 中文文档！

> 本文档是 [verl 官方文档](https://verl.readthedocs.io/en/latest/) 的社区中文翻译版本（非官方）。
>
> 原文档地址：https://verl.readthedocs.io/en/latest/

**verl** 是一个灵活、高效且可用于生产环境的强化学习（RL）训练框架，专为大语言模型（LLM）后训练（post-training）而设计。它是 [HybridFlow](https://arxiv.org/pdf/2409.19256) 论文的开源实现。

## verl 的灵活性与易用性

* **轻松扩展多种 RL 算法**：混合编程模型结合了单控制器（single-controller）和多控制器（multi-controller）范式的优势，能够灵活表示并高效执行复杂的后训练数据流，让用户只需几行代码即可构建 RL 数据流。

* **通过模块化 API 无缝集成现有 LLM 基础设施**：解耦计算与数据依赖，可与现有 LLM 框架无缝集成，例如 PyTorch FSDP、Megatron-LM、vLLM 和 SGLang。此外，用户还可以轻松扩展到其他 LLM 训练和推理框架。

* **灵活的设备映射与并行化**：支持将模型灵活放置到不同的 GPU 组上，实现高效的资源利用，并可在不同规模的集群上扩展。

* 开箱即用地集成流行的 HuggingFace 模型。

## verl 的高性能

* **业界领先的吞吐量**：通过无缝集成现有的 SOTA LLM 训练和推理框架，verl 实现了高生成吞吐量和高训练吞吐量。

* **基于 3D-HybridEngine 的高效 Actor 模型重分片**：消除内存冗余，并显著减少训练与生成阶段之间切换时的通信开销。

---

```{toctree}
:maxdepth: 1
:caption: 快速开始

安装 <start/install>
快速入门：在 GSM8K 数据集上进行 PPO 训练 <start/quickstart>
多节点训练（英文） <https://verl.readthedocs.io/en/latest/start/multinode.html>
Ray 调试教程（英文） <https://verl.readthedocs.io/en/latest/start/ray_debug_tutorial.html>
更多资源（英文） <https://verl.readthedocs.io/en/latest/start/more_resources.html>
Agentic RL 训练（英文） <https://verl.readthedocs.io/en/latest/start/agentic_rl.html>
```

```{toctree}
:maxdepth: 1
:caption: 编程指南

如何扩展 verl（英文） <https://verl.readthedocs.io/en/latest/extend_guide.html>
HybridFlow 编程指南（英文） <https://verl.readthedocs.io/en/latest/hybrid_flow.html>
verl.single_controller 的设计（英文） <https://verl.readthedocs.io/en/latest/single_controller.html>
```

```{toctree}
:maxdepth: 1
:caption: 数据准备

为后训练准备数据（英文） <https://verl.readthedocs.io/en/latest/preparation/prepare_data.html>
为数据集实现奖励函数（英文） <https://verl.readthedocs.io/en/latest/preparation/reward_function.html>
```

```{toctree}
:maxdepth: 1
:caption: 配置说明

配置详解（英文） <https://verl.readthedocs.io/en/latest/examples/config.html>
```

```{toctree}
:maxdepth: 1
:caption: PPO 示例

PPO 示例架构（英文） <https://verl.readthedocs.io/en/latest/examples/ppo_code_architecture.html>
GSM8K 示例（英文） <https://verl.readthedocs.io/en/latest/examples/gsm8k_example.html>
Megatron-FSDP 示例（英文） <https://verl.readthedocs.io/en/latest/examples/megatron_fsdp_example.html>
多模态示例架构（英文） <https://verl.readthedocs.io/en/latest/examples/multi_modal_example.html>
SkyPilot 示例（英文） <https://verl.readthedocs.io/en/latest/examples/skypilot_examples.html>
```

```{toctree}
:maxdepth: 1
:caption: 算法

近端策略优化 PPO（英文） <https://verl.readthedocs.io/en/latest/algo/ppo.html>
组相对策略优化 GRPO（英文） <https://verl.readthedocs.io/en/latest/algo/grpo.html>
配方：解耦裁剪与动态采样策略优化 DAPO（英文） <https://verl.readthedocs.io/en/latest/algo/dapo.html>
配方：自博弈微调 SPIN（英文） <https://verl.readthedocs.io/en/latest/algo/spin.html>
配方：自博弈偏好优化 SPPO（英文） <https://verl.readthedocs.io/en/latest/algo/sppo.html>
配方：熵机制（英文） <https://verl.readthedocs.io/en/latest/algo/entropy.html>
基于最优奖励基线的在策略 RL（OPO）（英文） <https://verl.readthedocs.io/en/latest/algo/opo.html>
算法基线（英文） <https://verl.readthedocs.io/en/latest/algo/baseline.html>
GPG：组策略梯度（英文） <https://verl.readthedocs.io/en/latest/algo/gpg.html>
Rollout 校正（英文） <https://verl.readthedocs.io/en/latest/algo/rollout_corr.html>
verl 中 Rollout 校正方法的数学公式（英文） <https://verl.readthedocs.io/en/latest/algo/rollout_corr_math.html>
最优 Token 基线（OTB）（英文） <https://verl.readthedocs.io/en/latest/algo/otb.html>
散度近端策略优化（DPPO）（英文） <https://verl.readthedocs.io/en/latest/algo/dppo.html>
在策略蒸馏（OPD）（英文） <https://verl.readthedocs.io/en/latest/algo/opd.html>
直接奖励优化（DRO）（英文） <https://verl.readthedocs.io/en/latest/algo/dro.html>
```

```{toctree}
:maxdepth: 1
:caption: PPO Trainer 与 Workers

PPO Ray Trainer（英文） <https://verl.readthedocs.io/en/latest/workers/ray_trainer.html>
模型引擎（英文） <https://verl.readthedocs.io/en/latest/workers/model_engine.html>
引擎 Workers（英文） <https://verl.readthedocs.io/en/latest/workers/engine_workers.html>
Automodel 后端（英文） <https://verl.readthedocs.io/en/latest/workers/automodel_workers.html>
TorchTitan 后端（英文） <https://verl.readthedocs.io/en/latest/workers/torchtitan_workers.html>
SGLang 后端（英文） <https://verl.readthedocs.io/en/latest/workers/sglang_worker.html>
TensorRT-LLM 后端（英文） <https://verl.readthedocs.io/en/latest/workers/trtllm_worker.html>
```

```{toctree}
:maxdepth: 1
:caption: 性能调优指南

训练 DeepSeek 671B（英文） <https://verl.readthedocs.io/en/latest/perf/dpsk.html>
动态上下文并行（英文） <https://verl.readthedocs.io/en/latest/advance/dynamic_context_parallel.html>
verl LLM 最佳实践（DAPO + Qwen3-235B）（英文） <https://verl.readthedocs.io/en/latest/perf/best_practices.html>
性能调优指南（英文） <https://verl.readthedocs.io/en/latest/perf/perf_tuning.html>
通过 Mooncake-Store 实现 Rollout KV Cache 卸载（英文） <https://verl.readthedocs.io/en/latest/perf/rollout_kv_offload.html>
升级到 vLLM >= 0.8（英文） <https://verl.readthedocs.io/en/latest/README_vllm0.8.html>
RL 所需硬件资源（英文） <https://verl.readthedocs.io/en/latest/perf/device_tuning.html>
verl Profiler 系统（英文） <https://verl.readthedocs.io/en/latest/perf/verl_profiler_system.html>
verl 中的 NVIDIA Nsight Systems 性能分析（英文） <https://verl.readthedocs.io/en/latest/perf/nsight_profiling.html>
verl 中的 PyTorch 性能分析（英文） <https://verl.readthedocs.io/en/latest/perf/torch_profiling.html>
```

```{toctree}
:maxdepth: 1
:caption: 添加新模型

使用 FSDP 后端添加模型（英文） <https://verl.readthedocs.io/en/latest/advance/fsdp_extension.html>
使用 Megatron-LM 后端添加模型（英文） <https://verl.readthedocs.io/en/latest/advance/megatron_extension.html>
添加 DeepSeek V4 支持（英文） <https://verl.readthedocs.io/en/latest/advance/deepseek_v4_integration.html>
实验性 Megatron Agent Compose 预览（英文） <https://verl.readthedocs.io/en/latest/advance/megatron_lite_backend.html>
```

```{toctree}
:maxdepth: 1
:caption: 异步训练

配方：单步离策略异步训练器（英文） <https://verl.readthedocs.io/en/latest/advance/one_step_off.html>
增量权重同步（英文） <https://verl.readthedocs.io/en/latest/advance/delta_weight_sync.html>
V1 异步训练器（英文） <https://verl.readthedocs.io/en/latest/advance/v1_async_trainer.html>
配方：全异步策略训练器（英文） <https://verl.readthedocs.io/en/latest/advance/fully_async.html>
配方：异步在策略知识蒸馏训练器（英文） <https://verl.readthedocs.io/en/latest/advance/async-on-policy-distill.html>
全异步训练的动态资源调度（英文） <https://verl.readthedocs.io/en/latest/advance/dynamic_schedule.html>
```

```{toctree}
:maxdepth: 1
:caption: 低精度

verl 中的 FP8 RL（英文） <https://verl.readthedocs.io/en/latest/low_precision/fp8.html>
verl 中的 NVFP4 QAT（量化感知训练）（英文） <https://verl.readthedocs.io/en/latest/low_precision/nvfp4_qat.html>
```

```{toctree}
:maxdepth: 1
:caption: 高级特性

使用 Checkpoint 支持容错训练（英文） <https://verl.readthedocs.io/en/latest/advance/checkpoint.html>
RoPE Scaling 覆盖（英文） <https://verl.readthedocs.io/en/latest/advance/rope.html>
Attention 实现覆盖（英文） <https://verl.readthedocs.io/en/latest/advance/attention_implementation.html>
支持 LoRA 的 RL(HF) 算法（英文） <https://verl.readthedocs.io/en/latest/advance/ppo_lora.html>
多轮 Rollout 支持（英文） <https://verl.readthedocs.io/en/latest/sglang_multiturn/multiturn.html>
Ray API 设计教程（英文） <https://verl.readthedocs.io/en/latest/advance/placement.html>
扩展到其他 RL(HF) 算法（英文） <https://verl.readthedocs.io/en/latest/advance/dpo_extension.html>
Sandbox Fusion 示例（英文） <https://verl.readthedocs.io/en/latest/examples/sandbox_fusion_example.html>
Trace 功能使用说明（英文） <https://verl.readthedocs.io/en/latest/advance/rollout_trace.html>
使用 RL-Insight 监控训练（英文） <https://verl.readthedocs.io/en/latest/advance/rl_insight.html>
SkipManager：跳过 RL 流水线中的一切（英文） <https://verl.readthedocs.io/en/latest/advance/skip_manager.html>
Agent Loop（英文） <https://verl.readthedocs.io/en/latest/advance/agent_loop.html>
Reward Loop（英文） <https://verl.readthedocs.io/en/latest/advance/reward_loop.html>
TransferQueue 数据系统（英文） <https://verl.readthedocs.io/en/latest/data/transfer_queue.html>
使用 Prometheus 和 Grafana 监控 Rollout（英文） <https://verl.readthedocs.io/en/latest/advance/grafana_prometheus.html>
在 SFT/RL 训练和推理中使用 MTP 的指南（英文） <https://verl.readthedocs.io/en/latest/advance/mtp.html>
可复现 RL 训练的完全确定性（英文） <https://verl.readthedocs.io/en/latest/advance/determinism.html>
FSDP-Turbo 后端（英文） <https://verl.readthedocs.io/en/latest/advance/fsdp_turbo_backend.html>
```

```{toctree}
:maxdepth: 1
:caption: 硬件支持

多芯片支持（英文） <https://verl.readthedocs.io/en/latest/hardware/multi_chip_support.html>
AMD (ROCm) 教程（英文） <https://verl.readthedocs.io/en/latest/amd_tutorial/index.html>
昇腾 (NPU) 教程（英文） <https://verl.readthedocs.io/en/latest/ascend_tutorial/index.html>
```

```{toctree}
:maxdepth: 1
:caption: API 参考

数据接口（英文） <https://verl.readthedocs.io/en/latest/api/data.html>
单控制器接口（英文） <https://verl.readthedocs.io/en/latest/api/single_controller.html>
Trainer 接口（英文） <https://verl.readthedocs.io/en/latest/api/trainer.html>
工具类（英文） <https://verl.readthedocs.io/en/latest/api/utils.html>
```

```{toctree}
:maxdepth: 1
:caption: 其他

博客：verl 0.7 发布（英文） <https://verl.readthedocs.io/en/latest/blog/v0.7.html>
常见问题 FAQ（英文） <https://verl.readthedocs.io/en/latest/faq/faq.html>
贡献指南（英文） <https://verl.readthedocs.io/en/latest/contributing/editing-agent-instructions.html>
Sandbox Fusion 工具集成（英文） <https://verl.readthedocs.io/en/latest/sglang_multiturn/sandbox_fusion.html>
```

---

## 贡献

verl 是自由软件；您可以根据 Apache License 2.0 的条款重新分发和/或修改它。我们欢迎贡献。欢迎加入 [GitHub](https://github.com/verl-project/verl)、[Slack](https://join.slack.com/t/verlgroup/shared_invite/zt-2w5p9o4c3-yy0x2Q56s_VlGLsJ93A6vA) 和[微信](https://raw.githubusercontent.com/eric-haibin-lin/verl-community/refs/heads/main/WeChat.JPG)进行讨论。

欢迎来自社区的贡献！请查看[项目路线图](https://github.com/verl-project/verl/issues/710)和 [good first issues](https://github.com/verl-project/verl/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22good%20first%20issue%22)，了解您可以贡献的方向。

### 代码检查与格式化

我们使用 pre-commit 来帮助提升代码质量。初始化 pre-commit，运行：

```bash
pip install pre-commit
pre-commit install
```

为了在本地解决 CI 错误，您也可以手动运行 pre-commit：

```bash
pre-commit run
```

### 添加 CI 测试

如果可能，请为您的新功能添加 CI 测试：

1. 找到最相关的 workflow yml 文件，它通常对应一个 `hydra` 默认配置（例如 `ppo_trainer`、`ppo_megatron_trainer`、`sft_trainer` 等）。

2. 如果尚未包含，请将相关路径模式添加到 `paths` 部分。

3. 尽量减少测试脚本的工作量（参考现有脚本的示例）。

**我们正在招聘！** 如果您对 MLSys / LLM 推理 / 多模态对齐方向的实习或全职机会感兴趣，请发送[邮件](mailto:haibin.lin%40bytedance.com)给我们。

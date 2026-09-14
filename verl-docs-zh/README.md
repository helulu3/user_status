# 欢迎使用 verl 中文文档！

> 本文档是 [verl 官方文档](https://verl.readthedocs.io/en/latest/) 的中文翻译版本。
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

## 文档目录

### 快速开始

* [安装](start/install.md)
    * [环境要求](start/install.md#环境要求)
    * [后端引擎的选择](start/install.md#后端引擎的选择)
    * [使用 uv 安装](start/install.md#使用-uv-安装)
    * [在自定义环境中使用 uv 安装](start/install.md#在自定义环境中使用-uv-安装)
    * [显式管理环境](start/install.md#显式管理环境)
    * [uv 故障排查](start/install.md#uv-故障排查)
    * [使用 Docker 镜像安装](start/install.md#使用-docker-镜像安装)
    * [使用 AMD GPU 安装 - ROCm 内核支持](start/install.md#使用-amd-gpu-安装---rocm-内核支持)

* [快速入门：在 GSM8K 数据集上进行 PPO 训练](start/quickstart.md)
    * [简介](start/quickstart.md#简介)
    * [数据集介绍](start/quickstart.md#数据集介绍)
    * [步骤 1：准备数据集](start/quickstart.md#步骤-1准备数据集)
    * [步骤 2：下载用于后训练的模型](start/quickstart.md#步骤-2下载用于后训练的模型)
    * [步骤 3：使用 instruct 模型进行 PPO 训练](start/quickstart.md#步骤-3使用-instruct-模型进行-ppo-训练)

* [多节点训练](https://verl.readthedocs.io/en/latest/start/multinode.html)（英文）
* [Ray 调试教程](https://verl.readthedocs.io/en/latest/start/ray_debug_tutorial.html)（英文）
* [更多资源](https://verl.readthedocs.io/en/latest/start/more_resources.html)（英文）
* [Agentic RL 训练](https://verl.readthedocs.io/en/latest/start/agentic_rl.html)（英文）

### 编程指南

* [如何扩展 verl](https://verl.readthedocs.io/en/latest/extend_guide.html)（英文）
* [HybridFlow 编程指南](https://verl.readthedocs.io/en/latest/hybrid_flow.html)（英文）
* [verl.single_controller 的设计](https://verl.readthedocs.io/en/latest/single_controller.html)（英文）

### 数据准备

* [为后训练准备数据](https://verl.readthedocs.io/en/latest/preparation/prepare_data.html)（英文）
* [为数据集实现奖励函数](https://verl.readthedocs.io/en/latest/preparation/reward_function.html)（英文）

### 配置说明

* [配置详解](https://verl.readthedocs.io/en/latest/examples/config.html)（英文）

### PPO 示例

* [PPO 示例架构](https://verl.readthedocs.io/en/latest/examples/ppo_code_architecture.html)（英文）
* [GSM8K 示例](https://verl.readthedocs.io/en/latest/examples/gsm8k_example.html)（英文）
* [Megatron-FSDP 示例](https://verl.readthedocs.io/en/latest/examples/megatron_fsdp_example.html)（英文）
* [多模态示例架构](https://verl.readthedocs.io/en/latest/examples/multi_modal_example.html)（英文）
* [SkyPilot 示例](https://verl.readthedocs.io/en/latest/examples/skypilot_examples.html)（英文）

### 算法

* [近端策略优化（PPO）](https://verl.readthedocs.io/en/latest/algo/ppo.html)（英文）
* [组相对策略优化（GRPO）](https://verl.readthedocs.io/en/latest/algo/grpo.html)（英文）
* [配方：解耦裁剪与动态采样策略优化（DAPO）](https://verl.readthedocs.io/en/latest/algo/dapo.html)（英文）
* [配方：自博弈微调（SPIN）](https://verl.readthedocs.io/en/latest/algo/spin.html)（英文）
* [配方：自博弈偏好优化（SPPO）](https://verl.readthedocs.io/en/latest/algo/sppo.html)（英文）
* [配方：熵机制](https://verl.readthedocs.io/en/latest/algo/entropy.html)（英文）
* [基于最优奖励基线的在策略 RL（OPO）](https://verl.readthedocs.io/en/latest/algo/opo.html)（英文）
* [算法基线](https://verl.readthedocs.io/en/latest/algo/baseline.html)（英文）
* [GPG：组策略梯度](https://verl.readthedocs.io/en/latest/algo/gpg.html)（英文）
* [Rollout 校正](https://verl.readthedocs.io/en/latest/algo/rollout_corr.html)（英文）
* [verl 中 Rollout 校正方法的数学公式](https://verl.readthedocs.io/en/latest/algo/rollout_corr_math.html)（英文）
* [最优 Token 基线（OTB）](https://verl.readthedocs.io/en/latest/algo/otb.html)（英文）
* [散度近端策略优化（DPPO）](https://verl.readthedocs.io/en/latest/algo/dppo.html)（英文）
* [在策略蒸馏（OPD）](https://verl.readthedocs.io/en/latest/algo/opd.html)（英文）
* [直接奖励优化（DRO）](https://verl.readthedocs.io/en/latest/algo/dro.html)（英文）

### PPO Trainer 与 Workers

* [PPO Ray Trainer](https://verl.readthedocs.io/en/latest/workers/ray_trainer.html)（英文）
* [模型引擎](https://verl.readthedocs.io/en/latest/workers/model_engine.html)（英文）
* [引擎 Workers](https://verl.readthedocs.io/en/latest/workers/engine_workers.html)（英文）
* [Automodel 后端](https://verl.readthedocs.io/en/latest/workers/automodel_workers.html)（英文）
* [TorchTitan 后端](https://verl.readthedocs.io/en/latest/workers/torchtitan_workers.html)（英文）
* [SGLang 后端](https://verl.readthedocs.io/en/latest/workers/sglang_worker.html)（英文）
* [TensorRT-LLM 后端](https://verl.readthedocs.io/en/latest/workers/trtllm_worker.html)（英文）

### 性能调优指南

* [训练 DeepSeek 671B](https://verl.readthedocs.io/en/latest/perf/dpsk.html)（英文）
* [动态上下文并行](https://verl.readthedocs.io/en/latest/advance/dynamic_context_parallel.html)（英文）
* [verl LLM 最佳实践（DAPO + Qwen3-235B）](https://verl.readthedocs.io/en/latest/perf/best_practices.html)（英文）
* [性能调优指南](https://verl.readthedocs.io/en/latest/perf/perf_tuning.html)（英文）
* [通过 Mooncake-Store 实现 Rollout KV Cache 卸载](https://verl.readthedocs.io/en/latest/perf/rollout_kv_offload.html)（英文）
* [升级到 vLLM >= 0.8](https://verl.readthedocs.io/en/latest/README_vllm0.8.html)（英文）
* [RL 所需硬件资源](https://verl.readthedocs.io/en/latest/perf/device_tuning.html)（英文）
* [verl Profiler 系统](https://verl.readthedocs.io/en/latest/perf/verl_profiler_system.html)（英文）
* [verl 中的 NVIDIA Nsight Systems 性能分析](https://verl.readthedocs.io/en/latest/perf/nsight_profiling.html)（英文）
* [verl 中的 PyTorch 性能分析](https://verl.readthedocs.io/en/latest/perf/torch_profiling.html)（英文）

### 添加新模型

* [使用 FSDP 后端添加模型](https://verl.readthedocs.io/en/latest/advance/fsdp_extension.html)（英文）
* [使用 Megatron-LM 后端添加模型](https://verl.readthedocs.io/en/latest/advance/megatron_extension.html)（英文）
* [添加 DeepSeek V4 支持](https://verl.readthedocs.io/en/latest/advance/deepseek_v4_integration.html)（英文）
* [实验性 Megatron Agent Compose 预览](https://verl.readthedocs.io/en/latest/advance/megatron_lite_backend.html)（英文）

### 异步训练

* [配方：单步离策略异步训练器](https://verl.readthedocs.io/en/latest/advance/one_step_off.html)（英文）
* [增量权重同步](https://verl.readthedocs.io/en/latest/advance/delta_weight_sync.html)（英文）
* [V1 异步训练器](https://verl.readthedocs.io/en/latest/advance/v1_async_trainer.html)（英文）
* [配方：全异步策略训练器](https://verl.readthedocs.io/en/latest/advance/fully_async.html)（英文）
* [配方：异步在策略知识蒸馏训练器](https://verl.readthedocs.io/en/latest/advance/async-on-policy-distill.html)（英文）
* [全异步训练的动态资源调度](https://verl.readthedocs.io/en/latest/advance/dynamic_schedule.html)（英文）

### 低精度

* [verl 中的 FP8 RL](https://verl.readthedocs.io/en/latest/low_precision/fp8.html)（英文）
* [verl 中的 NVFP4 QAT（量化感知训练）](https://verl.readthedocs.io/en/latest/low_precision/nvfp4_qat.html)（英文）

### 高级特性

* [使用 Checkpoint 支持容错训练](https://verl.readthedocs.io/en/latest/advance/checkpoint.html)（英文）
* [RoPE Scaling 覆盖](https://verl.readthedocs.io/en/latest/advance/rope.html)（英文）
* [Attention 实现覆盖](https://verl.readthedocs.io/en/latest/advance/attention_implementation.html)（英文）
* [支持 LoRA 的 RL(HF) 算法](https://verl.readthedocs.io/en/latest/advance/ppo_lora.html)（英文）
* [多轮 Rollout 支持](https://verl.readthedocs.io/en/latest/sglang_multiturn/multiturn.html)（英文）
* [Ray API 设计教程](https://verl.readthedocs.io/en/latest/advance/placement.html)（英文）
* [扩展到其他 RL(HF) 算法](https://verl.readthedocs.io/en/latest/advance/dpo_extension.html)（英文）
* [Sandbox Fusion 示例](https://verl.readthedocs.io/en/latest/examples/sandbox_fusion_example.html)（英文）
* [Trace 功能使用说明](https://verl.readthedocs.io/en/latest/advance/rollout_trace.html)（英文）
* [使用 RL-Insight 监控训练](https://verl.readthedocs.io/en/latest/advance/rl_insight.html)（英文）
* [SkipManager：跳过 RL 流水线中的一切](https://verl.readthedocs.io/en/latest/advance/skip_manager.html)（英文）
* [Agent Loop](https://verl.readthedocs.io/en/latest/advance/agent_loop.html)（英文）
* [Reward Loop](https://verl.readthedocs.io/en/latest/advance/reward_loop.html)（英文）
* [TransferQueue 数据系统](https://verl.readthedocs.io/en/latest/data/transfer_queue.html)（英文）
* [使用 Prometheus 和 Grafana 监控 Rollout](https://verl.readthedocs.io/en/latest/advance/grafana_prometheus.html)（英文）
* [在 SFT/RL 训练和推理中使用 MTP 的指南](https://verl.readthedocs.io/en/latest/advance/mtp.html)（英文）
* [可复现 RL 训练的完全确定性](https://verl.readthedocs.io/en/latest/advance/determinism.html)（英文）
* [FSDP-Turbo 后端](https://verl.readthedocs.io/en/latest/advance/fsdp_turbo_backend.html)（英文）

### 硬件支持

* [多芯片支持](https://verl.readthedocs.io/en/latest/hardware/multi_chip_support.html)（英文）
* [AMD (ROCm) 教程](https://verl.readthedocs.io/en/latest/amd_tutorial/index.html)（英文）
* [昇腾 (NPU) 教程](https://verl.readthedocs.io/en/latest/ascend_tutorial/index.html)（英文）

### API 参考

* [数据接口](https://verl.readthedocs.io/en/latest/api/data.html)（英文）
* [单控制器接口](https://verl.readthedocs.io/en/latest/api/single_controller.html)（英文）
* [Trainer 接口](https://verl.readthedocs.io/en/latest/api/trainer.html)（英文）
* [工具类](https://verl.readthedocs.io/en/latest/api/utils.html)（英文）

### 博客

* [verl 0.7 发布博客](https://verl.readthedocs.io/en/latest/blog/v0.7.html)（英文）

### 常见问题（FAQ）

* [常见问题](https://verl.readthedocs.io/en/latest/faq/faq.html)（英文）

### 贡献

* [编辑 Agent 指南](https://verl.readthedocs.io/en/latest/contributing/editing-agent-instructions.html)（英文）

### 开发笔记

* [Sandbox Fusion 工具集成](https://verl.readthedocs.io/en/latest/sglang_multiturn/sandbox_fusion.html)（英文）

---

## 贡献

verl 是自由软件；您可以根据 Apache License 2.0 的条款重新分发和/或修改它。我们欢迎贡献。欢迎加入我们的 [GitHub](https://github.com/verl-project/verl)、[Slack](https://join.slack.com/t/verlgroup/shared_invite/zt-2w5p9o4c3-yy0x2Q56s_VlGLsJ93A6vA) 和[微信](https://raw.githubusercontent.com/eric-haibin-lin/verl-community/refs/heads/main/WeChat.JPG)进行讨论。

欢迎来自社区的贡献！请查看我们的[项目路线图](https://github.com/verl-project/verl/issues/710)和 [good first issues](https://github.com/verl-project/verl/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22good%20first%20issue%22)，了解您可以贡献的方向。

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

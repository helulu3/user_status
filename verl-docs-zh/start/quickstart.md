# 快速入门：在 GSM8K 数据集上进行 PPO 训练

> 原文档地址：https://verl.readthedocs.io/en/latest/start/quickstart.html

使用 GSM8K 数据集对 LLM 进行后训练。

## 简介

在本示例中，我们使用基于函数的奖励来训练 LLM 解决 [GSM8k](https://verl.readthedocs.io/en/latest/start/hf_dataset_gsm8k) 任务。[\[1\]](#id3)

**前置条件：**

* 按照安装指南安装了最新版本的 `verl` 及其依赖。推荐使用 Docker 镜像。
* 至少 24 GB HBM 显存的 GPU。

> **注意**
>
> 下面的 `python3` 命令假设解释器已经提供了 verl——可以是 Docker 镜像之一，或已激活的 `.venv`。使用 uv 工作流时没有安装步骤：从仓库根目录运行，在前面加上 `uv run` 前缀，它会在首次使用时从提交的 `uv.lock` 构建 `.venv`：
>
> ```bash
> UV_RUN="uv run --frozen --all-packages --extra vllm --extra fsdp"
> $UV_RUN python3 examples/data_preprocess/gsm8k.py --local_save_dir ~/data/gsm8k
> $UV_RUN python3 -m verl.trainer.main_ppo ... \
>     ray_kwargs.ray_init.runtime_env.py_executable="${UV_RUN}"
> ```
>
> 最后一个覆盖配置是让 Ray 在同一环境中启动 TaskRunner 和每个 worker actor 的关键；`examples/` 脚本已经为您设置好了。完整的 uv 工作流请参阅[安装](install.md)。

## 数据集介绍

GSM8k 是一个数学问题数据集。提示（prompt）是一道小学数学题，要求 LLM 模型解决该数学问题。下面是一个例子：

**提示（Prompt）**

> Katy 用茶匙量的糖和杯量的水按 7:13 的比例煮咖啡。如果她总共用了 120 茶匙的糖和水，计算她用了多少茶匙的糖。

**解答（Solution）**

> 她用来煮咖啡的原料总比例是 7+13 = <<7+13=20>>20。由于代表她用糖茶匙数的分数是 7/20，她用了 7/20*120 = <<7/20*120=42>>42 #### 42

## 步骤 1：准备数据集

我们将数据集预处理为 parquet 格式，以便 (1) 包含计算 RL 奖励所需的字段，(2) 读取速度更快。

```bash
python3 examples/data_preprocess/gsm8k.py --local_save_dir ~/data/gsm8k
```

## 步骤 2：下载用于后训练的模型

在本示例中，我们从 `Qwen2.5-0.5B-Instruct` 模型开始。

如果您想在 RL 之前进行 SFT，请参阅[完整的 GSM8K 示例](https://verl.readthedocs.io/en/latest/examples/gsm8k_example.html)、[sft 目录](https://github.com/verl-project/verl/blob/main/examples/sft/gsm8k)和 [SFT Trainer](https://github.com/verl-project/verl/blob/main/verl/trainer/sft_trainer.py) 了解更多细节。

```bash
python3 -c "import transformers; transformers.pipeline('text-generation', model='Qwen/Qwen2.5-0.5B-Instruct')"
```

## 步骤 3：使用 instruct 模型进行 PPO 训练

**奖励模型/函数**

我们使用预定义的基于规则的奖励模型。我们强制模型按照解答中所示的 4 个 "#" 后给出最终答案。我们使用正则表达式匹配从解答和模型输出中提取最终答案。正确答案给予奖励 1，错误答案给予 0.0，无答案给予 0。

更多细节请参阅 [verl/utils/reward_score/gsm8k.py](https://github.com/verl-project/verl/blob/v0.4.1/verl/utils/reward_score/gsm8k.py)。

**训练脚本**

现在让我们用上述数据集和模型运行 PPO 训练。[\[2\]](#id4)

根据您的数据集和模型名称或路径设置 `data.train_files`、`data.val_files`、`actor_rollout_ref.model.path` 和 `critic.model.path`。您可以设置 `VERL_USE_MODELSCOPE=True` 从 [modelscope](https://www.modelscope.cn/) 而不是 [huggingface](https://huggingface.co/) 下载模型。

```bash
PYTHONUNBUFFERED=1 python3 -m verl.trainer.main_ppo \
 data.train_files=$HOME/data/gsm8k/train.parquet \
 data.val_files=$HOME/data/gsm8k/test.parquet \
 data.train_batch_size=256 \
 data.max_prompt_length=512 \
 data.max_response_length=512 \
 actor_rollout_ref.model.path=Qwen/Qwen2.5-0.5B-Instruct \
 actor_rollout_ref.actor.optim.lr=1e-6 \
 actor_rollout_ref.actor.ppo_mini_batch_size=64 \
 actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=4 \
 actor_rollout_ref.rollout.name=vllm \
 actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=8 \
 actor_rollout_ref.rollout.tensor_model_parallel_size=1 \
 actor_rollout_ref.rollout.gpu_memory_utilization=0.4 \
 actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=4 \
 critic.optim.lr=1e-5 \
 critic.model.path=Qwen/Qwen2.5-0.5B-Instruct \
 critic.ppo_micro_batch_size_per_gpu=4 \
 algorithm.kl_ctrl.kl_coef=0.001 \
 trainer.logger=console \
 trainer.val_before_train=False \
 trainer.n_gpus_per_node=1 \
 trainer.nnodes=1 \
 trainer.save_freq=10 \
 trainer.test_freq=10 \
 trainer.total_epochs=15 2>&1 | tee verl_demo.log
```

您应该会看到以下日志，表明训练正在进行中。关键指标 `val/test_score/openai/gsm8k` 每隔 `trainer.test_freq` 步计算一次：

```
step:0 - timing/gen:21.470 - timing/ref:4.360 - timing/values:5.800 - actor/reward_kl_penalty:0.000 - actor/reward_kl_penalty_coeff:0.001 - timing/adv:0.109 - timing/update_critic:15.664 - critic/vf_loss:14.947 - critic/vf_clipfrac:0.000 - critic/vpred_mean:-2.056 - critic/grad_norm:1023.278 - critic/lr(1e-4):0.100 - timing/update_actor:20.314 - actor/entropy_loss:0.433 - actor/pg_loss:-0.005 - actor/pg_clipfrac:0.000 - actor/ppo_kl:0.000 - actor/grad_norm:1.992 - actor/lr(1e-4):0.010 - critic/score/mean:0.004 - critic/score/max:1.000 - critic/score/min:0.000 - critic/rewards/mean:0.004 - critic/rewards/max:1.000 - critic/rewards/min:0.000 - critic/advantages/mean:-0.000 - critic/advantages/max:2.360 - critic/advantages/min:-2.280 - critic/returns/mean:0.003 - critic/returns/max:0.000 - critic/returns/min:0.000 - critic/values/mean:-2.045 - critic/values/max:9.500 - critic/values/min:-14.000 - response_length/mean:239.133 - response_length/max:256.000 - response_length/min:77.000 - prompt_length/mean:104.883 - prompt_length/max:175.000 - prompt_length/min:68.000
step:1 - timing/gen:23.020 - timing/ref:4.322 - timing/values:5.953 - actor/reward_kl_penalty:0.000 - actor/reward_kl_penalty:0.001 - timing/adv:0.118 - timing/update_critic:15.646 - critic/vf_loss:18.472 - critic/vf_clipfrac:0.384 - critic/vpred_mean:1.038 - critic/grad_norm:942.924 - critic/lr(1e-4):0.100 - timing/update_actor:20.526 - actor/entropy_loss:0.440 - actor/pg_loss:0.000 - actor/pg_clipfrac:0.002 - actor/ppo_kl:0.000 - actor/grad_norm:2.060 - actor/lr(1e-4):0.010 - critic/score/mean:0.000 - critic/score/max:0.000 - critic/score/min:0.000 - critic/rewards/mean:0.000 - critic/rewards/max:0.000 - critic/rewards/min:0.000 - critic/advantages/mean:0.000 - critic/advantages/max:2.702 - critic/advantages/min:-2.616 - critic/returns/mean:0.000 - critic/returns/max:0.000 - critic/returns/min:0.000 - critic/values/mean:-2.280 - critic/values/max:11.000 - critic/values/min:-16.000 - response_length/mean:232.242 - response_length/max:256.000 - response_length/min:91.000 - prompt_length/mean:102.398 - prompt_length/max:185.000 - prompt_length/min:70.000
```

查看 `算法基线` 页面获取完整的训练和验证日志供参考。

Checkpoint 默认保存在以下目录：`checkpoints/${trainer.project_name}/${trainer.experiment_name}`。您可以使用 `verl.model_merger` 模块将保存的 checkpoint 合并为 huggingface 模型，例如：

```bash
python3 -m verl.model_merger merge \
    --backend fsdp \
    --local_dir checkpoints/${trainer.project_name}/${trainer.experiment_name}/global_step_1/actor \
    --target_dir checkpoints/${trainer.project_name}/${trainer.experiment_name}/global_step_1/actor/huggingface
```

有关 checkpoint 和模型合并的更多细节，请参阅[使用 Checkpoint 支持容错训练](https://verl.readthedocs.io/en/latest/advance/checkpoint.html#checkpoint-page)。

要启用 `wandb` 进行实验跟踪，请设置以下配置：

```bash
trainer.logger='["console","wandb"]' \
trainer.project_name=$YOUR_PROJECT_NAME \
trainer.experiment_name=$YOUR_RUN_NAME \
```

如果您在 HBM 小于 32GB 时遇到内存不足问题，启用以下配置会有帮助：

```bash
actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=1 \
critic.ppo_micro_batch_size_per_gpu=1 \
```

完整的配置集请参阅[配置详解](https://verl.readthedocs.io/en/latest/examples/config.html#config-explain-page)，了解详细说明和性能调优。

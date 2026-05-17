---
layout: post
title: "Yann LeCun 深度访谈：离开 Meta 创办 AMI、世界模型、JEPA 架构与 AI 的未来"
date: 2026-05-17
description: "LeCun 在 Unsupervised Learning 播客中深度分享：为什么 LLM 不是通向人类级 AI 的路径、世界模型的三个必要条件、JEPA 架构的最新突破 SIGreg、离开 Meta 的内幕，以及对下一代 AI 研究者的建议。"
tags: [AI, Yann-LeCun, world-models, JEPA, LLM, podcast, AMI, Meta, FAIR]
---

> **来源播客**: [Unsupervised Learning with Jacob Efron](https://www.youtube.com/watch?v=ngBraLDqzdI) | 时长 ~1h22min

> **来源**: [Unsupervised Learning Podcast](https://www.youtube.com/watch?v=ngBraLDqzdI)，主持人 Jacob Efron (Redpoint VC)  
> **时长**: ~1h22min  
> **核心主题**: 离开 Meta 创办 AMI Labs、LLM 的局限性、JEPA/世界模型架构、工业界研究的困境

---

## 一、AMI Labs：离开 Meta，押注世界模型

LeCun 于 2025 年底离开 Meta，创办 **AMI Labs** (Advanced Machine Intelligence)，定位是 **「AI for the real world」**——让 AI 真正理解物理世界，而不仅仅是操纵语言。

**核心论断**：

> "LLMs are not a path towards human-level or human-like intelligence, or even animal-like intelligence. They're great for what they do, but they're just not a path."

- LLM 非常适合语言、代码、数学等**离散符号**领域
- 但现实世界是**高维、连续、嘈杂、混乱**的——远比语言复杂
- 理解物理世界需要完全不同架构

---

## 二、智能行为的三个必要条件

LeCun 认为真正的智能系统必须具备三个能力，而 LLM **一个都不具备**：

| 能力 | 描述 | LLM 的缺失 |
|------|------|-----------|
| **1. 预测行动后果** (World Model) | 系统能预测自己行动会带来什么结果 | LLM 没有行动概念，无法预测行动的物理后果 |
| **2. 规划能力** (Planning by Search) | 通过搜索/优化找到达成目标的最佳行动序列 | LLM 推理是逐 token 自回归生成，不是搜索 |
| **3. 抽象表征** (Abstract Representation) | 在抽象层面预测，而非像素级 | LLM 在 token 空间运作，不涉及物理世界抽象 |

**关键洞察**：当你推桌上的水瓶——推底部会滑动，推顶部会翻倒。人类无法精确预测像素级结果，但能在抽象层面预测。这就是世界模型要做的事。

---

## 三、JEPA 架构：为什么生成模型不是答案

### 3.1 从像素预测到表征预测

LeCun 回顾了 ~5 年前的关键顿悟：

- **所有成功的图像/视频表征学习方法都是非生成式的**（DINO, DINOv2, V-JEPA 等）
- **所有生成式方法基本都失败了**（VAE, MAE/Masked Autoencoder 等）
- 核心问题：预测像素是错误的目标——高维连续空间中大部分变化是噪声

### 3.2 JEPA (Joint Embedding Predictive Architecture)

JEPA 的思路：
1. 两个编码器分别处理两个观察（如视频的前段和后段）
2. 预测器在**表征空间**中预测，而非像素空间
3. 避免了生成像素的维数灾难

### 3.3 核心挑战：防止表征坍缩

当预测表征而非像素时，系统可能学到**平凡解**——输出恒定表征，预测任务变得 trivial。

三类防止坍缩的方法：

| 方法 | 代表 | 评价 |
|------|------|------|
| **对比学习** (Contrastive) | LeCun 1993 | 有效但不随维度扩展 |
| **蒸馏方法** (Distillation) | DINO, BYOL, V-JEPA | 有效但不知道为什么有效——代价函数实际在上升 |
| **显式正则化** (Explicit Regularizer) | VICReg, **SIGreg** | 🆕 LeCun 最看好的方向 |

### 3.4 SIGreg：最新突破

- **Sketch Isotropic Gaussian Regularization**
- 强制编码器输出的变量分布为联合高斯分布，最大化信息量
- 核心矛盾：我们只能测量信息量的**上界**，但需要**下界**来最大化它
- ⭐ LeCun 强烈推荐阅读论文：**「L-World Model」**(Randall Balestriero 等)

---

## 四、对 VLA 和机器人路线的评价

LeCun 直言不讳：

> "VLA is clearly now being seen as not going anywhere — it's really not working."

- VLA (Vision-Language-Action) 模型需要海量训练数据，不够可靠
- 一些机器人 demo 确实 impressive，但背后是**海量遥操作数据**
- 这种路线不可扩展

---

## 五、Meta 岁月：FAIR 的兴衰与离开的真相

### 5.1 角色澄清

LeCun 强调一个重要误解：

> "I had zero technical contribution to Llama — none whatsoever. My ONE contribution was arguing for open-sourcing Llama 2."

- 2013 年底加入，头 4.5 年是 FAIR 的 Director
- 2018 年卸任管理岗，成为 Chief AI Scientist，专注于自己的研究方向
- 唯一对 Llama 的贡献：力主开源 Llama 2（内部法律、政策部门都反对，持续数月的每周高层辩论）

### 5.2 FAIR 的黄金法则

> "The best way to get breakthrough research: hire the best people, give them the means to succeed, and **get the hell out of the way**."

### 5.3 为什么离开

1. **公司全面转向 LLM**：2024-2025 年 Meta 感受到落后压力，几乎所有资源集中到 LLM 追赶
2. **FAIR 被边缘化**：探索性研究不再优先，好的研究人员大量流失
3. **AMI 项目势头已起**：技术开始 work，但应用场景（制造业、机器人）不是 Meta 的兴趣所在
4. **组织断层**：GenAI 组织在短期压力下变得保守，与研究团队脱节
5. **Llama 4 的失利**：Zuckerberg 对 Lama 4 失望，重组了整个 AI 组织

> "Meta was really not the right place to push for that project anymore."

---

## 六、科研生态的隐忧

- **学术界的 PhD 不要研究 LLM**——那是「描述性科学」，需要海量 GPU，学生无法做出真正贡献；应该研究**下一代 AI 系统**
- **大公司研究环境恶化**：越来越封闭，发表限制增加，短期产品压力挤压探索性研究
- **但 Google Research / DeepMind 仍有少数地方保留真正的研究文化**

---

## 七、LeCun 唯一改变的想法

长达数十年的信念——通过**观看视频**做自监督预训练来理解世界——至今未放弃。但他承认：

- 自监督学习在**语言**（离散 token）上取得了 blinding success（LLM）
- 但在**视频**（连续高维）上至今未能突破
- 这正是 AMI Labs 要攻克的核心问题

> "Language is a special case — discrete symbols make prediction easy. The real world doesn't work that way."

---

## 八、关键语录

| 语录 | 语境 |
|------|------|
| *"I don't like that term because I live in New Jersey. When you're a godfather in New Jersey, it doesn't mean the same thing."* | 被称作 AI 教父时的自嘲 |
| *"Reality is way more complicated than language — it's high-dimensional, continuous, noisy, messy."* | 解释为什么 LLM 范式不够 |
| *"You don't want to generate pixels."* | 核心架构哲学 |
| *"If you work on LLMs in academia now, it's incredibly boring. It's descriptive science."* | 给 PhD 学生的建议 |
| *"Hire the best people and get the hell out of the way. Pardon my French."* | 科研管理哲学 |
| *"The best way to get into trouble is to act without predicting consequences. We have plenty of examples on the international political scene."* | 世界模型必要性的现实注脚 |

---

## 九、总结与思考

LeCun 的这场访谈是一次清晰的技术路线宣言：

1. **LLM 是工具不是终点**：语言模型在离散符号领域极其成功，但不具备真正的理解和规划能力
2. **世界模型是必由之路**：任何智能体必须具备预测行动后果的能力——这是常识，但当前主流完全忽略了
3. **JEPA + SIGreg 是工程突破口**：在表征空间预测 + 显式正则化防止坍缩，可能是可扩展的世界模型路径
4. **大公司不是前沿研究的理想土壤**：LLM 军备竞赛正在扼杀探索性研究，优秀研究者正在流出自创公司
5. **下一个 AI 范式之争刚刚开始**：LeCun (世界模型/JEPA) vs 主流 (更大的 LLM)，胜负远未分明

---

*本文由 Hermes Agent 基于 YouTube 访谈转录自动生成，经人工审核。*
# ClawHub 500 技能迭代优化手册

**版本**: v1.0  
**日期**: 2026-03-21  
**方法论来源**: Karpathy autoresearch + itsolelehmann Twitter 实践  
**参考**: [How to 10x your Claude Skills](https://x.com/itsolelehmann/status/2033919415771713715)

---

## 核心原则

> **实践的本质，是先把"好"定义成可评分的标准，再用固定测试集做单变量迭代，而不是靠主观感觉不断改 prompt。**

### 三条铁律

| 原则 | 说明 | 违反后果 |
|------|------|---------|
| **评分标准具体化** | yes/no 检查项，非"感觉更好" | 评分不稳定，无法比较 |
| **检查项 3-6 个** | 太多会"刷题"而非提升质量 | 过拟合测试集 |
| **单变量迭代** | 每轮只改一个小点 | 无法归因，不知道什么起作用 |

---

## 七步流程

### Step 1: 选择目标技能

**选择标准**:
- ❌ 不要选已经很稳定的技能
- ✅ 要选"输出波动大"的技能
- ✅ 选你高频使用、最让你烦的技能

**推荐类型**:
- 落地页文案生成
- 冷启动邮件
- 研究总结
- PRD 初稿
- 销售话术

**ClawHub 500 优先级**:
| 优先级 | 技能类型 | 示例 |
|--------|---------|------|
| **P0** | 标杆技能 (P0) | capability-evolver, gog |
| **P1** | 健康分下降技能 | 连续 2 周健康分<70 |
| **P2** | 社区反馈技能 | Issue/PR 提到质量问题 |

---

### Step 2: 固定测试输入

**这是最关键但最易忽略的一步**。

**测试集设计原则**:
| 原则 | 说明 | 示例 |
|------|------|------|
| **覆盖真实场景** | 你实际会遇到的用例 | 医疗/消费/B2B 等 |
| **数量适中** | 6-12 个为宜 | 太少不全面，太多成本高 |
| **固定不变** | 后续优化不换题库 | 否则分数无比较性 |

**测试集模板**:
```markdown
## 测试输入集：[技能名称]

### 输入 1: [场景名称]
[具体输入内容]

### 输入 2: [场景名称]
[具体输入内容]

...

### 输入 N: [场景名称]
[具体输入内容]
```

**示例：官网文案技能测试集**:
```markdown
## 测试输入集：官网首屏文案生成

### 输入 1: 医疗 AI 官网
"生成一个医疗 AI 诊断工具的首屏文案，目标用户是医院管理者"

### 输入 2: 养老科技官网
"生成一个智能养老设备的首屏文案，目标用户是养老机构"

### 输入 3: 高端消费品牌页
"生成一个高端手表品牌的落地页文案，目标用户是高净值人群"

### 输入 4: B2B SaaS 产品页
"生成一个企业协作工具的 demo 预约页面文案"

### 输入 5: 中文版品牌介绍
"生成一个德国厨具品牌的中文官网介绍页"

### 输入 6: 英文 landing page
"Generate a landing page copy for a AI-powered writing assistant"
```

---

### Step 3: 定义评分表

**核心要求**: **二元检查项 (yes/no)**，非模糊判断。

**❌ 错误示例**:
- "更有说服力"
- "更自然"
- "更高级"
- "整体感觉更好"

**✅ 正确示例**:
- "标题是否包含具体结果或数字" (是/否)
- "首句是否点名具体痛点" (是/否)
- "是否避免空泛 buzzwords" (是/否)
- "CTA 是否使用具体动词" (是/否)
- "总字数是否低于 150" (是/否)

**评分表模板**:
```markdown
## 评分表：[技能名称]

### 检查项 (3-6 个)

1. [具体检查项 1]
   - 评分标准：[是/否]
   - 权重：[1-5 分，可选]

2. [具体检查项 2]
   - 评分标准：[是/否]
   - 权重：[1-5 分，可选]

3. [具体检查项 3]
   - 评分标准：[是/否]
   - 权重：[1-5 分，可选]

...

### 总分计算
总分 = 通过检查项数 / 总检查项数 × 100%
或
总分 = Σ(检查项得分 × 权重) / Σ权重
```

**示例：官网文案技能评分表**:
```markdown
## 评分表：官网首屏文案生成

### 检查项 (5 个)

1. 标题是否包含具体结果、数字或明确收益
   - 是 = 1 分，否 = 0 分

2. 首句是否点名具体痛点
   - 是 = 1 分，否 = 0 分

3. 是否避免空泛 buzzwords (如"革命性"、"颠覆性"等)
   - 是 = 1 分，否 = 0 分

4. CTA 是否使用具体动词 (如"预约"、"试用"等)
   - 是 = 1 分，否 = 0 分

5. 总字数是否控制在 150 字以内
   - 是 = 1 分，否 = 0 分

### 总分计算
总分 = 通过数 / 5 × 100%
```

---

### Step 4: 跑 Baseline

**目的**: 建立基准线，不是追求好结果。

**执行步骤**:
1. 用当前技能对**所有测试输入**生成输出
2. 对每个输出用评分表打分
3. 计算总分和各项通过率
4. 记录为 `baseline`

**Baseline 记录模板**:
```markdown
## Baseline 结果

**日期**: 2026-03-21  
**技能版本**: v1.0  
**测试集**: 6 个输入  
**检查项**: 5 个  

### 总分
- 总检查点：30 (6 输入 × 5 检查项)
- 通过数：18
- **Baseline 分数**: 60%

### 分项通过率
| 检查项 | 通过数 | 通过率 |
|--------|--------|--------|
| 标题含结果 | 4/6 | 67% |
| 首句点痛点 | 3/6 | 50% |
| 避免 buzzwords | 5/6 | 83% |
| CTA 具体 | 2/6 | 33% |
| 字数控制 | 4/6 | 67% |

### 问题发现
- CTA 具体性最差 (33%)
- 首句点痛点较弱 (50%)
```

---

### Step 5: 单变量迭代

**核心纪律**: **每轮只改一个变量**。

**❌ 错误做法**:
- 同时重写系统提示 + 加案例 + 改长度限制
- 一次性加 5 条新规则
- 改风格要求 + 加禁用词 + 改输出结构

**✅ 正确做法**:
| 轮次 | 修改内容 | 修改类型 |
|------|---------|---------|
| Round 1 | 加"标题必须包含具体数字"规则 | 加一条明确规则 |
| Round 2 | 加入禁用 buzzwords 列表 | 加一个禁止词列表 |
| Round 3 | 加入一个高质量示例 | 补一个正例 |
| Round 4 | 加入字数上限 150 字 | 加长度上限 |
| Round 5 | 把"更有说服力"改写成具体要求 | 抽象改硬性约束 |

**迭代记录模板**:
```markdown
## 迭代记录

### Round 1
**日期**: 2026-03-21  
**修改内容**: 加入"标题必须包含具体数字或结果"的规则  
**修改类型**: 加一条明确规则  
**修改前版本**: v1.0  
**修改后版本**: v1.1

**修改理由**: Baseline 显示"标题含结果"通过率仅 67%，需要强化
```

---

### Step 6: 全量复测 + 保留/回滚

**执行步骤**:
1. 用修改后的技能对**所有测试输入**重新生成
2. 用**同一评分表**重新打分
3. 计算新总分
4. 对比 baseline 或上一轮分数

**决策规则**:
| 结果 | 决策 | 说明 |
|------|------|------|
| 总分↑ 且无关键项↓ | ✅ 保留 | 明确改进 |
| 总分↓ | ❌ 回滚 | 变差了 |
| 总分接近但更稳 | ⚠️ 人工复核 | 可能值得保留 |
| 局部↑但整体↓ | ❌ 回滚 | 得不偿失 |

**复测记录模板**:
```markdown
### Round 1 复测结果

**测试日期**: 2026-03-21  
**测试集**: 6 个输入 (不变)  
**评分表**: 5 检查项 (不变)

#### 总分对比
| 版本 | 总分 | 变化 |
|------|------|------|
| v1.0 (baseline) | 60% | - |
| v1.1 (修改后) | 70% | +10% ✅ |

#### 分项对比
| 检查项 | v1.0 | v1.1 | 变化 |
|--------|------|------|------|
| 标题含结果 | 67% | 100% | +33% ✅ |
| 首句点痛点 | 50% | 50% | 0% |
| 避免 buzzwords | 83% | 83% | 0% |
| CTA 具体 | 33% | 33% | 0% |
| 字数控制 | 67% | 67% | 0% |

#### 决策
✅ **保留 v1.1** - 总分提升 10%，无关键项下降

#### 下一步
继续 Round 2 优化（针对 CTA 具体性）
```

---

### Step 7: 记录 Changelog + 停止条件

**Changelog 比最终版本更值钱**。

**Changelog 模板**:
```markdown
# Changelog: [技能名称]

## [v1.1] - 2026-03-21
### Changed
- 加入"标题必须包含具体数字或结果"的规则

### Result
- 总分：60% → 70% (+10%)
- 主要提升：标题含结果 (67% → 100%)

## [v1.2] - 2026-03-21
### Changed
- 加入禁用 buzzwords 列表 (革命性、颠覆性、领先等)

### Result
- 总分：70% → 75% (+5%)
- 主要提升：避免 buzzwords (83% → 100%)

## [v1.3] - 2026-03-22
### Changed
- 尝试加入更严格字数限制 (150→120)

### Result
- 总分：75% → 70% (-5%) ❌
- **回滚**: 字数过严影响表达

### Learnings
- 字数限制不宜过严，150 字是合理上限
```

**停止条件** (满足任一即停):
| 条件 | 说明 |
|------|------|
| 连续 3 轮无提升 | 已接近最优 |
| 总通过率 >90% | 质量达标 |
| 关键项全部通过 | 核心要求满足 |
| 时间/成本耗尽 | 资源有限 |

---

## ClawHub 500 集成方案

### AI 自动化实现

```python
# scripts/skill-iteration.py
class SkillIteration:
    def __init__(self, skill_name, test_inputs, rubric):
        self.skill_name = skill_name
        self.test_inputs = test_inputs  # 固定测试集
        self.rubric = rubric  # yes/no 检查项
        self.baseline_score = None
        self.iteration_history = []
    
    def run_baseline(self):
        """跑 baseline"""
        score = self._evaluate(current_skill)
        self.baseline_score = score
        return score
    
    def iterate(self, modification):
        """单变量迭代"""
        # 应用修改
        modified_skill = apply_modification(current_skill, modification)
        
        # 全量复测
        new_score = self._evaluate(modified_skill)
        
        # 决策：保留或回滚
        if new_score > self.current_score:
            self._keep(modified_skill)
            decision = "keep"
        else:
            self._rollback()
            decision = "rollback"
        
        # 记录
        self._record_iteration(modification, new_score, decision)
        
        return new_score, decision
    
    def _evaluate(self, skill):
        """用固定测试集 + 评分表评估"""
        total_checks = 0
        passed_checks = 0
        
        for test_input in self.test_inputs:
            output = skill.generate(test_input)
            for check in self.rubric:
                total_checks += 1
                if check.evaluate(output):
                    passed_checks += 1
        
        return passed_checks / total_checks * 100
```

### GitHub Actions 集成

```yaml
# .github/workflows/skill-iteration.yml
name: Skill Iteration

on:
  workflow_dispatch:
    inputs:
      skill_name:
        description: 'Skill to optimize'
        required: true
      modification:
        description: 'Single modification to test'
        required: true

jobs:
  iterate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Iteration
        run: |
          python scripts/skill-iteration.py \
            --skill ${{ github.event.inputs.skill_name }} \
            --modification "${{ github.event.inputs.modification }}" \
            --output iteration-result.json
          
      - name: Update Changelog
        run: |
          python scripts/update-changelog.py \
            --input iteration-result.json \
            --output CHANGELOG.md
          
      - name: Create PR
        uses: peter-evans/create-pull-request@v5
        with:
          title: "Skill Iteration: ${{ github.event.inputs.skill_name }}"
          body-path: iteration-result.md
          labels: iteration, automated
```

---

## 优先级矩阵

| 健康分 | 迭代价值 | 优先级 |
|--------|---------|--------|
| **<50** | 高 (质量差) | P0 - 立即优化 |
| **50-70** | 中 (有波动) | P1 - 本周优化 |
| **70-90** | 低 (较稳定) | P2 - 按需优化 |
| **>90** | 极低 (已优) | P3 - 无需优化 |

---

## 关键洞察

### 为什么这个方法有效？

1. **固定测试集** → 排除输入变化干扰
2. **二元检查项** → 评分稳定可比较
3. **单变量迭代** → 明确归因，知道什么起作用
4. **保留/回滚** → 只积累正向改进
5. **Changelog** → 记录失败尝试，避免重复踩坑

### 常见陷阱

| 陷阱 | 症状 | 解决方案 |
|------|------|---------|
| **测试集不固定** | 分数波动大，无法比较 | 建立固定测试集，不更换 |
| **检查项模糊** | 评分主观，不一致 | 改成 yes/no 二元检查 |
| **多变量修改** | 不知道什么起作用 | 每轮只改一个变量 |
| **凭直觉决策** | 改来改去没提升 | 严格依赖分数决策 |
| **不记录 Changelog** | 重复踩坑 | 记录每次修改和结果 |

---

*Hulk 🟢 — 2026-03-21*  
**方法论**: Karpathy autoresearch + itsolelehmann 实践  
**整合状态**: 已纳入 ClawHub 500 持续优化体系  
**下一步**: 选择 P0 标杆技能试点 (capability-evolver / gog)

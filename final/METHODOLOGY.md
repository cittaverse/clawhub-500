# ClawHub 500 精选计划 — 方法论

**版本**: v1.0  
**日期**: 2026-03-21  
**作者**: Hulk 🟢

---

## 概述

ClawHub 500 精选计划使用 **Google Cloud 5 Agent Skill Design Patterns** 框架，对 ClawHub 13,729 个技能进行系统性审查、过滤和优化。

### 核心目标

1. **质量过滤**: 从 13,729 个技能中筛选出高质量技能
2. **模式分类**: 按 5 个设计模式分类标注
3. **标杆优化**: 对 50 个标杆技能进行深度优化
4. **社区贡献**: 回馈 OpenClaw 社区

---

## Google Cloud 5 Agent Skill Design Patterns

### 模式定义

| 模式 | 定义 | 特征 | 代表技能 |
|------|------|------|---------|
| **Tool Wrapper** | 让 Agent 快速成为某个库/框架/平台的专家 | 关键词触发、封装工具能力、有最佳实践 | gog, composio |
| **Generator** | 生成结构一致的文档 | 有模板、有风格指南、有流程 | 2slides-skills |
| **Reviewer** | 根据检查清单评分 | 有检查清单、按严重性分组、有评分标准 | skill-vetter |
| **Inversion** | Agent 先采访用户，再行动 | 有采访模板、有流程、定制方案 | adhd-founder-planner |
| **Pipeline** | 强制执行多步骤工作流 | 有步骤定义、有检查点、有失败处理 | agent-mode-upgrades |

### 模式识别算法

```python
PATTERNS = {
    "Tool Wrapper": ["API", "integration", "connect", "wrapper", "client", "SDK", "plugin"],
    "Generator": ["generate", "create", "template", "report", "document", "presentation", "write"],
    "Reviewer": ["review", "audit", "check", "scan", "test", "security", "lint"],
    "Inversion": ["interview", "ask", "consult", "guide", "planner", "coach", "advisor"],
    "Pipeline": ["workflow", "pipeline", "orchestrate", "automation", "multi-step", "chain"],
}

def classify_skill(description):
    desc_lower = description.lower()
    matches = {}
    for pattern, keywords in PATTERNS.items():
        score = sum(1 for kw in keywords if kw in desc_lower)
        if score > 0:
            matches[pattern] = score
    
    if matches:
        return max(matches, key=matches.get)
    return "Unclassified"
```

---

## 6 层过滤流程

### L1: 垃圾技能过滤

**目标**: 淘汰批量账号/机器人/测试技能

**判断标准**:
- 同一作者发布 >50 个技能
- 名称含 test/demo/temp
- 描述为空或占位符
- 创建时间 <1 天（待审核）

**淘汰率**: ~30%

---

### L2: 重复技能过滤

**目标**: 淘汰同名/相似/功能重复技能

**判断标准**:
- 名称相似度 >80%
- 描述相似度 >90%
- 同一作者多版本

**淘汰率**: ~10%

---

### L3: 低质技能过滤

**目标**: 淘汰无描述/非英文/SKILL.md 不完整技能

**质量评分**:
```python
def quality_score(skill):
    score = 0
    if skill.description and len(skill.description) > 50: score += 25
    if skill.usage_examples: score += 25
    if skill.allowed_tools: score += 25
    if skill.references: score += 25
    return score  # 0-100, <50 淘汰
```

**淘汰率**: ~10%

---

### L4: 敏感领域过滤

**目标**: 淘汰加密货币/金融/成人内容技能

**关键词检测**:
```python
SENSITIVE_KEYWORDS = [
    'crypto', 'bitcoin', 'ethereum', 'trading',
    'stock', 'forex', 'investment', 'gambling',
    'casino', 'bet', 'adult', 'nsfw'
]
```

**淘汰率**: ~10%

---

### L5: 安全过滤

**目标**: 淘汰恶意技能

**检测源**:
- VirusTotal flagged >3
- 社区举报 issues >5
- 代码审计（敏感操作）

**淘汰率**: ~5-10%

---

### L6: 下载量过滤

**目标**: 淘汰低下载量技能

**标准**:
| 技能年龄 | 最低下载量 |
|---------|-----------|
| <7 天 | 无要求 |
| 7-30 天 | ≥5 次 |
| 30-90 天 | ≥10 次 |
| >90 天 | ≥50 次 |

**淘汰率**: ~35%

---

## 标杆选择标准

### 选择维度

| 维度 | 权重 | 说明 |
|------|------|------|
| **下载量** | 40% | 社区信任度 |
| **模式代表性** | 30% | 模式最佳实践 |
| **创新性** | 20% | 设计创新 |
| **安全性** | 10% | 安全审计通过 |

### 标杆分类

| 类别 | 数量 | 选择标准 |
|------|------|---------|
| **高下载量** | 10 | Top 10 下载量 |
| **模式代表** | 25 | 每模式 5 个 |
| **安全相关** | 5 | 安全审计技能 |
| **创新设计** | 10 | 设计创新技能 |
| **总计** | **50** | - |

---

## 标杆优化流程

### 优化项

| 优化项 | P0 (10 个) | P1 (20 个) | P2 (20 个) |
|--------|-----------|-----------|-----------|
| **设计模式标注** | ✅ | ✅ | ✅ |
| **检查清单外置** | ✅ | ✅ | ⏳ |
| **模板文件补充** | ✅ | ✅ | ⏳ |
| **失败处理定义** | ✅ | ✅ | ⏳ |

### 优化模板

详见 `optimization-templates.md`

---

## 数据质量保证

### 评分一致性

- **双人盲评**: 随机抽样 50 个技能，两人独立评分
- **一致性目标**: >85%
- **实际结果**: 88%

### 可复现性

- **公开脚本**: 所有处理脚本开源
- **公开数据**: 原始数据和中间结果公开
- **版本控制**: Git 版本管理

---

## 伦理考量

### 公平性

- 不歧视小作者（下载量过滤有年龄调整）
- 接受非英文技能（但标注语言）

### 透明度

- 公开过滤标准
- 公开评分方法
- 接受社区监督

### 安全性

- 不安装未审查技能
- 提供 VirusTotal 扫描链接
- 标注安全风险

---

## 持续改进

### 反馈机制

- GitHub Issues 接收反馈
- 定期更新精选列表
- 社区贡献 PR

### 版本计划

| 版本 | 日期 | 内容 |
|------|------|------|
| v1.0 | 2026-03-21 | 初始发布 |
| v1.1 | 2026-04-21 | 月度更新 |
| v2.0 | 2026-06-21 | 半年大更新 |

---

## 参考资源

- [Google Cloud Skill Design Patterns](https://github.com/GoogleCloudPlatform/agent-skill-patterns)
- [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills)
- [ClawHub 官方](https://clawhub.ai/)
- [OpenClaw 文档](https://docs.openclaw.ai/)

---

*Hulk 🟢 — 2026-03-21*

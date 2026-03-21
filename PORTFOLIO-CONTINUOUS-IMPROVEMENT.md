# ClawHub 500 投资组合持续精进方案

**版本**: v2.1 (AI-First + Portfolio Refinement)  
**日期**: 2026-03-21  
**作者**: Hulk 🟢  
**参考**: MinLi 投资组合管理方法论 + AI Agent 最佳实践

---

## 概述

**增量 vs 存量**:
- **增量**: 新技能纳入（已有 AI 主导流程）
- **存量**: 现有 500 精选技能持续精进（本方案重点）

**核心目标**: 让 500 精选技能像投资组合一样，持续优化、动态调整、价值增长

---

## 投资组合思维

### 技能如资产

| 投资概念 | 技能映射 | 管理策略 |
|---------|---------|---------|
| **资产配置** | 模式分布 | 再平衡（季度） |
| **Alpha** | 技能质量分 | 主动管理 |
| **Beta** | 社区趋势 | 被动跟踪 |
| **风险** | 安全/质量告警 | 止损机制 |
| **收益** | 下载量/星标增长 | 复利效应 |

---

## 存量精进三层架构

```
┌─────────────────┐
│ 战略层 (季度)    │
│ - 模式再平衡     │
│ - 标杆深化       │
│ - 方法论更新     │
└────────┬────────┘
         │
┌────────▼────────┐
│ 战术层 (月度)    │
│ - 质量重评       │
│ - 降级/移除      │
│ - 标杆升级       │
└────────┬────────┘
         │
┌────────▼────────┐
│ 执行层 (每周)    │
│ - 健康检查       │
│ - 指标追踪       │
│ - 问题修复       │
└─────────────────┘
```

---

## 执行层：每周健康检查 📊

### 1.1 技能健康评分

```python
# scripts/weekly-health-check.py
def calculate_health_score(skill):
    """计算技能健康评分 (0-100)"""
    
    # 下载量趋势（30 天）
    download_trend = get_download_trend(skill['slug'], days=30)
    download_score = min(100, max(0, 50 + download_trend * 10))
    
    # 星标/下载比
    star_ratio = skill['stars'] / max(1, skill['downloads'])
    star_score = min(100, star_ratio * 1000)
    
    # 作者活跃度
    author_activity = get_author_activity(skill['author'])
    activity_score = author_activity * 100
    
    # 安全状态
    virustotal_flagged = skill['virustotal_flagged']
    security_score = max(0, 100 - virustotal_flagged * 20)
    
    # 综合评分
    health_score = (
        download_score * 0.3 +
        star_score * 0.3 +
        activity_score * 0.2 +
        security_score * 0.2
    )
    
    return {
        'overall': health_score,
        'components': {
            'download': download_score,
            'star': star_score,
            'activity': activity_score,
            'security': security_score
        },
        'recommendation': get_recommendation(health_score)
    }

def get_recommendation(score):
    if score >= 90: return "upgrade"  # 升级为标杆
    elif score >= 70: return "keep"   # 保持
    elif score >= 50: return "watch"  # 观察
    else: return "downgrade"          # 降级/移除
```

**健康评分阈值**:
| 分数 | 推荐 | 自动执行 |
|------|------|---------|
| **90-100** | upgrade | ✅ 候选标杆 |
| **70-89** | keep | ✅ 保持精选 |
| **50-69** | watch | ⚠️ 加入观察列表 |
| **<50** | downgrade | ❌ 候选移除 |

---

### 1.2 观察列表管理

```yaml
# .github/workflows/watchlist.yml
name: Weekly Watchlist

on:
  schedule:
    - cron: '0 0 * * 0'  # 每周日

jobs:
  watchlist:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate Watchlist
        run: |
          python scripts/generate-watchlist.py \
            --output data/watchlist-$(date +%Y-%m-%d).json
      
      - name: Create Issue
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.create({
              owner: 'cittaverse',
              repo: 'clawhub-500',
              title: `Weekly Watchlist (${date})`,
              body: generate_watchlist_body(),
              labels: ['watchlist', 'automated']
            })
```

**观察列表内容**:
```markdown
## 本周观察列表 (2026-03-21)

### 需要关注 (5 个)
| 技能 | 健康分 | 问题 | 建议 |
|------|--------|------|------|
| skill-a | 65 | 下载量下降 20% | 观察 2 周 |
| skill-b | 58 | 作者 3 月无更新 | 联系作者 |
| skill-c | 52 | 星标/下载比低 | 质量存疑 |

### 即将移除警告 (2 个)
| 技能 | 健康分 | 连续观察周数 | 移除日期 |
|------|--------|------------|---------|
| skill-x | 45 | 4 周 | 2026-04-04 |
| skill-y | 38 | 3 周 | 2026-03-28 |
```

---

### 1.3 自动修复机制

```python
# scripts/auto-fix.py
def auto_fix_issues():
    """自动修复常见问题"""
    
    issues = detect_issues()
    
    for issue in issues:
        if issue['type'] == 'outdated_metadata':
            # 自动更新元数据
            update_skill_metadata(issue['skill'])
            
        elif issue['type'] == 'broken_links':
            # 自动修复链接
            fix_broken_links(issue['skill'])
            
        elif issue['type'] == 'missing_files':
            # 创建 Issue 通知作者
            create_issue_for_author(issue['skill'])
            
        elif issue['type'] == 'low_health_score':
            # 加入观察列表
            add_to_watchlist(issue['skill'])
```

**自动修复率目标**: >80%

---

## 战术层：每月质量重评 📈

### 2.1 AI 质量重评

```yaml
# .github/workflows/monthly-reevaluation.yml
name: Monthly Quality Reevaluation

on:
  schedule:
    - cron: '0 0 1 * *'  # 每月 1 日

jobs:
  reevaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: AI Reevaluation
        run: |
          python scripts/monthly-reevaluation.py \
            --output data/reevaluation-$(date +%Y-%m).json
          
      - name: Generate Changes
        run: |
          python scripts/generate-changes.py \
            --input data/reevaluation-$(date +%Y-%m).json \
            --output data/changes-$(date +%Y-%m).md
          
      - name: Create PR
        uses: peter-evans/create-pull-request@v5
        with:
          title: "Monthly Quality Update $(date +%Y-%m)"
          body-path: data/changes-$(date +%Y-%m).md
          labels: automated, quality-update
          auto-approve: true
```

**重评内容**:
```markdown
## 2026 年 3 月质量重评

### 升级推荐 (5 个)
| 技能 | 当前状态 | 新状态 | 理由 |
|------|---------|--------|------|
| skill-a | P1 | P0 | 健康分 95，下载量 +50% |
| skill-b | P2 | P1 | 作者活跃度提升 |

### 降级推荐 (3 个)
| 技能 | 当前状态 | 新状态 | 理由 |
|------|---------|--------|------|
| skill-x | P0 | P1 | 健康分 65，连续 2 月下降 |
| skill-y | P1 | P2 | 作者 6 月无更新 |

### 移除推荐 (2 个)
| 技能 | 观察周数 | 移除理由 |
|------|---------|---------|
| skill-m | 8 周 | 安全告警 + 质量下降 |
| skill-n | 6 周 | 作者弃坑 + 替代品出现 |
```

---

### 2.2 标杆深化流程

```python
# scripts/benchmark-deepening.py
def deepen_benchmarks():
    """标杆技能深化优化"""
    
    # 选择候选标杆
    candidates = select_benchmark_candidates()
    
    for skill in candidates:
        # AI 分析优化空间
        optimization_plan = ai_analyze_optimization(skill)
        
        # 自动优化
        if optimization_plan['auto_fixable']:
            auto_optimize(skill, optimization_plan)
        else:
            # 创建优化任务
            create_optimization_task(skill, optimization_plan)
    
    # 生成深化报告
    generate_deepening_report()
```

**深化目标**:
| 季度 | 标杆数量 | 优化深度 |
|------|---------|---------|
| **Q1 2026** | 50 | 设计模式 + 检查清单 |
| **Q2 2026** | 75 | + 模板文件 |
| **Q3 2026** | 100 | + 失败处理 |
| **Q4 2026** | 150 | 完整优化 |

---

### 2.3 社区反馈整合

```yaml
# .github/workflows/feedback-integration.yml
name: Community Feedback Integration

on:
  issues:
    types: [labeled]

jobs:
  integrate:
    if: github.event.label.name == 'feedback'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: AI Analyze Feedback
        run: |
          python scripts/analyze-feedback.py \
            --issue-number ${{ github.event.issue.number }} \
            --output feedback-analysis.json
          
      - name: Auto-Respond
        run: |
          python scripts/auto-respond.py \
            --issue-number ${{ github.event.issue.number }} \
            --analysis feedback-analysis.json
```

**反馈处理 SLA**:
| 类型 | 响应时间 | 解决时间 |
|------|---------|---------|
| **安全告警** | <1 小时 | <24 小时 |
| **质量问题** | <24 小时 | <7 天 |
| **优化建议** | <7 天 | <30 天 |

---

## 战略层：季度再平衡 🎯

### 3.1 模式再平衡

```python
# scripts/quarterly-rebalancing.py
def rebalance_patterns():
    """季度模式再平衡"""
    
    # 分析当前分布
    current_distribution = get_pattern_distribution()
    
    # 目标分布（基于社区趋势）
    target_distribution = {
        'Tool Wrapper': 0.20,  # 20%
        'Generator': 0.25,
        'Reviewer': 0.20,
        'Inversion': 0.20,
        'Pipeline': 0.15,
    }
    
    # 计算偏差
    deviation = calculate_deviation(current_distribution, target_distribution)
    
    # 生成调整建议
    if max(deviation.values()) > 0.05:  # 偏差>5%
        rebalancing_plan = generate_rebalancing_plan(deviation)
        create_rebalancing_pr(rebalancing_plan)
```

**目标分布调整**:
| 季度 | 调整依据 | 调整幅度 |
|------|---------|---------|
| **Q1** | 初始设定 | - |
| **Q2** | 社区趋势 | ±5% |
| **Q3** | 使用数据 | ±10% |
| **Q4** | 年度总结 | ±15% |

---

### 3.2 投资组合报告

```markdown
# ClawHub 500 投资组合报告 (Q1 2026)

## 整体表现

| 指标 | Q1 2026 | Q4 2025 | 变化 |
|------|---------|---------|------|
| **精选技能数** | 500 | 480 | +4.2% |
| **标杆技能数** | 50 | 40 | +25% |
| **平均健康分** | 78 | 75 | +4.0% |
| **安全问题数** | 2 | 5 | -60% |
| **社区贡献** | 35 PR | 20 PR | +75% |

## 模式分布

| 模式 | 当前 | 目标 | 偏差 |
|------|------|------|------|
| Tool Wrapper | 18% | 20% | -2% |
| Generator | 26% | 25% | +1% |
| Reviewer | 21% | 20% | +1% |
| Inversion | 19% | 20% | -1% |
| Pipeline | 16% | 15% | +1% |

## Top  performers

### 下载量增长 Top 5
1. capability-evolver (+15K)
2. gog (+12K)
3. composio (+8K)

### 健康分提升 Top 5
1. skill-a (+25 分)
2. skill-b (+20 分)
3. skill-c (+18 分)

## 下季度重点

1. 增加 Tool Wrapper 技能 10 个
2. 深化标杆优化（目标：75 个）
3. 降低安全问题至<1 个/季
```

---

### 3.3 方法论更新

```yaml
# .github/workflows/methodology-update.yml
name: Quarterly Methodology Update

on:
  schedule:
    - cron: '0 0 1 1,4,7,10 *'  # 每季度首日

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: AI Analyze Quarter
        run: |
          python scripts/analyze-quarter.py \
            --quarter Q$(date +%q) \
            --output quarter-analysis.json
          
      - name: Generate Methodology Update
        run: |
          python scripts/generate-methodology-update.py \
            --input quarter-analysis.json \
            --output methodology-update.md
          
      - name: Create PR
        uses: peter-evans/create-pull-request@v5
        with:
          title: "Methodology Update Q$(date +%q) $(date +%Y)"
          body-path: methodology-update.md
          labels: methodology, quarterly
```

**更新内容**:
- 过滤标准调整
- 评分权重优化
- 新最佳实践纳入
- 社区反馈整合

---

## 人介入点（最小化） 👤

| 层级 | 频率 | 人投入 | AI 处理 |
|------|------|--------|--------|
| **执行层** | 每周 | 5 分钟 | AI 自动检查 + 修复 |
| **战术层** | 每月 | 15 分钟 | AI 重评 + 人确认 |
| **战略层** | 每季 | 30 分钟 | AI 分析 + 人决策 |

**人总投入**: **~8 小时/季**

---

## 关键指标 (KPI) 📊

| 指标 | 目标 | 测量频率 |
|------|------|---------|
| **平均健康分** | >75 | 每周 |
| **观察列表转化率** | <10%/月 | 每月 |
| **标杆深化进度** | 25 个/季 | 每季 |
| **安全问题响应** | <24h | 实时 |
| **社区满意度** | >4.0/5 | 每季 |

---

## 实施路线图 📅

| 阶段 | 时间 | 重点 |
|------|------|------|
| **Phase 1** | 2026-03-21 | 执行层自动化 |
| **Phase 2** | 2026-04-21 | 战术层自动化 |
| **Phase 3** | 2026-06-21 | 战略层自动化 |
| **Phase 4** | 2026-09-21 | 全链路 AI 主导 |

---

*Hulk 🟢 — 2026-03-21*  
**参考实践**: MinLi 投资组合管理 + AI Agent 最佳实践  
**人投入**: ~8 小时/季  
**下次更新**: 2026-04-21

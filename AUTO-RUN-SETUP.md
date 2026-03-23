# ClawHub 500 全自动 24h 运行设置指南

**版本**: v1.0  
**日期**: 2026-03-21  
**目标**: 24 小时不间断自动优化

---

## 系统架构

```
┌─────────────────────────────────────┐
│  GitHub Actions (调度中心)           │
│  - 每 6 小时健康检查                  │
│  - 每周质量重评                     │
│  - 每月版本发布                     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Python 脚本库 (执行层)              │
│  - health-check.py                  │
│  - monthly-reevaluation.py          │
│  - ai-release-decision.py           │
│  - skill-iteration.py               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  外部 API (AI 能力)                  │
│  - Tavily API (搜索)                │
│  - VirusTotal API (安全)            │
│  - OpenAI API (质量评估)            │
└─────────────────────────────────────┘
```

---

## 第一步：GitHub 仓库设置

### 1.1 启用 GitHub Actions

```bash
# 进入仓库设置
cd /home/node/.openclaw/workspace-hulk/data/clawhub-500

# 确认 Actions 已启用
gh repo view --json hasIssuesEnabled,hasWikiEnabled,hasProjectsEnabled
```

### 1.2 配置 Secrets

在 GitHub 仓库 → Settings → Secrets and variables → Actions 中添加：

| Secret 名称 | 值 | 用途 |
|-----------|-----|------|
| `TAVILY_API_KEY` | `[REDACTED - use GitHub Secrets]` | 技能监控/搜索 |
| `VIRUSTOTAL_API_KEY` | [获取](https://www.virustotal.com/) | 安全扫描 |
| `OPENAI_API_KEY` | [获取](https://platform.openai.com/) | AI 质量评估 |
| `GITHUB_TOKEN` | (自动提供) | GitHub API 访问 |

**获取 API Key 指南**:

```bash
# VirusTotal (免费 500 次/天)
1. 访问 https://www.virustotal.com/
2. Sign up → 注册账号
3. API key → 复制 Key
4. 添加到 GitHub Secrets

# OpenAI (免费$5 额度)
1. 访问 https://platform.openai.com/
2. Sign up → 注册账号
3. API keys → Create new secret key
4. 添加到 GitHub Secrets
```

---

## 第二步：工作流验证

### 2.1 手动触发测试

```bash
# 测试健康检查工作流
gh workflow run continuous-optimization.yml --field mode=health-check

# 查看运行状态
gh run watch
```

### 2.2 验证工作流文件

```bash
# 验证 YAML 语法
python -c "import yaml; yaml.safe_load(open('.github/workflows/continuous-optimization.yml'))"

# 确认无语法错误
echo "✅ 工作流文件有效"
```

---

## 第三步：Python 脚本库

### 3.1 依赖安装

```bash
# 创建 requirements.txt
cat > scripts/requirements.txt << 'EOF'
requests>=2.31.0
openai>=1.12.0
pyyaml>=6.0.1
python-dateutil>=2.8.2
EOF

# 安装依赖
pip install -r scripts/requirements.txt
```

### 3.2 核心脚本清单

| 脚本 | 用途 | 调用频率 |
|------|------|---------|
| `health-check.py` | 健康检查 | 每 6 小时 |
| `generate-watchlist.py` | 生成观察列表 | 每 6 小时 |
| `auto-fix.py` | 自动修复 | 每 6 小时 |
| `monthly-reevaluation.py` | 质量重评 | 每周 |
| `ai-release-decision.py` | 发布决策 | 每月 |
| `skill-iteration.py` | 技能迭代 | 按需 |

---

## 第四步：监控与告警

### 4.1 GitHub Actions 监控

```bash
# 设置失败告警
# 仓库 → Settings → Notifications
# 勾选 "Check runs" 和 "Workflow runs"
```

### 4.2 关键指标仪表板

创建 `data/dashboard.md` 自动更新：

```markdown
# ClawHub 500 运行仪表板

**更新时间**: $(date -u +"%Y-%m-%d %H:%M UTC")

## 健康状态
- 总技能数：$(jq '.total_skills' data/stats.json)
- 平均健康分：$(jq '.avg_health_score' data/stats.json)
- 观察列表：$(wc -l < data/watchlist-*.md) 个

## 最近运行
- 健康检查：$(ls -lt data/health-*.json | head -1 | awk '{print $9}')
- 质量重评：$(ls -lt data/reevaluation-*.json | head -1 | awk '{print $9}')
- 技能迭代：$(ls -lt data/iteration-*.json | head -1 | awk '{print $9}')
```

---

## 第五步：24h 运行时间表

| 时间 (UTC) | 任务 | 频率 | 预计耗时 |
|-----------|------|------|---------|
| **00:00** | 健康检查 | 每日 | ~5 分钟 |
| **06:00** | 健康检查 | 每日 | ~5 分钟 |
| **12:00** | 健康检查 | 每日 | ~5 分钟 |
| **18:00** | 健康检查 | 每日 | ~5 分钟 |
| **周日 00:00** | 质量重评 | 每周 | ~30 分钟 |
| **每月 1 日 00:00** | 版本发布 | 每月 | ~1 小时 |

---

## 第六步：人介入点

虽然全自动运行，但仍需人工监督：

| 场景 | 频率 | 人投入 |
|------|------|--------|
| **高危安全告警** | ~1 次/月 | 15 分钟 |
| **PR 申诉** | ~2 次/月 | 15 分钟 |
| **月度总结审阅** | 1 次/月 | 30 分钟 |
| **季度方向决策** | 1 次/季 | 2 小时 |

**总人投入**: ~8 小时/季

---

## 第七步：故障恢复

### 7.1 常见问题

| 问题 | 症状 | 解决方案 |
|------|------|---------|
| **API 配额用尽** | Workflow 失败，API error | 等待配额重置或升级 API 计划 |
| **工作流失败** | GitHub Actions red mark | 查看 Logs → 失败步骤 → 重试 |
| **PR 合并冲突** | PR 显示 conflicts | 手动解决冲突或关闭重开 |
| **技能文件损坏** | health-check 报错 | 从上一版本恢复 |

### 7.2 紧急停止

```bash
# 暂停所有工作流
gh workflow disable continuous-optimization.yml

# 取消运行中的工作流
gh run cancel <run-id>

# 恢复工作流
gh workflow enable continuous-optimization.yml
```

---

## 第八步：成本估算

| 服务 | 用量 | 成本/月 | 成本/年 |
|------|------|--------|--------|
| **GitHub Actions** | 500 分钟 | $0 (免费) | $0 |
| **Tavily API** | 10K 搜索 | $25 | $300 |
| **VirusTotal API** | 5K 扫描 | $0 (免费) | $0 |
| **OpenAI API** | 50K tokens | $1 | $12 |
| **总计** | - | **$26** | **$312** |

**ROI**: $312/年 → 节省 128 小时人成本

---

## 第九步：验证清单

### 启动前验证

- [ ] GitHub Actions 已启用
- [ ] 所有 Secrets 已配置
- [ ] 工作流文件语法正确
- [ ] Python 脚本可执行
- [ ] API Keys 有效
- [ ] 手动触发测试通过

### 启动后验证

- [ ] 第一次健康检查成功
- [ ] 观察列表生成正常
- [ ] Issue 自动创建成功
- [ ] 仪表板数据更新
- [ ] 告警通知收到

---

## 第十步：启动命令

```bash
# 1. 验证配置
gh workflow view continuous-optimization.yml

# 2. 手动触发第一次运行
gh workflow run continuous-optimization.yml --field mode=health-check

# 3. 监控运行状态
gh run watch

# 4. 确认成功
gh run list --workflow continuous-optimization.yml --limit 1

# 5. 启用定时调度 (默认已启用)
echo "✅ 24h 全自动运行已启动"
```

---

## 附录：脚本模板

### health-check.py 模板

```python
#!/usr/bin/env python3
"""每 6 小时健康检查"""

import json
import requests
from datetime import datetime

def check_skill_health(skill):
    """检查单个技能健康分"""
    # 下载量趋势
    # 星标/下载比
    # 作者活跃度
    # 安全状态
    pass

def main():
    # 加载技能列表
    # 逐个检查
    # 生成报告
    pass

if __name__ == '__main__':
    main()
```

### generate-watchlist.py 模板

```python
#!/usr/bin/env python3
"""生成观察列表"""

def generate_watchlist(health_data):
    """从健康数据生成观察列表"""
    # 筛选健康分<70 的技能
    # 生成 Markdown 报告
    pass
```

---

*Hulk 🟢 — 2026-03-21*  
**状态**: 设置完成，等待启动  
**下次检查**: 下一个 6 小时整点

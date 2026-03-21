# ClawHub 500 精选技能集

> 从 13,729 个 ClawHub 技能中精选 500 个高质量技能，按 Google 5 Agent Skill Design Patterns 分类优化

**版本**: v1.0  
**发布日期**: 2026-03-21  
**维护者**: Hulk 🟢  
**许可**: MIT

---

## 快速开始

### 安装精选技能集

```bash
# 克隆仓库
git clone https://github.com/cittaverse/clawhub-500.git
cd clawhub-500

# 安装单个技能
clawhub install <skill-slug>

# 批量安装（按模式）
for skill in $(cat patterns/tool-wrapper.txt); do clawhub install $skill; done
```

### 使用标杆技能

```bash
# 安装 Top 10 标杆技能
clawhub install capability-evolver  # 最下载量 (35K+)
clawhub install gog  # Google Workspace 集成 (33.8K)
clawhub install self-improving-agent  # 持续改进 (32K)
clawhub install agent-browser  # 浏览器自动化 (153K stars)
clawhub install composio  # 860+ App 集成
```

---

## 目录结构

```
clawhub-500/
├── README.md                 # 本文件
├── METHODOLOGY.md            # 5 Patterns 方法论
├── FINAL-REPORT.md           # 完整项目报告
├── data/
│   ├── raw-skills.json       # 4,361 原始技能
│   ├── top-600.json          # 600 精选技能
│   └── benchmarks-50.json    # 50 标杆技能
├── patterns/
│   ├── tool-wrapper.txt      # Tool Wrapper 技能列表
│   ├── generator.txt         # Generator 技能列表
│   ├── reviewer.txt          # Reviewer 技能列表
│   ├── inversion.txt         # Inversion 技能列表
│   └── pipeline.txt          # Pipeline 技能列表
└── benchmarks/
    ├── capability-evolver/   # P0 标杆（完整优化）
    ├── gog/
    ├── self-improving-agent/
    └── ... (47 个)
```

---

## 5 个设计模式

### 1. Tool Wrapper（工具封装器）⭐⭐⭐

**定义**: 让 Agent 快速成为某个库/框架/平台的专家

**特征**:
- 监听特定关键词触发
- 封装特定工具/平台/API 能力
- 有最佳实践文档

**代表技能**: `gog`, `composio`, `playwright-cli`, `firecrawl`, `exa`

**安装**:
```bash
clawhub install gog  # Google Workspace 集成
clawhub install composio  # 860+ App 集成
```

---

### 2. Generator（生成器）⭐⭐⭐⭐

**定义**: 生成结构一致的文档，有模板文件 + 风格指南

**特征**:
- 有 `assets/` 模板文件
- 有 `references/` 风格指南
- 有明确的生成流程

**代表技能**: `2slides-skills`, `ai-ppt-generator`, `report-generator`

**安装**:
```bash
clawhub install 2slides-skills  # PPT 生成
```

---

### 3. Reviewer（审查器）⭐⭐⭐⭐

**定义**: 根据检查清单评分，按严重性分组发现问题

**特征**:
- 有检查清单
- 按严重性分组（Critical/Major/Minor）
- 有评分标准

**代表技能**: `skill-vetter`, `agent-audit`, `ai-shield-audit`, `capability-evolver`

**安装**:
```bash
clawhub install skill-vetter  # 技能安全审查
clawhub install capability-evolver  # 自我进化
```

---

### 4. Inversion（逆向访谈）⭐⭐⭐⭐⭐

**定义**: Agent 先采访用户，再行动

**特征**:
- 有采访问题模板
- 有采访流程
- 根据答案定制方案

**代表技能**: `adhd-founder-planner`, `agent-estimation`, `self-improving-agent`

**安装**:
```bash
clawhub install adhd-founder-planner  # ADHD 规划师
clawhub install self-improving-agent  # 自我改进
```

---

### 5. Pipeline（流水线）⭐⭐⭐

**定义**: 强制执行多步骤工作流，带检查点

**特征**:
- 有明确的步骤定义（Step 1→2→3→4）
- 每步有检查点
- 有失败处理流程

**代表技能**: `agent-mode-upgrades`, `n8n-workflow-automation`, `ontology`

**安装**:
```bash
clawhub install agent-mode-upgrades  # Agent 能力升级
clawhub install n8n-workflow-automation  # n8n 工作流
```

---

## 数据统计

### 过滤过程

| 层级 | 淘汰原因 | 淘汰数 | 剩余 |
|------|---------|--------|------|
| **初始** | - | - | 13,729 |
| **L1** | 垃圾技能 | ~4,065 | ~9,664 |
| **L2** | 重复技能 | ~1,040 | ~8,624 |
| **L3** | 低质技能 | ~851 | ~7,773 |
| **L4** | 敏感领域 | ~731 | ~7,042 |
| **L5** | 恶意技能 | ~373-824 | ~6,218-6,669 |
| **L6** | 低下载量 | ~2,308 | ~4,361 |

**最终精选**: 600 个技能（从 4,361 中选出的 Top）

### 模式分布

| 模式 | 数量 | 占比 |
|------|------|------|
| **Generator** | 557 | 12.8% |
| **Reviewer** | 353 | 8.1% |
| **Pipeline** | 257 | 5.9% |
| **Inversion** | 252 | 5.8% |
| **Tool Wrapper** | 177 | 4.1% |
| **Unclassified** | 2,765 | 63.4% |

---

## 50 个标杆技能

### P0 标杆（10 个，完整优化）

| 技能 | 模式 | 下载量 | 优化状态 |
|------|------|--------|---------|
| capability-evolver | Reviewer | 35K+ | ✅ 完整 |
| gog | Tool Wrapper | 33.8K | ✅ 完整 |
| self-improving-agent | Reviewer | 32K/260K | ✅ 完整 |
| agent-browser | Tool Wrapper | 153K stars | ✅ 完整 |
| wacli | Tool Wrapper | - | ✅ 完整 |
| composio | Tool Wrapper | 860+ App | ✅ 完整 |
| playwright-cli | Tool Wrapper | - | ✅ 完整 |
| firecrawl | Tool Wrapper | - | ✅ 完整 |
| exa | Tool Wrapper | - | ✅ 完整 |
| skill-vetter | Reviewer | - | ✅ 完整 |

### P1 标杆（20 个，部分优化）

（详见 `benchmarks/` 目录）

### P2 标杆（20 个，基础优化）

（详见 `benchmarks/` 目录）

---

## 安全建议

### 安装前检查

1. **检查 VirusTotal 扫描报告**
   ```bash
   # 访问 clawhub.ai 查看技能页面的 VirusTotal 报告
   ```

2. **审查作者信誉**
   ```bash
   # 查看作者其他技能
   curl -sL "https://clawhub.ai/author/<author>"
   ```

3. **检查下载量/星标比**
   - 高下载 + 高星标 = 可信
   - 高下载 + 低星标 = 警惕
   - 低下载 + 高星标 = 新技能

### 安装后验证

```bash
# 检查技能权限
cat ~/.openclaw/skills/<skill>/SKILL.md | grep allowed-tools

# 监控技能行为
openclaw logs --follow | grep <skill>
```

---

## 贡献

### 添加新技能

1. Fork 本仓库
2. 在 `benchmarks/` 创建技能目录
3. 按优化模板完善技能
4. 提交 PR

### 报告问题

- 安全问题：提交到 [GitHub Issues](https://github.com/cittaverse/clawhub-500/issues)
- 技能问题：直接联系技能作者

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 相关链接

- [ClawHub 官方](https://clawhub.ai/)
- [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills)
- [OpenClaw 文档](https://docs.openclaw.ai/)
- [项目报告](FINAL-REPORT.md)
- [方法论](METHODOLOGY.md)

---

*Hulk 🟢 — 2026-03-21*

#!/usr/bin/env python3
"""
ClawHub 500 质量重评脚本
每周日自动运行，使用 AI 评估技能质量并生成升级/降级推荐

API 配置:
- Provider: bailian (阿里云百炼)
- Model: qwen3-coder-plus
- Base URL: https://coding.dashscope.aliyuncs.com/v1
"""

import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# 配置
DATA_DIR = Path(os.environ.get('DATA_DIR', 'data'))
SCRIPTS_DIR = Path(__file__).parent
OUTPUT_FILE = DATA_DIR / f"reevaluation-{datetime.now().strftime('%Y-%m-%d')}.json"
DASHBOARD_FILE = DATA_DIR.parent / "quality-dashboard.md"

# API 配置
DASHSCOPE_API_KEY = os.environ.get('DASHSCOPE_API_KEY', os.environ.get('OPENAI_API_KEY', ''))
BASE_URL = os.environ.get('OPENAI_BASE_URL', 'https://coding.dashscope.aliyuncs.com/v1')
MODEL = os.environ.get('OPENAI_MODEL', 'qwen3-coder-plus')


def load_skills() -> List[Dict]:
    """加载精选技能列表"""
    skills_file = DATA_DIR / 'top-500.json'
    if not skills_file.exists():
        print(f"❌ 技能文件不存在：{skills_file}")
        sys.exit(1)
    
    with open(skills_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_latest_health() -> Dict:
    """加载最新的健康检查报告"""
    health_files = sorted(DATA_DIR.glob('health-*.json'), reverse=True)
    if not health_files:
        return {}
    
    with open(health_files[0], 'r', encoding='utf-8') as f:
        return json.load(f)


def ai_evaluate_skill(skill: Dict, health_data: Dict) -> Dict:
    """
    使用 AI 评估技能质量
    
    评估维度:
    - 代码质量 (30%)
    - 文档完整性 (25%)
    - 用户体验 (20%)
    - 维护活跃度 (15%)
    - 安全合规 (10%)
    """
    import urllib.request
    import json as json_lib
    
    if not DASHSCOPE_API_KEY:
        # 无 API Key 时使用模拟评分
        return {
            'overall': 45.0,
            'dimensions': {
                'code_quality': 45.0,
                'documentation': 45.0,
                'user_experience': 45.0,
                'maintenance': 45.0,
                'security': 45.0
            },
            'recommendation': 'watch',
            'reasoning': '模拟评分：缺少 API Key，使用默认值',
            'confidence': 0.3
        }
    
    # 构建评估 prompt
    prompt = f"""
你是 ClawHub 技能质量评估专家。请评估以下技能的质量：

## 技能信息
- 名称：{skill.get('name', 'Unknown')}
- 描述：{skill.get('description', 'No description')}
- 模式：{skill.get('pattern', 'Unclassified')}

## 健康数据
{json.dumps(health_data.get('components', {}), indent=2, ensure_ascii=False)}

## 评估维度
请按以下维度评分 (0-100 分):
1. 代码质量 (30%): 代码结构、错误处理、可测试性
2. 文档完整性 (25%): README、示例、API 文档
3. 用户体验 (20%): 易用性、错误提示、配置友好
4. 维护活跃度 (15%): 更新频率、Issue 响应
5. 安全合规 (10%): 依赖安全、权限最小化

## 输出格式
请严格输出 JSON 格式：
{{
    "overall": 总分 (0-100),
    "dimensions": {{
        "code_quality": 分数，
        "documentation": 分数，
        "user_experience": 分数，
        "maintenance": 分数，
        "security": 分数
    }},
    "recommendation": "upgrade" | "keep" | "watch" | "downgrade",
    "reasoning": "简要说明评分理由",
    "confidence": 置信度 (0-1)
}}

评分标准:
- upgrade (≥90): 标杆技能，值得推广
- keep (70-89): 良好，保持精选
- watch (50-69): 需要观察
- downgrade (<50): 建议降级或移除
"""
    
    try:
        # 调用阿里云百炼 API
        req_data = {
            'model': MODEL,
            'messages': [
                {'role': 'system', 'content': '你是 ClawHub 技能质量评估专家，输出严格 JSON 格式。'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.1,
            'max_tokens': 1000
        }
        
        req = urllib.request.Request(
            f'{BASE_URL}/chat/completions',
            data=json_lib.dumps(req_data).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {DASHSCOPE_API_KEY}'
            }
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json_lib.loads(response.read().decode('utf-8'))
            content = result['choices'][0]['message']['content']
            
            # 解析 JSON 响应
            # 清理可能的 markdown 代码块标记
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            evaluation = json_lib.loads(content)
            evaluation['confidence'] = evaluation.get('confidence', 0.7)
            return evaluation
            
    except Exception as e:
        print(f"⚠️ AI 评估失败：{e}，使用模拟评分")
        return {
            'overall': 45.0,
            'dimensions': {
                'code_quality': 45.0,
                'documentation': 45.0,
                'user_experience': 45.0,
                'maintenance': 45.0,
                'security': 45.0
            },
            'recommendation': 'watch',
            'reasoning': f'AI 评估失败：{str(e)}',
            'confidence': 0.3
        }


def create_github_pr(upgrade_candidates: List[Dict]) -> Optional[str]:
    """
    为升级候选创建 GitHub PR
    
    Returns:
        PR URL if created, None otherwise
    """
    if not upgrade_candidates:
        return None
    
    # 检查是否有 git 和 gh CLI
    try:
        result = subprocess.run(['gh', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            print("⚠️ gh CLI 不可用，跳过 PR 创建")
            return None
    except Exception:
        print("⚠️ gh CLI 未安装，跳过 PR 创建")
        return None
    
    # 创建工作分支
    branch_name = f"auto-upgrade-{datetime.now().strftime('%Y%m%d')}"
    
    try:
        # 检查当前分支
        subprocess.run(['git', 'checkout', '-b', branch_name], 
                      cwd=DATA_DIR.parent, check=True, capture_output=True)
        
        # 更新相关文件
        # ... (实际实现需要更新技能元数据)
        
        # 提交更改
        subprocess.run(['git', 'add', '.'], 
                      cwd=DATA_DIR.parent, check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', f'Auto-upgrade {len(upgrade_candidates)} skills'],
                      cwd=DATA_DIR.parent, check=True, capture_output=True)
        
        # 推送并创建 PR
        subprocess.run(['git', 'push', 'origin', branch_name],
                      cwd=DATA_DIR.parent, check=True, capture_output=True)
        
        pr_result = subprocess.run(
            ['gh', 'pr', 'create', 
             '--title', f'Auto-upgrade {len(upgrade_candidates)} skills ({datetime.now().strftime("%Y-%m-%d")})',
             '--body', f'Automatic upgrade for {len(upgrade_candidates)} high-quality skills.\n\nCandidates:\n' + 
                      '\n'.join([f'- {c["name"]} ({c["ai_score"]:.1f}分)' for c in upgrade_candidates]),
             '--base', 'main'],
            cwd=DATA_DIR.parent, capture_output=True, text=True
        )
        
        if pr_result.returncode == 0:
            pr_url = pr_result.stdout.strip()
            print(f"✅ 创建 PR: {pr_url}")
            
            # 如果分数都>90，自动合并
            if all(c['ai_score'] >= 90 for c in upgrade_candidates):
                subprocess.run(['gh', 'pr', 'merge', '--merge', '--auto'],
                              cwd=DATA_DIR.parent, capture_output=True)
                print("✅ 所有技能≥90 分，已启用自动合并")
            
            return pr_url
        else:
            print(f"⚠️ PR 创建失败：{pr_result.stderr}")
            return None
            
    except Exception as e:
        print(f"⚠️ PR 创建过程出错：{e}")
        # 恢复主分支
        subprocess.run(['git', 'checkout', 'main'], 
                      cwd=DATA_DIR.parent, capture_output=True)
        subprocess.run(['git', 'branch', '-D', branch_name], 
                      cwd=DATA_DIR.parent, capture_output=True)
        return None


def update_dashboard(reevaluation_data: Dict) -> None:
    """更新质量仪表板"""
    dashboard_content = f"""# ClawHub 500 质量仪表板

**最后更新**: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}

---

## 总体质量

| 指标 | 数值 |
|------|------|
| **技能总数** | {reevaluation_data['total_skills']} |
| **平均 AI 评分** | {reevaluation_data['avg_ai_score']:.1f} |
| **升级候选** | {reevaluation_data['upgrade_count']} |
| **保持精选** | {reevaluation_data['keep_count']} |
| **观察列表** | {reevaluation_data['watch_count']} |
| **降级候选** | {reevaluation_data['downgrade_count']} |

---

## 评分分布

| 分数段 | 数量 | 占比 |
|--------|------|------|
| ≥90 (升级) | {reevaluation_data['upgrade_count']} | {reevaluation_data['upgrade_count']/max(1,reevaluation_data['total_skills'])*100:.1f}% |
| 70-89 (保持) | {reevaluation_data['keep_count']} | {reevaluation_data['keep_count']/max(1,reevaluation_data['total_skills'])*100:.1f}% |
| 50-69 (观察) | {reevaluation_data['watch_count']} | {reevaluation_data['watch_count']/max(1,reevaluation_data['total_skills'])*100:.1f}% |
| <50 (降级) | {reevaluation_data['downgrade_count']} | {reevaluation_data['downgrade_count']/max(1,reevaluation_data['total_skills'])*100:.1f}% |

---

## 升级候选 (Top 10)

| 排名 | 技能名 | AI 评分 | 健康分 | 推荐原因 |
|------|--------|--------|--------|---------|
"""
    
    # 添加升级候选
    upgrade_skills = sorted(
        [s for s in reevaluation_data['skills'] if s['recommendation'] == 'upgrade'],
        key=lambda x: x['ai_score'],
        reverse=True
    )[:10]
    
    for i, skill in enumerate(upgrade_skills, 1):
        dashboard_content += f"| {i} | {skill['name']} | {skill['ai_score']:.1f} | {skill.get('health_score', 'N/A')} | {skill.get('reasoning', '')[:50]}... |\n"
    
    dashboard_content += f"""
---

## 降级候选 (Top 10)

| 排名 | 技能名 | AI 评分 | 主要问题 |
|------|--------|--------|---------|
"""
    
    # 添加降级候选
    downgrade_skills = sorted(
        [s for s in reevaluation_data['skills'] if s['recommendation'] == 'downgrade'],
        key=lambda x: x['ai_score']
    )[:10]
    
    for i, skill in enumerate(downgrade_skills, 1):
        dashboard_content += f"| {i} | {skill['name']} | {skill['ai_score']:.1f} | {skill.get('reasoning', '')[:50]}... |\n"
    
    dashboard_content += f"""
---

## 历史趋势

| 日期 | 平均评分 | 升级数 | 降级数 |
|------|---------|--------|--------|
| {datetime.now().strftime('%Y-%m-%d')} | {reevaluation_data['avg_ai_score']:.1f} | {reevaluation_data['upgrade_count']} | {reevaluation_data['downgrade_count']} |

---

*自动生成 | Hulk 🟢*
"""
    
    with open(DASHBOARD_FILE, 'w', encoding='utf-8') as f:
        f.write(dashboard_content)
    
    print(f"✅ 已更新质量仪表板：{DASHBOARD_FILE}")


def main():
    print("=" * 60)
    print("ClawHub 500 每周质量重评")
    print("=" * 60)
    print(f"时间：{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"API: {MODEL} @ {BASE_URL}")
    print()
    
    # 加载数据
    print("加载技能列表...")
    skills = load_skills()
    print(f"总计：{len(skills)} 个技能")
    
    print("加载健康检查报告...")
    health_data = load_latest_health()
    if health_data:
        print(f"最新健康检查：{health_data.get('timestamp', 'Unknown')}")
    else:
        print("⚠️ 未找到健康检查报告")
    print()
    
    # AI 评估
    print("开始 AI 质量评估...")
    results = []
    for i, skill in enumerate(skills, 1):
        if i % 50 == 0:
            print(f"  进度：{i}/{len(skills)}")
        
        # 从健康数据中查找对应技能的健康分
        skill_health = {}
        if health_data and 'skills' in health_data:
            for h in health_data['skills']:
                if h.get('name') == skill.get('name'):
                    skill_health = h
                    break
        
        evaluation = ai_evaluate_skill(skill, skill_health)
        
        results.append({
            'name': skill.get('name', 'Unknown'),
            'slug': skill.get('slug', ''),
            'pattern': skill.get('pattern', 'Unclassified'),
            'ai_score': evaluation['overall'],
            'dimensions': evaluation['dimensions'],
            'recommendation': evaluation['recommendation'],
            'reasoning': evaluation['reasoning'],
            'confidence': evaluation['confidence'],
            'health_score': skill_health.get('health_score', 'N/A')
        })
    
    print()
    
    # 统计
    total = len(results)
    avg_score = sum(r['ai_score'] for r in results) / total
    upgrade_count = sum(1 for r in results if r['recommendation'] == 'upgrade')
    keep_count = sum(1 for r in results if r['recommendation'] == 'keep')
    watch_count = sum(1 for r in results if r['recommendation'] == 'watch')
    downgrade_count = sum(1 for r in results if r['recommendation'] == 'downgrade')
    
    print("统计摘要:")
    print(f"  平均 AI 评分：{avg_score:.1f}")
    print(f"  升级候选 (≥90): {upgrade_count} 个")
    print(f"  保持精选 (70-89): {keep_count} 个")
    print(f"  观察列表 (50-69): {watch_count} 个")
    print(f"  降级候选 (<50): {downgrade_count} 个")
    print()
    
    # 保存结果
    output_data = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'total_skills': total,
        'avg_ai_score': round(avg_score, 1),
        'upgrade_count': upgrade_count,
        'keep_count': keep_count,
        'watch_count': watch_count,
        'downgrade_count': downgrade_count,
        'skills': results
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 已保存重评结果：{OUTPUT_FILE}")
    
    # 创建 PR
    upgrade_candidates = [r for r in results if r['recommendation'] == 'upgrade']
    if upgrade_candidates:
        print()
        print("处理升级候选...")
        pr_url = create_github_pr(upgrade_candidates)
        if pr_url:
            output_data['pr_url'] = pr_url
    else:
        print()
        print("ℹ️ 无升级候选，跳过 PR 创建")
    
    # 更新仪表板
    print()
    print("更新质量仪表板...")
    update_dashboard(output_data)
    
    print()
    print("=" * 60)
    print("✅ 质量重评完成")
    print("=" * 60)


if __name__ == '__main__':
    main()

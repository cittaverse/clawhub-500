#!/usr/bin/env python3
"""
ClawHub 500 Weekly Quality Reevaluation - Fast Version
Batches skills in groups of 10 for AI evaluation to reduce API calls from 600 to ~60.
Uses concurrent execution for speed.
"""

import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Config
DATA_DIR = Path(os.environ.get('DATA_DIR', 'data'))
OUTPUT_FILE = DATA_DIR / f"reevaluation-{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.json"
DASHBOARD_FILE = DATA_DIR.parent / "quality-dashboard.md"

DASHSCOPE_API_KEY = os.environ.get('DASHSCOPE_API_KEY', os.environ.get('OPENAI_API_KEY', ''))
BASE_URL = os.environ.get('OPENAI_BASE_URL', 'https://coding.dashscope.aliyuncs.com/v1')
MODEL = os.environ.get('OPENAI_MODEL', 'qwen3-coder-plus')

BATCH_SIZE = 10
MAX_WORKERS = 5
MAX_RETRIES = 2

print("=" * 60)
print("ClawHub 500 Weekly Quality Reevaluation (Fast)")
print("=" * 60)
print(f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
print(f"API: {MODEL} @ {BASE_URL}")
print(f"API Key: {'SET' if DASHSCOPE_API_KEY else 'MISSING'}")
print(f"Batch size: {BATCH_SIZE}, Workers: {MAX_WORKERS}")
print()

# Load skills
skills_file = DATA_DIR / 'top-500.json'
if not skills_file.exists():
    print(f"FATAL: {skills_file} not found")
    sys.exit(1)

with open(skills_file, 'r') as f:
    skills = json.load(f)
print(f"Loaded {len(skills)} skills")

# Load latest health data
health_data = {}
health_files = sorted(DATA_DIR.glob('health-*.json'), reverse=True)
if health_files:
    with open(health_files[0], 'r') as f:
        health_data = json.load(f)
    print(f"Latest health check: {health_files[0].name}")
else:
    print("WARNING: No health check data found")

# Build health lookup
health_lookup = {}
if 'skills' in health_data:
    for h in health_data['skills']:
        health_lookup[h.get('name', '')] = h

print()

def evaluate_batch(batch_skills, batch_idx):
    """Evaluate a batch of skills in one API call"""
    if not DASHSCOPE_API_KEY:
        return [{
            'name': s.get('name', 'Unknown'),
            'overall': 45.0,
            'dimensions': {'code_quality': 45, 'documentation': 45, 'user_experience': 45, 'maintenance': 45, 'security': 45},
            'recommendation': 'watch',
            'reasoning': 'No API key - mock score',
            'confidence': 0.3
        } for s in batch_skills]

    skills_desc = ""
    for i, s in enumerate(batch_skills, 1):
        h = health_lookup.get(s.get('name', ''), {})
        health_score = h.get('health_score', 'N/A')
        skills_desc += f"""
Skill {i}:
- Name: {s.get('name', 'Unknown')}
- Description: {s.get('description', 'No description')[:200]}
- Pattern: {s.get('pattern', 'Unclassified')}
- Health Score: {health_score}
"""

    prompt = f"""You are a ClawHub skill quality evaluator. Evaluate the following {len(batch_skills)} skills.

{skills_desc}

For EACH skill, score on 5 dimensions (0-100):
1. code_quality (30%): structure, error handling, testability
2. documentation (25%): README, examples, API docs
3. user_experience (20%): usability, error messages, config friendliness
4. maintenance (15%): update frequency, issue response
5. security (10%): dependency safety, minimal permissions

Output STRICT JSON array (no markdown, no explanation outside JSON):
[
  {{
    "name": "skill-name",
    "overall": weighted_score,
    "dimensions": {{"code_quality": N, "documentation": N, "user_experience": N, "maintenance": N, "security": N}},
    "recommendation": "upgrade|keep|watch|downgrade",
    "reasoning": "brief reason",
    "confidence": 0.0-1.0
  }},
  ...
]

Rating scale:
- upgrade (>=90): benchmark skill
- keep (70-89): good, stays in top 500
- watch (50-69): needs monitoring
- downgrade (<50): consider removal

Be realistic and differentiated. Not all skills are equal. Use the full range."""

    for attempt in range(MAX_RETRIES):
        try:
            req_data = {
                'model': MODEL,
                'messages': [
                    {'role': 'system', 'content': 'You are a skill quality evaluator. Output ONLY valid JSON arrays. No markdown code blocks.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.15,
                'max_tokens': 4000
            }

            req = urllib.request.Request(
                f'{BASE_URL}/chat/completions',
                data=json.dumps(req_data).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {DASHSCOPE_API_KEY}'
                }
            )

            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                content = result['choices'][0]['message']['content'].strip()

                # Clean markdown artifacts
                if content.startswith('```'):
                    content = content.split('\n', 1)[1] if '\n' in content else content[3:]
                if content.endswith('```'):
                    content = content[:-3].strip()
                # Remove any leading text before the JSON array
                idx = content.find('[')
                if idx > 0:
                    content = content[idx:]

                evaluations = json.loads(content)

                # Validate and align with input
                if isinstance(evaluations, list) and len(evaluations) >= 1:
                    # Pad or trim to match input
                    while len(evaluations) < len(batch_skills):
                        evaluations.append({
                            'name': batch_skills[len(evaluations)].get('name', 'Unknown'),
                            'overall': 55.0,
                            'dimensions': {'code_quality': 55, 'documentation': 55, 'user_experience': 55, 'maintenance': 55, 'security': 55},
                            'recommendation': 'watch',
                            'reasoning': 'Partial batch - default score',
                            'confidence': 0.4
                        })
                    return evaluations[:len(batch_skills)]

        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 * (attempt + 1))
                continue
            print(f"  Batch {batch_idx} failed after {MAX_RETRIES} attempts: {e}")

    # Fallback
    return [{
        'name': s.get('name', 'Unknown'),
        'overall': 45.0,
        'dimensions': {'code_quality': 45, 'documentation': 45, 'user_experience': 45, 'maintenance': 45, 'security': 45},
        'recommendation': 'watch',
        'reasoning': f'API evaluation failed',
        'confidence': 0.2
    } for s in batch_skills]


# Create batches
batches = []
for i in range(0, len(skills), BATCH_SIZE):
    batches.append(skills[i:i+BATCH_SIZE])

print(f"Created {len(batches)} batches of ~{BATCH_SIZE} skills")
print("Starting AI evaluation...")
print()

all_results = [None] * len(batches)
completed = 0
api_success = 0
api_fallback = 0

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {}
    for idx, batch in enumerate(batches):
        future = executor.submit(evaluate_batch, batch, idx)
        futures[future] = idx

    for future in as_completed(futures):
        idx = futures[future]
        try:
            batch_result = future.result()
            all_results[idx] = batch_result
            # Check if any are fallback
            if any(r.get('confidence', 0) <= 0.3 for r in batch_result):
                api_fallback += 1
            else:
                api_success += 1
        except Exception as e:
            print(f"  FATAL batch {idx}: {e}")
            all_results[idx] = [{
                'name': s.get('name', 'Unknown'),
                'overall': 45.0,
                'dimensions': {'code_quality': 45, 'documentation': 45, 'user_experience': 45, 'maintenance': 45, 'security': 45},
                'recommendation': 'watch',
                'reasoning': 'Fatal error',
                'confidence': 0.1
            } for s in batches[idx]]
            api_fallback += 1

        completed += 1
        if completed % 10 == 0 or completed == len(batches):
            print(f"  Progress: {completed}/{len(batches)} batches ({completed*BATCH_SIZE}/{len(skills)} skills)")

print()
print(f"API calls: {api_success} success, {api_fallback} fallback")

# Flatten results
results = []
for idx, batch_result in enumerate(all_results):
    for j, eval_data in enumerate(batch_result):
        skill = batches[idx][j] if j < len(batches[idx]) else {}
        health = health_lookup.get(skill.get('name', ''), {})
        results.append({
            'name': eval_data.get('name', skill.get('name', 'Unknown')),
            'slug': skill.get('slug', ''),
            'pattern': skill.get('pattern', 'Unclassified'),
            'ai_score': eval_data.get('overall', 45.0),
            'dimensions': eval_data.get('dimensions', {}),
            'recommendation': eval_data.get('recommendation', 'watch'),
            'reasoning': eval_data.get('reasoning', ''),
            'confidence': eval_data.get('confidence', 0.5),
            'health_score': health.get('health_score', 'N/A')
        })

# Statistics
total = len(results)
avg_score = sum(r['ai_score'] for r in results) / max(1, total)
upgrade_count = sum(1 for r in results if r['recommendation'] == 'upgrade')
keep_count = sum(1 for r in results if r['recommendation'] == 'keep')
watch_count = sum(1 for r in results if r['recommendation'] == 'watch')
downgrade_count = sum(1 for r in results if r['recommendation'] == 'downgrade')

print()
print("=" * 40)
print("SUMMARY")
print("=" * 40)
print(f"  Total skills evaluated: {total}")
print(f"  Average AI score: {avg_score:.1f}")
print(f"  Upgrade candidates (≥90): {upgrade_count}")
print(f"  Keep (70-89): {keep_count}")
print(f"  Watch (50-69): {watch_count}")
print(f"  Downgrade (<50): {downgrade_count}")

# Top 5 and Bottom 5
sorted_by_score = sorted(results, key=lambda x: x['ai_score'], reverse=True)
print()
print("Top 5:")
for r in sorted_by_score[:5]:
    print(f"  {r['ai_score']:.0f} | {r['name']} | {r['recommendation']}")
print("Bottom 5:")
for r in sorted_by_score[-5:]:
    print(f"  {r['ai_score']:.0f} | {r['name']} | {r['recommendation']}")

# Save results
output_data = {
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'model': MODEL,
    'total_skills': total,
    'avg_ai_score': round(avg_score, 1),
    'upgrade_count': upgrade_count,
    'keep_count': keep_count,
    'watch_count': watch_count,
    'downgrade_count': downgrade_count,
    'api_success_batches': api_success,
    'api_fallback_batches': api_fallback,
    'skills': results
}

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)
print(f"\nSaved: {OUTPUT_FILE}")

# Update dashboard
dashboard = f"""# ClawHub 500 质量仪表板

**最后更新**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}
**评估模型**: {MODEL} (阿里云百炼)
**当前版本**: v2026.13

---

## 总体质量

| 指标 | 数值 | 状态 |
|------|------|------|
| **技能总数** | {total} | ✅ |
| **平均 AI 评分** | {avg_score:.1f} | {'✅ 良好' if avg_score >= 70 else '⚠️ 需改进' if avg_score >= 50 else '🔴 较低'} |
| **升级候选** | {upgrade_count} | {'🎉' if upgrade_count > 0 else '-'} |
| **保持精选** | {keep_count} | ✅ |
| **观察列表** | {watch_count} | ⚠️ |
| **降级候选** | {downgrade_count} | {'🔴' if downgrade_count > 0 else '-'} |
| **API 成功率** | {api_success}/{api_success+api_fallback} batches | {'✅' if api_fallback == 0 else '⚠️'} |

---

## 评分分布

| 分数段 | 数量 | 占比 |
|--------|------|------|
| ≥90 (升级) | {upgrade_count} | {upgrade_count/max(1,total)*100:.1f}% |
| 70-89 (保持) | {keep_count} | {keep_count/max(1,total)*100:.1f}% |
| 50-69 (观察) | {watch_count} | {watch_count/max(1,total)*100:.1f}% |
| <50 (降级) | {downgrade_count} | {downgrade_count/max(1,total)*100:.1f}% |

---

## 升级候选 (Top 10)

| 排名 | 技能名 | AI 评分 | 模式 | 推荐原因 |
|------|--------|--------|------|---------|
"""

upgrades = sorted([r for r in results if r['recommendation'] == 'upgrade'], key=lambda x: x['ai_score'], reverse=True)[:10]
if upgrades:
    for i, s in enumerate(upgrades, 1):
        dashboard += f"| {i} | {s['name']} | {s['ai_score']:.0f} | {s['pattern']} | {s['reasoning'][:60]} |\n"
else:
    dashboard += "| - | *暂无升级候选* | - | - | - |\n"

dashboard += f"""
---

## 降级候选 (Top 10)

| 排名 | 技能名 | AI 评分 | 模式 | 主要问题 |
|------|--------|--------|------|---------|
"""

downgrades = sorted([r for r in results if r['recommendation'] == 'downgrade'], key=lambda x: x['ai_score'])[:10]
if downgrades:
    for i, s in enumerate(downgrades, 1):
        dashboard += f"| {i} | {s['name']} | {s['ai_score']:.0f} | {s['pattern']} | {s['reasoning'][:60]} |\n"
else:
    dashboard += "| - | *暂无降级候选* | - | - | - |\n"

# Load previous reevaluation for trend
prev_files = sorted(DATA_DIR.glob('reevaluation-*.json'), reverse=True)
prev_trend = ""
for pf in prev_files[:5]:
    try:
        with open(pf, 'r') as f:
            pd = json.load(f)
        prev_trend += f"| {pf.stem.replace('reevaluation-','')} | {pd.get('avg_ai_score', 'N/A')} | {pd.get('upgrade_count', 0)} | {pd.get('downgrade_count', 0)} | {pd.get('model', 'N/A')} |\n"
    except:
        pass

dashboard += f"""
---

## 历史趋势

| 日期 | 平均评分 | 升级数 | 降级数 | 模型 |
|------|---------|--------|--------|------|
{prev_trend}
---

*自动生成 | Hulk 🟢 — ClawHub 500 Weekly Reevaluation*
**下次评估**: {(datetime.now(timezone.utc)).strftime('%Y-')}W{int(datetime.now(timezone.utc).strftime('%W'))+1}
"""

with open(DASHBOARD_FILE, 'w', encoding='utf-8') as f:
    f.write(dashboard)
print(f"Dashboard updated: {DASHBOARD_FILE}")

print()
print("=" * 60)
print("DONE")
print("=" * 60)

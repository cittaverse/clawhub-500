#!/usr/bin/env python3
"""
ClawHub 500 健康检查脚本
每 6 小时自动运行，检查所有技能健康状态
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 配置
DATA_DIR = Path(os.environ.get('DATA_DIR', 'data'))
OUTPUT_FILE = DATA_DIR / f"health-{datetime.now().strftime('%Y-%m-%d-%H')}.json"

def load_skills():
    """加载精选技能列表"""
    skills_file = DATA_DIR / 'top-500.json'
    if not skills_file.exists():
        print(f"❌ 技能文件不存在：{skills_file}")
        sys.exit(1)
    
    with open(skills_file, 'r') as f:
        return json.load(f)

def calculate_health_score(skill):
    """
    计算技能健康评分 (0-100)
    
    评分维度:
    - 下载量趋势 (30%)
    - 星标/下载比 (30%)
    - 作者活跃度 (20%)
    - 安全状态 (20%)
    """
    score = 0
    
    # 下载量趋势 (模拟数据，实际应调用 API)
    download_trend = skill.get('download_trend', 0)
    download_score = min(100, max(0, 50 + download_trend * 10))
    
    # 星标/下载比
    stars = skill.get('stars', 0)
    downloads = skill.get('downloads', 1)
    star_ratio = stars / max(1, downloads)
    star_score = min(100, star_ratio * 1000)
    
    # 作者活跃度 (模拟)
    author_activity = skill.get('author_activity', 0.5)
    activity_score = author_activity * 100
    
    # 安全状态
    virustotal_flagged = skill.get('virustotal_flagged', 0)
    security_score = max(0, 100 - virustotal_flagged * 20)
    
    # 综合评分
    health_score = (
        download_score * 0.3 +
        star_score * 0.3 +
        activity_score * 0.2 +
        security_score * 0.2
    )
    
    return {
        'overall': round(health_score, 1),
        'components': {
            'download': round(download_score, 1),
            'star': round(star_score, 1),
            'activity': round(activity_score, 1),
            'security': round(security_score, 1)
        },
        'recommendation': get_recommendation(health_score)
    }

def get_recommendation(score):
    """根据健康分给出推荐"""
    if score >= 90:
        return "upgrade"  # 升级为标杆
    elif score >= 70:
        return "keep"     # 保持精选
    elif score >= 50:
        return "watch"    # 观察
    else:
        return "downgrade"  # 降级/移除

def main():
    print("=" * 60)
    print("ClawHub 500 健康检查")
    print("=" * 60)
    print(f"时间：{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print()
    
    # 加载技能
    print("加载技能列表...")
    skills = load_skills()
    print(f"总计：{len(skills)} 个技能")
    print()
    
    # 健康检查
    print("执行健康检查...")
    results = []
    for skill in skills:
        health = calculate_health_score(skill)
        results.append({
            'name': skill.get('name', 'Unknown'),
            'slug': skill.get('slug', ''),
            'health_score': health['overall'],
            'recommendation': health['recommendation'],
            'components': health['components']
        })
    
    # 统计
    total = len(results)
    avg_score = sum(r['health_score'] for r in results) / total
    watchlist_count = sum(1 for r in results if r['recommendation'] == 'watch')
    downgrade_count = sum(1 for r in results if r['recommendation'] == 'downgrade')
    
    # 保存结果
    output_data = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'total_skills': total,
        'avg_health_score': round(avg_score, 1),
        'watchlist_count': watchlist_count,
        'downgrade_count': downgrade_count,
        'skills': results
    }
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"已保存：{OUTPUT_FILE}")
    print()
    print("统计摘要:")
    print(f"  平均健康分：{avg_score:.1f}")
    print(f"  观察列表：{watchlist_count} 个")
    print(f"  降级候选：{downgrade_count} 个")
    print()
    print("✅ 健康检查完成")

if __name__ == '__main__':
    main()

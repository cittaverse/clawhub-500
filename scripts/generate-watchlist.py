#!/usr/bin/env python3
"""生成观察列表"""
import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path('data')
HEALTH_FILE = sorted(DATA_DIR.glob('health-*.json'))[-1]
WATCHLIST_FILE = DATA_DIR / f"watchlist-{datetime.now().strftime('%Y-%m-%d-%H')}.md"

with open(HEALTH_FILE) as f:
    data = json.load(f)

skills = data['skills']
watchlist = [s for s in skills if s['recommendation'] in ['watch', 'downgrade']]

with open(WATCHLIST_FILE, 'w') as f:
    f.write(f"# ClawHub 500 观察列表\n\n")
    f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n")
    f.write(f"总计：{len(watchlist)} 个技能需要关注\n\n")
    f.write("| 技能名 | 健康分 | 建议 | 下载分 | 星标分 | 活跃度 | 安全分 |\n")
    f.write("|--------|--------|------|--------|--------|--------|--------|\n")
    for s in sorted(watchlist, key=lambda x: x['health_score'])[:50]:
        f.write(f"| {s['name']} | {s['health_score']} | {s['recommendation']} | {s['components']['download']} | {s['components']['star']} | {s['components']['activity']} | {s['components']['security']} |\n")
    
    if len(watchlist) > 50:
        f.write(f"\n... 还有 {len(watchlist) - 50} 个技能，详见 {HEALTH_FILE.name}\n")

print(f"已生成：{WATCHLIST_FILE}")
print(f"观察列表：{len(watchlist)} 个技能")

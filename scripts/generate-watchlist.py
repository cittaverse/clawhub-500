#!/usr/bin/env python3
"""生成观察列表"""
import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

DATA_DIR = Path('data')


def latest_health_file():
    health_files = sorted(DATA_DIR.glob('health-*.json'))
    if not health_files:
        raise FileNotFoundError("No health-*.json files found in data/")
    return health_files[-1]


def parse_args():
    parser = argparse.ArgumentParser(description="Generate a ClawHub 500 watchlist from health check data.")
    parser.add_argument("--input", default=None, help="Path to the health JSON report.")
    parser.add_argument(
        "--output",
        default=str(DATA_DIR / f"watchlist-{datetime.now(UTC).strftime('%Y-%m-%d-%H')}.md"),
        help="Path to write the watchlist Markdown file.",
    )
    return parser.parse_args()


args = parse_args()
health_file = Path(args.input) if args.input else latest_health_file()
watchlist_file = Path(args.output)

with open(health_file) as f:
    data = json.load(f)

skills = data['skills']
watchlist = [s for s in skills if s['recommendation'] in ['watch', 'downgrade']]

watchlist_file.parent.mkdir(parents=True, exist_ok=True)
with open(watchlist_file, 'w') as f:
    f.write(f"# ClawHub 500 观察列表\n\n")
    f.write(f"**生成时间**: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}\n\n")
    f.write(f"总计：{len(watchlist)} 个技能需要关注\n\n")
    f.write("| 技能名 | 健康分 | 建议 | 下载分 | 星标分 | 活跃度 | 安全分 |\n")
    f.write("|--------|--------|------|--------|--------|--------|--------|\n")
    for s in sorted(watchlist, key=lambda x: x['health_score'])[:50]:
        f.write(f"| {s['name']} | {s['health_score']} | {s['recommendation']} | {s['components']['download']} | {s['components']['star']} | {s['components']['activity']} | {s['components']['security']} |\n")
    
    if len(watchlist) > 50:
        f.write(f"\n... 还有 {len(watchlist) - 50} 个技能，详见 {health_file.name}\n")

print(f"已生成：{watchlist_file}")
print(f"观察列表：{len(watchlist)} 个技能")

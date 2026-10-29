#!/usr/bin/env python3
"""今天吃什么？—— 一个帮你决定吃饭的随机选择器。

用法：
    python3 eat_what.py                    # 交互模式
    python3 eat_what.py --no-spicy         # 不吃辣
    python3 eat_what.py --max-price 30     # 预算 30 元以内
    python3 eat_what.py --category 面食     # 只在面食里选
    python3 eat_what.py --list             # 看看都有哪些选择
"""

import argparse
import random
import sys

# 食物库：名称、分类、价格(元)、是否辣、预计耗时(分钟)、标签
FOODS = [
    {"name": "兰州牛肉面", "category": "面食", "price": 22, "spicy": False, "time": 20, "tags": ["汤面", "经典"]},
    {"name": "重庆小面", "category": "面食", "price": 18, "spicy": True, "time": 15, "tags": ["麻辣"]},
    {"name": "番茄鸡蛋面", "category": "面食", "price": 16, "spicy": False, "time": 15, "tags": ["家常"]},
    {"name": "饺子", "category": "面食", "price": 25, "spicy": False, "time": 25, "tags": ["管饱"]},
    {"name": "黄焖鸡米饭", "category": "米饭", "price": 26, "spicy": False, "time": 20, "tags": ["下饭"]},
    {"name": "扬州炒饭", "category": "米饭", "price": 20, "spicy": False, "time": 15, "tags": ["快手"]},
    {"name": "麻辣香锅", "category": "米饭", "price": 45, "spicy": True, "time": 30, "tags": ["重口"]},
    {"name": "盖浇饭", "category": "米饭", "price": 22, "spicy": False, "time": 15, "tags": ["省事"]},
    {"name": "麻辣烫", "category": "小吃", "price": 32, "spicy": True, "time": 20, "tags": ["自选"]},
    {"name": "煎饼果子", "category": "小吃", "price": 12, "spicy": False, "time": 10, "tags": ["早餐", "快手"]},
    {"name": "关东煮", "category": "小吃", "price": 20, "spicy": False, "time": 10, "tags": ["清淡"]},
    {"name": "烤冷面", "category": "小吃", "price": 15, "spicy": True, "time": 10, "tags": ["路边摊"]},
    {"name": "汉堡套餐", "category": "快餐", "price": 35, "spicy": False, "time": 10, "tags": ["省事"]},
    {"name": "炸鸡", "category": "快餐", "price": 40, "spicy": False, "time": 20, "tags": ["解馋"]},
    {"name": "轻食沙拉", "category": "轻食", "price": 35, "spicy": False, "time": 10, "tags": ["减脂", "清淡"]},
    {"name": "粥 + 小菜", "category": "轻食", "price": 15, "spicy": False, "time": 10, "tags": ["养胃"]},
    {"name": "酸菜鱼", "category": "炒菜", "price": 55, "spicy": True, "time": 40, "tags": ["聚餐"]},
    {"name": "宫保鸡丁", "category": "炒菜", "price": 38, "spicy": True, "time": 35, "tags": ["下饭"]},
    {"name": "西红柿炒蛋盖饭", "category": "炒菜", "price": 24, "spicy": False, "time": 20, "tags": ["家常"]},
    {"name": "火锅", "category": "炒菜", "price": 80, "spicy": True, "time": 60, "tags": ["聚餐", "慢"]},
]


def filter_foods(args):
    """按条件筛选，返回可选列表。"""
    result = []
    for f in FOODS:
        if args.no_spicy and f["spicy"]:
            continue
        if args.max_price and f["price"] > args.max_price:
            continue
        if args.max_time and f["time"] > args.max_time:
            continue
        if args.category and f["category"] != args.category:
            continue
        result.append(f)
    return result


def describe(food):
    spicy = "辣" if food["spicy"] else "不辣"
    tags = "、".join(food["tags"])
    return (
        f"\n  🍽  {food['name']}\n"
        f"     分类：{food['category']}  |  {spicy}  |  约 {food['price']} 元  |  约 {food['time']} 分钟\n"
        f"     标签：{tags}\n"
    )


def pick(pool, exclude):
    remain = [f for f in pool if f["name"] not in exclude]
    if not remain:
        return None
    return random.choice(remain)


def print_list(pool):
    print(f"\n共 {len(pool)} 个候选：\n")
    for f in pool:
        print(f"  - {f['name']}（{f['category']}，{f['price']}元，{f['time']}分钟）")
    print()


def interactive(pool, rng):
    exclude = set()
    print("今天吃什么？我来帮你决定！")
    print("命令：再选一次 / 不要这个 / 列表 / 退出\n")

    current = pick(pool, exclude)
    if current is None:
        print("没有符合条件的选择了。")
        return
    print(f"👉 今天就吃：{current['name']}！{describe(current)}")

    while True:
        cmd = input("> ").strip()
        if cmd in ("退出", "q", "quit", "exit"):
            print("祝你吃得开心！")
            return
        if cmd in ("列表", "list", "ls"):
            print_list(pool)
        elif cmd in ("不要这个", "换一个", "再选一次", "next", "skip", "x"):
            if current:
                exclude.add(current["name"])
            current = pick(pool, exclude)
            if current is None:
                print("候选都被排除啦，重新开始一轮。")
                exclude.clear()
                current = pick(pool, exclude)
            print(f"👉 那就吃：{current['name']}！{describe(current)}")
        else:
            print("可用命令：再选一次 / 不要这个 / 列表 / 退出")


def main():
    parser = argparse.ArgumentParser(description="今天吃什么？")
    parser.add_argument("--no-spicy", action="store_true", help="只要不辣的")
    parser.add_argument("--max-price", type=int, help="最高预算（元）")
    parser.add_argument("--max-time", type=int, help="最长等待（分钟）")
    parser.add_argument("--category", help="限定分类，如 面食/米饭/小吃/快餐/轻食/炒菜")
    parser.add_argument("--list", action="store_true", help="只列出候选食物")
    parser.add_argument("--seed", type=int, help="随机种子（结果可复现）")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    pool = filter_foods(args)
    if not pool:
        print("没有符合条件的食物，放宽一下条件试试？")
        sys.exit(1)

    if args.list:
        print_list(pool)
        return

    # 无交互终端时（如管道/CI）直接给一个结果
    if not sys.stdin.isatty():
        print(f"今天就吃：{pool[random.randrange(len(pool))]['name']}")
        return

    interactive(pool, random)


if __name__ == "__main__":
    main()

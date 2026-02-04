import json
import os
from collections import defaultdict

# 1. 读取数据文件
json_path = os.path.join("..", "assets", "data", "papers_data.json")

if not os.path.exists(json_path):
    print(f"❌ 错误：找不到文件 {json_path}")
    exit()

with open(json_path, 'r', encoding='utf-8') as f:
    papers = json.load(f)

print(f"📊 正在检查 {len(papers)} 篇论文的重复情况 (按链接查重)...\n")

# 2. 按链接分组
# Key: 清洗后的链接, Value: 对应的论文对象列表
link_map = defaultdict(list)

for p in papers:
    # 忽略 https/http 差异，忽略末尾斜杠
    raw_link = p.get('link', '')
    clean_link = raw_link.replace('https://', '').replace('http://', '').rstrip('/')

    link_map[clean_link].append(p)

# 3. 找出重复项
dup_count = 0
for link, group in link_map.items():
    # 如果同一个链接对应了多条数据，说明有重复
    if len(group) > 1:
        dup_count += 1
        print(f"🔗 发现链接重复组 [共 {len(group)} 篇]:")
        print(f"   Link: {group[0]['link']}")
        print("   分别对应的标题:")
        for item in group:
            print(f"     ❌ {item['title']}")
        print("-" * 50)

# 4. 总结
if dup_count == 0:
    print("✅ 完美！所有论文的链接都是唯一的，没有重复。")
else:
    print(f"\n🚫 共发现 {dup_count} 组重复链接。")
    print("原因：这些论文链接相同，但标题不同，导致被'标题指纹法'当成了不同的论文。")
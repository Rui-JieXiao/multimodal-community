import re
import json
import os

# --- 1. 路径配置 (使用相对于脚本位置的绝对路径) ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 输入：原材料仓库中的 MD 文件
INPUT_FILE = os.path.join(PROJECT_ROOT, "assets", "raw_sources", "source_awesome_mllm.md")
# 输出：主数据库
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "assets", "data", "datasets_data.json")

# 🟢 核心配置：数据集章节白名单
TARGET_SECTIONS = [
    ("## Datasets of Pre-Training for Alignment", "Pre-Training"),
    ("## Datasets of Multimodal Instruction Tuning", "Instruction Tuning"),
    ("## Datasets of In-Context Learning", "In-Context Learning"),
    ("## Datasets of Multimodal Chain-of-Thought", "Chain-of-Thought"),
    ("## Datasets of Multimodal RLHF", "RLHF"),
    ("## Benchmarks for Evaluation", "Benchmark"),
    ("## Others", "Others"),
]

def get_dataset_id(title):
    """生成数据集唯一 ID (忽略大小写和特殊符号)"""
    if not title:
        return "unknown"
    return re.sub(r'[^a-z0-9]', '', title.lower())

def extract_first_link(text_cell):
    """从单元格提取第一个非装饰性链接"""
    candidates = re.findall(r'\]\((http.*?)\)', text_cell)
    for url in candidates:
        url = url.strip()
        if any(bad in url for bad in ['.svg', 'shields.io', 'badge']):
            continue
        return url
    return ""

def clean_text(text):
    """移除 Markdown 语法，保留纯文本"""
    if not text: return ""
    text = text.replace('**', '')
    text = re.sub(r'\[([^\]]+)\]\(http.*?\)', r'\1', text) # 提取 [Text](Link) 中的 Text
    text = text.replace('`', '')
    text = text.replace('\n', ' ').strip()
    return text

def parse_datasets():
    print(f"🚀 启动数据集提取器...")

    # --- A. 准备工作：读取现有数据库 ---
    existing_data = []
    existing_map = {}

    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                for item in existing_data:
                    if 'title' in item:
                        pid = get_dataset_id(item['title'])
                        existing_map[pid] = item
            print(f"📖 读取到主库现有数据集：{len(existing_data)} 条")
        except Exception as e:
            print(f"⚠️ 读取现有 JSON 失败: {e}")
    else:
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # --- B. 读取 MD 源文件 ---
    if not os.path.exists(INPUT_FILE):
        print(f"❌ 错误：找不到源文件 {INPUT_FILE}")
        print("💡 请确认 README.md 已重命名并放入 assets/raw_sources/ 文件夹")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        full_content = f.read()

    # 锁定数据集专属区域，防止误抓论文
    datasets_start_marker = "# Awesome Datasets"
    if datasets_start_marker in full_content:
        content_for_scan = full_content.split(datasets_start_marker)[1]
    else:
        print("⚠️ 警告：未找到 '# Awesome Datasets' 标记，将扫描全文件")
        content_for_scan = full_content

    current_run_map = {}

    # --- C. 循环解析章节 ---
    for section_header, tag_name in TARGET_SECTIONS:
        print(f"   🔍 解析章节: [{section_header}]")

        pattern = re.escape(section_header) + r"\n(.*?)(?=\n## |$)"
        match = re.search(pattern, content_for_scan, re.DOTALL)

        if not match: continue

        lines = match.group(1).split('\n')

        # 智能识别表格结构
        table_type = "TYPE_B"
        for line in lines[:5]:
            if "| Modalities |" in line:
                table_type = "TYPE_A"
                break

        count = 0
        for line in lines:
            line = line.strip()
            # 过滤掉非数据行（表头、分隔线等）
            if not line.startswith('|') or ':---' in line or '| Name' in line:
                continue

            cols = [c.strip() for c in line.split('|')]
            if len(cols) < 5: continue

            name_cell = cols[1]
            paper_cell = cols[2]

            # 提取名称
            title_match = re.search(r"\*\*(?P<title>.*?)\*\*", name_cell)
            title = title_match.group("title").strip() if title_match else clean_text(name_cell)

            if not title: continue
            pid = get_dataset_id(title)

            # 提取链接和描述
            final_link = ""
            final_desc = ""

            if table_type == "TYPE_A":
                if len(cols) >= 6:
                    type_val = clean_text(cols[3])
                    mod_val = clean_text(cols[4])
                    final_desc = f"{type_val} | {mod_val}"
                final_link = extract_first_link(paper_cell)
            else:
                if len(cols) >= 6:
                    link_cell = cols[3]
                    notes_cell = cols[4]
                    link_from_col3 = extract_first_link(link_cell)
                    link_from_col2 = extract_first_link(paper_cell)
                    final_link = link_from_col3 if link_from_col3 else link_from_col2
                    final_desc = clean_text(notes_cell)

            # 存入本次抓取结果映射表（处理同文件重复项）
            if pid in current_run_map:
                if tag_name not in current_run_map[pid]['tags']:
                    current_run_map[pid]['tags'].append(tag_name)
            else:
                current_run_map[pid] = {
                    "title": title,
                    "link": final_link,
                    "venue": "Dataset",
                    "description": final_desc,
                    "tags": [tag_name],
                    "source": "auto-script"
                }
            count += 1
        print(f"      ✅ 扫描到 {count} 条")

    # --- D. 最终合并与保护 ---
    final_data = []
    current_run_ids = set(current_run_map.keys())

    # 1. 合并本次抓取的数据与旧数据
    for pid, new_item in current_run_map.items():
        if pid in existing_map:
            old_item = existing_map[pid]
            merged_tags = list(set(old_item.get('tags', []) + new_item['tags']))

            # 🛡️ 描述保护逻辑：如果旧库已有描述，则不覆盖
            saved_desc = old_item.get("description")
            final_desc = saved_desc if saved_desc else new_item['description']

            final_item = {
                "title": new_item['title'],
                "link": new_item['link'] if new_item['link'] else old_item.get("link"),
                "venue": "Dataset",
                "tags": merged_tags,
                "source": old_item.get("source", "auto-script"),
                "description": final_desc,
                # 继承保护字段
                "authors": old_item.get("authors", ""),
                "image": old_item.get("image", ""),
                "code": old_item.get("code", "")
            }
            final_data.append(final_item)
        else:
            # 🔵 纯新增项初始化
            new_item["authors"] = ""
            new_item["image"] = ""
            new_item["code"] = ""
            final_data.append(new_item)

    # 2. 保留库中原本存在但本次 MD 中没抓到的手动录入项
    for old_item in existing_data:
        old_pid = get_dataset_id(old_item.get('title', ''))
        if old_pid not in current_run_ids:
            if old_item.get('source') != 'auto-script':
                final_data.append(old_item)
                print(f"🛡️  保留手动录入项: {old_item.get('title')}")

    # --- E. 保存结果 ---
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 数据集同步完成！")
    print(f"📊 数据库总条数: {len(final_data)}")
    print(f"📂 更新路径: {os.path.abspath(OUTPUT_FILE)}")

if __name__ == "__main__":
    parse_datasets()
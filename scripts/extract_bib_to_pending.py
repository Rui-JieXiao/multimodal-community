import os
import re
import json
import hashlib

# ================= 核心配置区 =================
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

SOURCE_BIB = os.path.join(project_root, "assets", "raw_sources", "surveys", "2411_17040_refs.bib")
OUTPUT_JSON = os.path.join(project_root, "assets", "data", "pending", "imported_from_survey.json")
HISTORY_FILE = os.path.join(project_root, "assets", "raw_sources", "surveys", "history_log.txt")

DEFAULT_VENUE = "arXiv"


# ================= 工具函数区 =================

def load_history():
    if not os.path.exists(HISTORY_FILE): return set()
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)


def append_to_history(identifier):
    with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{identifier}\n")


def get_string_hash(text):
    """生成标题的唯一哈希指纹"""
    return hashlib.md5(text.strip().lower().encode('utf-8')).hexdigest()


def parse_bib_file(file_path):
    if not os.path.exists(file_path):
        print(f"❌ 找不到输入文件: {file_path}")
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    raw_entries = re.split(r'@\w+\s*\{', content)[1:]
    parsed_entries = []
    seen_titles = set()

    for raw in raw_entries:
        t_match = re.search(r'title\s*=\s*[\{"](.+?)[\}"]', raw, re.IGNORECASE | re.DOTALL)
        if not t_match: continue

        # 清理标题
        clean_title = " ".join(t_match.group(1).split()).replace('{', '').replace('}', '')
        title_fingerprint = clean_title.lower()
        if title_fingerprint in seen_titles: continue
        seen_titles.add(title_fingerprint)

        entry = {'title': clean_title}

        # 尝试拼凑链接
        link = ""
        ep_match = re.search(r'eprint\s*=\s*[\{"](.*?)[\}"]', raw, re.IGNORECASE)
        if ep_match:
            clean_id = re.search(r'(\d{4}\.\d{4,5})', ep_match.group(1))
            if clean_id: link = f"https://arxiv.org/abs/{clean_id.group(1)}"

        if not link:
            doi_match = re.search(r'doi\s*=\s*[\{"](.+?)[\}"]', raw, re.IGNORECASE)
            if doi_match: link = f"https://doi.org/{doi_match.group(1)}"

        entry['link'] = link
        y_match = re.search(r'year\s*=\s*[\{"](\d{4})[\}"]', raw, re.IGNORECASE)
        entry['year'] = y_match.group(1) if y_match else "Unknown"
        v_match = re.search(r'(journal|booktitle)\s*=\s*[\{"](.+?)[\}"]', raw, re.IGNORECASE)
        entry['venue'] = v_match.group(2) if v_match else ""

        parsed_entries.append(entry)

    return parsed_entries


def save_to_json(new_paper):
    data = []
    if os.path.exists(OUTPUT_JSON):
        try:
            with open(OUTPUT_JSON, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            data = []

    data.append(new_paper)
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ================= 主逻辑流程 =================

def main():
    entries = parse_bib_file(SOURCE_BIB)
    history = load_history()

    print(f"🚀 文献提取器已就绪。待处理: {len(entries)} 篇，已跳过: {len(history)} 篇。")
    print("-" * 50)

    for i, item in enumerate(entries):
        title_hash = get_string_hash(item['title'])
        if title_hash in history: continue

        print(f"\n[{i + 1}/{len(entries)}] --------------------------------")
        print(f"TITLE: {item['title']}")
        print(f"YEAR : {item['year']} | VENUE: {item['venue'] if item['venue'] else 'N/A'}")

        current_link = item['link']
        if current_link:
            print(f"LINK : {current_link}")
        else:
            print(f"LINK : [!] 脚本未能在 BibTeX 中自动找到链接")

        while True:
            choice = input("👉 操作 (y:收录 / n:跳过 / q:退出): ").lower().strip()

            if choice == 'q':
                print("👋 进度已保存。")
                return

            if choice == 'n':
                append_to_history(title_hash)
                print("🗑️  已标记为跳过。")
                break

            if choice == 'y':
                # 1. 链接质量闸门
                if not current_link:
                    manual_input = input("🔗 缺少链接，请输入 URL (回车则放弃收录此篇): ").strip()
                    if not manual_input:
                        append_to_history(title_hash)
                        print("⏭️  因无链接，已自动放弃收录。")
                        break
                    else:
                        current_link = manual_input

                # 2. 标签处理：默认置空，由你输入
                user_tags_input = input("🏷️  请输入标签 (多个用逗号或空格分隔，直接回车则为空): ").strip()

                final_tags = []
                if user_tags_input:
                    # 分割并清理标签
                    final_tags = [t.strip() for t in re.split(r'[,，\s]+', user_tags_input) if t.strip()]

                # 3. 构造正式对象并保存
                paper_obj = {
                    "title": item['title'],
                    "link": current_link,
                    "venue": item['venue'] if item['venue'] else DEFAULT_VENUE,
                    "date": item['year'],
                    "tags": final_tags,  # 可能是 []
                    "source": "survey:2411.17040",
                    "code": "",
                    "authors": "TBA",
                    "description": "",
                    "image": ""
                }
                save_to_json(paper_obj)
                append_to_history(title_hash)
                print(f"✅ 已收录。标签: {final_tags}")
                break


if __name__ == "__main__":
    main()
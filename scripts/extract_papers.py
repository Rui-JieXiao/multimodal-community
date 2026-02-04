import re
import json
import os

# --- 1. 路径与全局配置 ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 生产环境主库 (用于去重参考)
DB_FILE = os.path.join(PROJECT_ROOT, "assets", "data", "papers_data.json")

# 加工区 (Staging Area)
STAGING_FILE = os.path.join(PROJECT_ROOT, "assets", "data", "staging", "incoming_papers.json")

# 🟢 核心配置：多源管理器
SOURCES_CONFIG = {
    # 源 1: 原始的 MLLM 表格
    "awesome_mllm": {
        "file_path": os.path.join(PROJECT_ROOT, "assets", "raw_sources", "source_awesome_mllm.md"),
        "parser_type": "table",
        "sections": [
            ("## Multimodal Instruction Tuning", "Instruction Tuning"),
            ("## Multimodal Hallucination", "Hallucination"),
            ("## Multimodal In-Context Learning", "In-Context Learning"),
            ("## Multimodal Chain-of-Thought", "Chain-of-Thought"),
            ("## LLM-Aided Visual Reasoning", "Visual Reasoning"),
            ("## Foundation Models", "Foundation Models"),
            ("## Evaluation", "Evaluation"),
            ("## Multimodal RLHF", "RLHF"),
            ("## Others", "Others"),
        ]
    },
    # 源 2: 梁让大佬的列表 (Paul Liang) - 仅三大核心领域
    "pliang_list": {
        "file_path": os.path.join(PROJECT_ROOT, "assets", "raw_sources", "source_pliang_list.md"),
        "parser_type": "list",
        "sections": [
            ("### Multimodal Representations", "Representations"),
            ("### Multimodal Fusion", "Fusion"),
            ("### Multimodal Alignment", "Alignment"),
        ]
    }
}


# --- 2. 工具函数 ---

def get_paper_id(title):
    """生成标题唯一指纹"""
    if not title: return "unknown"
    return re.sub(r'[^a-z0-9]', '', title.lower())


def extract_valid_link(text):
    """从文本提取第一个 HTTP 链接 (排除徽章图片)"""
    candidates = re.findall(r'\]\((http.*?)\)', text)
    for url in candidates:
        url = url.strip()
        if any(bad in url for bad in ['.svg', 'shields.io', 'badge']):
            continue
        return url
    return ""


def clean_md_syntax(text):
    """清除 Markdown 语法 (**bold**, `code`)"""
    if not text: return ""
    return text.replace('**', '').replace('`', '').strip()


def load_json_safely(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_json_safely(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# --- 3. 核心解析策略 (策略分离) ---

def parse_table_row(line):
    """策略 A: 解析 Markdown 表格行"""
    if not line.startswith('|') or ':---' in line or '| Title' in line:
        return None

    cols = [c.strip() for c in line.split('|')]
    if len(cols) < 4: return None

    title_cell = cols[1]
    venue_cell = cols[2]
    date_cell = cols[3]

    title_match = re.search(r"\*\*(?P<title>.*?)\*\*", title_cell)
    valid_url = extract_valid_link(title_cell)

    if title_match and valid_url:
        return {
            "title": clean_md_syntax(title_match.group("title")),
            "link": valid_url,
            "venue": venue_cell if venue_cell != "-" else "Research Community",
            "date": date_cell[:4] if len(date_cell) >= 4 else "2024",
            "code": ""
        }
    return None


def parse_list_line(line):
    """策略 B: 解析嵌套列表行 (Liang's format)"""
    # 格式: [Title](Link), Venue Year [[blog]](BlogLink) [[code]](CodeLink)
    if not line.strip().startswith('['): return None

    # 1. 提取标题和主链接
    main_match = re.search(r'^\[(?P<title>.*?)\]\((?P<link>http.*?)\)', line)
    if not main_match: return None

    title = clean_md_syntax(main_match.group("title"))
    link = main_match.group("link").strip()

    # 2. 提取 Code 链接 (先提取，提取完就可以把原来的字符串删掉了)
    code_link = ""
    code_match = re.search(r'\[\[code\]\]\((?P<code>http.*?)\)', line)
    if code_match:
        code_link = code_match.group("code").strip()

    # 3. 🧹 开始大清洗 (Cleaning)
    rest = line[main_match.end():]  # 截取标题之后的所有内容

    # 3.1 移除 code 块 (无论是否有链接)
    rest = re.sub(r'\[\[code\]\].*?(?=\s|\[|$)', '', rest, flags=re.IGNORECASE)
    # 3.2 移除 markdown 链接结构 [text](url) -> 比如 [[blog]](http...)
    rest = re.sub(r'\[.*?\]\(.*?\)', '', rest)
    # 3.3 移除残留的方括号标签 -> 比如 [PDF], [Slides]
    rest = re.sub(r'\[.*?\]', '', rest)

    # 4. 提取年份
    year_match = re.search(r'(20\d{2}|19\d{2})', rest)
    year = year_match.group(1) if year_match else "2024"

    # 5. 提取 Venue
    # 移除年份
    rest = rest.replace(year, '')
    # 移除首尾杂质 (逗号, 句号, 括号, 竖线, 空格)
    venue = rest.strip(' ,.-|()')

    # 🛡️ 6. 安全气囊 (Safety Guard)
    # 如果清洗后 Venue 依然包含 http，说明源文本格式极度混乱
    # 此时强制重置，防止前端卡片被长链接撑爆
    if 'http' in venue:
        venue = "Research Community"

    # 如果清洗过头变空了，给个默认值
    if not venue:
        venue = "Research Community"

    return {
        "title": title,
        "link": link,
        "venue": venue,
        "date": year,
        "code": code_link
    }


# --- 4. 主流程控制器 ---

def run_extraction(source_key):
    config = SOURCES_CONFIG.get(source_key)
    if not config:
        print(f"❌ 找不到配置项: {source_key}")
        return

    # A. 准备数据
    main_db = load_json_safely(DB_FILE)
    existing_ids = {get_paper_id(item.get('title')) for item in main_db}

    staging_data = load_json_safely(STAGING_FILE)
    staging_map = {get_paper_id(item['title']): item for item in staging_data}

    # B. 读取文件
    if not os.path.exists(config['file_path']):
        print(f"❌ 找不到源文件: {config['file_path']}")
        return

    with open(config['file_path'], 'r', encoding='utf-8') as f:
        content = f.read()

    new_count = 0
    print(f"🚀 开始从 [{source_key}] 进货 (模式: {config['parser_type']})...")

    # C. 遍历章节
    for section_header, tag_name in config['sections']:
        pattern = re.escape(section_header) + r"\n(.*?)(?=\n#+ |$)"
        match = re.search(pattern, content, re.DOTALL)

        if not match: continue

        lines = match.group(1).split('\n')

        for line in lines:
            line = line.strip()
            if not line: continue

            parsed_item = None
            if config['parser_type'] == 'table':
                parsed_item = parse_table_row(line)
            elif config['parser_type'] == 'list':
                parsed_item = parse_list_line(line)

            if parsed_item:
                pid = get_paper_id(parsed_item['title'])

                if pid in existing_ids: continue

                if pid not in staging_map:
                    staging_map[pid] = {
                        "title": parsed_item['title'],
                        "link": parsed_item['link'],
                        "venue": parsed_item['venue'],
                        "date": parsed_item['date'],
                        "tags": [tag_name],
                        "source": source_key,
                        "code": parsed_item.get('code', ""),
                        "authors": "",
                        "description": "",
                        "image": ""
                    }
                    new_count += 1
                else:
                    if tag_name not in staging_map[pid]['tags']:
                        staging_map[pid]['tags'].append(tag_name)

    # D. 保存
    final_staging = list(staging_map.values())
    save_json_safely(final_staging, STAGING_FILE)

    print(f"✅ [{source_key}] 提取完成！")
    print(f"📊 本次新增到加工区: {new_count} 篇")
    print(f"📁 加工区当前总数: {len(final_staging)} 篇")


if __name__ == "__main__":
    # 执行精简后的梁让列表抓取
    run_extraction("pliang_list")
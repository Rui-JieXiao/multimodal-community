import os
import json
import re
import sys

# ================= 配置区 =================
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

OLD_DATA_FILE = os.path.join(project_root, "assets", "data", "datasets_data.json")
NEW_DATA_FILE = os.path.join(project_root, "assets", "data", "datasets_clean.json")

# 弱提示标准词表
HINT_MODALITIES = ["Image", "Text", "Video", "Audio", "3D", "Thermal"]
# 任务列表
HINT_TASKS = [
    "Pre-training", "Image-to-Text", "Text-to-Image",
    "Visual-Question-Answering", "Instruction-Tuning",
    "Caption", "QA", "Grounding", "Benchmark", "Zero-Shot-Classification"
]


# 已移除 HINT_LICENSES


# ================= 工具函数 =================

def load_json(path):
    if not os.path.exists(path): return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def parse_tags(user_input):
    """
    清洗输入：
    1. 支持空格或逗号分隔
    2. 自动首字母大写 (如 vqa -> VQA, image-to-text -> Image-To-Text)
    """
    if not user_input.strip(): return []
    # 按照逗号、中文逗号或一个/多个空格分割
    tokens = re.split(r'[,，\s]+', user_input)
    clean_tokens = []
    for t in tokens:
        val = t.strip()
        if not val: continue

        # 常见缩写全大写，其他首字母大写
        if val.lower() in ['vqa', 'qa', 'en', 'zh']:
            clean_tokens.append(val.upper() if val.lower() != 'en' and val.lower() != 'zh' else val.lower())
        else:
            clean_tokens.append(val.title() if val.islower() else val)

    return list(dict.fromkeys(clean_tokens))


# ================= 主逻辑 =================

def main():
    print("🚀 数据集清洗终端：高效搬运模式 (无License版)")
    print("-" * 60)

    # 1. 确定 Source
    default_source = "source_awesome_mllm.md"
    source_input = input(f"🔖 设定 Source [回车默认: {default_source}]: ").strip()
    current_source = source_input if source_input else default_source

    old_data = load_json(OLD_DATA_FILE)
    new_data = load_json(NEW_DATA_FILE)
    processed_titles = set(item['title'] for item in new_data)
    pending_items = [item for item in old_data if item['title'] not in processed_titles]

    print(f"📦 进度: {len(new_data)} / {len(old_data)} (剩余 {len(pending_items)} 篇)")

    for i, old_item in enumerate(pending_items):
        try:
            print("-" * 60)
            print(f"🔥 [{i + 1}/{len(pending_items)}] 处理对象: {old_item['title']}")
            print(f"   💡 参考描述: {old_item.get('description', '无')}")
            print(f"   🔗 参考旧链: {old_item.get('link', '无')}")
            print("-" * 20)

            # --- 1. 链接 ---
            access_url = input("1. Access URL (HF/Code): ").strip()

            # 默认为空，不复用旧链接，强制确认论文地址
            ref_input = input(f"2. Ref URL (优先录入论文地址) [直接回车为空]: ").strip()
            final_ref_url = ref_input

            # --- 2. 模态与任务 ---
            print(f"🧩 模态参考: {', '.join(HINT_MODALITIES)}")
            mod_input = input("3. 输入模态 (多个用空格隔开): ").strip()
            modalities = parse_tags(mod_input)

            print(f"🎯 任务参考: {', '.join(HINT_TASKS)}")
            task_input = input("4. 输入任务 (多个用空格隔开): ").strip()
            tasks = parse_tags(task_input)

            # --- 3. 其他属性 (License已移除) ---
            lang_input = input(f"🌐 语言 [默认 en, 多个用空格隔开]: ").strip()
            languages = parse_tags(lang_input) if lang_input else ["en"]

            year_input = input("📅 年份 (如 2024): ").strip()
            samples = input("🔢 样本量 (如 4.8M): ").strip()

            # --- 4. 简介 ---
            desc_input = input(f"📝 简介 [回车复用旧描述]: ").strip()
            final_desc = old_item.get('description', "") if not desc_input else (
                "" if desc_input == "." else desc_input)

            # --- 保存 ---
            new_item = {
                "title": old_item['title'],
                "access_url": access_url,
                "reference_url": final_ref_url,
                "description": final_desc,
                "modalities": modalities,
                "tasks": tasks,
                "languages": languages,
                # "license" 字段已彻底删除
                "year": year_input,
                "samples": samples,
                "source": current_source
            }

            new_data.append(new_item)
            save_json(NEW_DATA_FILE, new_data)
            print(f"✅ 已存入: {old_item['title']} (Tasks: {tasks})")

        except KeyboardInterrupt:
            print("\n🛑 进度已存档，下次从这里开始。")
            sys.exit(0)


if __name__ == "__main__":
    main()
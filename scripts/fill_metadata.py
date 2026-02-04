import json
import os
import webbrowser
import re

# --- 1. 路径配置 ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 生产库 (Destination)
DB_FILE = os.path.join(PROJECT_ROOT, "assets", "data", "papers_data.json")
# 加工区 (Source)
STAGING_FILE = os.path.join(PROJECT_ROOT, "assets", "data", "staging", "incoming_papers.json")


def get_paper_id(title):
    """生成标题唯一指纹 (用于查重)"""
    if not title: return "unknown"
    return re.sub(r'[^a-z0-9]', '', title.lower())


def load_json_safely(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 读取文件失败 {file_path}: {e}")
        return []


def save_json_safely(data, file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"❌ 保存文件失败 {file_path}: {e}")
        return False


def fill_metadata():
    # 1. 加载数据
    db_data = load_json_safely(DB_FILE)
    staging_data = load_json_safely(STAGING_FILE)

    # 建立主库指纹索引 (用于快速查重)
    existing_ids = {get_paper_id(p.get('title')) for p in db_data}

    total_queue = len(staging_data)
    if total_queue == 0:
        print("🎉 加工区 (Staging) 是空的！所有论文都已入库。")
        return

    print("=" * 60)
    print(f"🏭 启动流水线加工模式")
    print(f"📥 待处理队列: {total_queue} 篇")
    print(f"💾 目标主库: {len(db_data)} 篇已收录")
    print("-" * 60)
    print("操作指南:")
    print("   [输入文字] : 录入信息")
    print("   [Enter]    : 跳过/确认")
    print("   'open'     : 打开浏览器看原文")
    print("   'exit'     : 💾 保存进度并退出 (不会丢失当前正在处理的)")
    print("=" * 60)

    # 2. 队列循环 (贪吃蛇模式：处理一个，吃掉一个)
    # 我们不使用 for 循环，因为列表长度会变
    processed_count = 0

    while len(staging_data) > 0:
        # A. 始终取第一个
        paper = staging_data[0]
        pid = get_paper_id(paper.get('title'))
        title = paper.get('title', '无标题')

        print(f"\n📦 [{processed_count + 1}/{total_queue}] 正在加工: {title}")

        # B. 二次查重 (Double Check)
        if pid in existing_ids:
            print(f"⚠️  检测到主库已存在该论文，自动从待办中移除...")
            staging_data.pop(0)
            save_json_safely(staging_data, STAGING_FILE)
            continue

        # C. 交互式补全信息
        # 如果用户输入 'exit'，函数直接返回，不做任何保存更改，数据留在 Staging 等下次
        try:
            # --- 1. 作者 ---
            if not paper.get('authors'):
                print(f"🔗 Link: {paper.get('link', '无链接')}")
                while True:
                    val = input("   ✍️  [作者] (例如: Kaiming He, et al.): ").strip()
                    if val.lower() == 'exit': return
                    if val.lower() == 'open':
                        webbrowser.open(paper.get('link', ''))
                        continue
                    if val:
                        paper['authors'] = val
                    break  # 即使为空(回车)也跳出，允许之后在主库修改

            # --- 2. 描述 ---
            if not paper.get('description'):
                while True:
                    print("   📝 [中文描述] (建议: 复制摘要 -> 翻译):")
                    val = input("   > ").strip()
                    if val.lower() == 'exit': return
                    if val.lower() == 'open':
                        webbrowser.open(paper.get('link', ''))
                        continue
                    if val:
                        paper['description'] = val
                    break

            # --- 3. 代码 ---
            if not paper.get('code'):
                while True:
                    val = input("   💻 [代码链接] (GitHub URL / 回车为空): ").strip()
                    if val.lower() == 'exit': return
                    if val.lower() == 'open':
                        webbrowser.open(paper.get('link', ''))
                        continue
                    if val:
                        paper['code'] = val
                    break

        except KeyboardInterrupt:
            print("\n🛑 用户强制中断。")
            return

        # D. 事务提交 (Transaction Commit)
        print("   🔄 正在入库...", end="")

        # 1. 追加到内存中的主库列表
        db_data.append(paper)
        # 更新内存索引防止同批次重复
        existing_ids.add(pid)

        # 2. 保存主库 (这是最重要的一步，成品落袋)
        if save_json_safely(db_data, DB_FILE):
            # 3. 只有主库保存成功，才从 Staging 移除
            staging_data.pop(0)
            save_json_safely(staging_data, STAGING_FILE)
            print(" ✅ 已从加工区移除并归档！")
            processed_count += 1
        else:
            print(" ❌ 保存主库失败！停止处理以保护数据。")
            return

    print("\n🎉🎉🎉 太棒了！加工区已清空，所有新论文均已入库！")


if __name__ == "__main__":
    fill_metadata()
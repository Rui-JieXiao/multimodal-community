import os

# ❌ 目录黑名单：完全不显示这些文件夹
IGNORE_DIRS = {
    'venv', '.git', '__pycache__', '.idea', 'node_modules',
    '.vscode', '.nuxt', '.output', 'dist', 'coverage'
}

# 🚫 文件后缀黑名单：不显示这些类型的具体文件
IGNORE_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg', '.ico',  # 图片
    '.pyc', '.log', '.DS_Store', '.map'  # 系统/日志文件
}

# 📂 折叠目录：只显示文件夹名字，不打印里面的内容（适合放满图片的文件夹）
COLLAPSE_DIRS = {
    'cfp_covers', 'paper_images', 'competitions_images', 'public'
}


def print_tree(dir_path, prefix=''):
    try:
        files = os.listdir(dir_path)
    except PermissionError:
        return

    # 1. 排序：文件夹排前面，文件排后面 (可选，也可以直接 sort() 按字母排)
    files.sort(key=lambda x: (not os.path.isdir(os.path.join(dir_path, x)), x))

    # 2. 核心过滤逻辑
    filtered_files = []
    for f in files:
        # 过滤目录黑名单
        if f in IGNORE_DIRS:
            continue

        # 过滤文件后缀
        _, ext = os.path.splitext(f)
        if ext.lower() in IGNORE_EXTENSIONS:
            continue

        filtered_files.append(f)

    files = filtered_files
    count = len(files)

    for i, file in enumerate(files):
        path = os.path.join(dir_path, file)
        is_last = (i == count - 1)

        # 打印树枝
        connector = '└── ' if is_last else '├── '

        # 如果是需要折叠的目录，在后面加个标记
        if file in COLLAPSE_DIRS:
            print(f"{prefix}{connector}{file} 📦 (内容已折叠)")
            continue  # 跳过递归，不再打印里面的内容

        print(f"{prefix}{connector}{file}")

        # 如果是文件夹，且不在折叠名单里，才递归
        if os.path.isdir(path):
            extension = '    ' if is_last else '│   '
            print_tree(path, prefix + extension)


if __name__ == "__main__":
    # 获取项目根目录 (假设脚本在 scripts/ 下，根目录就是上一级)
    # 如果脚本就在根目录下，可以直接用 os.getcwd()
    current_script_path = os.path.abspath(__file__)

    # 这里假设脚本在项目根目录，如果不是，请调整 os.path.dirname 的层数
    project_root = os.path.dirname(os.path.dirname(current_script_path))
    # 如果脚本就在根目录，用这行：
    # project_root = os.path.dirname(current_script_path)

    print(f"📦 项目结构: {os.path.basename(project_root)}")
    print_tree(project_root)
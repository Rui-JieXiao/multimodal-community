import os
import requests

# 目标会议列表
CONFERENCES = ["neurips", "icml", "iclr", "acm_mm", "cvpr"]
# 数据源地址
BASE_URL = "https://raw.githubusercontent.com/huggingface/ai-deadlines/refs/heads/main/src/data/conferences/"
# 保存目录：只保存 .yml 源文件
SAVE_DIR = os.path.join(os.path.dirname(__file__), "../assets/data/deadlines")


def update_deadlines():
    # 确保目录存在
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    print(f"🚀 开始同步 .yml 源文件...")

    for conf in CONFERENCES:
        file_name = f"{conf}.yml"
        url = f"{BASE_URL}{file_name}"
        save_path = os.path.join(SAVE_DIR, file_name)

        try:
            print(f"⬇️  正在下载: {file_name} ...")
            response = requests.get(url, timeout=15)

            if response.status_code == 200:
                # 直接以二进制写入文件，不做任何解析或修改
                with open(save_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ 下载成功: {save_path}")
            else:
                print(f"⚠️ 下载失败: {file_name} (Status: {response.status_code})")

        except Exception as e:
            print(f"❌ 网络/IO错误: {conf} -> {str(e)}")

    print(f"\n✨ 同步任务结束。请前往 assets/data/deadlines 检查源文件。")


if __name__ == "__main__":
    update_deadlines()
import os
from PIL import Image


def process_competition_covers():
    base_path = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(base_path, "raw")
    output_folder = os.path.join(base_path, "processed")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if not os.path.exists(input_folder):
        print(f"❌ 错误：请先创建 {input_folder} 文件夹并放入原始图片")
        return

    # 设置目标画框参数 (3.2:1)
    TARGET_W, TARGET_H = 1200, 375
    # 背景颜色：绝对纯白
    BG_COLOR = (255, 255, 255)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            img_path = os.path.join(input_folder, filename)

            try:
                with Image.open(img_path) as img:
                    # 1. 统一转为 RGBA 处理透明度
                    img = img.convert("RGBA")

                    # 2. 计算最佳缩放比例 (Contain 模式)
                    # 逻辑：比较原图比例和目标框比例，以“短板”为准，确保图片能完整塞进去
                    img_ratio = img.width / img.height
                    target_ratio = TARGET_W / TARGET_H

                    if img_ratio > target_ratio:
                        # 原图比画框更“扁长”：宽度撑满，高度自动缩放
                        new_w = TARGET_W
                        new_h = int(new_w / img_ratio)
                    else:
                        # 原图比画框更“方”或“高”：高度撑满，宽度自动缩放
                        new_h = TARGET_H
                        new_w = int(new_h * img_ratio)

                    # 3. 执行缩放
                    img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

                    # 4. 创建纯白背景画布
                    background = Image.new('RGBA', (TARGET_W, TARGET_H), BG_COLOR)

                    # 5. 居中合成
                    # 计算居中位置
                    offset_x = (TARGET_W - new_w) // 2
                    offset_y = (TARGET_H - new_h) // 2

                    # 粘贴 (使用 mask 确保透明通道正确处理)
                    background.paste(img_resized, (offset_x, offset_y), mask=img_resized)

                    # 6. 转回 RGB 并保存
                    final_output = background.convert('RGB')
                    clean_name = os.path.splitext(filename)[0]
                    save_path = os.path.join(output_folder, f"{clean_name}.webp")

                    final_output.save(save_path, "WEBP", quality=95)
                    print(f"✅ [完整模式] 已处理: {clean_name}.webp (原图无裁切，背景纯白)")

            except Exception as e:
                print(f"⚠️ 处理失败 {filename}: {e}")


if __name__ == "__main__":
    process_competition_covers()
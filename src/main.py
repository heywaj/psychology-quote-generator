from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import textwrap, os

# ========== 路径配置 ==========
# 获取项目根目录
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

logo_path = os.path.join(project_root, "resources", "logo.png")
font_path = os.path.join(project_root, "resources", "fonts", "SmileySans-Oblique.ttf")
quotes_path = os.path.join(project_root, "resources", "quotes.csv")
output_dir = os.path.join(project_root, "output")
os.makedirs(output_dir, exist_ok=True)

# ========== 画布参数 ==========
# 提升到4K分辨率以获得MB级别的高清图片
IMG_WIDTH, IMG_HEIGHT = 2160, 3840  # 4K竖屏分辨率 (原来的2倍)
# BACKGROUND_TOP = (25, 30, 50)    # 渐变上部颜色（深蓝）
# BACKGROUND_BOTTOM = (10, 15, 25) # 渐变下部颜色（更深蓝）
BACKGROUND_TOP = (245, 240, 230)
BACKGROUND_BOTTOM = (230, 220, 200)
TEXT_COLOR_MAIN = (60, 60, 60)        # 深灰色主文字，与浅色背景形成对比
TEXT_COLOR_REFLECT = (120, 120, 120)  # 中灰色反思文字

# DPI设置，提升打印和显示质量
DPI = 300  # 高质量DPI

# ========== 字体 ==========
# 4K分辨率下的字体大小 (按2倍比例放大)
FONT_SIZE_MAIN = 160      # 主字体 (原80*2)
FONT_SIZE_REFLECT = 110   # 副字体 (原55*2)

try:
    font_main = ImageFont.truetype(font_path, FONT_SIZE_MAIN)
    font_reflect = ImageFont.truetype(font_path, FONT_SIZE_REFLECT)
    print("✅ 已载入自定义字体 (4K高分辨率)")
except OSError:
    print(f"⚠️ 字体文件未找到: {font_path}")
    print("💡 使用系统默认字体，建议下载字体文件以获得更好效果")
    try:
        # Windows 系统字体
        font_main = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", FONT_SIZE_MAIN)
        font_reflect = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", FONT_SIZE_REFLECT)
    except OSError:
        font_main = ImageFont.load_default()
        font_reflect = ImageFont.load_default()
        print("⚠️ 使用默认字体，显示效果可能不佳")

# ========== 渐变背景函数 ==========
def create_gradient_bg(width, height, top_color, bottom_color):
    """创建高质量渐变背景"""
    # 创建高分辨率背景
    bg = Image.new("RGB", (width, height), top_color)
    draw = ImageDraw.Draw(bg)
    
    top_r, top_g, top_b = top_color
    bot_r, bot_g, bot_b = bottom_color
    
    # 使用更高效的渐变算法
    for y in range(height):
        ratio = y / height
        # 使用浮点数计算以获得更平滑的渐变
        r = int(top_r * (1 - ratio) + bot_r * ratio)
        g = int(top_g * (1 - ratio) + bot_g * ratio)
        b = int(top_b * (1 - ratio) + bot_b * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return bg.convert("RGBA")

# ========== 载入语录 ==========
df = pd.read_csv(quotes_path, encoding="utf-8")
logo = Image.open(logo_path).convert("RGBA")

print(f"🎨 开始生成4K高清图片 ({IMG_WIDTH}x{IMG_HEIGHT})")
print(f"📝 共有 {len(df)} 条语录待处理")
print("=" * 50)

for idx, (_, row) in enumerate(df.iterrows(), 1):
    print(f"🔄 处理第 {idx}/{len(df)} 条语录: ID {row['id']}")
    # 创建渐变背景
    bg = create_gradient_bg(IMG_WIDTH, IMG_HEIGHT, BACKGROUND_TOP, BACKGROUND_BOTTOM)
    draw = ImageDraw.Draw(bg)

    # --- 放置 logo (4K分辨率下按比例放大) ---
    logo_size = (360, 360)  # 4K下的logo尺寸 (原180*2)
    logo_resized = logo.resize(logo_size, Image.Resampling.LANCZOS)  # 使用高质量重采样
    
    # 创建logo阴影效果，避免硬嵌入感
    logo_pos = (160, 160)  # 4K下的logo位置 (原80*2)
    
    # 添加轻微的阴影效果 (按比例放大)
    shadow_offset = (6, 6)  # 原3*2
    shadow_color = (0, 0, 0, 60)  # 半透明黑色阴影
    shadow_img = Image.new('RGBA', logo_size, shadow_color)
    bg.paste(shadow_img, (logo_pos[0] + shadow_offset[0], logo_pos[1] + shadow_offset[1]), shadow_img)
    
    # 粘贴主logo
    bg.paste(logo_resized, logo_pos, logo_resized)

    # --- 主体心理句 (4K分辨率下按比例放大) ---
    text = textwrap.fill(row['content'], width=10)  # 保持每行字数不变
    bbox = draw.textbbox((0, 0), text, font=font_main)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    main_text_y = 1500  # 4K下的Y位置 (原750*2)
    
    # 使用超采样技术来消除锯齿
    # 创建更大尺寸的临时画布进行渲染，然后缩放回原尺寸
    scale_factor = 2  # 超采样倍数
    temp_size = (int(w * scale_factor), int(h * scale_factor))
    temp_img = Image.new('RGBA', temp_size, (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # 在超采样画布上绘制文字
    temp_font = ImageFont.truetype(font_path if os.path.exists(font_path) else "C:/Windows/Fonts/msyh.ttc", 
                                  int(FONT_SIZE_MAIN * scale_factor))
    temp_draw.text((0, 0), text, font=temp_font, fill=TEXT_COLOR_MAIN)
    
    # 缩放回原尺寸并应用抗锯齿
    final_text_img = temp_img.resize((w, h), Image.Resampling.LANCZOS)
    
    # 粘贴到主画布
    text_x = int((IMG_WIDTH - w) / 2)
    bg.paste(final_text_img, (text_x, main_text_y), final_text_img)

    # --- 引发思考 (4K分辨率下按比例放大) ---
    reflection = textwrap.fill(row['reflection'], width=16)  # 保持每行字数不变
    bbox_r = draw.textbbox((0, 0), reflection, font=font_reflect)
    rw, rh = bbox_r[2] - bbox_r[0], bbox_r[3] - bbox_r[1]
    reflect_text_y = 2800  # 4K下的Y位置 (原1400*2)
    
    # 对反思文字也使用超采样抗锯齿
    temp_size_r = (int(rw * scale_factor), int(rh * scale_factor))
    temp_img_r = Image.new('RGBA', temp_size_r, (0, 0, 0, 0))
    temp_draw_r = ImageDraw.Draw(temp_img_r)
    
    # 在超采样画布上绘制反思文字
    temp_font_r = ImageFont.truetype(font_path if os.path.exists(font_path) else "C:/Windows/Fonts/msyh.ttc", 
                                    int(FONT_SIZE_REFLECT * scale_factor))
    temp_draw_r.text((0, 0), reflection, font=temp_font_r, fill=TEXT_COLOR_REFLECT)
    
    # 缩放回原尺寸并应用抗锯齿
    final_reflect_img = temp_img_r.resize((rw, rh), Image.Resampling.LANCZOS)
    
    # 粘贴到主画布
    reflect_x = int((IMG_WIDTH - rw) / 2)
    bg.paste(final_reflect_img, (reflect_x, reflect_text_y), final_reflect_img)

    # --- 保存高质量图片 ---
    filename = os.path.join(output_dir, f"{row['id']}_独白之所_4K.png")
    
    # 保存为无损高质量PNG，确保达到MB级别
    # 关闭所有压缩以获得最大文件大小和质量
    bg.save(filename, "PNG", 
            optimize=False,      # 关闭优化
            compress_level=0,    # 最低压缩级别
            dpi=(DPI, DPI))      # 设置高DPI
    
    # 获取文件大小并显示
    file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
    print(f"📸 生成图片: {os.path.basename(filename)} ({file_size:.1f}MB)")

print("✅ 批量生成完成！输出目录：", output_dir)

from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import textwrap, os

# ========== 路径配置 ==========
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

logo_path = os.path.join(project_root, "resources", "logo.png")
font_path = os.path.join(project_root, "resources", "fonts", "SmileySans-Oblique.ttf")
quotes_path = os.path.join(project_root, "resources", "quotes.csv")
output_dir = os.path.join(project_root, "output")
os.makedirs(output_dir, exist_ok=True)

# ========== 画布参数 ==========
IMG_WIDTH, IMG_HEIGHT = 2160, 3840  # 4K竖屏分辨率
BACKGROUND_TOP = (245, 240, 230)
BACKGROUND_BOTTOM = (230, 220, 200)
TEXT_COLOR_MAIN = (60, 60, 60)
TEXT_COLOR_REFLECT = (120, 120, 120)
DPI = 300

# ========== 专业级抗锯齿设置 ==========
SUPER_SAMPLE_FACTOR = 4  # 4倍超采样，完全消除锯齿
FONT_SIZE_MAIN = 160
FONT_SIZE_REFLECT = 110

# ========== 字体 ==========
try:
    font_main = ImageFont.truetype(font_path, FONT_SIZE_MAIN)
    font_reflect = ImageFont.truetype(font_path, FONT_SIZE_REFLECT)
    print("✅ 已载入自定义字体 (专业级抗锯齿)")
except OSError:
    print(f"⚠️ 字体文件未找到: {font_path}")
    try:
        font_main = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", FONT_SIZE_MAIN)
        font_reflect = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", FONT_SIZE_REFLECT)
    except OSError:
        font_main = ImageFont.load_default()
        font_reflect = ImageFont.load_default()

def create_gradient_bg(width, height, top_color, bottom_color):
    """创建高质量渐变背景"""
    bg = Image.new("RGB", (width, height), top_color)
    draw = ImageDraw.Draw(bg)
    
    top_r, top_g, top_b = top_color
    bot_r, bot_g, bot_b = bottom_color
    
    for y in range(height):
        ratio = y / height
        r = int(top_r * (1 - ratio) + bot_r * ratio)
        g = int(top_g * (1 - ratio) + bot_g * ratio)
        b = int(top_b * (1 - ratio) + bot_b * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return bg.convert("RGBA")

def render_text_with_supersampling(text, font_size, text_color, max_width=None):
    """使用超高倍采样渲染无锯齿文字"""
    # 创建超高分辨率字体
    super_font_size = font_size * SUPER_SAMPLE_FACTOR
    try:
        super_font = ImageFont.truetype(font_path if os.path.exists(font_path) else "C:/Windows/Fonts/msyh.ttc", super_font_size)
    except:
        super_font = ImageFont.load_default()
    
    # 在超高分辨率画布上绘制
    temp_draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    bbox = temp_draw.textbbox((0, 0), text, font=super_font)
    super_w, super_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    # 增加更多边距以防止裁剪，特别是底部
    padding_x = 40  # 左右边距
    padding_y = 60  # 上下边距，增加更多以防止底部裁剪
    
    # 创建超高分辨率临时画布，增加足够的边距
    canvas_w = super_w + padding_x * 2
    canvas_h = super_h + padding_y * 2
    super_img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    super_draw = ImageDraw.Draw(super_img)
    
    # 计算文字在画布上的位置，确保有足够边距
    text_x = padding_x
    text_y = padding_y
    
    # 绘制文字
    super_draw.text((text_x, text_y), text, font=super_font, fill=text_color)
    
    # 缩放回原尺寸，使用最高质量的Lanczos算法
    final_w = canvas_w // SUPER_SAMPLE_FACTOR
    final_h = canvas_h // SUPER_SAMPLE_FACTOR
    
    final_img = super_img.resize((final_w, final_h), Image.Resampling.LANCZOS)
    
    return final_img, final_w, final_h

def draw_decorative_divider(draw, x, y, width, style="elegant"):
    """绘制装饰性分隔栏"""
    center_x = x + width // 2
    
    if style == "elegant":
        # 优雅的线条设计
        line_color = (150, 150, 150, 180)
        accent_color = (100, 100, 100, 200)
        
        # 主线条
        draw.line([(x + 100, y), (x + width - 100, y)], fill=line_color, width=2)
        
        # 中心装饰
        draw.ellipse([center_x - 15, y - 15, center_x + 15, y + 15], fill=accent_color)
        draw.ellipse([center_x - 8, y - 8, center_x + 8, y + 8], fill=(200, 200, 200, 150))
        
        # 两侧小装饰
        for offset in [-120, 120]:
            draw.ellipse([center_x + offset - 5, y - 5, center_x + offset + 5, y + 5], fill=accent_color)
    
    elif style == "geometric":
        # 几何图形设计
        line_color = (120, 120, 120, 160)
        
        # 主线条
        draw.line([(x + 80, y), (x + width - 80, y)], fill=line_color, width=3)
        
        # 菱形装饰
        diamond_size = 20
        points = [
            (center_x, y - diamond_size),
            (center_x + diamond_size, y),
            (center_x, y + diamond_size),
            (center_x - diamond_size, y)
        ]
        draw.polygon(points, fill=(140, 140, 140, 180))
        
        # 小三角形
        for offset in [-100, 100]:
            tri_points = [
                (center_x + offset, y - 8),
                (center_x + offset - 8, y + 8),
                (center_x + offset + 8, y + 8)
            ]
            draw.polygon(tri_points, fill=line_color)

def add_corner_decorations(draw, width, height):
    """添加角落装饰"""
    corner_color = (160, 160, 160, 100)
    
    # 左上角装饰
    points = [(50, 50), (150, 50), (50, 150)]
    draw.polygon(points, fill=corner_color)
    
    # 右下角装饰
    points = [(width - 50, height - 50), (width - 150, height - 50), (width - 50, height - 150)]
    draw.polygon(points, fill=corner_color)

def draw_subtle_pattern(bg, width, height):
    """添加微妙的背景图案"""
    pattern_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    pattern_draw = ImageDraw.Draw(pattern_img)
    
    # 绘制微妙的网格图案
    grid_color = (255, 255, 255, 15)  # 非常淡的白色
    grid_size = 100
    
    # 垂直线
    for x in range(0, width, grid_size):
        pattern_draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    
    # 水平线
    for y in range(0, height, grid_size):
        pattern_draw.line([(0, y), (width, y)], fill=grid_color, width=1)
    
    # 将图案叠加到背景
    bg = Image.alpha_composite(bg, pattern_img)
    return bg

# ========== 载入语录 ==========
df = pd.read_csv(quotes_path, encoding="utf-8")
logo = Image.open(logo_path).convert("RGBA")

print(f"🎨 开始生成专业级抗锯齿4K图片 ({IMG_WIDTH}x{IMG_HEIGHT})")
print(f"🔧 超采样倍数: {SUPER_SAMPLE_FACTOR}x (完全消除锯齿)")
print(f"📝 共有 {len(df)} 条语录待处理")
print("=" * 60)

for idx, (_, row) in enumerate(df.iterrows(), 1):
    print(f"🔄 处理第 {idx}/{len(df)} 条语录: ID {row['id']}")
    
    # 创建渐变背景
    bg = create_gradient_bg(IMG_WIDTH, IMG_HEIGHT, BACKGROUND_TOP, BACKGROUND_BOTTOM)
    
    # --- 添加微妙背景图案 ---
    bg = draw_subtle_pattern(bg, IMG_WIDTH, IMG_HEIGHT)
    
    # 创建绘制对象
    draw = ImageDraw.Draw(bg)
    
    # --- 添加角落装饰 ---
    add_corner_decorations(draw, IMG_WIDTH, IMG_HEIGHT)
    
    # --- 放置 logo ---
    logo_size = (360, 360)
    logo_resized = logo.resize(logo_size, Image.Resampling.LANCZOS)
    logo_pos = (160, 160)
    
    # 添加logo周围的装饰圆环
    ring_center = (logo_pos[0] + logo_size[0]//2, logo_pos[1] + logo_size[1]//2)
    ring_radius = logo_size[0]//2 + 30
    ring_color = (180, 180, 180, 80)
    
    # 绘制装饰圆环
    draw.ellipse([ring_center[0] - ring_radius, ring_center[1] - ring_radius,
                  ring_center[0] + ring_radius, ring_center[1] + ring_radius], 
                 outline=ring_color, width=3)
    
    # 添加阴影效果
    shadow_offset = (8, 8)
    shadow_color = (0, 0, 0, 40)
    shadow_img = Image.new('RGBA', logo_size, shadow_color)
    bg.paste(shadow_img, (logo_pos[0] + shadow_offset[0], logo_pos[1] + shadow_offset[1]), shadow_img)
    bg.paste(logo_resized, logo_pos, logo_resized)
    
    # --- 添加标题文字 "每天一点心理学" ---
    title_text = "每天一点心理学"
    title_font_size = 85  # 适中的标题字体大小
    title_color = (80, 80, 80)  # 深灰色
    
    # 创建标题字体
    try:
        title_font = ImageFont.truetype(font_path if os.path.exists(font_path) else "C:/Windows/Fonts/msyh.ttc", title_font_size)
    except:
        title_font = ImageFont.load_default()
    
    # 使用超采样渲染标题
    title_img, title_w, title_h = render_text_with_supersampling(title_text, title_font_size, title_color)
    
    # 标题位置：logo右边，垂直居中对齐
    title_x = logo_pos[0] + logo_size[0] + 80  # logo右边留80px间距
    title_y = logo_pos[1] + (logo_size[1] - title_h) // 2  # 与logo垂直居中
    
    # 为标题添加装饰性下划线
    underline_y = title_y + title_h + 15
    underline_color = (120, 120, 120, 150)
    draw.line([(title_x, underline_y), (title_x + title_w, underline_y)], 
              fill=underline_color, width=3)
    
    # 粘贴标题文字
    bg.paste(title_img, (title_x, title_y), title_img)

    # --- 上装饰分隔栏 ---
    divider_y_top = 1300
    draw_decorative_divider(draw, 0, divider_y_top, IMG_WIDTH, "elegant")
    
    # --- 主体心理句 (专业级抗锯齿) ---
    text = textwrap.fill(row['content'], width=10)
    main_text_img, text_w, text_h = render_text_with_supersampling(text, FONT_SIZE_MAIN, TEXT_COLOR_MAIN)
    
    main_text_y = 1400
    text_x = (IMG_WIDTH - text_w) // 2
    
    # 直接粘贴主文字，不添加背景框
    bg.paste(main_text_img, (text_x, main_text_y), main_text_img)
    
    # --- 下装饰分隔栏 ---
    divider_y_bottom = main_text_y + text_h + 150
    draw_decorative_divider(draw, 0, divider_y_bottom, IMG_WIDTH, "geometric")

    # --- 引发思考 (专业级抗锯齿) ---
    reflection = textwrap.fill(row['reflection'], width=16)
    reflect_img, reflect_w, reflect_h = render_text_with_supersampling(reflection, FONT_SIZE_REFLECT, TEXT_COLOR_REFLECT)
    
    reflect_text_y = divider_y_bottom + 200
    reflect_x = (IMG_WIDTH - reflect_w) // 2
    
    # 为反思文字添加引号装饰
    quote_size = 40
    quote_color = (150, 150, 150, 120)
    
    # 左引号
    left_quote_x = reflect_x - 80
    left_quote_y = reflect_text_y - 20
    draw.text((left_quote_x, left_quote_y), '"', font=ImageFont.truetype(
        font_path if os.path.exists(font_path) else "C:/Windows/Fonts/msyh.ttc", quote_size*2), 
        fill=quote_color)
    
    # 右引号
    right_quote_x = reflect_x + reflect_w + 40
    right_quote_y = reflect_text_y + reflect_h - 60
    draw.text((right_quote_x, right_quote_y), '"', font=ImageFont.truetype(
        font_path if os.path.exists(font_path) else "C:/Windows/Fonts/msyh.ttc", quote_size*2), 
        fill=quote_color)
    
    bg.paste(reflect_img, (reflect_x, reflect_text_y), reflect_img)
    
    # --- 底部装饰线条 ---
    bottom_line_y = reflect_text_y + reflect_h + 100
    line_color = (140, 140, 140, 100)
    draw.line([(IMG_WIDTH//4, bottom_line_y), (IMG_WIDTH*3//4, bottom_line_y)], 
              fill=line_color, width=3)

    # --- 保存超高质量图片 ---
    filename = os.path.join(output_dir, f"{row['id']}_独白之所_超清抗锯齿.png")
    
    bg.save(filename, "PNG", optimize=False, compress_level=0, dpi=(DPI, DPI))
    
    file_size = os.path.getsize(filename) / (1024 * 1024)
    print(f"📸 生成图片: {os.path.basename(filename)} ({file_size:.1f}MB)")

print("✅ 专业级抗锯齿批量生成完成！输出目录：", output_dir)
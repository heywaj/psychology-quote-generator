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
FONT_SIZE_MAIN = 160     # 默认字体大小（短文本）
FONT_SIZE_REFLECT = 110  # 副文字字体大小

# ========== 动态字体大小调整 ==========
def get_optimal_font_size(text_length, base_font_size=160):
    """根据文本长度动态调整字体大小"""
    # 文本长度阈值和对应的字体大小
    if text_length <= 30:        # 短文本
        return base_font_size
    elif text_length <= 50:      # 中等文本
        return int(base_font_size * 0.85)  # 136px
    elif text_length <= 80:      # 较长文本
        return int(base_font_size * 0.7)   # 112px
    elif text_length <= 120:     # 长文本
        return int(base_font_size * 0.6)   # 96px
    else:                        # 超长文本
        return int(base_font_size * 0.5)   # 80px

def extract_theme_keyword(content):
    """从内容中提取主题关键词"""
    # 常见的心理学主题词映射
    theme_keywords = {
        '焦虑与安全感': ['焦虑', '紧张', '不安', '担心', '恐惧', '害怕', '威胁', '危险', '安全'],
        '情绪与感受': ['情绪', '感受', '心情', '愤怒', '难过', '开心', '悲伤', '快乐', '痛苦'],
        '自我认知': ['自己', '自我', '内心', '性格', '个性', '认识', '了解', '发现'],
        '人际关系': ['关系', '朋友', '家人', '同事', '社交', '交往', '沟通', '理解'],
        '压力与释放': ['压力', '疲惫', '累', '负担', '重压', '紧绷', '疲劳', '休息'],
        '成长与改变': ['成长', '改变', '进步', '学习', '发展', '提升', '突破', '蜕变'],
        '内心平静': ['平静', '安静', '宁静', '放松', '冥想', '呼吸', '缓慢', '安心'],
        '自信与勇气': ['自信', '勇气', '坚强', '力量', '能力', '勇敢', '坚持', '相信'],
        '生活智慧': ['智慧', '道理', '明白', '领悟', '思考', '理解', '感悟', '启发'],
        '心理疗愈': ['疗愈', '治疗', '康复', '恢复', '健康', '修复', '愈合'],
        '敏感与天赋': ['敏感', '天赋', '感官', '细腻', '敏锐', '天生', '特质'],
        '控制与接纳': ['控制', '掌控', '接纳', '允许', '放手', '顺其自然'],
        '时间与节奏': ['时间', '节奏', '时区', '慢下来', '当下', '现在', '此刻'],
        '希望与连接': ['希望', '连接', '在乎', '爱', '关心', '联系', '纽带']
    }
    
    # 检查内容中是否包含特定关键词
    for theme, keywords in theme_keywords.items():
        for keyword in keywords:
            if keyword in content:
                return theme
    
    # 如果没有匹配到特定主题，返回默认主题
    if '你' in content and ('自己' in content or '内心' in content):
        return '自我对话'
    elif '生活' in content or '人生' in content:
        return '生活感悟'
    elif '身体' in content or '呼吸' in content:
        return '身心合一'
    else:
        return '心理洞察'

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

def render_text_with_supersampling(text, font_size, text_color, line_spacing=1.4):
    """使用超高倍采样渲染无锯齿文字，支持行距调整"""
    # 创建超高分辨率字体
    super_font_size = font_size * SUPER_SAMPLE_FACTOR
    try:
        super_font = ImageFont.truetype(font_path if os.path.exists(font_path) else "C:/Windows/Fonts/msyh.ttc", super_font_size)
    except:
        super_font = ImageFont.load_default()
    
    # 分割文本为多行
    lines = text.split('\n')
    
    # 计算每行的尺寸
    temp_draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    line_heights = []
    line_widths = []
    max_width = 0
    
    for line in lines:
        bbox = temp_draw.textbbox((0, 0), line, font=super_font)
        line_w = bbox[2] - bbox[0]
        line_h = bbox[3] - bbox[1]
        line_widths.append(line_w)
        line_heights.append(line_h)
        max_width = max(max_width, line_w)
    
    # 计算总高度（包含行距）
    if len(lines) > 1:
        base_line_height = max(line_heights) if line_heights else super_font_size
        total_height = base_line_height * len(lines) + (len(lines) - 1) * base_line_height * (line_spacing - 1.0)
    else:
        total_height = line_heights[0] if line_heights else super_font_size
    
    # 增加边距
    padding_x = 40
    padding_y = 60
    
    canvas_w = int(max_width + padding_x * 2)
    canvas_h = int(total_height + padding_y * 2)
    super_img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    super_draw = ImageDraw.Draw(super_img)
    
    # 绘制每行文字
    current_y = padding_y
    base_line_height = max(line_heights) if line_heights else super_font_size
    
    for i, line in enumerate(lines):
        text_x = padding_x + (max_width - line_widths[i]) // 2  # 居中对齐
        super_draw.text((text_x, current_y), line, font=super_font, fill=text_color)
        
        if i < len(lines) - 1:  # 不是最后一行
            current_y += base_line_height * line_spacing
    
    # 缩放回原尺寸
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

    # --- 主题小标题（高位浮动，超大字号设计） ---
    content_text = row['content'].strip()
    theme_keyword = extract_theme_keyword(content_text)
    
    # 渲染主题小标题 - 超大字号，现代化设计
    theme_font_size = 140  # 继续增大到140px，更加突出
    theme_color = (50, 90, 140, 255)  # 更深的蓝色，增强视觉冲击力
    theme_img, theme_w, theme_h = render_text_with_supersampling(theme_keyword, theme_font_size, theme_color)
    
    # 主题标题位置（超高位浮动，视觉焦点）
    theme_y = 1000  # 继续上移到1000，极致突出
    theme_x = (IMG_WIDTH - theme_w) // 2
    
    # 为主题词添加微妙阴影效果
    shadow_offset = 6
    shadow_color = (50, 90, 140, 80)  # 浅色阴影
    shadow_img, _, _ = render_text_with_supersampling(theme_keyword, theme_font_size, shadow_color)
    bg.paste(shadow_img, (theme_x + shadow_offset, theme_y + shadow_offset), shadow_img)
    
    # 粘贴主题词
    bg.paste(theme_img, (theme_x, theme_y), theme_img)
    
    # 主题标题下方添加现代化装饰线组
    line_length = theme_w + 100  # 进一步增加装饰线长度
    line_x = (IMG_WIDTH - line_length) // 2
    line_y = theme_y + theme_h + 30  # 增加更多间距
    
    # 现代化四线设计，创造丰富层次
    draw.line([(line_x, line_y), (line_x + line_length, line_y)], 
              fill=(50, 90, 140, 220), width=5)  # 主线，最粗最深
    draw.line([(line_x + 40, line_y + 12), (line_x + line_length - 40, line_y + 12)], 
              fill=(80, 120, 160, 160), width=3)  # 中粗线
    draw.line([(line_x + 70, line_y + 22), (line_x + line_length - 70, line_y + 22)], 
              fill=(120, 150, 180, 120), width=2)  # 细线
    draw.line([(line_x + 90, line_y + 30), (line_x + line_length - 90, line_y + 30)], 
              fill=(170, 180, 190, 80), width=1)  # 最轻装饰线
    
    # --- 上装饰分隔栏（调整到更下方，给主题词更多空间） ---
    divider_y_top = 1320  # 进一步下移，增加主题词的独立空间
    draw_decorative_divider(draw, 0, divider_y_top, IMG_WIDTH, "elegant")

    # --- 主体心理句 (动态字体大小 + 增强行距 + 极小页边距) ---
    content_length = len(content_text)
    
    # 根据文本长度动态调整字体大小和换行宽度
    optimal_font_size = get_optimal_font_size(content_length)
    
    # 进一步增加换行宽度，极大化内容显示范围
    if optimal_font_size >= 140:
        wrap_width = 14  # 大字体，进一步增加每行字数
    elif optimal_font_size >= 120:
        wrap_width = 18  # 中字体，显著增加
    elif optimal_font_size >= 100:
        wrap_width = 22  # 小字体，大幅增加
    else:
        wrap_width = 26  # 最小字体，最大化利用空间
    
    text = textwrap.fill(content_text, width=wrap_width)
    
    # 使用增强的行距提升可读性
    line_spacing = 1.6  # 增加行距到1.6倍，提升阅读舒适度
    main_text_img, text_w, text_h = render_text_with_supersampling(text, optimal_font_size, TEXT_COLOR_MAIN, line_spacing)
    
    # 输出调试信息
    print(f"   🏷️  主题标签: {theme_keyword}")
    print(f"   📝 内容长度: {content_length}字 | 字体大小: {optimal_font_size}px | 换行宽度: {wrap_width}字/行 | 行距: {line_spacing}")
    
    # 主体文本位置（调整到分割线下方）
    main_text_y = divider_y_top + 120  # 在装饰分割线下方
    text_x = (IMG_WIDTH - text_w) // 2
    
    # 直接粘贴主文字，享受增强的行距效果
    bg.paste(main_text_img, (text_x, main_text_y), main_text_img)
    
    # --- 下装饰分隔栏 ---
    divider_y_bottom = main_text_y + text_h + 150
    draw_decorative_divider(draw, 0, divider_y_bottom, IMG_WIDTH, "geometric")

    # --- 引发思考 (动态字体大小 + 增强行距 + 专业级抗锯齿) ---
    reflection_text = row['reflection'].strip()
    reflection_length = len(reflection_text)
    
    # 反思文字也根据长度调整字体大小
    reflection_font_size = get_optimal_font_size(reflection_length, base_font_size=110)
    
    # 根据字体大小调整换行宽度，进一步增加
    if reflection_font_size >= 100:
        reflect_wrap_width = 18  # 增加页边距利用
    elif reflection_font_size >= 80:
        reflect_wrap_width = 22
    else:
        reflect_wrap_width = 25
    
    reflection = textwrap.fill(reflection_text, width=reflect_wrap_width)
    
    # 反思文字也使用舒适的行距
    reflection_line_spacing = 1.5
    reflect_img, reflect_w, reflect_h = render_text_with_supersampling(reflection, reflection_font_size, TEXT_COLOR_REFLECT, reflection_line_spacing)
    
    print(f"   💭 反思长度: {reflection_length}字 | 字体大小: {reflection_font_size}px | 换行宽度: {reflect_wrap_width}字/行 | 行距: {reflection_line_spacing}")
    
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
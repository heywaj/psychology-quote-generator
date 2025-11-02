from main_antialiasing import *

print("🎨 生成单张测试图片 - 展示设计元素")

# 载入数据
df = pd.read_csv(quotes_path, encoding="utf-8")
logo = Image.open(logo_path).convert("RGBA")

# 选择第一条语录进行测试
row = df.iloc[0]

print(f"📝 测试语录: {row['content'][:20]}...")

# 创建渐变背景
bg = create_gradient_bg(IMG_WIDTH, IMG_HEIGHT, BACKGROUND_TOP, BACKGROUND_BOTTOM)

# 添加微妙背景图案
bg = draw_subtle_pattern(bg, IMG_WIDTH, IMG_HEIGHT)

# 创建绘制对象
draw = ImageDraw.Draw(bg)

# 添加角落装饰
add_corner_decorations(draw, IMG_WIDTH, IMG_HEIGHT)

# 放置 logo 和装饰圆环
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

# 添加标题文字 "每天一点心理学"
title_text = "每天一点心理学"
title_font_size = 85
title_color = (80, 80, 80)

# 创建标题字体
try:
    title_font = ImageFont.truetype(font_path if os.path.exists(font_path) else "C:/Windows/Fonts/msyh.ttc", title_font_size)
except:
    title_font = ImageFont.load_default()

# 使用超采样渲染标题
title_img, title_w, title_h = render_text_with_supersampling(title_text, title_font_size, title_color)

# 标题位置：logo右边，垂直居中对齐
title_x = logo_pos[0] + logo_size[0] + 80
title_y = logo_pos[1] + (logo_size[1] - title_h) // 2

# 为标题添加装饰性下划线
underline_y = title_y + title_h + 15
underline_color = (120, 120, 120, 150)
draw.line([(title_x, underline_y), (title_x + title_w, underline_y)], 
          fill=underline_color, width=3)

# 粘贴标题文字
bg.paste(title_img, (title_x, title_y), title_img)

# 上装饰分隔栏
divider_y_top = 1300
draw_decorative_divider(draw, 0, divider_y_top, IMG_WIDTH, "elegant")

# 主体心理句
text = textwrap.fill(row['content'], width=10)
main_text_img, text_w, text_h = render_text_with_supersampling(text, FONT_SIZE_MAIN, TEXT_COLOR_MAIN)

main_text_y = 1400
text_x = (IMG_WIDTH - text_w) // 2

# 直接粘贴主文字，不添加背景框
bg.paste(main_text_img, (text_x, main_text_y), main_text_img)

# 下装饰分隔栏
divider_y_bottom = main_text_y + text_h + 150
draw_decorative_divider(draw, 0, divider_y_bottom, IMG_WIDTH, "geometric")

# 引发思考
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

# 底部装饰线条
bottom_line_y = reflect_text_y + reflect_h + 100
line_color = (140, 140, 140, 100)
draw.line([(IMG_WIDTH//4, bottom_line_y), (IMG_WIDTH*3//4, bottom_line_y)], 
          fill=line_color, width=3)

# 保存测试图片
filename = os.path.join(output_dir, "PREVIEW_设计增强版.png")
bg.save(filename, "PNG", optimize=False, compress_level=0, dpi=(DPI, DPI))

file_size = os.path.getsize(filename) / (1024 * 1024)
print(f"📸 预览图片已生成: {os.path.basename(filename)} ({file_size:.1f}MB)")
print("🎨 设计元素包含:")
print("   ✨ 微妙背景网格图案")
print("   🎯 角落三角装饰")
print("   ⭕ Logo装饰圆环")
print("   � 标题文字 + 装饰下划线")
print("   �📏 优雅分隔栏 (椭圆+线条)")
print("   🔷 几何分隔栏 (菱形+三角)")
print("   📝 引号装饰")
print("   📐 底部装饰线条")
print("✅ 已移除突兀的白色背景框，增加标题设计！")
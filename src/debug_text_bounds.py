from main_antialiasing import *

print("🔍 测试文字渲染边界")

# 测试不同的文字内容
test_texts = [
    "每个人都有自己的时区，不要被别人的节奏打乱",
    "完美主义是进步的敌人", 
    "真正的成长发生在舒适圈之外",
    "接受自己的脆弱是力量的体现"
]

for i, text in enumerate(test_texts):
    print(f"\n📝 测试文字 {i+1}: {text}")
    
    # 创建测试背景
    bg = create_gradient_bg(IMG_WIDTH, IMG_HEIGHT, BACKGROUND_TOP, BACKGROUND_BOTTOM)
    
    # 渲染文字
    wrapped_text = textwrap.fill(text, width=10)
    text_img, text_w, text_h = render_text_with_supersampling(wrapped_text, FONT_SIZE_MAIN, TEXT_COLOR_MAIN)
    
    print(f"   📐 文字尺寸: {text_w} x {text_h}")
    
    # 放置文字并添加边界框用于调试
    text_x = (IMG_WIDTH - text_w) // 2
    text_y = 1400
    
    # 在背景上画一个调试边界框
    draw = ImageDraw.Draw(bg)
    debug_color = (255, 0, 0, 100)  # 半透明红色
    draw.rectangle([text_x-5, text_y-5, text_x+text_w+5, text_y+text_h+5], 
                   outline=debug_color, width=4)
    
    # 粘贴文字
    bg.paste(text_img, (text_x, text_y), text_img)
    
    # 保存测试图片
    filename = os.path.join(output_dir, f"DEBUG_文字边界测试_{i+1}.png")
    bg.save(filename, "PNG", optimize=False, compress_level=0)
    
    file_size = os.path.getsize(filename) / (1024 * 1024)
    print(f"   💾 保存: {os.path.basename(filename)} ({file_size:.1f}MB)")

print("\n✅ 边界测试完成！")
print("🔍 查看DEBUG_文字边界测试_*.png文件")
print("📦 红色边框显示文字的实际边界")
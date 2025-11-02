# 🎨 自动化心理语录图片生成器

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![PIL](https://img.shields.io/badge/PIL-Pillow-green.svg)](https://pillow.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个专业的批量心理语录图片生成工具，支持4K高清输出和专业级抗锯齿渲染。

## ✨ 功能特点

- 🎨 **专业设计**：渐变背景 + 装饰元素 + 精美排版
- 📱 **4K高清**：2160x3840分辨率，31.7MB无损输出
- � **抗锯齿**：4倍超采样技术，完全消除锯齿
- 📝 **智能排版**：自动换行、居中对齐、字体回退
- 🎯 **批量处理**：CSV数据驱动，一键生成所有图片
- 🖼️ **设计元素**：Logo圆环、分隔栏、引号装饰等

## 🖼️ 效果展示

生成的图片包含以下设计元素：
- ✨ 微妙背景网格图案
- 🎯 角落三角装饰  
- ⭕ Logo装饰圆环
- 📚 "每天一点心理学" 标题
- 📏 优雅分隔栏（椭圆+线条）
- 🔷 几何分隔栏（菱形+三角）
- 📝 装饰性引号
- 📐 底部装饰线条

## 📁 项目结构

```
automatedPNG/
├── run.py                     # 🚀 一键启动入口（推荐）
├── start.bat                  # Windows批处理启动文件
├── start.ps1                  # PowerShell启动脚本
├── src/
│   ├── main_antialiasing.py    # 主程序（推荐）
│   └── debug_text_bounds.py    # 调试工具
├── resources/
│   ├── logo.png               # Logo文件
│   ├── quotes.csv             # 语录数据
│   └── fonts/
│       ├── SmileySans-Oblique.ttf  # 字体文件
│       └── README.md          # 字体下载说明
├── output/                    # 输出目录
├── .venv/                     # Python虚拟环境
├── requirements.txt           # 依赖列表
└── README.md                 # 项目说明
```

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/automatedPNG.git
cd automatedPNG
```

### 2. 安装依赖
```bash
# 使用 pip
pip install -r requirements.txt

# 或者使用国内镜像加速
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 准备字体（可选）
```bash
# 下载 SmileySans 字体到 resources/fonts/ 目录
# 详见 resources/fonts/README.md
```

### 4. 运行程序

#### 🚀 方式一：一键启动（推荐）

**Windows 用户：**
```bash
# 双击运行批处理文件
start.bat

# 或者双击运行 PowerShell 脚本
start.ps1

# 或者命令行运行
python run.py
```

**其他系统：**
```bash
python run.py
```

#### 📝 方式二：直接运行脚本
```bash
cd src

# 使用虚拟环境Python（Windows）
..\.venv\Scripts\python.exe main_antialiasing.py   # 批量生成所有图片

# 使用虚拟环境Python（Linux/Mac）
../.venv/bin/python main_antialiasing.py           # 批量生成所有图片
```

### 5. 查看结果
生成的4K高清图片保存在 `output/` 目录中，每张约31.7MB。

## 📝 数据格式

编辑 `resources/quotes.csv` 文件，包含以下字段：

| 字段 | 说明 | 示例 |
|------|------|------|
| `id` | 语录编号 | 1 |
| `content` | 主要语录内容 | 每个人都有自己的时区，不要被别人的节奏打乱 |
| `reflection` | 引发思考的问题 | 你觉得自己是否在为了迎合他人而违背内心？ |

## ⚙️ 自定义配置

在 `main_antialiasing.py` 中可以调整：

```python
# 画布尺寸
IMG_WIDTH, IMG_HEIGHT = 2160, 3840  # 4K分辨率

# 背景颜色
BACKGROUND_TOP = (245, 240, 230)     # 渐变顶部
BACKGROUND_BOTTOM = (230, 220, 200)  # 渐变底部

# 字体大小
FONT_SIZE_MAIN = 160      # 主文字
FONT_SIZE_REFLECT = 110   # 副文字

# 超采样倍数（影响抗锯齿质量）
SUPER_SAMPLE_FACTOR = 4   # 4倍超采样
```

## 🛠️ 开发工具

- `debug_text_bounds.py` - 调试文字边界问题
- 支持系统字体回退（微软雅黑）
- 智能动态字体大小调整
- 专业级抗锯齿渲染技术

## 📋 依赖要求

- Python 3.9+
- Pillow >= 10.0.0
- pandas >= 2.0.0

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [SmileySans](https://github.com/atelier-anchor/smiley-sans) - 开源中文字体
- [Pillow](https://pillow.readthedocs.io/) - Python图像处理库
- [pandas](https://pandas.pydata.org/) - 数据处理库
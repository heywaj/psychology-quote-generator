#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🎨 自动化心理语录图片生成器 - 一键运行入口
Author: heywaj
Repository: psychology-quote-generator
License: MIT
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """打印启动横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                  🎨 自动化心理语录图片生成器                    ║
    ║                    Auto Psychology Quote Generator            ║
    ╚══════════════════════════════════════════════════════════════╝
    
    ✨ 功能：4K高清图片 + 专业抗锯齿 + 批量生成
    📱 输出：2160x3840分辨率，约31.7MB/张
    🎯 数据源：resources/quotes.csv
    """
    print(banner)

def get_project_root():
    """获取项目根目录"""
    return Path(__file__).parent.absolute()

def get_venv_python():
    """获取虚拟环境中的Python可执行文件路径"""
    project_root = get_project_root()
    venv_dir = project_root / ".venv"
    
    if platform.system() == "Windows":
        python_exe = venv_dir / "Scripts" / "python.exe"
    else:
        python_exe = venv_dir / "bin" / "python"
    
    return python_exe if python_exe.exists() else None

def check_dependencies():
    """检查依赖是否安装"""
    venv_python = get_venv_python()
    if not venv_python:
        print("❌ 未找到虚拟环境，请先创建虚拟环境：")
        print("   python -m venv .venv")
        return False
    
    try:
        result = subprocess.run([str(venv_python), "-c", "import PIL, pandas"], 
                              capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ 缺少必要依赖，正在安装...")
        install_dependencies()
        return True

def install_dependencies():
    """安装项目依赖"""
    venv_python = get_venv_python()
    project_root = get_project_root()
    requirements_file = project_root / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ 未找到 requirements.txt 文件")
        return False
    
    print("📦 正在安装依赖包...")
    try:
        subprocess.run([str(venv_python), "-m", "pip", "install", "-r", str(requirements_file)], 
                      check=True)
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def check_resources():
    """检查必要资源文件"""
    project_root = get_project_root()
    resources_dir = project_root / "resources"
    quotes_file = resources_dir / "quotes.csv"
    output_dir = project_root / "output"
    
    # 检查resources目录
    if not resources_dir.exists():
        print("❌ resources目录不存在")
        return False
    
    # 检查quotes.csv文件
    if not quotes_file.exists():
        print("❌ 未找到 resources/quotes.csv 文件")
        return False
    
    # 创建output目录（如果不存在）
    if not output_dir.exists():
        output_dir.mkdir()
        print("📁 已创建 output 目录")
    
    return True

def show_menu():
    """显示功能菜单"""
    menu = """
    🎛️  请选择要执行的功能：
    
    [1] 🎨 批量生成所有图片 (main_antialiasing.py) - 推荐
    [2] 🛠️  调试文字边界 (debug_text_bounds.py)
    [3] 📂 打开输出目录
    [4] 📝 编辑语录数据 (quotes.csv)
    [5] 🗑️  清空输出目录
    [0] ❌ 退出程序
    
    """
    print(menu)

def run_script(script_name):
    """运行指定的Python脚本"""
    project_root = get_project_root()
    src_dir = project_root / "src"
    script_path = src_dir / script_name
    venv_python = get_venv_python()
    
    if not script_path.exists():
        print(f"❌ 脚本文件不存在: {script_path}")
        return False
    
    print(f"🚀 正在运行: {script_name}")
    print("=" * 60)
    
    try:
        # 切换到src目录运行脚本
        subprocess.run([str(venv_python), str(script_path)], 
                      cwd=str(src_dir), check=True)
        print("=" * 60)
        print("✅ 运行完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 运行失败: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⏹️  用户中断运行")
        return False

def open_output_directory():
    """打开输出目录"""
    project_root = get_project_root()
    output_dir = project_root / "output"
    
    if not output_dir.exists():
        print("❌ 输出目录不存在")
        return
    
    try:
        if platform.system() == "Windows":
            os.startfile(str(output_dir))
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", str(output_dir)])
        else:  # Linux
            subprocess.run(["xdg-open", str(output_dir)])
        print(f"📂 已打开输出目录: {output_dir}")
    except Exception as e:
        print(f"❌ 无法打开目录: {e}")
        print(f"📂 输出目录路径: {output_dir}")

def edit_quotes_file():
    """编辑语录文件"""
    project_root = get_project_root()
    quotes_file = project_root / "resources" / "quotes.csv"
    
    if not quotes_file.exists():
        print("❌ quotes.csv 文件不存在")
        return
    
    try:
        if platform.system() == "Windows":
            os.startfile(str(quotes_file))
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", str(quotes_file)])
        else:  # Linux
            subprocess.run(["xdg-open", str(quotes_file)])
        print(f"📝 已打开语录文件: {quotes_file}")
    except Exception as e:
        print(f"❌ 无法打开文件: {e}")
        print(f"📝 语录文件路径: {quotes_file}")

def clear_output_directory():
    """清空输出目录（保留重要文件）"""
    project_root = get_project_root()
    output_dir = project_root / "output"
    
    if not output_dir.exists():
        print("❌ 输出目录不存在")
        return
    
    # 定义需要保留的文件（Git和说明文件）
    keep_files = {".gitkeep", ".gitignore", "README.md", ".keep", "readme.txt"}
    
    # 获取输出目录中的所有文件
    all_files = list(output_dir.glob("*"))
    files_to_delete = [f for f in all_files if f.name not in keep_files]
    keep_files_found = [f for f in all_files if f.name in keep_files]
    
    if not files_to_delete:
        print("📂 输出目录中没有可删除的文件")
        if keep_files_found:
            print("🔒 以下重要文件已保留:")
            for file_path in keep_files_found:
                print(f"   • {file_path.name}")
        return
    
    # 显示将要删除的文件
    print(f"📁 输出目录: {output_dir}")
    print(f"📊 发现 {len(files_to_delete)} 个可删除文件:")
    
    total_size = 0
    for file_path in files_to_delete[:10]:  # 只显示前10个
        if file_path.is_file():
            file_size = file_path.stat().st_size
            total_size += file_size
            size_mb = file_size / (1024 * 1024)
            print(f"   📄 {file_path.name} ({size_mb:.1f}MB)")
        elif file_path.is_dir():
            print(f"   � {file_path.name}/ (目录)")
    
    if len(files_to_delete) > 10:
        print(f"   ... 还有 {len(files_to_delete) - 10} 个文件")
    
    # 计算所有待删除文件的总大小
    for file_path in files_to_delete[10:]:
        if file_path.is_file():
            total_size += file_path.stat().st_size
    
    print(f"�💾 总大小: {total_size / (1024 * 1024):.1f}MB")
    
    # 显示保留的文件
    if keep_files_found:
        print(f"\n🔒 以下重要文件将被保留:")
        for file_path in keep_files_found:
            print(f"   • {file_path.name}")
    
    print("")
    
    # 确认删除
    while True:
        confirm = input("⚠️  确定要删除这些文件吗？(y/N): ").strip().lower()
        if confirm in ['y', 'yes', '是', '确定']:
            break
        elif confirm in ['n', 'no', '否', '取消', '']:
            print("❌ 操作已取消")
            return
        else:
            print("❓ 请输入 y(是) 或 n(否)")
    
    # 执行删除
    deleted_count = 0
    failed_count = 0
    deleted_size = 0
    
    print("🗑️  正在清空输出目录...")
    
    for file_path in files_to_delete:
        try:
            if file_path.is_file():
                file_size = file_path.stat().st_size
                file_path.unlink()
                deleted_size += file_size
                deleted_count += 1
                print(f"   ✅ 已删除: {file_path.name}")
            elif file_path.is_dir():
                # 如果是目录，递归删除
                import shutil
                shutil.rmtree(file_path)
                deleted_count += 1
                print(f"   ✅ 已删除目录: {file_path.name}")
        except Exception as e:
            failed_count += 1
            print(f"   ❌ 删除失败: {file_path.name} - {e}")
    
    print("")
    if failed_count == 0:
        print(f"🎉 清空完成！成功删除 {deleted_count} 个项目")
    else:
        print(f"⚠️  部分完成：成功删除 {deleted_count} 个，失败 {failed_count} 个")
    
    print(f"� 释放空间: {deleted_size / (1024 * 1024):.1f}MB")
    print(f"�📂 输出目录: {output_dir}")
    
    # 显示保留文件的提醒
    if keep_files_found:
        print(f"🔒 已保留 {len(keep_files_found)} 个重要文件")

def main():
    """主函数"""
    print_banner()
    
    # 检查环境
    if not check_dependencies():
        return
    
    if not check_resources():
        return
    
    print("✅ 环境检查通过，程序已就绪！")
    
    while True:
        show_menu()
        try:
            choice = input("请输入选项 (0-5): ").strip()
            
            if choice == "0":
                print("👋 感谢使用！再见！")
                break
            elif choice == "1":
                run_script("main_antialiasing.py")
            elif choice == "2":
                run_script("debug_text_bounds.py")
            elif choice == "3":
                open_output_directory()
            elif choice == "4":
                edit_quotes_file()
            elif choice == "5":
                clear_output_directory()
            else:
                print("❌ 无效选项，请重新选择")
            
            input("\n按回车键继续...")
            print("\n" + "="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 感谢使用！再见！")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    main()
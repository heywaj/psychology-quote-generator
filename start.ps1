# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "🎨 自动化心理语录图片生成器"

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                  🎨 自动化心理语录图片生成器                    ║" -ForegroundColor Cyan  
Write-Host "║                  一键启动 - PowerShell版本                   ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 检查虚拟环境
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "❌ 未找到虚拟环境，正在创建..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 创建虚拟环境失败，请确保已安装Python 3.9+" -ForegroundColor Red
        Read-Host "按回车键退出"
        exit 1
    }
    Write-Host "✅ 虚拟环境创建成功" -ForegroundColor Green
}

# 运行入口程序
Write-Host "🚀 正在启动程序..." -ForegroundColor Green
Write-Host ""

try {
    & ".venv\Scripts\python.exe" "run.py"
}
catch {
    Write-Host "❌ 运行失败: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "👋 程序已退出" -ForegroundColor Cyan
Read-Host "按回车键关闭"
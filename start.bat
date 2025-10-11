@echo off
chcp 65001 >nul
echo ========================================
echo   井身结构MCP服务启动脚本
echo ========================================
echo.

REM 检查 uv 是否安装
where uv >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未找到 uv 工具！
    echo.
    echo 请先安装 uv，可以使用以下命令之一：
    echo   1. PowerShell: irm https://astral.sh/uv/install.ps1 ^| iex
    echo   2. 或访问: https://github.com/astral-sh/uv
    echo.
    pause
    exit /b 1
)

echo [√] 检测到 uv 工具
echo.

REM 检查 pyproject.toml 是否存在
if not exist "pyproject.toml" (
    echo [错误] 未找到 pyproject.toml 文件！
    echo 请确保在项目根目录下运行此脚本。
    echo.
    pause
    exit /b 1
)

echo [√] 找到 pyproject.toml
echo.

REM 检查 main.py 是否存在
if not exist "main.py" (
    echo [错误] 未找到 main.py 文件！
    echo 请确保在项目根目录下运行此脚本。
    echo.
    pause
    exit /b 1
)

echo [√] 找到 main.py
echo.

echo [*] 正在使用 uv 创建虚拟环境并安装依赖...
echo     (首次运行可能需要下载 Python 和依赖包，请耐心等待)
echo.

REM 使用 uv sync 来同步环境
uv sync
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [错误] 环境同步失败！
    echo.
    pause
    exit /b 1
)

echo.
echo [√] 虚拟环境创建完成，依赖安装成功
echo.
echo ========================================
echo   正在启动 MCP 服务...
echo ========================================
echo.

REM 使用 uv run 运行 main.py
uv run python main.py

REM 如果程序异常退出，暂停以便查看错误信息
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [错误] 程序异常退出，错误代码: %ERRORLEVEL%
    echo.
    pause
)


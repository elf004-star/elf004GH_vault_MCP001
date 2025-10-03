"""
井身结构图生成器 MCP 服务

基于井数据生成井身结构图的服务
"""

import json
import subprocess
import base64
import os
import shutil
import time
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("WellStructureGenerator")


def validate_well_data(data: Dict[str, Any]) -> bool:
    """验证井数据完整性"""
    required_fields = [
        "wellName", "totalDepth_m", "wellType", 
        "stratigraphy", "drillingFluidAndPressure", "wellboreStructure"
    ]
    
    for field in required_fields:
        if field not in data:
            return False
    
    # 验证井型
    if data["wellType"] not in ["straight well", "horizontal well"]:
        return False
    
    # 验证深度数据
    if not isinstance(data["totalDepth_m"], (int, float)) or data["totalDepth_m"] <= 0:
        return False
    
    return True


def update_well_data_file(data: Dict[str, Any]) -> bool:
    """更新well_data.json文件"""
    try:
        # 创建备份
        backup_path = Path("well_data_backup.json")
        if Path("well_data.json").exists():
            shutil.copy2("well_data.json", backup_path)
        
        # 写入新数据
        with open("well_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"更新井数据文件失败: {e}")
        return False


def run_well_generator() -> bool:
    """执行井身结构生成器"""
    try:
        generator_path = Path("井身结构图生成器.exe")
        if not generator_path.exists():
            print("井身结构图生成器.exe 不存在")
            return False
        
        # 调用生成器
        result = subprocess.run(
            [str(generator_path)],
            timeout=60  # 60秒超时
        )
        
        if result.returncode != 0:
            print(f"生成器执行失败，返回码: {result.returncode}")
            return False
        
        # 检查输出文件
        output_file = Path("well_structure_plot.png")
        if not output_file.exists():
            print("生成的图片文件不存在")
            return False
        
        return True
    except subprocess.TimeoutExpired:
        print("生成器执行超时")
        return False
    except Exception as e:
        print(f"执行生成器失败: {e}")
        return False


def get_generated_image(format: str = "base64") -> Optional[str]:
    """获取生成的图片数据"""
    try:
        image_path = Path("well_structure_plot.png")
        if not image_path.exists():
            return None
        
        if format == "base64":
            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            return image_data
        elif format == "path":
            return str(image_path.absolute())
        else:
            return None
    except Exception as e:
        print(f"获取图片数据失败: {e}")
        return None


def create_timestamp_folder() -> str:
    """创建时间戳文件夹"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_path = Path(timestamp)
        folder_path.mkdir(exist_ok=True)
        return str(folder_path)
    except Exception as e:
        print(f"创建时间戳文件夹失败: {e}")
        return ""


def move_generated_files(folder_path: str) -> bool:
    """移动生成的文件到时间戳文件夹"""
    try:
        if not folder_path:
            return False
        
        target_folder = Path(folder_path)
        if not target_folder.exists():
            return False
        
        # 需要移动的文件列表
        files_to_move = [
            "well_structure_plot.png",
            "well_structure_report.md",
            "stratigraphy.csv",
            "stratigraphy_raw.csv",
            "casing_sections.csv", 
            "casing_sections_raw.csv",
            "hole_sections.csv",
            "hole_sections_raw.csv",
            "drilling_fluid_pressure.csv",
            "drilling_fluid_pressure_raw.csv",
            "deviationData.csv",
            "deviationData_raw.csv"
        ]
        
        moved_files = []
        for filename in files_to_move:
            source_file = Path(filename)
            if source_file.exists():
                target_file = target_folder / filename
                shutil.move(str(source_file), str(target_file))
                moved_files.append(filename)
        
        print(f"已移动 {len(moved_files)} 个文件到文件夹: {folder_path}")
        return True
        
    except Exception as e:
        print(f"移动文件失败: {e}")
        return False


def read_report_content(report_path: str) -> str:
    """读取MD报告内容"""
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"读取报告内容失败: {e}")
        return ""


def get_image_absolute_path(folder_path: str) -> str:
    """获取图片绝对路径"""
    try:
        image_path = Path(folder_path) / "well_structure_plot.png"
        if image_path.exists():
            return str(image_path.absolute())
        else:
            print("图片文件不存在")
            return ""
    except Exception as e:
        print(f"获取图片路径失败: {e}")
        return ""


def wait_for_completion():
    """等待3秒，确保exe程序完全结束"""
    try:
        print("等待3秒，确保程序完全结束...")
        time.sleep(3)
        print("等待完成")
    except Exception as e:
        print(f"等待过程出错: {e}")


def get_folder_absolute_path(folder_path: str) -> str:
    """获取文件夹绝对路径"""
    try:
        folder = Path(folder_path)
        if folder.exists():
            return str(folder.absolute())
        else:
            print("文件夹不存在")
            return ""
    except Exception as e:
        print(f"获取文件夹路径失败: {e}")
        return ""


def format_simple_response(image_path: str) -> str:
    """简化的格式化回答"""
    try:
        response = f"井身结构示意图为：\n![PNG]({image_path})"
        return response
    except Exception as e:
        print(f"格式化回答失败: {e}")
        return ""


def cleanup_temp_files():
    """清理临时文件"""
    try:
        # 清理备份文件
        backup_path = Path("well_data_backup.json")
        if backup_path.exists():
            backup_path.unlink()
    except Exception as e:
        print(f"清理临时文件失败: {e}")


@mcp.tool()
def generate_well_structure(well_data: Dict[str, Any], output_format: str = "base64") -> Dict[str, Any]:
    """
    生成井身结构图
    
    Args:
        well_data: 井数据JSON对象
        output_format: 输出格式 ("base64" 或 "path")
    
    Returns:
        包含生成结果和图片数据的字典
    """
    try:
        # 验证数据
        if not validate_well_data(well_data):
            return {
                "success": False,
                "error": "井数据验证失败",
                "error_code": "VALIDATION_ERROR",
                "details": "缺少必需字段或数据格式不正确"
            }
        
        # 更新井数据文件
        if not update_well_data_file(well_data):
            return {
                "success": False,
                "error": "更新井数据文件失败",
                "error_code": "FILE_UPDATE_ERROR",
                "details": "无法写入well_data.json文件"
            }
        
        # 执行生成器
        if not run_well_generator():
            return {
                "success": False,
                "error": "井身结构生成器执行失败",
                "error_code": "GENERATOR_ERROR",
                "details": "生成器无法正常执行或生成图片"
            }
        
        # 等待3秒，确保exe程序完全结束
        wait_for_completion()
        
        # 创建时间戳文件夹并移动生成的文件
        timestamp_folder = create_timestamp_folder()
        if not timestamp_folder:
            return {
                "success": False,
                "error": "创建归档文件夹失败",
                "error_code": "FOLDER_CREATION_ERROR",
                "details": "无法创建时间戳文件夹"
            }
        
        if not move_generated_files(timestamp_folder):
            return {
                "success": False,
                "error": "文件归档失败",
                "error_code": "FILE_ARCHIVE_ERROR",
                "details": "无法移动生成的文件到归档文件夹"
            }
        
        # 获取文件夹绝对路径
        folder_absolute_path = get_folder_absolute_path(timestamp_folder)
        if not folder_absolute_path:
            return {
                "success": False,
                "error": "获取文件夹路径失败",
                "error_code": "FOLDER_PATH_ERROR",
                "details": "无法获取归档文件夹的绝对路径"
            }
        
        # 构建图片绝对路径
        image_path = f"{folder_absolute_path}\\well_structure_plot.png"
        
        # 清理临时文件
        cleanup_temp_files()
        
        # 返回成功结果
        well_name = well_data.get("wellName", "")
        return {
            "success": True,
            "response": "注意！给用户回答的时候，必须在合适的地方添加Markdown格式链接引用，如：![well_name](image_path)",
            "well_info": {
                "well_name": well_name,
                "well_type": well_data.get("wellType", ""),
                "total_depth": well_data.get("totalDepth_m", 0)
            },
            "archive_folder": timestamp_folder,
            "image_path": image_path,
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"生成井身结构图时发生未知错误: {str(e)}",
            "error_code": "UNKNOWN_ERROR",
            "details": str(e)
        }


if __name__ == "__main__":
    mcp.run(transport='stdio')
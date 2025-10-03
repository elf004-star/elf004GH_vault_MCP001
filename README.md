# 井身结构图生成器 MCP 服务

这是一个基于 MCP (Model Context Protocol) 的井身结构图生成服务，可以根据井数据自动生成井身结构图。

## 功能特性

- 支持三种井型：直井、水平井、直改平井
- 自动生成井身结构图（PNG格式）
- 生成相关数据文件（CSV格式）
- 返回简化的图片路径（大幅减少token消耗）
- 自动文件归档管理（时间戳文件夹）
- 完整的错误处理和验证

## 使用方法

### 启动MCP服务

```bash
# 使用uv运行（推荐）
uv run python main.py

# 或直接使用python
python main.py
```

### MCP客户端配置

在MCP客户端中添加以下配置：

```json
{
  "mcpServers": {
    "well-structure-generator": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "项目路径"
    }
  }
}
```

### MCP工具调用

工具名称：`generate_well_structure`

参数：
- `well_data`: 井数据JSON对象
- `output_format`: 输出格式（可选，默认"base64"）

返回：
- 成功时返回简化的图片路径（<1200 token）
- 失败时返回错误信息

**返回格式**：
```
井身结构示意图为：
![PNG](文件夹绝对路径+well_structure_plot.png)
```

**返回数据结构**：
```json
{
  "success": true,
  "response": "井身结构示意图为：\n![PNG](图片绝对路径)",
  "well_info": {
    "well_name": "井名",
    "well_type": "井型", 
    "total_depth": 深度
  },
  "archive_folder": "2025-10-03_11-37-29",
  "image_path": "图片的绝对路径"
}
```

**Token优化**：
- 返回内容大幅简化，减少token消耗
- 每次返回不超过1200个token
- 移除冗长的报告内容，只保留核心信息

### 支持的井型

1. **直井** (`straight well`)
   - `deviationAngle_deg: 0`
   - `kickoffPoint_m: null`

2. **水平井** (`horizontal well`)
   - `deviationAngle_deg: 90`
   - `kickoffPoint_m: 有值`

3. **直改平井** (`horizontal well`)
   - `deviationAngle_deg: 90`
   - `kickoffPoint_m: null`
   - `REAL_kickoffPoint_m: 有值`

## 生成的文件

每次请求完成后，所有生成的文件会自动移动到以时间戳命名的文件夹中：

- `well_structure_plot.png`: 井身结构图
- `well_structure_report.md`: 井身结构报告
- `stratigraphy.csv`: 地层数据
- `casing_sections.csv`: 套管数据
- `hole_sections.csv`: 井眼数据
- `drilling_fluid_pressure.csv`: 钻井液压力数据
- `deviationData.csv`: 偏移数据
- 对应的 `*_raw.csv` 原始数据文件

**文件归档**：
- 文件夹命名格式：`YYYY-MM-DD_HH-MM-SS`
- 示例：`2025-10-03_11-37-29`
- 每次请求都会创建新的归档文件夹

## 技术实现

- 使用 FastMCP 框架
- 支持异步处理
- 完整的错误处理机制
- 自动文件备份和清理
- 3秒延迟确保程序完全结束
- Token优化，减少API调用成本

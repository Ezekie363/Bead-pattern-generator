# 拼豆图纸生成器

将图片一键转换为拼豆（Fuse Bead）图纸，支持多品牌色板，可导出含色号统计的 PNG 图纸。

## 功能特点

- **图片上传** — 点击或拖拽上传 JPG、PNG、WEBP 格式图片
- **多品牌色板** — 内置散兵、Perler、Hama 三大品牌色板，一键切换
- **灵活尺寸** — 支持 29×29（小方板）、48×48（标准板）、58×58（大板）预设及自定义尺寸
- **Lab 色彩匹配** — 使用 CIE Lab 色彩空间进行颜色匹配，感知准确度更高
- **实时预览** — 处理后即时显示带色号标注的色块网格
- **色号统计** — 底部自动汇总各色号用量，方便采购
- **导出 PNG** — 一键导出含完整色号统计栏的图纸文件

## 效果预览

上传图片 → 选择色板和尺寸 → 点击处理 → 导出图纸

```
┌─────────────────────────────────────────┐
│  拼豆图纸生成器                           │
├─────────────────────────────────────────┤
│  [色板: 散兵 ▼]  [尺寸: 48×48 ▼]        │
├───────────────────┬─────────────────────┤
│                   │  C5  C5  B24  B24   │
│   原图预览         │  A13 A13 A13  A13   │
│                   │  ...                │
├───────────────────┴─────────────────────┤
│  色号统计: ■C5(1528) ■A13(496) ■B24(248) │
├─────────────────────────────────────────┤
│  [处理图片]              [导出 PNG]       │
└─────────────────────────────────────────┘
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.9+, Flask, Pillow, NumPy |
| 前端 | Vue.js 3 (CDN), HTML5 Canvas |
| 算法 | CIE Lab 色彩空间最近邻匹配 |

## 快速开始

### 环境要求

- Python 3.9 或更高版本
- pip

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/Ezekie363/Bead-pattern-generator.git
cd Bead-pattern-generator

# 2. 安装 Python 依赖
pip install -r backend/requirements.txt

# 3. 启动服务
cd backend
python app.py
```

### 访问应用

打开浏览器，访问 `http://127.0.0.1:5000`

> **注意（macOS）**：macOS 的 AirPlay 服务可能占用 `localhost:5000` 的 IPv6 接口，请使用 `http://127.0.0.1:5000` 访问。

### 开发模式

```bash
# 启用调试模式（自动重载）
FLASK_DEBUG=true python app.py
```

## 项目结构

```
bead-pattern-generator/
├── backend/
│   ├── app.py                  # Flask 主入口，API 路由
│   ├── color_utils.py          # RGB→Lab 转换，最近邻色板匹配
│   ├── image_processor.py      # 图像缩放与逐像素颜色映射
│   ├── palettes/
│   │   ├── sanbing.json        # 散兵色板（30色）
│   │   ├── perler.json         # Perler 色板（30色）
│   │   └── hama.json           # Hama 色板（30色）
│   ├── tests/                  # 单元测试（14个）
│   └── requirements.txt
└── frontend/
    ├── index.html              # 单页面入口
    ├── app.js                  # Vue.js 3 应用逻辑
    └── style.css               # 深色主题样式
```

## API 接口

### 获取色板列表

```
GET /api/palettes
```

响应示例：
```json
[
  {"id": "sanbing", "name": "散兵"},
  {"id": "perler",  "name": "Perler"},
  {"id": "hama",    "name": "Hama"}
]
```

### 处理图片

```
POST /api/process
Content-Type: multipart/form-data

参数：
  image   图片文件（JPG/PNG/WEBP）
  palette 色板 ID（sanbing / perler / hama）
  width   图纸宽度（1-200，默认 48）
  height  图纸高度（1-200，默认 48）
```

响应示例：
```json
{
  "grid": [["C5", "C5", "B24"], ...],
  "stats": [
    {"code": "C5", "count": 1528, "hex": "#1E88E5", "name": "蓝色"}
  ],
  "width": 48,
  "height": 48
}
```

## 运行测试

```bash
cd backend
pytest tests/ -v
```

## 色板说明

| 品牌 | 颜色数量 | 说明 |
|------|----------|------|
| 散兵 | 30 色 | 国内常见品牌，色号格式如 A13、B24、C5 |
| Perler | 30 色 | 美国品牌，色号格式如 P001-P030 |
| Hama | 30 色 | 丹麦品牌，色号格式如 H01-H30 |

> 当前内置各品牌最常用的 30 种颜色。如需扩展色板，可直接编辑 `backend/palettes/` 目录下对应的 JSON 文件，格式为 `[{"code": "色号", "name": "颜色名", "hex": "#RRGGBB"}]`。

## 许可证

MIT License

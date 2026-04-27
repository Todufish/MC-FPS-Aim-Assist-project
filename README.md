# 🎯 MC-FPS-Aim-Assist

基于 YOLOv11 的 Minecraft 目标检测与自动瞄准辅助工具

## ✨ 功能特性

- **实时目标检测** - 使用 YOLOv11 模型实时检测游戏中的目标头部
- **自动瞄准辅助** - 智能计算目标位置并平滑移动准星
- **高帧率运行** - 优化的推理流程，支持高 FPS 实时检测
- **可视化界面** - 实时显示检测结果、FPS 和置信度
- **参数可调** - 支持自定义灵敏度、平滑度、检测阈值等参数
- **DPI 自适应** - 自动检测系统 DPI 缩放比例

## 📋 环境要求

- Windows 10/11
- Python 3.10+
- CUDA (可选，用于 GPU 加速)

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/Todufish/MC-FPS-Aim-Assist-project.git
cd MC-FPS-Aim-Assist
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 准备模型

将训练好的模型文件 `best.pt` 或 `best.onnx` 放入项目根目录。

### 4. 运行程序

```bash
python yolo_mc.py
```

按 `Q` 键退出程序。

## ⚙️ 参数配置

在 `yolo_mc.py` 中可以调整以下参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `model_path` | 模型文件路径 | `best.pt` |
| `conf_threshold` | 检测置信度阈值 | `0.6` |
| `aim_smooth` | 瞄准平滑度 (值越小移动越快) | `5.0` |
| `head_offset_ratio` | 头部偏移比例 (向上偏移) | `0.15` |
| `game_sensitivity` | 游戏内灵敏度 | `1.2` |

```python
detector = MinecraftZombieDetector(
    model_path="best.pt",
    conf_threshold=0.6,
    aim_smooth=5.0,
    head_offset_ratio=0.15,
    game_sensitivity=1.2
)
```

## 🎮 使用方法

1. 启动 Minecraft 游戏
2. 进入游戏画面（建议全屏或窗口化）
3. 运行 `python yolo_mc.py`
4. 程序会自动检测屏幕并锁定目标

## 🔧 模型训练

### 1. 准备数据集

将原始数据放入 `dataset_org` 目录：
```
dataset_org/
├── images/     # 图片文件
└── labels/     # YOLO 格式标注文件 (.txt)
```

### 2. 划分数据集

```bash
python data_split.py
```

默认划分比例：训练集 70%、验证集 20%、测试集 10%

### 3. 开始训练

```bash
python train.py
```

训练参数可在 `train.py` 中修改：
```python
model.train(
    data="data.yaml",
    epochs=100,
    batch=4,
    workers=4
)
```

### 4. 模型评估

```bash
python test.py
```

### 5. 模型预测

```bash
python predict.py
```

## 📁 项目结构

```
MC-FPS-Aim-Assist/
├── yolo_mc.py          # 主程序 - 实时检测与瞄准
├── train.py            # 模型训练脚本
├── predict.py          # 模型预测脚本
├── test.py             # 模型评估脚本
├── data_split.py       # 数据集划分脚本
├── data.yaml           # YOLO 数据配置文件
├── requirements.txt    # Python 依赖
├── best.pt             # 训练好的模型 (PyTorch)
├── best.onnx           # ONNX 格式模型
├── yolo11n.pt          # YOLOv11 预训练权重
├── dataset/            # 划分后的数据集
│   ├── train/
│   ├── valid/
│   └── test/
├── dataset_org/        # 原始数据集
├── runs/               # 训练输出目录
└── weights/            # 模型权重目录
```

## 📊 数据集格式

项目使用 YOLO 格式数据集：

```
dataset/
├── train/
│   ├── images/
│   │   └── *.jpg
│   └── labels/
│       └── *.txt
├── valid/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

标注文件格式 (YOLO):
```
class_id center_x center_y width height
```

## 🔍 检测目标

当前模型检测类别：
- `head` - 目标头部

可在 `data.yaml` 中修改类别：
```yaml
nc: 1
names: ['head']
```

## ⚠️ 注意事项

1. **仅供学习研究使用** - 请勿在多人游戏或竞技环境中使用
2. **游戏安全** - 使用此类工具可能导致账号被封禁
3. **性能优化** - 建议使用 GPU 加速以提高检测帧率
4. **DPI 设置** - 如遇准星偏移问题，请检查系统 DPI 设置

## 🛠️ 常见问题

**Q: 检测帧率低怎么办？**

A: 
- 使用 GPU 加速 (确保安装了 CUDA 版本的 PyTorch)
- 减小输入图像尺寸 (修改 `imgsz` 参数)
- 使用更小的模型 (如 yolo11n)

**Q: 准星偏移不准确？**

A:
- 检查游戏内灵敏度设置
- 调整 `game_sensitivity` 参数
- 检查系统 DPI 缩放比例

**Q: 如何训练自己的模型？**

A:
1. 收集目标图像
2. 使用 labelImg 标注数据
3. 按照上述训练步骤操作

## 📦 依赖说明

核心依赖：
- `ultralytics` - YOLOv11 框架
- `opencv-python` - 图像处理
- `torch` - PyTorch 深度学习框架
- `numpy` - 数值计算
- `mss` - 屏幕截图
- `pyautogui` - 鼠标控制

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式

如有问题或建议，请提交 Issue。

---

**⚠️ 免责声明：本项目仅供学习研究目的，请勿用于违反游戏规则或法律法规的用途。使用本工具所产生的一切后果由使用者自行承担。**

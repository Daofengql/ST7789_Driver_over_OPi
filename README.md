# ST7789 Python 驱动库

**许可证**: 本项目基于 [Apache 2.0 许可证](https://www.apache.org/licenses/LICENSE-2.0) 开源，用户可以自由使用、修改和分发，但需保留原始版权声明及许可证信息。

---

## 库简介

本项目是一个用于控制 ST7789 圆形 TFT 屏幕的 Python 驱动库，基于 `wiringpi` 和 `spidev` 实现，支持通过 SPI 接口对屏幕进行像素级控制，包括清屏、绘制像素、设置窗口区域和显示图像等功能。该库专为嵌入式开发板（如 Raspberry Pi）设计，适用于需要高性能图形显示的项目。

---

## 功能特点

1. **SPI 通信支持**：
   - 使用 `spidev` 库与 ST7789 屏幕进行高效通信。
   - 支持高达 40MHz 的 SPI 通信速率。

2. **GPIO 控制**：
   - 通过 `wiringpi` 管理 D/C（数据/命令）、RST（复位）和 BL（背光）引脚。

3. **显示控制**：
   - 支持清屏、窗口区域绘制和像素级设置。
   - 支持全屏显示图片。

4. **兼容 ST7789 圆形屏幕**：
   - 默认分辨率为 240x240。

---

## 环境依赖

### 硬件要求

1. **ST7789 圆形屏幕**
2. **支持 SPI 的嵌入式开发板**，如 Raspberry Pi

### 软件要求

1. **Python 版本**：Python 3.6 或更高
2. **依赖库**：
   - `spidev`
   - `wiringpi`
   - `numpy`

使用以下命令安装所需库：

```bash
pip install spidev numpy
sudo apt-get install python3-wiringpi
```

---

## 使用指南

### 硬件连接

确保正确连接 ST7789 屏幕和开发板：

| 屏幕引脚 | 功能        | 开发板引脚（Raspberry Pi 示例） |
|----------|-------------|-------------------------------|
| VCC      | 电源        | 3.3V 或 5V                   |
| GND      | 地          | GND                          |
| SCL      | SPI 时钟    | GPIO 11 (SPI_CLK)            |
| SDA      | SPI 数据    | GPIO 10 (SPI_MOSI)           |
| RES      | 复位引脚    | GPIO 24                      |
| DC       | 数据/命令引脚| GPIO 23                      |
| BL       | 背光引脚    | GPIO 18                      |

### 初始化代码

```python
from st7789 import ST7789

# 初始化 ST7789 屏幕
lcd = ST7789(
    rst=24,   # 复位引脚
    dc=23,    # 数据/命令引脚
    bl=18,    # 背光引脚
    bus=0,    # SPI 总线
    dev=0,    # SPI 设备
    speed=40000000  # SPI 速度
)

# 初始化屏幕
lcd.lcd_init()

# 清屏为白色
lcd.clear(color=0xFFFF)
```

---

## 示例代码

### 清屏和绘制像素

```python
# 清屏为黑色
lcd.clear(color=0x0000)

# 在指定位置绘制一个红色像素
lcd.set_pixel(x=120, y=120, color=0xF800)  # 红色
```

### 绘制窗口区域

```python
# 在 (50, 50) 到 (100, 100) 区域绘制蓝色背景
lcd.clear_window(start_x=50, start_y=50, end_x=100, end_y=100, color=0x001F)  # 蓝色
```

### 显示图像

```python
from PIL import Image

# 加载图片并调整大小
image = Image.open("example.jpg").resize((240, 240))

# 显示图像
lcd.img_show(image)
```

---

## API 接口

### `__init__(rst, dc, bl, bus=1, dev=0, speed=40000000)`
初始化 ST7789 屏幕。

- **rst**: 复位引脚 GPIO 编号。
- **dc**: 数据/命令引脚 GPIO 编号。
- **bl**: 背光引脚 GPIO 编号。
- **bus**: SPI 总线编号（默认 `1`）。
- **dev**: SPI 设备编号（默认 `0`）。
- **speed**: SPI 通信速度，单位为 Hz（默认 `40000000`）。

### `lcd_init()`
初始化 ST7789 屏幕并设置默认参数。

### `clear(color=0xFFFF)`
清屏。

- **color**: 清屏颜色，默认为白色。

### `clear_window(start_x, start_y, end_x, end_y, color=0xFFFF)`
清除指定区域并填充颜色。

- **start_x, start_y**: 区域左上角坐标。
- **end_x, end_y**: 区域右下角坐标。
- **color**: 填充颜色，默认为白色。

### `set_pixel(x, y, color)`
设置单个像素的颜色。

- **x, y**: 像素位置。
- **color**: 像素颜色。

### `img_show(img)`
显示图片。

- **img**: 图像对象，需为 `PIL.Image` 对象，大小为 240x240。

---

## 项目结构

```plaintext
├── st7789.py          # ST7789 驱动库
├── example_clear.py   # 清屏与像素设置示例
├── example_image.py   # 图像显示示例
```

---

## 注意事项

1. **SPI 权限问题**：在某些系统上，操作 SPI 设备需要 root 权限。可使用 `sudo` 运行脚本或更改 SPI 设备权限：
   ```bash
   sudo chmod 666 /dev/spidev0.0
   ```

2. **屏幕坐标系**：屏幕分辨率为 240x240，左上角为 (0, 0)，右下角为 (239, 239)。

3. **刷新速率**：大面积绘图或全屏图片显示时，可能需要较高的 SPI 通信速度（如 40MHz）。

---

## 许可证

本项目基于 [Apache 2.0 许可证](https://www.apache.org/licenses/LICENSE-2.0) 发布，用户可自由使用、修改和分发，但需保留原始版权声明及许可证信息。

---

## 联系

如有任何问题或建议，请随时提交 Issue 或 PR。

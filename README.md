# PCA9685 Python 驱动库

**许可证**: 本项目基于 [Apache 2.0 许可证](https://www.apache.org/licenses/LICENSE-2.0) 开源。您可以自由使用、修改和分发本项目，但需保留原始版权声明及许可证信息。

---

## PCA9685 驱动库简介

本项目提供一个基于 `periphery` 的 Python 驱动库，用于通过 I2C 控制 PCA9685 16通道 PWM 控制器。适用于 ARM 嵌入式开发板（如 Raspberry Pi）或其他运行 Linux 的设备，广泛应用于伺服电机、LED 灯光控制等场景。

---

## 功能特点

- **I2C 控制支持**：通过 `periphery` 库实现稳定的 I2C 通信。
- **可调 PWM 频率**：支持从 40Hz 到 1000Hz 的 PWM 频率设置。
- **单通道与全局控制**：灵活地操作单个或所有 PWM 通道。
- **轻量级与跨平台**：适用于任何支持 `periphery` 的 Linux 平台。

---

## 安装与环境依赖

### 硬件要求

1. **PCA9685 模块**
2. **支持 I2C 的 ARM 开发板**，如 Raspberry Pi 或其他嵌入式设备
3. 确保 **I2C 接口硬件连接正确**：
   - **VCC**: 连接开发板的 3.3V 或 5V 电源
   - **GND**: 接地
   - **SCL**: I2C 时钟线
   - **SDA**: I2C 数据线

### 软件要求

1. **Python 版本**：3.6 或更高
2. **依赖库**：
   - `periphery`
   - `logging`
3. 使用以下命令安装 Python 依赖：
   ```bash
   pip install python-periphery
   ```

---

## 使用指南

### 硬件连接与准备

确保开发板的 I2C 接口已启用：
- Raspberry Pi 用户可通过 `raspi-config` 工具启用 I2C 接口。

### 初始化代码

```python
from pca9685 import PCA9685

# 初始化 PCA9685，默认 I2C 地址为 0x40，I2C 设备为 /dev/i2c-1
pwm = PCA9685(address=0x40, i2c_dev="/dev/i2c-1")

# 设置 PWM 频率为 50Hz，适合伺服电机
pwm.set_pwm_freq(50)

# 设置通道 0 的 PWM 输出，占空比为 50%
pwm.set_pwm(channel=0, on=0, off=2048)
```

---

## 示例代码

### 驱动舵机

```python
import time
from pca9685 import PCA9685

# 初始化 PCA9685
pwm = PCA9685(address=0x40, i2c_dev="/dev/i2c-1")
pwm.set_pwm_freq(50)  # 设置频率为 50Hz

# 设置舵机在不同角度之间摆动
while True:
    pwm.set_pwm(channel=0, on=0, off=150)  # 最小角度
    time.sleep(1)
    pwm.set_pwm(channel=0, on=0, off=600)  # 最大角度
    time.sleep(1)
```

### 控制多通道 LED

```python
# 初始化所有通道
for channel in range(16):
    pwm.set_pwm(channel=channel, on=0, off=1024)  # 设置 25% 占空比
```

---

## API 接口

### 初始化与设置

- `__init__(address, i2c_dev)`
  - **address**: I2C 地址，默认为 `0x40`。
  - **i2c_dev**: I2C 设备路径，例如 `/dev/i2c-1`。

- `set_pwm_freq(freq_hz)`
  - 设置 PWM 频率，单位为 Hz（范围：40~1000）。

- `set_pwm(channel, on, off)`
  - 设置单个 PWM 通道。
  - **channel**: 通道编号，范围 `0~15`。
  - **on**: 信号开启时间。
  - **off**: 信号关闭时间。

- `set_all_pwm(on, off)`
  - 设置所有 PWM 通道。

---

## 项目结构

```plaintext
├── pca9685.py          # PCA9685 驱动库
├── example_servo.py    # 舵机控制示例
├── example_led.py      # 多通道 LED 控制示例
```

---

## 注意事项

1. **权限问题**：运行时可能需要 root 权限。可使用 `sudo` 或设置设备权限：
   ```bash
   sudo chmod 666 /dev/i2c-1
   ```
2. **频率兼容性**：伺服电机推荐设置为 50Hz，LED 可根据需要调整频率。
3. **I2C 地址冲突**：确保连接的其他 I2C 设备地址不同。如需修改 PCA9685 的地址，可调整模块上的地址跳线。

---

## 许可证

本项目基于 [Apache 2.0 许可证](https://www.apache.org/licenses/LICENSE-2.0) 发布，您可以自由使用、修改和分发，但需保留原始版权声明及许可证信息。 

---

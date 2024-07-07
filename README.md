# Python ST7789

Python库，用于控制ST7789 TFT LCD显示屏

专门设计用于控制基于ST7789的240x240像素的TFT SPI显示屏。

使用了wiringpi库和spidev库同时驱动GPIO

可以对更多型号的ARM开发版提供良好兼容

寄存器设置为最佳支持圆形的屏幕，其他规格的请对寄存器初始化进行修改


# Licensing

此库可以随意使用，包括商用等，遵循Apache-2.0许可证

## Modifications include:

此库源于网络多个st7789项目融合迁移而来，将原有的各种RPi或OPi的gpio库改为使用Wiringpi，使更多开发板可以兼容使用

遵循Apache-2.0许可证

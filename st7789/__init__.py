import spidev
import time
import wiringpi as wpi
import numpy as np

class ST7789():
    def __init__(
            self,
            rst,
            dc,
            bl,
            bus=1,
            dev=0,
            speed=40000000
            ):
        self.rst = rst
        self.dc = dc
        self.bl = bl

        # 初始化GPIO
        wpi.wiringPiSetup()
        wpi.pinMode(self.dc, wpi.OUTPUT)  # D/C引脚
        wpi.pinMode(self.rst, wpi.OUTPUT)  # 复位引脚
        wpi.pinMode(self.bl, wpi.OUTPUT)  # 背光控制引脚
        wpi.softPwmCreate(self.bl, 0, 100)
        wpi.softPwmWrite(self.bl, 90)
        
        # 初始化SPI
        self.bus = bus
        self.dev = dev
        self.spi_speed = speed
        self.spi = spidev.SpiDev()
        self.spi.open(self.bus, self.dev)
        self.spi.max_speed_hz = self.spi_speed
        self.spi.mode = 0b00
        
        # 定义LCD的宽度和高度
        self.w = 240
        self.h = 240
        
    def write_cmd(self, cmd):
        """发送命令"""
        wpi.digitalWrite(self.dc, wpi.LOW)
        self.spi.writebytes([cmd])
        
    def write_data(self, value):
        """发送数据"""
        wpi.digitalWrite(self.dc, wpi.HIGH)
        self.spi.writebytes([value])
        
    def write_data_word(self, value):
        """发送双字节数据"""
        wpi.digitalWrite(self.dc, wpi.HIGH)
        self.spi.writebytes([value >> 8, value & 0xFF])
        
    def reset(self):
        """复位LCD"""
        wpi.digitalWrite(self.rst, wpi.HIGH)
        time.sleep(0.02)
        wpi.digitalWrite(self.rst, wpi.LOW)
        time.sleep(0.02)
        wpi.digitalWrite(self.rst, wpi.HIGH)
        time.sleep(0.02)
        
    def lcd_init(self):
        """LCD初始化"""
        self.reset()

        self.write_cmd(0x36) 
        self.write_data(0x00)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7) 
        self.write_data(0x35)

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6) 
        self.write_data(0x0F)    

        self.write_cmd(0xD0) 
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)

        self.write_cmd(0x21)

        self.write_cmd(0x11) 

        self.write_cmd(0x29)
        
    def set_cursor(self, start_x, start_y, end_x, end_y):
        """设置光标位置"""
        self.write_cmd(0x2A)
        self.write_data(start_x >> 8)
        self.write_data(start_x & 0xFF)
        self.write_data(end_x >> 8)
        self.write_data(end_x & 0xFF)
        
        self.write_cmd(0x2B)
        self.write_data((start_y + 40) >> 8)
        self.write_data((start_y + 40) & 0xFF)
        self.write_data((end_y + 40) >> 8)
        self.write_data((end_y + 40) & 0xFF)
        
        self.write_cmd(0x2C)

    def clear(self, color=0xFFFF):
        """清屏"""
        self.set_cursor(0, 0, self.w - 1, self.h - 1)
        wpi.digitalWrite(self.dc, wpi.HIGH)
        buf = [color >> 8, color & 0xFF] * (self.w * self.h)
        for i in range(0, len(buf), 4096):
            self.spi.writebytes(buf[i:i+4096])

    def clear_window(self, start_x, start_y, end_x, end_y, color=0xFFFF):
        """清除窗口区域"""
        self.set_cursor(start_x, start_y, end_x, end_y)
        wpi.digitalWrite(self.dc, wpi.HIGH)
        buf = [color >> 8, color & 0xFF] * ((end_x - start_x) * (end_y - start_y))
        for i in range(0, len(buf), 4096):
            self.spi.writebytes(buf[i:i+4096])
    
    def set_pixel(self, x, y, color):
        """设置像素颜色"""
        self.set_cursor(x, y, x, y)
        self.write_data_word(color)

    def img_show(self, img):
        """显示图像"""
        image = np.asarray(img)
        pixel = np.zeros((self.w, self.h, 2), dtype=np.uint8)
        pixel[..., [0]] = np.add(np.bitwise_and(image[..., [0]], 0xf8), np.right_shift(image[..., [1]], 5))
        pixel[..., [1]] = np.add(np.bitwise_and(np.left_shift(image[..., [1]], 3), 0xe0), np.right_shift(image[..., [2]], 3))
        pixel = pixel.flatten().tolist()
        self.set_cursor(0, 0, self.w, self.h)
        wpi.digitalWrite(self.dc, wpi.HIGH)
        for i in range(0, len(pixel), 4096):
            self.spi.writebytes(pixel[i:i+4096])

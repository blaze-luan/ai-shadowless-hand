"""
無影手 (Shadowless Hand) - AI 桌面自動化操作工具

核心模組：
- mouse: 擬人化鼠標控制
- keyboard: 擬人化鍵盤輸入
- clipboard: 剪貼板操作
- captcha: 驗證碼突破
- electric_eye: 電眼聯動接口
- electric_eye_advanced: 電眼高級版（預判+權重分析）
"""

from shadowless.mouse import HumanMouse
from shadowless.keyboard import HumanKeyboard
from shadowless.clipboard import Clipboard
from shadowless.captcha.slider import SliderBypass
from shadowless.captcha.click import ClickBypass
from shadowless.electric_eye import ElectricEyeInterface
from shadowless.electric_eye_advanced import ElectricEyeAdvanced

__version__ = "1.0.0"
__author__ = "小白 (矽靈) & 趙亮"
__license__ = "MIT"


class ShadowlessHand:
    """
    無影手主類 - 整合所有操作能力
    
    示例:
        hand = ShadowlessHand()
        hand.click(500, 300)  # 擬人化點擊
        hand.drag(100, 300, 350, 300)  # 擬人化拖拽
    """
    
    def __init__(self):
        self.mouse = HumanMouse()
        self.keyboard = HumanKeyboard()
        self.clipboard = Clipboard()
        self.slider_bypass = SliderBypass()
        self.click_bypass = ClickBypass()
    
    def move_to(self, x, y, duration=1.0):
        """擬人化移動到指定位置"""
        self.mouse.move_to(x, y, duration=duration)
    
    def click(self, x=None, y=None, button="left", clicks=1):
        """擬人化點擊"""
        if x is not None and y is not None:
            self.mouse.move_to(x, y, duration=0.3)
        self.mouse.click(button=button, clicks=clicks)
    
    def double_click(self, x=None, y=None):
        """擬人化雙擊"""
        self.click(x, y, clicks=2)
    
    def right_click(self, x=None, y=None):
        """擬人化右鍵點擊"""
        self.click(x, y, button="right")
    
    def drag(self, start_x, start_y, end_x, end_y, duration=1.5):
        """擬人化拖拽（核心：用於滑塊驗證）"""
        self.mouse.drag(start_x, start_y, end_x, end_y, duration=duration)
    
    def scroll(self, clicks=3, direction="down"):
        """滾動"""
        self.mouse.scroll(clicks, direction)
    
    def type_text(self, text, interval=0.05):
        """擬人化輸入文字"""
        self.keyboard.type_text(text, interval=interval)
    
    def hotkey(self, *keys):
        """快捷鍵"""
        self.keyboard.hotkey(*keys)
    
    def press_key(self, key):
        """按下单個鍵"""
        self.keyboard.press(key)
    
    def solve_slider(self, gap_x, gap_y, start_x=0, start_y=None):
        """
        突破滑塊驗證
        
        Args:
            gap_x: 缺口 X 坐標（電眼提供）
            gap_y: 缺口 Y 坐標（電眼提供）
            start_x: 滑塊起始 X 位置
            start_y: 滑塊 Y 位置（如果為 None，使用 gap_y）
        """
        if start_y is None:
            start_y = gap_y
        return self.slider_bypass.solve(gap_x, gap_y, start_x, start_y)
    
    def solve_click(self, points):
        """
        突破點擊驗證
        
        Args:
            points: 點擊坐標列表 [(x1, y1), (x2, y2), ...]
        """
        return self.click_bypass.solve(points)
    
    def execute(self, command):
        """
        執行電眼指令
        
        Args:
            command: JSON 格式的指令
                {
                    "action": "move|click|drag|slide|type|hotkey|scroll",
                    ... 其他參數
                }
        """
        action = command.get("action")
        
        if action == "move":
            self.move_to(command["x"], command["y"], command.get("duration", 1.0))
        
        elif action == "click":
            self.click(command.get("x"), command.get("y"), 
                      command.get("button", "left"),
                      command.get("clicks", 1))
        
        elif action == "drag":
            self.drag(command["start_x"], command["start_y"],
                     command["end_x"], command["end_y"],
                     command.get("duration", 1.5))
        
        elif action == "slide":
            self.solve_slider(command["target_x"], command["target_y"],
                            command.get("start_x", 0),
                            command.get("start_y"))
        
        elif action == "type":
            self.type_text(command["text"], command.get("interval", 0.05))
        
        elif action == "hotkey":
            self.hotkey(*command["keys"])
        
        elif action == "scroll":
            self.scroll(command.get("clicks", 3), command.get("direction", "down"))
        
        else:
            raise ValueError(f"未知指令：{action}")
        
        return {"status": "success", "action": action}


# 便捷實例
hand = ShadowlessHand()

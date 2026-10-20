"""
剪貼板操作模組

提供跨平台的剪貼板讀寫功能
"""

import pyperclip
import time
import random


class Clipboard:
    """
    剪貼板控制器
    
    支持文本讀寫，帶有人類操作延遲
    """
    
    def __init__(self):
        pass
    
    def copy(self, text: str):
        """
        複製文本到剪貼板
        
        Args:
            text: 要複製的文本
        """
        pyperclip.copy(text)
        time.sleep(random.uniform(0.05, 0.15))
    
    def paste(self) -> str:
        """
        從剪貼板貼上文本
        
        Returns:
            剪貼板內容
        """
        content = pyperclip.paste()
        time.sleep(random.uniform(0.05, 0.15))
        return content
    
    def cut(self):
        """
        剪下（Ctrl+X）
        """
        import pyautogui
        pyautogui.hotkey("ctrl", "x")
        time.sleep(random.uniform(0.1, 0.2))
    
    def select_all(self):
        """
        全選（Ctrl+A）
        """
        import pyautogui
        pyautogui.hotkey("ctrl", "a")
        time.sleep(random.uniform(0.1, 0.2))
    
    def clear(self):
        """清空剪貼板"""
        pyperclip.copy("")
    
    def append(self, text: str, separator: str = "\n"):
        """
        追加文本到剪貼板
        
        Args:
            text: 要追加的文本
            separator: 分隔符
        """
        current = self.paste()
        if current:
            new_content = current + separator + text
        else:
            new_content = text
        self.copy(new_content)

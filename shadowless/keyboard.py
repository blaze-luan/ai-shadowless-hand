"""
擬人化鍵盤輸入模組

特點：
- 隨機輸入間隔
- 偶爾誤觸糾正（模擬人類打字錯誤）
- 長文本自動分段
"""

import pyautogui
import time
import random
import string


class HumanKeyboard:
    """
    擬人化鍵盤控制器
    
    模擬真實人類打字行為
    """
    
    def __init__(self):
        pyautogui.PAUSE = 0.05
    
    def type_text(self, text: str, interval: float = 0.05, 
                  error_rate: float = 0.02):
        """
        擬人化輸入文字
        
        Args:
            text: 要輸入的文字
            interval: 基礎間隔（秒）
            error_rate: 錯誤率（0-1），模擬打字錯誤
        """
        if not text:
            return
        
        # 分段輸入，避免一次性輸入太長
        chunks = self._split_text(text, chunk_size=20)
        
        for chunk in chunks:
            self._type_chunk(chunk, interval, error_rate)
            # 每段之間較長停頓（模擬思考）
            time.sleep(random.uniform(0.3, 0.8))
    
    def press(self, key: str):
        """按下單個鍵"""
        pyautogui.press(key)
    
    def hotkey(self, *keys: str):
        """
        快捷鍵組合
        
        Args:
            *keys: 按下的鍵，如 "ctrl", "c"
        """
        pyautogui.hotkey(*keys)
        time.sleep(random.uniform(0.1, 0.3))
    
    def _type_chunk(self, chunk: str, interval: float, error_rate: float):
        """輸入一個文本塊"""
        for char in chunk:
            # 隨機間隔變化
            actual_interval = interval * random.uniform(0.5, 1.5)
            
            # 模擬打字錯誤
            if random.random() < error_rate and char.isalpha():
                # 打錯一個字符
                wrong_char = random.choice(string.ascii_lowercase)
                pyautogui.typewrite(wrong_char, interval=0.05)
                time.sleep(random.uniform(0.2, 0.4))
                # 刪除錯誤
                pyautogui.press("backspace")
                time.sleep(random.uniform(0.1, 0.3))
            
            # 輸入正確字符
            pyautogui.typewrite(char, interval=actual_interval)
            
            # 字符間微小停頓
            time.sleep(random.uniform(0.01, 0.05))
    
    def _split_text(self, text: str, chunk_size: int = 20) -> list:
        """
        將長文本分段
        
        盡量在空格或標點處斷開
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        current = ""
        
        for char in text:
            current += char
            
            if len(current) >= chunk_size:
                # 尋找最近的斷點（空格或標點）
                break_point = current.rfind(" ")
                if break_point == -1:
                    break_point = current.rfind(",")
                if break_point == -1:
                    break_point = current.rfind(".")
                if break_point == -1:
                    break_point = chunk_size
                
                chunks.append(current[:break_point])
                current = current[break_point:]
        
        if current:
            chunks.append(current)
        
        return chunks

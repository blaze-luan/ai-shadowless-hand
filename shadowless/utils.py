"""
工具函數模組
"""

import pyautogui
import time
import random


def get_screen_size() -> tuple:
    """獲取屏幕尺寸"""
    return pyautogui.size()


def get_mouse_position() -> tuple:
    """獲取當前鼠標位置"""
    return pyautogui.position()


def safe_sleep(min_seconds: float = 0.5, max_seconds: float = 1.5):
    """安全休眠（隨機時長）"""
    time.sleep(random.uniform(min_seconds, max_seconds))


def is_within_screen(x: int, y: int) -> bool:
    """檢查坐標是否在屏幕範圍內"""
    width, height = get_screen_size()
    return 0 <= x <= width and 0 <= y <= height


def validate_coordinates(x: int, y: int):
    """驗證坐標有效性"""
    if not is_within_screen(x, y):
        raise ValueError(f"坐標 ({x}, {y}) 超出屏幕範圍")


def human_delay(base_seconds: float = 0.5, variance: float = 0.3):
    """擬人化延遲"""
    delay = base_seconds + random.uniform(-variance, variance)
    delay = max(0.1, delay)  # 最短 0.1 秒
    time.sleep(delay)


def generate_random_offset(max_offset: int = 5) -> tuple:
    """生成隨機偏移量"""
    return (
        random.randint(-max_offset, max_offset),
        random.randint(-max_offset, max_offset)
    )


def calculate_distance(x1: int, y1: int, x2: int, y2: int) -> float:
    """計算兩點距離"""
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def wait_for_user(message: str = "按 Enter 繼續..."):
    """等待用戶確認"""
    input(f"\n{message}")


def log_action(action: str, details: dict = None):
    """記錄操作日誌"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {action}")
    if details:
        for key, value in details.items():
            print(f"  {key}: {value}")


class CaptchaSolver:
    """
    通用驗證碼解決器
    
    整合電眼和無影手，提供一鍵解決
    """
    
    def __init__(self, hand=None, eye=None):
        """
        初始化解決器
        
        Args:
            hand: ShadowlessHand 實例
            eye: ElectricEyeInterface 實例
        """
        self.hand = hand
        self.eye = eye
    
    def solve(self, captcha_type: str, **kwargs) -> dict:
        """
        解決驗證碼
        
        Args:
            captcha_type: 驗證碼類型 (slider/click/etc)
            **kwargs: 類型特定參數
        
        Returns:
            解決結果
        """
        if captcha_type == "slider":
            return self._solve_slider(**kwargs)
        elif captcha_type == "click":
            return self._solve_click(**kwargs)
        else:
            return {"success": False, "error": f"不支持的類型：{captcha_type}"}
    
    def _solve_slider(self, gap_x: int, gap_y: int, **kwargs) -> dict:
        """解決滑塊驗證"""
        if not self.hand:
            return {"success": False, "error": "未配置無影手"}
        return self.hand.captcha.solve_slider(gap_x, gap_y)
    
    def _solve_click(self, points: list, **kwargs) -> dict:
        """解決點擊驗證"""
        if not self.hand:
            return {"success": False, "error": "未配置無影手"}
        return self.hand.captcha.solve_click(points)

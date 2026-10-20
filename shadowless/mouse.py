"""
擬人化鼠標控制模組

核心算法：
- 貝塞爾曲線軌跡生成
- 隨機擾動模擬人類手部顫抖
- 加速度/減速度模擬真實移動
- 隨機暫停模擬思考
"""

import pyautogui
import numpy as np
import time
import random
from typing import Tuple, List


class HumanMouse:
    """
    擬人化鼠標控制器
    
    特點：
    - 非直線移動，使用貝塞爾曲線
    - 隨機速度變化
    - 偶爾微小回退（模擬人類不確定性）
    - 移動前後隨機延遲
    """
    
    def __init__(self):
        # 安全設置：移動到屏幕邊緣時不會失敗
        pyautogui.FAILSAFE = True
        # 每次操作後暫停 0.1 秒（可關閉以提升速度）
        pyautogui.PAUSE = 0.1
    
    def move_to(self, x: int, y: int, duration: float = 1.0):
        """
        擬人化移動到指定位置
        
        Args:
            x: 目標 X 坐標
            y: 目標 Y 坐標
            duration: 移動時間（秒），越長越像人類
        """
        # 獲取當前位置
        current_x, current_y = pyautogui.position()
        
        # 生成擬人化軌跡
        trajectory = self._generate_human_trajectory(
            current_x, current_y, x, y, duration
        )
        
        # 沿軌跡移動
        for point_x, point_y in trajectory:
            pyautogui.moveTo(point_x, point_y, duration=0.01)
    
    def click(self, button: str = "left", clicks: int = 1, interval: float = 0.1):
        """
        擬人化點擊
        
        Args:
            button: 'left', 'right', 'middle'
            clicks: 點擊次數
            interval: 多次點擊間隔
        """
        # 點擊前微調位置（模擬人類不精確）
        offset_x = random.uniform(-2, 2)
        offset_y = random.uniform(-2, 2)
        pyautogui.moveRel(offset_x, offset_y, duration=0.05)
        
        # 執行點擊
        pyautogui.click(button=button, clicks=clicks, interval=interval)
        
        # 點擊後短暫停留（模擬人類確認）
        time.sleep(random.uniform(0.05, 0.15))
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, 
             duration: float = 1.5):
        """
        擬人化拖拽（核心：用於滑塊驗證）
        
        Args:
            start_x: 起始 X
            start_y: 起始 Y
            end_x: 結束 X
            end_y: 結束 Y
            duration: 拖拽時間
        """
        # 先移動到起始位置
        self.move_to(start_x, start_y, duration=0.3)
        time.sleep(random.uniform(0.2, 0.5))  # 模擬人類準備
        
        # 按下鼠標
        pyautogui.mouseDown()
        time.sleep(random.uniform(0.1, 0.2))
        
        # 生成拖拽軌跡（更複雜，包含回退）
        trajectory = self._generate_drag_trajectory(
            start_x, start_y, end_x, end_y, duration
        )
        
        # 沿軌跡移動
        for point_x, point_y in trajectory:
            pyautogui.moveTo(point_x, point_y, duration=0.01)
        
        # 釋放鼠標
        time.sleep(random.uniform(0.1, 0.3))
        pyautogui.mouseUp()
    
    def scroll(self, clicks: int = 3, direction: str = "down"):
        """
        滾動
        
        Args:
            clicks: 滾動量
            direction: 'up' 或 'down'
        """
        scroll_value = clicks if direction == "up" else -clicks
        pyautogui.scroll(scroll_value)
    
    def _generate_human_trajectory(self, x1: int, y1: int, x2: int, y2: int, 
                                    duration: float) -> List[Tuple[int, int]]:
        """
        生成擬人化移動軌跡
        
        使用貝塞爾曲線 + 隨機擾動
        """
        # 計算距離
        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        # 根據距離和時間計算點數
        num_points = max(int(duration * 60), 30)  # 至少 30 個點
        
        # 生成貝塞爾曲線控制點
        # 控制點偏離直線，模擬人類弧形移動
        mid_x = (x1 + x2) / 2 + random.uniform(-50, 50)
        mid_y = (y1 + y2) / 2 + random.uniform(-50, 50)
        
        # 貝塞爾曲線參數
        t = np.linspace(0, 1, num_points)
        
        # 二次貝塞爾曲線
        trajectory_x = (1-t)**2 * x1 + 2*(1-t)*t * mid_x + t**2 * x2
        trajectory_y = (1-t)**2 * y1 + 2*(1-t)*t * mid_y + t**2 * y2
        
        # 添加隨機擾動（模擬手部顫抖）
        noise_scale = max(2, distance * 0.02)  # 距離越遠，擾動越大
        noise_x = np.random.normal(0, noise_scale, num_points)
        noise_y = np.random.normal(0, noise_scale, num_points)
        
        trajectory_x += noise_x
        trajectory_y += noise_y
        
        # 確保起點和終點準確
        trajectory_x[0] = x1
        trajectory_y[0] = y1
        trajectory_x[-1] = x2
        trajectory_y[-1] = y2
        
        # 轉換為整數坐標
        trajectory = list(zip(trajectory_x.astype(int), trajectory_y.astype(int)))
        
        return trajectory
    
    def _generate_drag_trajectory(self, x1: int, y1: int, x2: int, y2: int,
                                   duration: float) -> List[Tuple[int, int]]:
        """
        生成拖拽軌跡（用於滑塊驗證）
        
        特點：
        - 開始慢（猶豫）
        - 中間快（確定方向）
        - 結束慢（精確對準）
        - 偶爾微小回退
        """
        # 基礎軌跡
        base_trajectory = self._generate_human_trajectory(x1, y1, x2, y2, duration)
        
        # 添加速度變化（開始慢，中間快，結束慢）
        num_points = len(base_trajectory)
        speed_profile = []
        
        for i in range(num_points):
            progress = i / num_points
            
            if progress < 0.2:
                # 開始階段：慢速
                speed_profile.append(0.3)
            elif progress < 0.8:
                # 中間階段：快速
                speed_profile.append(1.0)
            else:
                # 結束階段：慢速精確
                speed_profile.append(0.2)
        
        # 應用速度剖面（重複某些點以模擬慢速）
        trajectory = []
        for i, (x, y) in enumerate(base_trajectory):
            repeat = max(1, int(3 * speed_profile[i]))
            trajectory.extend([(x, y)] * repeat)
        
        # 在 70-80% 位置添加微小回退（模擬人類不確定）
        if random.random() < 0.3:  # 30% 概率
            backtrack_index = int(len(trajectory) * 0.75)
            backtrack_amount = random.randint(5, 15)
            for j in range(backtrack_index, min(backtrack_index + 10, len(trajectory))):
                trajectory[j] = (trajectory[j][0] - backtrack_amount, trajectory[j][1])
        
        return trajectory

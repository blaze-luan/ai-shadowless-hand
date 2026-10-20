"""
擬人化軌跡生成算法

核心技術：
- 貝塞爾曲線基礎路徑
- 物理加速度模擬
- 隨機擾動（手部顫抖）
- 猶豫回退（人類不確定性）

這是突破驗證碼的關鍵算法
"""

import numpy as np
import random
from typing import List, Tuple


class HumanTrajectory:
    """
    擬人化軌跡生成器
    
    生成無法被機器學習區分的人類操作軌跡
    """
    
    @staticmethod
    def generate_slider_trajectory(start_x: int, start_y: int,
                                    end_x: int, end_y: int,
                                    duration: float = 2.0) -> List[Tuple[int, int]]:
        """
        生成滑塊拖拽軌跡
        
        特點：
        - 開始慢（猶豫）
        - 中間加速（確定方向）
        - 結束減速（精確對準）
        - 偶爾微小回退
        
        Args:
            start_x: 起始 X
            start_y: 起始 Y
            end_x: 結束 X
            end_y: 結束 Y
            duration: 總時間（秒）
        
        Returns:
            軌跡點列表 [(x, y), ...]
        """
        # 基礎參數
        num_points = int(duration * 50)  # 每秒 50 個點
        distance = end_x - start_x
        
        # 生成時間參數
        t = np.linspace(0, 1, num_points)
        
        # 速度剖面：慢 - 快 - 慢
        speed_profile = np.zeros(num_points)
        for i in range(num_points):
            progress = i / num_points
            if progress < 0.15:
                # 開始階段：極慢（猶豫）
                speed_profile[i] = 0.2 + progress * 2
            elif progress < 0.85:
                # 中間階段：快速
                speed_profile[i] = 1.0 + random.uniform(-0.2, 0.2)
            else:
                # 結束階段：減速精確
                speed_profile[i] = 0.3 * (1 - progress) * 6.67
        
        # 累積位置（根據速度剖面）
        cumulative_distance = np.cumsum(speed_profile)
        cumulative_distance = cumulative_distance / cumulative_distance[-1] * distance
        
        # 生成 X 坐標
        x_coords = start_x + cumulative_distance
        
        # 生成 Y 坐標（基本保持不變，微小抖動）
        y_jitter = np.random.normal(0, 1.5, num_points)
        y_coords = np.full(num_points, start_y) + y_jitter
        
        # 添加隨機擾動（模擬手部顫抖）
        noise_scale = max(1, abs(distance) * 0.01)
        x_noise = np.random.normal(0, noise_scale, num_points)
        y_noise = np.random.normal(0, noise_scale * 0.5, num_points)
        
        x_coords += x_noise
        y_coords += y_noise
        
        # 在 70-80% 位置添加回退（30% 概率）
        if random.random() < 0.3:
            backtrack_start = int(num_points * 0.7)
            backtrack_end = int(num_points * 0.78)
            backtrack_amount = random.randint(3, 8)
            
            for i in range(backtrack_start, backtrack_end):
                x_coords[i] -= backtrack_amount * ((i - backtrack_start) / (backtrack_end - backtrack_start))
            
            # 回退後恢復
            for i in range(backtrack_end, min(backtrack_end + 10, num_points)):
                recovery = backtrack_amount * (1 - (i - backtrack_end) / 10)
                x_coords[i] -= recovery
        
        # 確保起點和終點準確
        x_coords[0] = start_x
        y_coords[0] = start_y
        x_coords[-1] = end_x
        y_coords[-1] = end_y
        
        # 轉換為整數
        trajectory = list(zip(x_coords.astype(int), y_coords.astype(int)))
        
        return trajectory
    
    @staticmethod
    def generate_click_trajectory(points: List[Tuple[int, int]], 
                                   base_delay: float = 0.5) -> List[dict]:
        """
        生成點擊驗證的操作序列
        
        Args:
            points: 點擊坐標列表
            base_delay: 基礎延遲
        
        Returns:
            操作序列 [{"x": x, "y": y, "delay": delay}, ...]
        """
        actions = []
        
        for i, (x, y) in enumerate(points):
            # 隨機延遲（模擬人類思考）
            delay = base_delay * random.uniform(0.7, 1.5)
            
            # 第一次點擊前較長延遲（觀察時間）
            if i == 0:
                delay += random.uniform(0.5, 1.0)
            
            # 添加微偏移（模擬點擊不精確）
            offset_x = random.uniform(-2, 2)
            offset_y = random.uniform(-2, 2)
            
            actions.append({
                "x": int(x + offset_x),
                "y": int(y + offset_y),
                "delay": delay,
                "index": i
            })
        
        return actions
    
    @staticmethod
    def generate_mouse_path(x1: int, y1: int, x2: int, y2: int, 
                            num_points: int = 50) -> List[Tuple[int, int]]:
        """
        生成貝塞爾曲線鼠標路徑
        
        Args:
            x1, y1: 起點
            x2, y2: 終點
            num_points: 點數
        
        Returns:
            路徑點列表
        """
        # 控制點（偏離直線）
        mid_x = (x1 + x2) / 2 + random.uniform(-30, 30)
        mid_y = (y1 + y2) / 2 + random.uniform(-30, 30)
        
        # 貝塞爾曲線
        t = np.linspace(0, 1, num_points)
        
        x = (1-t)**2 * x1 + 2*(1-t)*t * mid_x + t**2 * x2
        y = (1-t)**2 * y1 + 2*(1-t)*t * mid_y + t**2 * y2
        
        # 添加微小擾動
        x += np.random.normal(0, 1, num_points)
        y += np.random.normal(0, 1, num_points)
        
        # 確保起終點準確
        x[0] = x1
        y[0] = y1
        x[-1] = x2
        y[-1] = y2
        
        return list(zip(x.astype(int), y.astype(int)))

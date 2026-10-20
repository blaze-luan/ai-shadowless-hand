"""
點擊驗證突破模組

用於突破按順序點擊文字/圖標的驗證碼
"""

import pyautogui
import time
import random
from shadowless.captcha.trajectory import HumanTrajectory


class ClickBypass:
    """
    點擊驗證突破器
    
    使用示例:
        clicker = ClickBypass()
        result = clicker.solve([(100, 150), (200, 180), (150, 220)])
    """
    
    def __init__(self):
        self.success_count = 0
        self.fail_count = 0
    
    def solve(self, points: list, max_attempts: int = 3) -> dict:
        """
        突破點擊驗證
        
        Args:
            points: 點擊坐標列表 [(x1, y1), (x2, y2), ...]
            max_attempts: 最大嘗試次數
        
        Returns:
            {
                "success": bool,
                "attempts": int,
                "points_clicked": int
            }
        """
        attempts = 0
        
        while attempts < max_attempts:
            attempts += 1
            
            try:
                # 生成點擊序列
                actions = HumanTrajectory.generate_click_trajectory(points)
                
                # 執行點擊
                success = self._execute_clicks(actions)
                
                if success:
                    self.success_count += 1
                    return {
                        "success": True,
                        "attempts": attempts,
                        "points_clicked": len(points)
                    }
                
            except Exception as e:
                print(f"嘗試 {attempts} 失敗：{e}")
            
            if attempts < max_attempts:
                time.sleep(random.uniform(1.0, 2.0))
        
        self.fail_count += 1
        return {
            "success": False,
            "attempts": attempts,
            "points_clicked": 0
        }
    
    def _execute_clicks(self, actions: list) -> bool:
        """
        執行點擊序列
        
        Args:
            actions: 操作序列 [{"x": x, "y": y, "delay": delay}, ...]
        
        Returns:
            是否完成
        """
        for i, action in enumerate(actions):
            x, y = action["x"], action["y"]
            delay = action["delay"]
            
            # 移動到目標位置（擬人化）
            self._human_move_to(x, y)
            
            # 延遲（模擬思考）
            time.sleep(delay)
            
            # 點擊
            pyautogui.click(x, y)
            
            # 點擊後短暫停頓
            time.sleep(random.uniform(0.2, 0.5))
        
        return True
    
    def _human_move_to(self, x: int, y: int):
        """擬人化移動"""
        # 使用貝塞爾曲線移動
        current_x, current_y = pyautogui.position()
        path = HumanTrajectory.generate_mouse_path(
            current_x, current_y, x, y, num_points=30
        )
        
        for px, py in path:
            pyautogui.moveTo(px, py, duration=0.01)
    
    def get_stats(self) -> dict:
        """獲取統計"""
        total = self.success_count + self.fail_count
        success_rate = self.success_count / total if total > 0 else 0
        
        return {
            "total_attempts": total,
            "success_count": self.success_count,
            "fail_count": self.fail_count,
            "success_rate": f"{success_rate:.1%}"
        }

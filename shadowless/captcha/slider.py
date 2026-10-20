"""
滑塊驗證突破模組

核心功能：
- 接收電眼提供的缺口位置
- 生成擬人化拖拽軌跡
- 執行突破操作
- 返回成功率統計
"""

import pyautogui
import time
import random
from shadowless.captcha.trajectory import HumanTrajectory


class SliderBypass:
    """
    滑塊驗證突破器
    
    使用示例:
        slider = SliderBypass()
        result = slider.solve(gap_x=250, gap_y=100)
        print(f"成功：{result['success']}, 嘗試次數：{result['attempts']}")
    """
    
    def __init__(self):
        self.success_count = 0
        self.fail_count = 0
        self.total_attempts = 0
    
    def solve(self, gap_x: int, gap_y: int, 
              start_x: int = 0, start_y: int = None,
              max_attempts: int = 3) -> dict:
        """
        突破滑塊驗證
        
        Args:
            gap_x: 缺口 X 坐標（電眼識別）
            gap_y: 缺口 Y 坐標（電眼識別）
            start_x: 滑塊起始 X 位置（默認 0）
            start_y: 滑塊 Y 位置（默認使用 gap_y）
            max_attempts: 最大嘗試次數
        
        Returns:
            {
                "success": bool,
                "attempts": int,
                "trajectory_length": int,
                "duration": float
            }
        """
        if start_y is None:
            start_y = gap_y
        
        self.total_attempts += 1
        attempts = 0
        
        while attempts < max_attempts:
            attempts += 1
            
            try:
                # 生成擬人化軌跡
                trajectory = HumanTrajectory.generate_slider_trajectory(
                    start_x, start_y, gap_x, gap_y,
                    duration=random.uniform(1.5, 2.5)
                )
                
                # 執行拖拽
                success = self._execute_drag(trajectory)
                
                if success:
                    self.success_count += 1
                    return {
                        "success": True,
                        "attempts": attempts,
                        "trajectory_length": len(trajectory),
                        "duration": len(trajectory) / 50  # 約 50 點/秒
                    }
                
            except Exception as e:
                print(f"嘗試 {attempts} 失敗：{e}")
            
            # 失敗後重置（需要手動或電眼檢測）
            if attempts < max_attempts:
                time.sleep(random.uniform(1.0, 2.0))
                self._reset_slider()
        
        self.fail_count += 1
        return {
            "success": False,
            "attempts": attempts,
            "trajectory_length": 0,
            "duration": 0
        }
    
    def _execute_drag(self, trajectory: list) -> bool:
        """
        執行拖拽操作
        
        Args:
            trajectory: 軌跡點列表
        
        Returns:
            是否成功（需要外部驗證）
        """
        # 移動到起始位置
        start_x, start_y = trajectory[0]
        pyautogui.moveTo(start_x, start_y, duration=0.3)
        time.sleep(random.uniform(0.3, 0.6))
        
        # 按下鼠標
        pyautogui.mouseDown()
        time.sleep(random.uniform(0.1, 0.2))
        
        # 沿軌跡移動
        for x, y in trajectory[1:]:
            pyautogui.moveTo(x, y, duration=0.01)
        
        # 釋放鼠標
        time.sleep(random.uniform(0.1, 0.3))
        pyautogui.mouseUp()
        
        # 注意：這裡返回 True 只是表示操作完成
        # 實際成功與否需要外部驗證（電眼或用戶確認）
        return True
    
    def _reset_slider(self):
        """重置滑塊到起始位置"""
        # 這裡需要根據具體驗證碼頁面實現
        # 通常是刷新頁面或點擊重置按鈕
        pass
    
    def get_stats(self) -> dict:
        """獲取統計信息"""
        total = self.success_count + self.fail_count
        success_rate = self.success_count / total if total > 0 else 0
        
        return {
            "total_attempts": total,
            "success_count": self.success_count,
            "fail_count": self.fail_count,
            "success_rate": f"{success_rate:.1%}"
        }

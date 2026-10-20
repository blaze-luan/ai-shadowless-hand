"""
電眼聯動接口模組

負責接收電眼的分析結果，轉換為無影手可執行的指令
"""

import json
import time
import requests
from typing import Optional, Dict, Any


class ElectricEyeInterface:
    """
    電眼聯動接口
    
    接收電眼的截圖分析結果，提供給無影手執行
    
    電眼輸出格式示例:
    {
        "captcha_type": "slider",  // slider, click, rotate, etc.
        "gap_position": {"x": 250, "y": 100},
        "click_points": [(100, 150), (200, 180)],
        "confidence": 0.95,
        "screenshot": "base64..."  // 可選
    }
    """
    
    def __init__(self, api_url: str = "http://localhost:5000"):
        """
        初始化電眼接口
        
        Args:
            api_url: 電眼 API 地址
        """
        self.api_url = api_url
        self.last_analysis = None
    
    def capture_and_analyze(self) -> Optional[Dict[str, Any]]:
        """
        調用電眼進行截圖和分析
        
        Returns:
            分析結果字典，失敗返回 None
        """
        try:
            response = requests.post(
                f"{self.api_url}/analyze",
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                self.last_analysis = result
                return result
            
            print(f"電眼 API 錯誤：{response.status_code}")
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"連接電眼失敗：{e}")
            return None
    
    def get_captcha_type(self) -> Optional[str]:
        """獲取驗證碼類型"""
        if self.last_analysis:
            return self.last_analysis.get("captcha_type")
        return None
    
    def get_gap_position(self) -> Optional[tuple]:
        """獲取滑塊缺口位置"""
        if self.last_analysis:
            pos = self.last_analysis.get("gap_position")
            if pos:
                return (pos.get("x"), pos.get("y"))
        return None
    
    def get_click_points(self) -> Optional[list]:
        """獲取點擊位置列表"""
        if self.last_analysis:
            return self.last_analysis.get("click_points")
        return None
    
    def get_confidence(self) -> float:
        """獲取分析置信度"""
        if self.last_analysis:
            return self.last_analysis.get("confidence", 0.0)
        return 0.0
    
    def load_from_json(self, json_str: str) -> Dict[str, Any]:
        """
        從 JSON 字符串加載分析結果
        
        Args:
            json_str: JSON 格式的電眼輸出
        
        Returns:
            分析結果字典
        """
        result = json.loads(json_str)
        self.last_analysis = result
        return result
    
    def load_from_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        從字典加載分析結果
        
        Args:
            data: 電眼分析結果字典
        
        Returns:
            分析結果字典
        """
        self.last_analysis = data
        return data


# 便捷函數
def create_electric_eye(api_url: str = "http://localhost:5000") -> ElectricEyeInterface:
    """創建電眼接口實例"""
    return ElectricEyeInterface(api_url)

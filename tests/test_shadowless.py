#!/usr/bin/env python3
"""
無影手測試套件
"""

import unittest
import json
from shadowless import ShadowlessHand
from shadowless.captcha.trajectory import HumanTrajectory


class TestShadowlessHand(unittest.TestCase):
    """測試主類"""
    
    def setUp(self):
        """測試前初始化"""
        self.hand = ShadowlessHand(debug=False)
    
    def test_initialization(self):
        """測試初始化"""
        self.assertIsNotNone(self.hand)
        self.assertIsNotNone(self.hand.mouse)
        self.assertIsNotNone(self.hand.keyboard)
        self.assertIsNotNone(self.hand.captcha)
    
    def test_json_parsing(self):
        """測試 JSON 解析"""
        test_json = '{"action": "move_to", "x": 100, "y": 200}'
        data = json.loads(test_json)
        
        self.assertEqual(data["action"], "move_to")
        self.assertEqual(data["x"], 100)
        self.assertEqual(data["y"], 200)


class TestTrajectory(unittest.TestCase):
    """測試軌跡生成"""
    
    def test_slider_trajectory(self):
        """測試滑塊軌跡"""
        trajectory = HumanTrajectory.generate_slider_trajectory(
            start_x=0, start_y=100,
            end_x=200, end_y=100,
            duration=2.0
        )
        
        self.assertIsNotNone(trajectory)
        self.assertGreater(len(trajectory), 0)
        
        # 檢查起點和終點
        start = trajectory[0]
        end = trajectory[-1]
        
        self.assertAlmostEqual(start[0], 0, delta=5)
        self.assertAlmostEqual(end[0], 200, delta=5)
    
    def test_click_trajectory(self):
        """測試點擊軌跡"""
        points = [(100, 100), (200, 200)]
        actions = HumanTrajectory.generate_click_trajectory(points)
        
        self.assertIsNotNone(actions)
        self.assertEqual(len(actions), len(points))
        
        # 檢查每個動作都有必要字段
        for action in actions:
            self.assertIn("x", action)
            self.assertIn("y", action)
            self.assertIn("delay", action)
    
    def test_mouse_path(self):
        """測試鼠標路徑"""
        path = HumanTrajectory.generate_mouse_path(
            start_x=0, start_y=0,
            end_x=100, end_y=100,
            num_points=10
        )
        
        self.assertIsNotNone(path)
        self.assertGreater(len(path), 0)


class TestCaptchaBypass(unittest.TestCase):
    """測試驗證碼突破"""
    
    def setUp(self):
        """測試前初始化"""
        self.hand = ShadowlessHand(debug=False)
    
    def test_slider_bypass_initialization(self):
        """測試滑塊突破器初始化"""
        self.assertIsNotNone(self.hand.captcha.slider)
        self.assertEqual(self.hand.captcha.slider.success_count, 0)
        self.assertEqual(self.hand.captcha.slider.fail_count, 0)
    
    def test_click_bypass_initialization(self):
        """測試點擊突破器初始化"""
        self.assertIsNotNone(self.hand.captcha.clicker)
        self.assertEqual(self.hand.captcha.clicker.success_count, 0)
        self.assertEqual(self.hand.captcha.clicker.fail_count, 0)


if __name__ == "__main__":
    # 創建測試套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加測試
    suite.addTests(loader.loadTestsFromTestCase(TestShadowlessHand))
    suite.addTests(loader.loadTestsFromTestCase(TestTrajectory))
    suite.addTests(loader.loadTestsFromTestCase(TestCaptchaBypass))
    
    # 運行測試
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 輸出結果
    print("\n" + "=" * 50)
    print(f"測試完成：{result.testsRun} 個測試")
    print(f"成功：{result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失敗：{len(result.failures)}")
    print(f"錯誤：{len(result.errors)}")
    print("=" * 50)

#!/usr/bin/env python3
"""
無影手基礎使用示例

展示核心功能：鼠標控制、鍵盤輸入、驗證碼突破
"""

from shadowless import ShadowlessHand

def example_basic():
    """基礎操作示例"""
    print("=== 無影手基礎示例 ===\n")
    
    # 初始化
    hand = ShadowlessHand(debug=True)
    
    # 移動鼠標（擬人化）
    print("1. 移動鼠標到 (500, 300)")
    hand.move_to(500, 300)
    
    # 點擊
    print("2. 點擊")
    hand.click()
    
    # 雙擊
    print("3. 雙擊")
    hand.double_click()
    
    # 輸入文字
    print("4. 輸入文字：Hello 你好世界")
    hand.type_text("Hello 你好世界", interval=0.15)
    
    # 快捷鍵
    print("5. 執行快捷鍵 Ctrl+C")
    hand.hotkey('ctrl', 'c')


def example_slider_captcha():
    """滑塊驗證示例"""
    print("\n=== 滑塊驗證示例 ===\n")
    
    hand = ShadowlessHand(debug=True)
    
    # 模擬電眼識別結果
    gap_x = 250
    gap_y = 100
    
    print(f"電眼檢測到缺口位置：({gap_x}, {gap_y})")
    print("正在生成擬人化軌跡...")
    
    # 解決滑塊驗證
    result = hand.captcha.solve_slider(gap_x, gap_y)
    
    if result["success"]:
        print(f"✓ 突破成功！嘗試次數：{result['attempts']}")
    else:
        print(f"✗ 突破失敗，已嘗試 {result['attempts']} 次")


def example_click_captcha():
    """點擊驗證示例"""
    print("\n=== 點擊驗證示例 ===\n")
    
    hand = ShadowlessHand(debug=True)
    
    # 模擬電眼識別結果（按順序點擊三個位置）
    points = [(100, 150), (200, 180), (150, 220)]
    
    print(f"電眼檢測到點擊位置：{points}")
    print("正在執行點擊序列...")
    
    # 解決點擊驗證
    result = hand.captcha.solve_click(points)
    
    if result["success"]:
        print(f"✓ 突破成功！點擊了 {result['points_clicked']} 個位置")
    else:
        print(f"✗ 突破失敗")


def example_electric_eye_integration():
    """電眼聯動示例"""
    print("\n=== 電眼聯動示例 ===\n")
    
    hand = ShadowlessHand(debug=True)
    
    # 模擬電眼返回的 JSON
    electric_eye_json = '''
    {
        "captcha_type": "slider",
        "gap_position": {"x": 250, "y": 100},
        "confidence": 0.95
    }
    '''
    
    print("接收電眼指令...")
    result = hand.execute(electric_eye_json)
    
    if result["success"]:
        print(f"✓ 執行成功：{result['message']}")
        print(f"詳細結果：{result['result']}")
    else:
        print(f"✗ 執行失敗：{result.get('error')}")


if __name__ == "__main__":
    print("無影手 v1.0 - 示例程序\n")
    
    # 基礎操作
    example_basic()
    
    # 滑塊驗證
    example_slider_captcha()
    
    # 點擊驗證
    example_click_captcha()
    
    # 電眼聯動
    example_electric_eye_integration()
    
    print("\n=== 示例完成 ===")

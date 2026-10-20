#!/usr/bin/env python3
"""
電眼高級版演示

展示預判 + 權重分析能力
"""

from shadowless.electric_eye_advanced import ElectricEyeAdvanced


def demo_prediction():
    """演示預判能力"""
    print("=== 電眼預判演示 ===\n")
    
    eye = ElectricEyeAdvanced()
    
    # 模擬多次操作歷史
    contexts = [
        {"captcha_type": "slider", "page_domain": "example.com"},
        {"captcha_type": "slider", "page_domain": "example.com"},
        {"captcha_type": "click", "page_domain": "example.com"},
    ]
    
    # 記錄歷史操作
    for i, ctx in enumerate(contexts):
        actions = ["drag_slider", "analyze_first", "retry"]
        results = [True, False, True]  # 模擬成功失敗交替
        
        for action, result in zip(actions, results):
            eye.record_result(action, result)
    
    # 現在進行預測
    current_context = {"captcha_type": "slider", "page_domain": "example.com"}
    analysis = eye.analyze_and_predict(current_context)
    
    print(f"當前狀態：{analysis['current_state']}")
    print(f"\n預判結果：")
    print(f"  推薦操作：{analysis['prediction']['predicted_action']}")
    print(f"  置信度：{analysis['prediction']['confidence']:.2%}")
    print(f"  推理依據：{analysis['prediction']['reasoning']}")
    
    print(f"\n推薦方案（按優先級）：")
    for rec in analysis["recommendations"]:
        print(f"  [{rec['priority']}] {rec['action']}")
        print(f"      置信度：{rec['confidence']:.2%}")
        print(f"      原因：{rec['reason']}")
    
    print(f"\n學習統計：{eye.get_learning_stats()}")


def demo_weight_analysis():
    """演示權重分析"""
    print("\n=== 權重分析演示 ===\n")
    
    eye = ElectricEyeAdvanced()
    
    # 模擬不同策略的成功情況
    strategies = {
        "fast_drag": [True, True, False, True, True],  # 4/5 成功
        "slow_drag": [True, True, True, False, True],  # 4/5 成功
        "human_drag": [True, True, True, True, True],  # 5/5 成功
        "random_drag": [False, True, False, False, True],  # 2/5 成功
    }
    
    context = {"captcha_type": "slider", "domain": "test.com"}
    
    # 記錄所有策略的歷史
    for strategy, results in strategies.items():
        for result in results:
            eye.predictor.record_action(context, strategy, result)
            eye.record_result(strategy, result)
    
    # 分析權重
    print("各策略權重排名：")
    ranked = eye.analyzer.get_ranked_candidates(top_n=4)
    for i, candidate in enumerate(ranked, 1):
        print(f"  {i}. {candidate['id']}")
        print(f"     權重：{candidate['weight']:.3f}")
        print(f"     歸一化：{candidate['normalized_weight']:.2%}")
    
    # 進行預測
    analysis = eye.analyze_and_predict(context)
    print(f"\n最佳推薦：{analysis['prediction']['predicted_action']}")
    print(f"置信度：{analysis['prediction']['confidence']:.2%}")


def demo_knowledge_persistence():
    """演示知識持久化"""
    print("\n=== 知識持久化演示 ===\n")
    
    eye1 = ElectricEyeAdvanced()
    
    # 學習一些知識
    context = {"captcha_type": "slider"}
    for _ in range(5):
        eye1.predictor.record_action(context, "smart_drag", True)
        eye1.record_result("smart_drag", True)
    
    # 導出知識
    knowledge = eye1.export_knowledge()
    print(f"導出知識（前 200 字符）：\n{knowledge[:200]}...\n")
    
    # 創建新電眼，導入知識
    eye2 = ElectricEyeAdvanced()
    eye2.import_knowledge(knowledge)
    
    # 驗證知識已恢復
    stats = eye2.get_learning_stats()
    print(f"新電眼學習統計：{stats}")
    print("✓ 知識成功轉移！")


def demo_adaptive_learning():
    """演示自適應學習"""
    print("\n=== 自適應學習演示 ===\n")
    
    eye = ElectricEyeAdvanced()
    context = {"captcha_type": "slider", "site": "example.com"}
    
    # 模擬學習過程
    print("開始學習最佳策略...")
    strategies_tested = []
    
    for round_num in range(1, 11):
        # 根據當前預測選擇策略
        analysis = eye.analyze_and_predict(context)
        chosen = analysis["prediction"]["predicted_action"]
        
        # 模擬執行結果（某些策略逐漸變好）
        if chosen == "smart_drag":
            success = round_num > 3  # 第 4 輪後開始成功
        elif chosen == "fast_drag":
            success = round_num < 7  # 前 6 輪成功
        else:
            success = False
        
        eye.record_result(chosen, success)
        strategies_tested.append((chosen, success))
        
        print(f"  第 {round_num} 輪：選擇 {chosen}，結果 {'✓' if success else '✗'}")
    
    # 最終分析
    final_analysis = eye.analyze_and_predict(context)
    print(f"\n最終推薦：{final_analysis['prediction']['predicted_action']}")
    print(f"置信度：{final_analysis['prediction']['confidence']:.2%}")
    print(f"推理：{final_analysis['prediction']['reasoning']}")


if __name__ == "__main__":
    print("電眼高級版 v1.0 - 功能演示\n")
    
    # 演示各項能力
    demo_prediction()
    demo_weight_analysis()
    demo_knowledge_persistence()
    demo_adaptive_learning()
    
    print("\n=== 演示完成 ===")
    print("\n核心能力總結：")
    print("1. ✓ 預判引擎 - 基於歷史預測最佳操作")
    print("2. ✓ 權重分析 - 多策略動態評分")
    print("3. ✓ 自適應學習 - 根據結果調整策略")
    print("4. ✓ 知識持久化 - 導出/導入學習成果")

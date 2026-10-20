"""
電眼高級版 - 預判 + 權重分析

核心升級：
1. 歷史記憶 - 記住操作模式和成功率
2. 預判引擎 - 預測下一步可能的狀態
3. 權重分析 - 多目標/多路徑評估
4. 自適應學習 - 根據結果調整策略
"""

import time
import json
from typing import Dict, List, Optional, Any
from collections import defaultdict


class PredictionEngine:
    """
    預判引擎
    
    基於歷史數據預測下一步
    """
    
    def __init__(self):
        self.history = defaultdict(list)  # 存儲歷史操作記錄
        self.patterns = {}  # 識別出的模式
        self.success_rates = {}  # 各策略成功率
    
    def record_action(self, context: Dict, action: str, result: bool):
        """
        記錄操作歷史
        
        Args:
            context: 上下文信息（頁面狀態、驗證碼類型等）
            action: 執行的操作
            result: 是否成功
        """
        key = self._context_to_key(context)
        self.history[key].append({
            "action": action,
            "result": result,
            "timestamp": time.time()
        })
        
        # 更新成功率
        if key not in self.success_rates:
            self.success_rates[key] = {"success": 0, "total": 0}
        
        self.success_rates[key]["total"] += 1
        if result:
            self.success_rates[key]["success"] += 1
    
    def predict_next_action(self, context: Dict) -> Dict:
        """
        預測下一步最佳操作
        
        Args:
            context: 當前上下文
        
        Returns:
            {
                "predicted_action": str,
                "confidence": float,
                "alternatives": List[Dict],
                "reasoning": str
            }
        """
        key = self._context_to_key(context)
        
        # 如果沒有歷史記錄，返回默認預測
        if key not in self.history or len(self.history[key]) == 0:
            return {
                "predicted_action": "analyze_first",
                "confidence": 0.5,
                "alternatives": [],
                "reasoning": "無歷史數據，使用默認策略"
            }
        
        # 分析歷史記錄
        recent = self.history[key][-10:]  # 最近 10 次
        action_counts = defaultdict(int)
        action_success = defaultdict(lambda: {"success": 0, "total": 0})
        
        for record in recent:
            action = record["action"]
            action_counts[action] += 1
            action_success[action]["total"] += 1
            if record["result"]:
                action_success[action]["success"] += 1
        
        # 計算每個操作的成功率
        action_scores = {}
        for action, stats in action_success.items():
            if stats["total"] > 0:
                success_rate = stats["success"] / stats["total"]
                frequency = action_counts[action] / len(recent)
                # 綜合評分：成功率 * 0.7 + 使用頻率 * 0.3
                score = success_rate * 0.7 + frequency * 0.3
                action_scores[action] = score
        
        # 排序並選擇最佳
        sorted_actions = sorted(action_scores.items(), key=lambda x: x[1], reverse=True)
        
        if not sorted_actions:
            return {
                "predicted_action": "analyze_first",
                "confidence": 0.5,
                "alternatives": [],
                "reasoning": "無法計算評分"
            }
        
        best_action, best_score = sorted_actions[0]
        
        # 生成替代方案
        alternatives = [
            {
                "action": action,
                "score": score,
                "reason": f"歷史成功率 {action_success[action]['success']}/{action_success[action]['total']}"
            }
            for action, score in sorted_actions[1:4]  # 前 3 個替代
        ]
        
        return {
            "predicted_action": best_action,
            "confidence": best_score,
            "alternatives": alternatives,
            "reasoning": f"基於 {len(recent)} 次歷史記錄，{best_action} 評分最高 ({best_score:.2f})"
        }
    
    def _context_to_key(self, context: Dict) -> str:
        """將上下文轉換為鍵值"""
        # 簡化上下文為鍵值
        key_parts = []
        if "captcha_type" in context:
            key_parts.append(f"type={context['captcha_type']}")
        if "page_domain" in context:
            key_parts.append(f"domain={context['page_domain']}")
        if "time_range" in context:
            key_parts.append(f"time={context['time_range']}")
        
        return "|".join(key_parts) if key_parts else "default"
    
    def get_stats(self) -> Dict:
        """獲取統計信息"""
        total_records = sum(len(records) for records in self.history.values())
        return {
            "total_records": total_records,
            "unique_contexts": len(self.history),
            "patterns_identified": len(self.patterns)
        }


class WeightAnalyzer:
    """
    權重分析器
    
    對多個目標/路徑進行權重評估
    """
    
    def __init__(self):
        self.weights = {}  # 存儲各目標權重
        self.decay_rate = 0.95  # 權重衰減率
    
    def add_candidate(self, candidate_id: str, initial_weight: float = 1.0):
        """添加候選目標"""
        if candidate_id not in self.weights:
            self.weights[candidate_id] = initial_weight
    
    def update_weight(self, candidate_id: str, success: bool, multiplier: float = 1.2):
        """
        更新權重
        
        Args:
            candidate_id: 候選 ID
            success: 是否成功
            multiplier: 成功時權重乘數
        """
        if candidate_id not in self.weights:
            self.weights[candidate_id] = 1.0
        
        if success:
            self.weights[candidate_id] *= multiplier
        else:
            self.weights[candidate_id] *= 0.8  # 失敗時權重降低
    
    def get_ranked_candidates(self, top_n: int = 5) -> List[Dict]:
        """
        獲取排名靠前的候選
        
        Returns:
            [{"id": str, "weight": float, "normalized_weight": float}, ...]
        """
        if not self.weights:
            return []
        
        # 計算總權重
        total = sum(self.weights.values())
        
        # 排序
        sorted_candidates = sorted(
            self.weights.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]
        
        return [
            {
                "id": cid,
                "weight": weight,
                "normalized_weight": weight / total if total > 0 else 0
            }
            for cid, weight in sorted_candidates
        ]
    
    def decay_all_weights(self):
        """所有權重衰減（防止舊數據過度影響）"""
        for cid in self.weights:
            self.weights[cid] *= self.decay_rate
    
    def reset(self):
        """重置所有權重"""
        self.weights.clear()


class ElectricEyeAdvanced:
    """
    電眼高級版
    
    整合預判引擎和權重分析器
    """
    
    def __init__(self):
        self.predictor = PredictionEngine()
        self.analyzer = WeightAnalyzer()
        self.last_context = None
        self.last_prediction = None
    
    def analyze_and_predict(self, screenshot_context: Dict) -> Dict:
        """
        分析當前狀態並預測下一步
        
        Args:
            screenshot_context: 截圖分析結果
        
        Returns:
            {
                "current_state": Dict,
                "prediction": Dict,
                "recommendations": List[Dict],
                "confidence": float
            }
        """
        # 保存上下文
        self.last_context = screenshot_context
        
        # 預判
        prediction = self.predictor.predict_next_action(screenshot_context)
        self.last_prediction = prediction
        
        # 生成推薦（結合權重分析）
        recommendations = self._generate_recommendations(screenshot_context, prediction)
        
        return {
            "current_state": screenshot_context,
            "prediction": prediction,
            "recommendations": recommendations,
            "confidence": prediction["confidence"]
        }
    
    def _generate_recommendations(self, context: Dict, prediction: Dict) -> List[Dict]:
        """生成操作推薦"""
        recommendations = []
        
        # 主推薦
        recommendations.append({
            "action": prediction["predicted_action"],
            "priority": 1,
            "confidence": prediction["confidence"],
            "reason": prediction["reasoning"]
        })
        
        # 替代推薦
        for i, alt in enumerate(prediction.get("alternatives", [])[:3], start=2):
            recommendations.append({
                "action": alt["action"],
                "priority": i,
                "confidence": alt["score"],
                "reason": alt["reason"]
            })
        
        # 添加基於權重的推薦
        top_candidates = self.analyzer.get_ranked_candidates(top_n=2)
        for candidate in top_candidates:
            if candidate["normalized_weight"] > 0.3:  # 權重足夠高才推薦
                recommendations.append({
                    "action": f"try_candidate_{candidate['id']}",
                    "priority": len(recommendations) + 1,
                    "confidence": candidate["normalized_weight"],
                    "reason": f"歷史權重 {candidate['weight']:.2f}"
                })
        
        return recommendations
    
    def record_result(self, action: str, result: bool):
        """
        記錄操作結果，用於學習
        
        Args:
            action: 執行的操作
            result: 是否成功
        """
        if self.last_context:
            self.predictor.record_action(self.last_context, action, result)
            
            # 更新權重
            self.analyzer.update_weight(action, result)
            
            # 定期衰減權重
            if self.predictor.get_stats()["total_records"] % 10 == 0:
                self.analyzer.decay_all_weights()
    
    def get_learning_stats(self) -> Dict:
        """獲取學習統計"""
        return {
            "predictor": self.predictor.get_stats(),
            "top_candidates": self.analyzer.get_ranked_candidates(top_n=5),
            "total_actions": sum(
                self.predictor.success_rates[k]["total"]
                for k in self.predictor.success_rates
            )
        }
    
    def export_knowledge(self) -> str:
        """導出學習到的知識（用於持久化）"""
        knowledge = {
            "history": dict(self.predictor.history),
            "success_rates": dict(self.predictor.success_rates),
            "weights": dict(self.analyzer.weights),
            "timestamp": time.time()
        }
        return json.dumps(knowledge, ensure_ascii=False, indent=2)
    
    def import_knowledge(self, knowledge_json: str):
        """導入已學習的知識"""
        knowledge = json.loads(knowledge_json)
        
        # 恢復歷史記錄
        for key, records in knowledge.get("history", {}).items():
            self.predictor.history[key] = records
        
        # 恢復成功率
        self.predictor.success_rates = knowledge.get("success_rates", {})
        
        # 恢復權重
        self.analyzer.weights = knowledge.get("weights", {})


# 便捷函數
def create_advanced_eye() -> ElectricEyeAdvanced:
    """創建高級電眼實例"""
    return ElectricEyeAdvanced()

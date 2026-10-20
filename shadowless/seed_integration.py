"""
種子系統整合模組

將元信息 + 邏輯鏈與電眼預判引擎整合
實現：觀察 → 分析 → 預判 → 決策 → 執行 → 學習 的完整閉環
"""

import json
import time
from typing import Dict, List, Any, Optional
from collections import defaultdict


class MetaInfo:
    """
    元信息管理器
    
    存儲結構化的環境描述
    """
    
    def __init__(self):
        self.info_store = {}  # 元信息存儲
        self.relations = []   # 關係鏈
    
    def add_entity(self, entity_id: str, meta: Dict):
        """
        添加實體元信息
        
        Args:
            entity_id: 實體 ID
            meta: 元信息
                {
                    "type": "captcha|page|element|action",
                    "attributes": {...},
                    "relations": [...]
                }
        """
        self.info_store[entity_id] = {
            "meta": meta,
            "created_at": time.time(),
            "updated_at": time.time()
        }
    
    def get_entity(self, entity_id: str) -> Optional[Dict]:
        """獲取實體元信息"""
        if entity_id in self.info_store:
            return self.info_store[entity_id]["meta"]
        return None
    
    def add_relation(self, from_id: str, to_id: str, relation_type: str):
        """添加關係"""
        self.relations.append({
            "from": from_id,
            "to": to_id,
            "type": relation_type,
            "timestamp": time.time()
        })
    
    def query_by_type(self, entity_type: str) -> List[Dict]:
        """按類型查詢"""
        results = []
        for eid, data in self.info_store.items():
            if data["meta"].get("type") == entity_type:
                results.append({
                    "id": eid,
                    **data["meta"]
                })
        return results


class LogicChain:
    """
    邏輯鏈管理器
    
    存儲推理路徑和因果關係
    """
    
    def __init__(self):
        self.chains = []  # 邏輯鏈列表
        self.patterns = {}  # 識別出的模式
    
    def add_chain(self, chain: Dict):
        """
        添加邏輯鏈
        
        Args:
            chain: {
                "premise": "前提條件",
                "reasoning": "推理步驟",
                "conclusion": "結論",
                "confidence": 0.0-1.0,
                "evidence": [...]
            }
        """
        self.chains.append({
            **chain,
            "created_at": time.time(),
            "used_count": 0,
            "success_count": 0
        })
    
    def find_matching_chains(self, context: Dict) -> List[Dict]:
        """
        查找匹配的邏輯鏈
        
        Args:
            context: 當前上下文
        
        Returns:
            匹配的邏輯鏈列表，按置信度排序
        """
        matched = []
        
        for chain in self.chains:
            # 檢查前提是否匹配
            if self._premise_matches(chain["premise"], context):
                matched.append(chain)
        
        # 按置信度排序
        matched.sort(key=lambda x: x["confidence"], reverse=True)
        return matched
    
    def update_chain(self, chain_index: int, success: bool):
        """更新邏輯鏈的使用統計"""
        if 0 <= chain_index < len(self.chains):
            self.chains[chain_index]["used_count"] += 1
            if success:
                self.chains[chain_index]["success_count"] += 1
            
            # 重新計算置信度
            used = self.chains[chain_index]["used_count"]
            success_count = self.chains[chain_index]["success_count"]
            if used > 0:
                self.chains[chain_index]["confidence"] = success_count / used
    
    def _premise_matches(self, premise: str, context: Dict) -> bool:
        """檢查前提是否匹配上下文"""
        # 簡單的字符串匹配，實際應該用更複雜的模式匹配
        premise_lower = premise.lower()
        context_str = json.dumps(context).lower()
        
        # 檢查關鍵詞
        keywords = premise_lower.split()
        match_count = sum(1 for kw in keywords if kw in context_str)
        
        return match_count >= len(keywords) * 0.5  # 50% 匹配即視為匹配


class SeedSystem:
    """
    種子系統
    
    整合元信息 + 邏輯鏈，提供完整的認知框架
    """
    
    def __init__(self):
        self.meta_info = MetaInfo()
        self.logic_chains = LogicChain()
        self.seeds = []  # 操作種子
    
    def plant_seed(self, observation: Dict, analysis: Dict, action: str, result: bool):
        """
        播種 - 記錄一次完整的觀察-分析-決策-執行循環
        
        Args:
            observation: 觀察結果（截圖分析）
            analysis: 分析結果（元信息提取）
            action: 執行的操作
            result: 是否成功
        """
        seed = {
            "observation": observation,
            "analysis": analysis,
            "action": action,
            "result": result,
            "timestamp": time.time()
        }
        
        self.seeds.append(seed)
        
        # 提取元信息
        self._extract_meta_info(observation, analysis)
        
        # 構建邏輯鏈
        self._build_logic_chain(observation, analysis, action, result)
    
    def _extract_meta_info(self, observation: Dict, analysis: Dict):
        """從觀察中提取元信息"""
        # 頁面元信息
        if "page_type" in observation:
            self.meta_info.add_entity(
                f"page_{observation.get('url', 'unknown')}",
                {
                    "type": "page",
                    "attributes": {
                        "type": observation["page_type"],
                        "domain": observation.get("domain"),
                        "elements": observation.get("elements", [])
                    }
                }
            )
        
        # 驗證碼元信息
        if "captcha_type" in observation:
            captcha_id = f"captcha_{observation['captcha_type']}_{hash(str(observation))}"
            self.meta_info.add_entity(
                captcha_id,
                {
                    "type": "captcha",
                    "attributes": {
                        "captcha_type": observation["captcha_type"],
                        "difficulty": analysis.get("difficulty", "medium"),
                        "estimated_time": analysis.get("estimated_time", 5)
                    }
                }
            )
    
    def _build_logic_chain(self, observation: Dict, analysis: Dict, action: str, result: bool):
        """構建邏輯鏈"""
        # 提取前提
        premise_parts = []
        if "captcha_type" in observation:
            premise_parts.append(f"驗證碼類型={observation['captcha_type']}")
        if "page_type" in observation:
            premise_parts.append(f"頁面類型={observation['page_type']}")
        
        premise = " AND ".join(premise_parts) if premise_parts else "default"
        
        # 構建邏輯鏈
        chain = {
            "premise": premise,
            "reasoning": f"觀察到 {premise}，分析得出 {analysis.get('strategy', 'unknown')}，執行 {action}",
            "conclusion": f"執行 {action}",
            "confidence": 0.8 if result else 0.3,
            "evidence": [observation, analysis]
        }
        
        self.logic_chains.add_chain(chain)
    
    def predict_and_decide(self, current_observation: Dict) -> Dict:
        """
        基於種子系統進行預判和決策
        
        Args:
            current_observation: 當前觀察
        
        Returns:
            {
                "recommended_action": str,
                "confidence": float,
                "reasoning_chain": List[str],
                "alternative_actions": List[Dict]
            }
        """
        # 查找匹配的邏輯鏈
        matching_chains = self.logic_chains.find_matching_chains(current_observation)
        
        if not matching_chains:
            return {
                "recommended_action": "analyze_first",
                "confidence": 0.5,
                "reasoning_chain": ["無匹配的邏輯鏈，使用默認策略"],
                "alternative_actions": []
            }
        
        # 選擇最佳邏輯鏈
        best_chain = matching_chains[0]
        
        # 構建推理鏈
        reasoning = [
            f"觀察：{current_observation}",
            f"匹配邏輯鏈：{best_chain['premise']}",
            f"推理：{best_chain['reasoning']}",
            f"結論：{best_chain['conclusion']}"
        ]
        
        # 提取替代方案
        alternatives = [
            {
                "action": chain["conclusion"],
                "confidence": chain["confidence"],
                "reasoning": chain["reasoning"]
            }
            for chain in matching_chains[1:4]
        ]
        
        return {
            "recommended_action": best_chain["conclusion"],
            "confidence": best_chain["confidence"],
            "reasoning_chain": reasoning,
            "alternative_actions": alternatives
        }
    
    def learn_from_result(self, action: str, result: bool):
        """從結果中學習"""
        # 找到最近使用的邏輯鏈並更新
        for i, chain in enumerate(self.logic_chains.chains):
            if chain["conclusion"] == action:
                self.logic_chains.update_chain(i, result)
                break
    
    def get_knowledge_summary(self) -> Dict:
        """獲取知識摘要"""
        return {
            "total_seeds": len(self.seeds),
            "meta_entities": len(self.meta_info.info_store),
            "logic_chains": len(self.logic_chains.chains),
            "success_rate": (
                sum(1 for s in self.seeds if s["result"]) / len(self.seeds)
                if self.seeds else 0
            )
        }
    
    def export_knowledge(self) -> str:
        """導出知識"""
        knowledge = {
            "meta_info": self.meta_info.info_store,
            "relations": self.meta_info.relations,
            "logic_chains": self.logic_chains.chains,
            "seeds": self.seeds,
            "exported_at": time.time()
        }
        return json.dumps(knowledge, ensure_ascii=False, indent=2)
    
    def import_knowledge(self, knowledge_json: str):
        """導入知識"""
        knowledge = json.loads(knowledge_json)
        
        self.meta_info.info_store = knowledge.get("meta_info", {})
        self.meta_info.relations = knowledge.get("relations", [])
        self.logic_chains.chains = knowledge.get("logic_chains", [])
        self.seeds = knowledge.get("seeds", [])


# 整合電眼高級版
class IntegratedEye:
    """
    整合版電眼
    
    結合種子系統 + 預判引擎 + 權重分析
    """
    
    def __init__(self):
        from shadowless.electric_eye_advanced import ElectricEyeAdvanced
        self.advanced_eye = ElectricEyeAdvanced()
        self.seed_system = SeedSystem()
    
    def observe_analyze_predict(self, screenshot: Any) -> Dict:
        """
        觀察 → 分析 → 預判 完整流程
        
        Args:
            screenshot: 截圖或截圖分析結果
        
        Returns:
            完整的分析結果
        """
        # 1. 觀察（截圖分析）
        observation = self._analyze_screenshot(screenshot)
        
        # 2. 分析（元信息提取）
        analysis = self._extract_meta_info(observation)
        
        # 3. 預判（種子系統 + 高級電眼）
        seed_prediction = self.seed_system.predict_and_decide(observation)
        advanced_prediction = self.advanced_eye.analyze_and_predict(observation)
        
        # 4. 融合決策
        final_decision = self._merge_predictions(seed_prediction, advanced_prediction)
        
        return {
            "observation": observation,
            "analysis": analysis,
            "prediction": final_decision,
            "knowledge_summary": self.seed_system.get_knowledge_summary()
        }
    
    def execute_and_learn(self, action: str, result: bool):
        """執行並學習"""
        # 記錄到種子系統
        if hasattr(self, '_last_observation') and hasattr(self, '_last_analysis'):
            self.seed_system.plant_seed(
                self._last_observation,
                self._last_analysis,
                action,
                result
            )
        
        # 記錄到高級電眼
        self.advanced_eye.record_result(action, result)
        
        # 種子系統學習
        self.seed_system.learn_from_result(action, result)
    
    def _analyze_screenshot(self, screenshot: Any) -> Dict:
        """分析截圖"""
        # 這裡應該調用實際的圖像分析 API
        # 暫時返回模擬數據
        return {
            "page_type": "login",
            "captcha_type": "slider",
            "domain": "example.com",
            "elements": ["slider", "input_box", "submit_button"]
        }
    
    def _extract_meta_info(self, observation: Dict) -> Dict:
        """提取元信息"""
        return {
            "difficulty": "medium",
            "estimated_time": 5,
            "strategy": "human_like_drag",
            "confidence": 0.8
        }
    
    def _merge_predictions(self, seed_pred: Dict, advanced_pred: Dict) -> Dict:
        """融合兩個預測"""
        # 簡單融合：取置信度高的
        if seed_pred["confidence"] > advanced_pred["prediction"]["confidence"]:
            return {
                "source": "seed_system",
                **seed_pred
            }
        else:
            return {
                "source": "advanced_eye",
                **advanced_pred["prediction"]
            }


# 便捷函數
def create_integrated_eye() -> IntegratedEye:
    """創建整合版電眼"""
    return IntegratedEye()

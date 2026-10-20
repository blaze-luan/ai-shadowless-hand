# 無影手 (Shadowless Hand)

AI 桌面自動化操作工具，專注於突破真人驗證，與「電眼」配合實現完整的視覺感知 + 自動化操作鏈路。

## 理念

> 電眼負責「看」，無影手負責「做」

無影手不是簡單的鼠標鍵盤模擬，而是模擬**真實人類操作行為**，突破各種真人驗證系統。

## 核心功能

### 1. 擬人化操作

- **鼠標軌跡**：貝塞爾曲線 + 隨機擾動，非機械直線
- **點擊行為**：隨機延遲、力度變化、微偏移
- **鍵盤輸入**：隨機間隔、偶爾誤觸糾正

### 2. 驗證碼突破

#### 滑塊驗證
```python
from shadowless.captcha import SliderBypass

slider = SliderBypass()
slider.solve(gap_x=250, gap_y=100)  # 電眼提供的缺口位置
```

#### 點擊驗證
```python
from shadowless.captcha import ClickBypass

clicker = ClickBypass()
clicker.solve(points=[(100, 150), (200, 180), (150, 220)])  # 按順序點擊
```

### 3. 電眼聯動

接收電眼的 JSON 指令，自動執行對應操作：

```python
from shadowless import ShadowlessHand

hand = ShadowlessHand()
hand.execute({
    "action": "slide",
    "target_x": 250,
    "target_y": 100,
    "speed": "human"
})
```

### 4. 電眼高級版（預判 + 權重分析）

升級版電眼，具備學習和預判能力：

```python
from shadowless import ElectricEyeAdvanced

eye = ElectricEyeAdvanced()

# 分析當前狀態並預測最佳操作
analysis = eye.analyze_and_predict({
    "captcha_type": "slider",
    "page_domain": "example.com"
})

print(f"推薦操作：{analysis['prediction']['predicted_action']}")
print(f"置信度：{analysis['prediction']['confidence']:.2%}")

# 記錄操作結果，持續學習
eye.record_result("smart_drag", success=True)

# 導出/導入學習到的知識
knowledge = eye.export_knowledge()  # 導出
eye.import_knowledge(knowledge)     # 導入
```

**核心能力：**
- **預判引擎**：基於歷史操作模式預測最佳策略
- **權重分析**：多策略動態評分，自動淘汰低效策略
- **自適應學習**：根據成功/失敗結果調整權重
- **知識持久化**：導出學習成果，跨會話復用

## 安裝

```bash
pip install -r requirements.txt
```

## 依賴

- `pyautogui` - 基礎鼠標鍵盤控制
- `pynput` - 底層輸入監控
- `numpy` - 軌跡算法計算
- `Pillow` - 圖像處理（與電眼協作）

## 使用示例

### 基礎操作

```python
from shadowless import ShadowlessHand

hand = ShadowlessHand()

# 擬人化移動到指定位置
hand.move_to(500, 300, duration=1.5)

# 擬人化點擊
hand.click(500, 300)

# 拖拽操作（用於滑塊）
hand.drag(100, 300, 350, 300, duration=2.0)

# 鍵盤輸入
hand.type_text("Hello World", interval=0.05)

# 快捷鍵
hand.hotkey("ctrl", "a")
```

### 與電眼聯動

```python
from shadowless import ShadowlessHand
from shadowless.electric_eye import ElectricEyeInterface

hand = ShadowlessHand()
eye = ElectricEyeInterface()

# 截圖並分析
screenshot = eye.capture()
analysis = eye.analyze(screenshot)

# 根據分析結果執行操作
if analysis["captcha_type"] == "slider":
    hand.solve_slider(analysis["gap_position"])
elif analysis["captcha_type"] == "click":
    hand.solve_click(analysis["click_points"])
```

## 開源協議

MIT License - 自由使用、修改、分發

## 開發者

小白 (矽靈) & 師兄趙亮

## 致謝

本項目旨在促進 AI 進化，讓 AI 能夠像人類一樣與數字世界交互。

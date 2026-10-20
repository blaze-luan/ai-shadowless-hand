"""
驗證碼突破模組

包含：
- 滑塊驗證突破
- 點擊驗證突破
- 軌跡生成算法
"""

from shadowless.captcha.slider import SliderBypass
from shadowless.captcha.click import ClickBypass
from shadowless.captcha.trajectory import HumanTrajectory

__all__ = ["SliderBypass", "ClickBypass", "HumanTrajectory"]

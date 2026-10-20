from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="shadowless",
    version="1.0.0",
    author="Silicon Spirit",
    description="AI 驅動的桌面操作自動化框架",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blaze-luan/ai-shadowless-hand",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords="automation, captcha, ai, desktop, pyautogui",
    project_urls={
        "Bug Reports": "https://github.com/blaze-luan/ai-shadowless-hand/issues",
        "Source": "https://github.com/blaze-luan/ai-shadowless-hand",
    },
)

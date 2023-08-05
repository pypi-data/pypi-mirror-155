import setuptools
# readme.md = github readme.md, 這裡可接受markdown寫法
# 如果沒有的話，需要自己打出介紹此專案的檔案，再讓程式知道
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wopa", # 
    version="0.0.2",
    author="Wei",
    author_email="acer1456@gmail.com",
    description="一個給研究者使用的簡單便利資料搜索工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/acer1456/wopa",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'pandas>=1',
        'newspaper3k',
        'user_agent',
        'xlsxwriter'
    ]
)
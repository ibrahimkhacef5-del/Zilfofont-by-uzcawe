cat > ~/zalfofont/setup.py << 'PYEOF'
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="zalfofont",
    version="1.0.0",
    description="لغة برمجة للخطوط — اكتب الخط، واحصل على TTF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ibrahimkhacef5-del",
    url="https://github.com/ibrahimkhacef5-del/zalfofont",
    packages=find_packages(),
    install_requires=[
        "fonttools>=4.40.0",
    ],
    entry_points={
        "console_scripts": [
            "zf=zalfofont.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics :: Fonts",
    ],
)
PYEOF

echo "✅ setup.py"

from setuptools import setup


setup(
    name="pyicon",
    version="0.1.0",
    install_requires=[
        "click",
        "pillow",
    ],
    entry_points={
        "console_scripts": [
            "icon = icon:cli",
        ],
    },
)

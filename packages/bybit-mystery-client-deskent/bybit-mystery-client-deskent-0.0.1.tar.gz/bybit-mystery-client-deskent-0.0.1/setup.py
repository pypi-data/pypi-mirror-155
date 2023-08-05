from setuptools import setup, find_packages
exec(open("src/bybit_mystery/_resources.py").read())
setup(
    name='bybit-mystery-client-deskent',
    version=__version__,
    author=__author__,
    author_email='battenetciz@gmail.com',
    description='Bybit Mystery',
    install_requires=[
        'aiohttp==3.8.1',
        'python-dotenv==0.19.2',
        'selenium-wire==4.6.2',
        'selenium~=4.1.5',
        'webdriver-manager==3.7.0',
        'myloguru-deskent~=0.0.9'
    ],
    scripts=['src/bybit_mystery/main.py'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/Deskent/bybit-mystery",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
)

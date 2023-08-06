from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Command line tool to get your alpha, beta stats out of box"

requirements = [
    'numpy>=1.22.0',
    'pandas>=1.4.0',
]

setup(
    name="finstats",
    version=VERSION,
    author="chrisHchen",
    author_email="chenchris1986@163.com",
    description=DESCRIPTION,
    classifiers = [
        'Programming Language :: Python :: 3',
    ],
    url="https://github.com/chrisHchen/finstats",
    install_requires=requirements,
    python_requires='>=3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'finstats = finstats.stats:finstats'
        ]
    },
)
from setuptools import setup, find_packages

VERSION = "0.0.3"
DESCRIPTION = "Command line tool to get your alpha, beta metrics out of box"

LONG_DESCRIPTION="""finstats is a command line tool to get your 
A-share stocks alpha, beta"""

requirements = [
    'numpy>=1.22.0',
    'pandas>=1.4.0',
    'requests>=2.27.0',
]

setup(
    name="finstats",
    version=VERSION,
    author="chrisHchen",
    author_email="chenchris1986@163.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
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
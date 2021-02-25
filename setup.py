from setuptools import setup
from pathlib import Path

ROOT = Path(__file__).expanduser().resolve().parent

with open(Path('requirements', 'dev.in')) as f:
    required = f.read().splitlines()

setup(install_requires=required)

from setuptools import setup

setup(
	name="piction",
	version="0.2.0",
	description="絵を関数化するライブラリ",
	auther="hackathonNIT",
	url="https://github.com/hackathonNIT/piction",
	packages=["piction"],
	install_requires=open('requirements.txt').read().splitlines(),
)
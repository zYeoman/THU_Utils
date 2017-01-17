# Makefile for THU_Utils
# 
# Author        : Yongwen Zhuang(zYeoman)
# Created       : 2017-01-17
# Last Modified : 2017-01-17

init:
	pip install -r requirements.txt

test:
	cd tests && python test.py

install:
	python setup.py install

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf thu_utils.egg-info/
	rm -rf __pycache__/
	rm -rf thu_utils/__pycache__/
	rm -rf tests/__pycache__/
	rm -rf scripts/__pycache__/

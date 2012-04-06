clean:
	rm *.pyc
	rm */*.pyc
	rm errors.err

release:
	python setup.py sdist

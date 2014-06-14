clean:
	find . -name '*.pyc' -delete
	rm -f errors.err

release:
	python setup.py sdist

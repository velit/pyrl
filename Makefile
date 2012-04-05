clean:
	rm *.pyc
	rm */*.pyc
	rm errors.err

release:
	python setup.py sdist
	mv dist/pyrl-alpha.tar.gz ~/public_html/
	rm -rf dist MANIFEST

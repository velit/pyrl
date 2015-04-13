test:
	py.test-3 -k-slow

test-all:
	py.test-3

future-test:
	grep "from __future__ import absolute_import, division, print_function, unicode_literals" -L *.py */*.py

profile-test:
	python3 -m profile_util.run_profiler
	less data/profiling_results

profile-in-place:
	./pyrl.py -p
	less data/profiling_results

debug:
	python3 -m pdb pyrl.py

clean:
	find . -name '*.pyc' -delete
	rm -f data/errors.err data/profiling_results
	rm -f MANIFEST
	rm -rf dist

release:
	python3 setup.py sdist

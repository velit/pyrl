test-porcelain-output:
	py.test-3 -q -k-slow --tb=line

test:
	py.test-3 -k-slow

test-all:
	py.test-3

future-test:
	grep "from __future__ import absolute_import, division, print_function, unicode_literals" -L *.py */*.py

profile-test:
	python3 -m profile_util.run_profiler
	less save_data/profiling_results

profile-in-place:
	./pyrl.py -p
	less save_data/profiling_results

debug:
	python3 -m pdb pyrl.py

clean:
	find . -name '*.pyc' -delete
	rm -f save_data/errors.err save_data/profiling_results save_data/pyrl.log
	rm -f MANIFEST
	rm -rf dist

release:
	python3 setup.py sdist

log:
	tail -n 50 save_data/pyrl.log

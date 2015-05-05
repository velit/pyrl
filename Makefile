test-porcelain-output:
	py.test-3 -q -k-slow --tb=line

test:
	py.test-3 -k-slow

slow-test:
	py.test-3

test-debug:
	py.test-3 -k-slow -x --pdb

debug:
	python3 -m pdb pyrl.py

log:
	tail -n 50 save_data/pyrl.log

clean:
	find . -name '*.pyc' -delete
	rm -f save_data/errors.err save_data/profiling_results save_data/pyrl.log
	rm -f MANIFEST
	rm -rf dist

profile-test:
	py.test-3 tests/profile_test.py && less save_data/profiling_results

profile-in-place:
	./pyrl.py -p && less save_data/profiling_results

profile-log:
	less save_data/profiling_results

release:
	python3 setup.py sdist

future-test:
	grep "from __future__ import absolute_import, division, print_function, unicode_literals" -L *.py */*.py

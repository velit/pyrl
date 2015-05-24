test-porcelain-output:
	py.test-3 -q -k-slow --tb=line

test:
	py.test-3 -k-slow

all-tests:
	py.test-3

debug:
	python3 -m pdb pyrl.py

test-debug:
	py.test-3 -k-slow -x --pdb

log:
	tail -n 50 save_data/pyrl.log

clean:
	find . -name '*.pyc' -delete
	rm -rf save_data dist
	rm -f MANIFEST errors.err

profile-test:
	py.test-3 tests/profile_test.py && less save_data/profiling_results

profile-in-place:
	./pyrl.py -p && less save_data/profiling_results

profile-log:
	less save_data/profiling_results

future-test:
	grep "from __future__ import absolute_import, division, print_function, unicode_literals" -L *.py */*.py

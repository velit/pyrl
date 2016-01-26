PYTHON = python3
TEST = $(PYTHON) -m pytest

test-porcelain-output:
	$(TEST) -q -k-slow --tb=line

test:
	$(TEST) -k-slow

all-tests:
	$(TEST)

debug:
	$(PYTHON) -m pdb pyrl.py

test-debug:
	$(TEST) -x --pdb

profile-test:
	$(TEST) tests/profile_test.py && less save_data/profiling_results

profile-in-place:
	./pyrl.py -p && less save_data/profiling_results

log:
	tail -n 50 save_data/pyrl.log

profile-log:
	less save_data/profiling_results

future-test:
	grep "from __future__ import absolute_import, division, print_function, unicode_literals" -L *.py */*.py

ctags:
	ctags -R .

clean:
	find . -name '*.pyc' -delete
	rm -rf save_data dist
	rm -f MANIFEST errors.err

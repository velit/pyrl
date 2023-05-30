PYTHON = python3.11
TEST = $(PYTHON) -m pytest

test-porcelain-output:
	$(TEST) -q -k 'not slow' --tb=line

test:
	$(TEST) -k 'not slow'

all-tests:
	$(TEST)

live-test:
	$(TEST) --live

debug:
	$(PYTHON) -m pdb -c continue pyrl.py -o terminal

test-debug:
	$(TEST) -x --pdb

profile-test:
	$(TEST) tests/profile_test.py && less save_data/profiling_results

profile-in-place:
	./pyrl.py -p && less save_data/profiling_results

log:
	tail -n 50 -f save_data/pyrl.log

profile-log:
	less save_data/profiling_results

tags:
	ctags -R .

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -rf save_data dist
	rm -f MANIFEST errors.err

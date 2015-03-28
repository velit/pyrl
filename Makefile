test:
	py.test-3 -k-slow

test-all:
	py.test-3

profile-test:
	python3 -m profile_util.run_profiler
	less data/profiling_results

profile-test-2:
	python2 -m profile_util.run_profiler
	less data/profiling_results

pypy-profile-test:
	pypy -m profile_util.run_profiler
	less data/profiling_results

profile-pyrl:
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

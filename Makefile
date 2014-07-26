test:
	py.test -k-slow

profile-test:
	python -m profile_util.run_profiler
	less data/profiling_results

p3-profile-test:
	python3 -m profile_util.run_profiler
	less data/profiling_results

pypy-profile-test:
	pypy -m profile_util.run_profiler
	less data/profiling_results

profile-pyrl:
	python pyrl.py -p
	less data/profiling_results

debug:
	python -m pdb pyrl.py

clean:
	find . -name '*.pyc' -delete
	rm -f data/errors.err data/profiling_results

release:
	python setup.py sdist

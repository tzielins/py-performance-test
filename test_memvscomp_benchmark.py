import pytest

from memvscomp_benchmark import convolute, convoluteT
from memvscomp_benchmark import ExecutionPlan, makeTasks, clockTasks, doBenchmark, benchmark


def test_convolute_runs():

	datas = [ [1,2,3]]
	patterns = [ [2, 3, 4]]
	memalloc = False

	res = convolute(datas, patterns, memalloc)

	assert res != 0

	memalloc = True
	res = convolute(datas, patterns, memalloc)

	assert res != 0


def test_convoluteT_runs():

        datas = [ [1,2,3]]
        patterns = [ [2, 3, 4]]
        memalloc = False

        res = convoluteT((datas, patterns, memalloc))



def test_executionpplan_inits():

	plan = ExecutionPlan(2, True)
	assert plan.threads == 2
	assert plan.memalloc


def test_makeData():
	plan = ExecutionPlan(2, True)
	data = plan.makeData(3)
	assert len(data)==3
	assert data[0] > 0

def test_makeDatas():
	plan = ExecutionPlan(2, True)
	
	datas = plan.makeDatas(4,3)
	assert len(datas) == 4
	data = datas[3]
	assert len(data) == 3


def test_makeTaks():
	plan = ExecutionPlan(2, True)

	tasks = makeTasks(plan)

	for task in tasks:
		#print(task)
		data, patterns, memalloc = task
		assert patterns == plan.patterns
		assert memalloc == plan.memalloc
		assert len(data) == plan.chunk

	assert len(tasks) == 64*5-1


def test_clockTasks():

	task = ([[1, 2, 3]], [[2, 3, 4]], False)
	res = convoluteT(task)

	tasks = [task]
	threads = 1

	dur, val = clockTasks(tasks, threads)

	assert dur >= 0
	assert dur <= 10
	assert val == res

@pytest.mark.skip(reason="for speeding up")
def test_doBenchmark():
	threadss = [ 1, 4, 8 ]
	memallocs = [ False ]

	times = doBenchmark([16], memallocs, 5, True)

	times = doBenchmark(threadss, memallocs, 5, True)
	
	for r in times:
		print(r)

	assert len(times) ==  2
	#assert len(times) == 1


@pytest.mark.skip(reason="for speeding up")
def test_benchmark():
	benchmark()
	assert False

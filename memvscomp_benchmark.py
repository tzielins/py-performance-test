import math
import random
import numpy
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

class ExecutionPlan:
	def __init__(self, threads, memalloc):
		self.threads = threads
		self.memalloc = memalloc
		self.chunk = 50
		self.length = 100;
		self.patternSize = 50;
		self.dataSize = 64*5*self.chunk

		self.patterns = self.makeDatas(self.patternSize, self.length)
		self.data = self.makeDatas(self.dataSize, self.length)

	def makeDatas(self, size, length):
		datas = []
		for i in range(size):
			datas.append(self.makeData(length))
		return datas

	def makeData(self, length):
		data = []
		for i in range(length):
			data.append(random.random()*100)
		return data

def convolute(datas, patterns, memalloc):
	
	val = 0
	joined = numpy.empty(len(datas[0]), dtype = object)

	for i in range(len(datas[0])):
		joined

	for pattern in patterns:
		for data in datas:
			for i in range(len(data)):
				x = math.cos(data[i])
				y = math.cos(pattern[i])

				val+=x * y
				
				if not memalloc:
					x = math.cos(data[len(data)-1-i])
					y = math.cos(pattern[len(data)-1-i])
					val += x * y

				else:
					row = [x, y]
					if bool(random.getrandbits(1)):
						joined[i] = row
					
						

	for pair in joined:
		if pair is not None:
			val+= pair[0]*pair[1]

	return val

def convoluteT(task):
	data, patterns, memalloc = task
	return convolute(data, patterns, memalloc)


def makeTasks(plan):

	tasks = []
	for ix in range(0, len(plan.data)-plan.chunk, plan.chunk):
		data = plan.data[ix:ix+plan.chunk]
		tasks.append((data, plan.patterns, plan.memalloc))

	return tasks


def clockTasks(tasks, threads):
	sT = time.time()

	val = 0
	with ThreadPoolExecutor(max_workers=threads) as executor:
		results = executor.map(convoluteT, tasks)
	
		for res in results:
			val+=res

	dur = time.time()-sT
	dur = dur

	return (dur, val)

def clockTasksP(tasks, threads):
        sT = time.time()

        val = 0
        with ProcessPoolExecutor(max_workers=threads) as executor:
                results = executor.map(convoluteT, tasks)

                for res in results:
                        val+=res

        dur = time.time()-sT
        dur = dur

        return (dur, val)
	
		

def doBenchmark(threadss, memallocs, iter=1, proc=False):

	times = []
	for threads in threadss:
		for memalloc in memallocs:
			vals=0
			durs = []
			for i in range(iter):
				plan = ExecutionPlan(threads, memalloc)
	
				tasks = makeTasks(plan)
			
				dur = 0
				val = 0

				if proc:
					dur, val = clockTasksP(tasks, threads)
				else:
					dur, val = clockTasks(tasks, threads)

				vals+=val
				durs.append(dur)
				print("Iter "+str(i)+"\tt: "+str(threads)+"\td: "+str(dur))

			dur = round(sum(durs)/len(durs))
			times.append((threads, memalloc, dur, iter, round(vals)))
	return times


def benchmark():

	threadss = [ 1, 4, 8, 16, 32, 64 ]
	memallocs = [ False, True ]

	#times = doBenchmark([16], [True], 5, False)

	#times = doBenchmark(threadss, memallocs, 5, False)

	#print("Threading")

	#for r in times:
	#        print(r)

	times = doBenchmark([16], [True], 5, True)

	times = doBenchmark(threadss, memallocs, 5, True)

	print("Processing")
	for r in times:
                print(r)


benchmark()


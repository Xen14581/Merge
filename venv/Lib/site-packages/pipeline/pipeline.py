#!/usr/bin/python

'''
Copyright 2007, Nathan Coulter, pipeline.py@pooryorick.com

Licensed under the same Same terms as the PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2, taking 'PSF' to mean the copyright holder of this work, and 'Python' to mean this work. See http://www.python.org/download/releases/2.5.1/license/
'''

import io
import os
import signal
import sys
import signal
import subprocess

class PipelineError(RuntimeError):
	pass


class pipelineclass:

	def terminate(self):
		'''
		Like close, but ignores all errors.
		'''
		try:
			self.close()
		except Exception:
			pass

	def close(self):
		'''
		Kills any running pipeline processes.

		Returns the exit status of each process in the pipeline.
		'''
		if hasattr(self,'file'):
			self.file.close()
		try:
			outchan = os.fdopen(self.read)
			outchan.close()
			os.close(self.read)
		except Exception:
			pass
		terminators = (signal.SIGQUIT, signal.SIGABRT , signal.SIGKILL ,signal.SIGTERM)
		processes1 = self.processes[:]
		for terminator in terminators:
			for i in range(len(processes1)):
				process = processes1[i]
				returncode = process.returncode
				if returncode is not None:
					processes1.pop(i)
					break
				process.send_signal(terminator)
				terminated = process.poll()
				if terminated:
					processes1.pop(i)
					break
			if terminated:
				break
		for i in range(len(processes1)):
			process = processes1[i]
			try:
				process.communicate(timeout=0)
			except:
				pass
			process.kill()
			# needed to reaps the pid out of "defunct" state
			process.wait()
		for process in self.processes:
			if process.returncode is None:
				raise PipelineError("could not terminate process")
			if process.returncode != 0:
				raise PipelineError({'msg': 'process status',
					'code': process.returncode,
					'command': process.args}
				)

	def open(self ,*args ,**kwargs):
		self.file = os.fdopen(self.read,*args ,**kwargs)
		return self.file


def pipeline(*cmds):
	'''
	Returns a pipline.

	The first process in the pipeline sys.stdin.  All error streams go to
	sys.stderr.
	'''
	pipeline = pipelineclass()
	pipeline.processes = [] 
	read = sys.stdin.fileno()
	pipes = []
	for cmd in cmds:
		read1, write1 = os.pipe()
		if len(pipes):
			newstdin = pipes[0]
			dupstdin = 1
			pipes.pop()
			newstdout = write1
		else:
			pipewrite = write1
			newstdin = sys.stdin.fileno()
			dupstdin = 0
			read1, write1 = os.pipe()
			newstdout = write1
		pipes.append(read1)

		stdin = os.dup(sys.stdin.fileno())
		stdout = os.dup(sys.stdout.fileno())
		if dupstdin:
			os.dup2(newstdin, 0)
			os.close(newstdin)
		os.dup2(newstdout,1)
		os.close(newstdout)
		process = subprocess.Popen(cmd)
		os.dup2(stdin, 0)
		os.close(stdin)
		os.dup2(stdout, 1)
		pipeline.processes.append(process)
	pipeline.read = read1
	return pipeline

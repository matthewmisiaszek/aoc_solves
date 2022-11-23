import dancer
import multiprocessing
import time


NCORES = 4
CONVERGENCE = 1.1


class MPControl:
    def __init__(self):
        self.keep_popping = True
        self.keep_appending = True
        self.app_limit = None


def proc_fun_wrapper(proc_fun, proc_args, i, batch_size, t_start, pipe):
    result = proc_fun(i, batch_size, *proc_args)
    t_end = time.time()
    t_elapsed = t_end - t_start
    if t_elapsed > 0:
        rate = batch_size / t_elapsed
    else:
        rate = -1
    pipe.send((rate, batch_size, result))


def pool(proc_fun, proc_args, post_fun, post_args, i=0):
    mpc = MPControl()
    batch_size = 1
    rate_history = {}
    mp_pool = multiprocessing.Pool(NCORES)
    pqueue = []
    while mpc.keep_popping:
        while (mpc.keep_appending and (mpc.app_limit is None or i <= mpc.app_limit)) and len(pqueue) < NCORES:
            pipe_a, pipe_b = multiprocessing.Pipe()
            mp_pool.apply_async(proc_fun_wrapper, (proc_fun, proc_args, i, batch_size, time.time(), pipe_b))
            pqueue.append(pipe_a)
            i += batch_size
        if not pqueue:
            break
        pipe_a = pqueue.pop(0)
        rate, proc_batch_size, result = pipe_a.recv()
        post_fun(mpc, result, *post_args)
        if proc_batch_size not in rate_history or rate / rate_history[proc_batch_size] > CONVERGENCE:
            batch_size = proc_batch_size * 2
            rate_history[batch_size] = rate
    mp_pool.close()

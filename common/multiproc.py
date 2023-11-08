import dancer
import multiprocessing
import time


NCORES = multiprocessing.cpu_count()
CONVERGENCE = 1.1
TIMEOUT = 10


class MPControl:
    def __init__(self):
        self.keep_popping = True
        self.keep_appending = True
        self.app_limit = None


def proc_fun_wrapper(proc_fun, proc_args, i, batch_size, t_start):
    result = proc_fun(i, batch_size, *proc_args)
    t_end = time.time()
    t_elapsed = t_end - t_start
    return t_elapsed, result


def pool(proc_fun, proc_args, post_fun, post_args, i=0):
    mpc = MPControl()
    batch_size = 1
    rate_history = {}
    mp_pool = multiprocessing.Pool(NCORES)
    pqueue = []
    maxt=0
    while mpc.keep_popping:
        while (mpc.keep_appending and (mpc.app_limit is None or i <= mpc.app_limit)) and len(pqueue) < NCORES:
            proc = mp_pool.apply_async(proc_fun_wrapper, (proc_fun, proc_args, i, batch_size, time.time()))
            pqueue.append((proc, i, batch_size))
            i += batch_size
        if not pqueue:
            break
        proc, proc_i, proc_batch_size = pqueue.pop(0)
        try:
            pget = proc.get(timeout=TIMEOUT)
        except:
            # print('fail')
            pget = proc_fun_wrapper(proc_fun, proc_args, proc_i, proc_batch_size, time.time())
        t_elapsed, result = pget
        maxt = max(maxt, t_elapsed)
        if maxt < TIMEOUT * 0.3:
            if t_elapsed == 0:
                t_elapsed = -1
            rate = proc_batch_size / t_elapsed
            if proc_batch_size not in rate_history or rate / rate_history[proc_batch_size] > CONVERGENCE:
                batch_size = proc_batch_size * 2
                rate_history[batch_size] = rate
            # else:
                # print('converged')
        # else:
            # print(maxt)
        post_fun(mpc, result, *post_args)
    mp_pool.close()

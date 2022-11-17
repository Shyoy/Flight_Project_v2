import multiprocessing as mp
import threading
import time
from concurrent.futures import ProcessPoolExecutor as P_Pool
from concurrent.futures import ThreadPoolExecutor as T_Pool
import math



def do_staff(seconds):
    # print(f'sleeping for {seconds} seconds')
    time.sleep(seconds)
    return f'Done sleeping: {seconds}'


if __name__ == '__main__':

    secs = [1]*100
    
    start = time.perf_counter()
    with P_Pool() as p_pool:
        results = p_pool.map(do_staff, secs)

        # for f in results:
        #     print(f)

    finish = time.perf_counter()


    print(f"Processes  finished in {round(finish-start,2)} seconds")
    start = time.perf_counter()

    threads= []
    # with T_Pool() as t_pool:

    #     for sec in secs:
    #         results = t_pool.submit(do_staff, sec)



    for sec in secs:
        t = threading.Thread(target=do_staff, args=(sec,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join() 

    finish = time.perf_counter()

    print(f"Threads  finished in {round(finish-start,2)} seconds")

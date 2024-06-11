import os
import time
import ray

# Normal Python
def fibonacci_local(sequence_size):
    fibonacci = []
    for i in range(0, sequence_size):
        if i < 2:
            fibonacci.append(i)
            continue
        fibonacci.append(fibonacci[i-1]+fibonacci[i-2])
    return sequence_size



# Ray task
@ray.remote
def fibonacci_distributed(sequence_size):
    fibonacci = []
    for i in range(0, sequence_size):
        if i < 2:
            fibonacci.append(i)
            continue
        fibonacci.append(fibonacci[i-1]+fibonacci[i-2])
    return sequence_size


# Normal Python
def run_local(sequence_size):
    start_time = time.time()
    results = [fibonacci_local(sequence_size) for _ in range(os.cpu_count())]
    duration = time.time() - start_time
    print('Sequence size: {}, Local execution time: {}'.format(sequence_size, duration))

# Ray
def run_remote(sequence_size):
    # starts all of the relevant Ray processes. By default, Ray creates one worker process per CPU core
    # If you would want to run Ray on a cluster, you would need to pass in a cluster address with something like ray.init(address= 'InsertAddressHere')
    ray.init()
    start_time = time.time()
    # .get() return value when all tasks have completed
    results = ray.get([fibonacci_distributed.remote(sequence_size) for _ in range(os.cpu_count())])
    duration = time.time() - start_time
    print('Sequence size: {}, Remote execution time: {}'.format(sequence_size, duration))  
    # NOTE: when the process calling ray.init() terminates, the Ray runtime will also terminate. 
    # explicitly shut down the Ray runtime by calling ray.shutdown() - if running 2nd time, it will throw an error
    ray.shutdown()


run_local(100000)
run_remote(100000)




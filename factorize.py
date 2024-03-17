from multiprocessing import Process
from time import time
import concurrent.futures


def factorize(*numbers):
    result_list = []
    for number in numbers:
        factor_list = []
        for num in range(1, number + 1):
            if number % num == 0:
                factor_list.append(num)
        result_list.append(factor_list)
        print(factor_list)

    return result_list


def factorize_multiproc(numbers):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(factorize, numbers))

    return results


if __name__ == '__main__':
    numbers = (123684974, 568974235, 23587469, 106510609)
    processes = []
    time_before = time()
    for number in numbers:
        pr = Process(target=factorize, args=(number, ))
        pr.start()
        processes.append(pr)

    [pr.join() for pr in processes]
    print(f'Parallel execution time: {time() - time_before: 0.3}!!!')


    time_before = time()
    factorize_multiproc(numbers)
    print(f'Parallel execution time: {time() - time_before: 0.3}!!!')


    time_before = time()
    for num in numbers:
        factorize(num)
    print(f'Synchro execution time: {time() - time_before: 0.3}!!!')



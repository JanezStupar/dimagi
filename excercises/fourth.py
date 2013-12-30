__author__ = 'Janez Stupar'
import itertools
import timeit

a = [[1, 8, 2], [44, 75, 3], [11, 33, 44, 543, 33], [43543, 32, 547, 65, 63, 132]]


def product_builtin(lists):
    """
    This is what comes with Python and what I would have used normally.
    """
    return list(itertools.product(*lists))


def product_iterative(lists):
    """
    This is a simple iterative solution that I came up with.
    """
    results = [()]
    for subset in lists:
        temp = []
        for partial in results:
            for element in subset:
                temp.append(partial + (element,))
        results = temp

    return results


def product_iterative_generator(lists):
    """
    I created this approach as a modification of previous iterative version.
    I wanted to see how a generator approach could be implemented.
    """
    lists_len = len(lists)
    results = [()]
    for subset in lists:
        temp = []
        for partial in results:
            partial_len = len(partial) + 1
            for element in subset:
                if partial_len == lists_len:
                    yield partial + (element,)
                else:
                    temp.append(partial + (element,))
        results = temp


def product_recursive(lists):
    """
    This is a simple recursive implementation that was derived from product_recursive_generator
    """
    if not lists:
        return [()]

    retval = []
    for items in product_recursive(lists[:-1]):
        for item in lists[-1]:
            retval.append(items + (item,))
    return retval


def product_recursive_generator(lists):
    """
    This is what I came up after I found out the product_recursive_generator_comprehension solution.

    Seeking to understand better how it works I have refactored it into a straight generator form, without comprehensions.
    """
    if not lists:
        yield ()
    for items in product_recursive_generator(lists[:-1]):
        if len(lists) == 0:
            break
        for item in lists[-1]:
            yield items + (item,)


def product_recursive_generator_comprehension(lists):
    """
    I picked up this implementation somewhere while exploring the whole problem started intriguing me.

    This is a generator approach.
    """
    if not lists:
        return iter(((),))
    return (items + (item,)
            for items in product_recursive_generator_comprehension(lists[:-1])
            for item in lists[-1])


def run_benchmark(func, lists, generator=False):
    if generator:
        return list(func(lists))
    else:
        return func(lists)

if __name__ == "__main__":
    t = timeit.Timer(stmt="fourth.run_benchmark(fourth.product_builtin, fourth.a)", setup="import fourth")
    print "Product builtin, time: %s  \n" % t.timeit(5)

    t = timeit.Timer(stmt="fourth.run_benchmark(fourth.product_iterative, fourth.a)", setup="import fourth")
    print "Product iterative, time: %s  \n" % t.timeit(5)

    t = timeit.Timer(stmt="fourth.run_benchmark(fourth.product_iterative_generator, fourth.a, True)", setup="import fourth")
    print "Product iterative generator, time: %s  \n" % t.timeit(5)

    t = timeit.Timer(stmt="fourth.run_benchmark(fourth.product_recursive, fourth.a)", setup="import fourth")
    print "Product recursive, time: %s  \n" % t.timeit(5)

    t = timeit.Timer(stmt="fourth.run_benchmark(fourth.product_recursive_generator, fourth.a, True)", setup="import fourth")
    print "Product recursive generator, time: %s  \n" % t.timeit(5)

    t = timeit.Timer(stmt="fourth.run_benchmark(fourth.product_recursive_generator_comprehension, fourth.a, True)", setup="import fourth")
    print "Product recursive generator comprehension, time: %s  \n" % t.timeit(5)


'''Itertools backport'''
from typing import Iterator, List, TypeVar, Iterable, Callable

T = TypeVar("T")

def take(iterable: Iterator[T], n: int) -> List[T] | None:
    res = []
    try:
        for _ in range(n):
            res.append(next(iterable))
    except StopIteration as _:
        if len(res) == 0:
            return None
        

    return res

def batched(iterable: Iterable[T], n: int, pad_with: Callable[[], T] | None = None):
    '''Similar to itertools.batched. For iterables whose lengths are not multiples of n, pad_with will be called to fill the last batch'''
    it = iter(iterable)
    while True:
        res = take(it, n)
        if res is None:
            return
        if len(res) != n and pad_with is not None:
            for _ in range(n-len(res)):
                res.append(pad_with())
        yield res

if __name__ == "__main__":
    print(list(batched([1,2,3,4,5,6], 3, lambda: 42)))
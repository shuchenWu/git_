# using metaclass, __new__ method, decorator implementing Singleton


# using metaclass
class SingletonMeta(type):
    _instance = None

    def __call__(self):
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Yisin1(metaclass=SingletonMeta):
    """There's only one Yisin1"""


# using __new__
class Yisin2:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


# using decorator
def singleton(klass):
    instance = None

    def wrapper(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = klass(*args, **kwargs)
        return instance
    return wrapper


@singleton
class Yisin3:
    """one and only"""


if __name__ == '__main__':
    print(Yisin1() is Yisin1())
    print(Yisin2() is Yisin2())
    print(Yisin3() is Yisin3())

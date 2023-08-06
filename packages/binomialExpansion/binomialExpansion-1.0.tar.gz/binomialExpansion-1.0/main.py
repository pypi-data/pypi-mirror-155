import ctypes
import os


lib_path = os.path.join(os.path.dirname(__file__), 'binomialExpansion.dll')
inter = ctypes.cdll.LoadLibrary(lib_path)
inter.binomial_expansion.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int)
inter.binomial_expansion.restype = ctypes.c_int


def newton(a, b, n):
    result = inter.binomial_expansion(ctypes.c_int(a), ctypes.c_int(b), ctypes.c_int(n))
    print(result)
    return result



if __name__ == '__main__':
    newton(3, 2, 2)


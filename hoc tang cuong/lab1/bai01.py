"""
Bai 01. Kiem tra moi truong Python.
In ra phien ban Python, Gymnasium, NumPy ma KHONG nhap thu cong so phien ban.
"""

import sys
import gymnasium
import numpy


def main():
    print("Python version:", sys.version.split()[0])
    print("Gymnasium version:", gymnasium.__version__)
    print("NumPy version:", numpy.__version__)


if __name__ == "__main__":
    main()

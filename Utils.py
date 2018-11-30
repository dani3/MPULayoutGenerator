import os
from Constants import *


def format_size(size):
    formatted = str("%x" % size).upper()
    if len(formatted) < 2:
        formatted = "0" + formatted

    return formatted


def generate_powers_array():
    temp = []

    for i in range(MIN_POWER, MAX_POWER + 1):
        temp.append(1 << (i + 1))

    return temp


def delete_and_rename_file():
    # The generated temp file has the new and correct MPU configuration
    #if os.path.isfile('..\Source\HAL\ST31_MPU_temp.c'):
    if os.path.isfile('ST31_MPU_temp.c'):
        try:
            # This generated file can't be read protected.
            os.remove("..\Source\HAL\ST31_MPU.c")
            os.rename('..\Source\HAL\ST31_MPU_temp.c', '..\Source\HAL\ST31_MPU.c')

        except OSError:
            os.rename('..\Source\HAL\ST31_MPU_temp.c', '..\Source\HAL\ST31_MPU.c')

        finally:
            return True

    else:
        print("Error: This tool didn't generate the new MPU configs in ST31_MPU_temp.c")

        return False

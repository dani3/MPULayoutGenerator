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
    if os.path.isfile('..\Source\HAL\ST31_MPU_temp.c'):
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


def calculate_region_without_subregions(code_remaining, powers_array):
    # Look for the biggest power of two that fits inside the code
    for ii in range(len(powers_array)):
        if powers_array[ii] > code_remaining:
            # We've surpassed the code, decrease it by one
            ii -= 1

            # Just some formatting
            region_size = format_size(MIN_POWER + ii)

            return powers_array[ii], region_size


def calculate_region_with_subregions(code_remaining, powers_array):
    # Look for the biggest power of two that just surpasses the code size
    for ii in range(len(powers_array)):
        if powers_array[ii] > code_remaining:
            # Calculate the subregion size
            subregion_size = powers_array[ii] / 8

            # Enable all the regions
            subregions = 0xFF

            for i in range(1, MPU_NO_SUBREGIONS + 1):
                subregions = subregions >> 1

                # Subtract the previous regions plus the next one
                if powers_array[ii] - (subregion_size * i) <= code_remaining:
                    code_protected = powers_array[ii] - (subregion_size * i)

                    # Just some formatting
                    region_size = format_size(MIN_POWER + ii)
                    subregions = format_size(subregions)

                    return code_protected, region_size, subregions


# TimeProbe

TimeProbe is a WCET analysis tool. It performs measurement-based probabilistic timing analysis (MBPTA) using extreme value theory (EVT). During application of EVT, it uses the block maxima method (hence generalized extreme value distribution) and the method of l-moments.

The program takes the execution time values of the analyzed program as a numpy array and an integer bound value whose exceedance probability will be calculated.
Providing execution times is compulsory. Providing bloksize and the boundary value is optional. 

TimeProbe performs four primary operations regarding WCET analysis.

- Fits a generalized extreme value (GEV) distribution to the execution times.

- Calculates and plots CDF and 1-CDF using the fitted GEV distribution.

- Applies the Q-Q plot method to determine the success of the fitted GEV distribution, and plots the results for visual inspection. 

- Calculates the exceedance probability of the given boundary value and prints the result on the command line.


TimeProbe takes three command line arguments:

- File name: The name of file that stores execution times. This is a positional argument and it is mandatory. This file should be provided as a csv file. A sample csv file is provided in this repository namely execution_times.csv.

- Block size (bsize): The block size as an integer value. This argument is optional. However, the block maxima method should have a block size value; and if it is not provided the default block size value which is 10 is applied.

- Boundary value (bval): The value of whose exceedance probability will be calculated. This argument is optional. If it is not provided an exceedance value will not be calculated.

## Usage

### Usage syntax

`python3 time_probe.py file_name -bsize block_size -bval boundary_value`

### Usage examples

`python3 time_probe.py execution_times.csv -bsize 20 -bval 93`

`python3 time_probe.py execution_times.csv -bsize 20`

`python3 time_probe.py execution_times.csv -bval 93`

`python3 time_probe.py execution_times.csv`


## Requirements

TimeProbe is developed using Python 3.13. It requires numpy packaage for array operations, lmoments3 package for EVT operations, and mathplotlib package for plotting operations.
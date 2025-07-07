"""TimeProbe

TimeProbe is a WCET analysis tool. It performs measurement-based probabilistic 
timing analysis (MBPTA) using extreme value theory (EVT). During application of EVT,
TimeProbe uses the block maxima method (hence generalized extreme value 
distribution) and the method of l-moments.

The program takes the execution time values of the analyzed program as a numpy 
array and an integer bound value whose exceedance probability will be calculated.
Providing execution times is compulsory. Providing bloksize and the boundary 
value is optional. 

The program performs four primary operations regarding WCET analysis.

First, it fits a generalized extreme value (GEV) distribution to the
execution times. The "fitted_gev" variable represents the probability 
distribution of the WCETs of the program. Then any probability calculation 
can be performed using the fitted_gev distribution.

Second, it calculates and plots CDF and 1-CDF using the fitted 
GEV distribution.

Third, it applies the Q-Q plot method to determine the success of 
the fitted GEV distribution, and plots the results for visual inspection. 

Fourth, it calculates the exceedance probability of the given boundary
value and prints the result on the command line.

Currently, TimeProbe uses 10 as the default block size. In block maxima method,
the number provided execution time values must be the multiple of the block 
size.

As stated above, TimeProbe uses the block maxima method. Block size is an 
essential parameter of this WCET approach. Choosing a proper value is of 
critical importance to WCET calculation. In addition, the number of execution 
times should be the multiple of block size. The default block size is 10. 
However, the user can set custom block size value.


Usage           : python3 time_probe.py file_name -bsize block_size -bval boundary_value
Example usage   : python3 time_probe.py execution_times.csv -bsize 20 -bval 93
Example usage   : python3 time_probe.py execution_times.csv -bsize 20
Example usage   : python3 time_probe.py execution_times.csv -bval 93
Example usage   : python3 time_probe.py execution_times.csv
"""


# Array operations
import numpy as np

# EVT operations
import lmoments3 as lm
from lmoments3 import distr

# Plotting operations
import matplotlib.pyplot as plt 

# CSV file operations
import csv

# Command line options, arguments and sub-commands parsing operations
import argparse


# Global configuration variables. TimeProbe has three configuration variables.
# File name of the input csv file, block size, and boundary value.
# File name is compulsory, the default value is block size is 10, and the
# boundary value is optional.
file_name: str = None
block_size: int = 10
boundary_value: int = None



def read_data_file() -> np.array:
    """Read the csv data file

    This function reads the csv data file. The data file includes execution
    times of the real-time program. The execution times are then rounded and 
    stored into an array. The array is returned from this function.

    The data file should include the execution times in a single row,
    separated by commas. An example of a csv file can be found in the current
    directory named execution_times.csv.


    Returns
    -------
    e_time : np.array
        e_time is a floating point np.array. The array stores the
        execution times.
    """

    # Floating point array of execution times.
    e_time = np.array

    # Open and read the csv file. Copy the contents of the file to my_array.
    with open(file_name, 'r', encoding='UTF8') as data_file:
        reader = csv.reader(data_file)
        for row in reader:
            my_array = np.asarray(row)

    # Convert my_array to a floating point array.
    my_array_1 = my_array.astype(np.float64)

    # Round the values of the array and put them in a new array.
    e_time = np.around(my_array_1, decimals=2)

    # Return the rounded execution times.
    return e_time



def calc_wcet(e_time: np.array) -> None:
    """Calculate the WCET

    This function calculates the WCET of the real-time program using extreme 
    value theory (EVT). During the EVT application, it uses the block maxima 
    method (hence generalized extreme value distribution) and the method of 
    l-moments.

    It takes the execution time values of the analyzed program as a numpy array
    and an integer bound value whose exceedance probability will be calculated.
    Providing execution times is compulsory, and the boundary value is optional. 
 
    This function performs four primary operations regarding WCET analysis.

    First, it fits a generalized extreme value (GEV) distribution to the
    execution times. The "fitted_gev" variable represents the probability 
    distribution of the WCETs of the program. Then any probability calculation 
    can be performed using the fitted_gev distribution.
 
    Second, it calculates and plots CDF and 1-CDF using the fitted 
    GEV distribution.
 
    Third, it applies the Q-Q plot method to determine the success of 
    the fitted GEV distribution, and plots the results for visual inspection. 

    Fourth, it calculates the exceedance probability of the given boundary
    value and prints the result on the command line.
    
    Parameters
    ----------
    e_time : np.array
        e_time is a floating point np.array. It includes the execution times.

    Returns
    -------
    None
    """


    # We will divide the execution times into blocks and pick the maximum value
    # (block maxima) of each block. Therefore, we need an array to store the 
    # maximum values.
    block_count: int = len(e_time) // block_size
    e_time_max: np.array = np.zeros(block_count)


    # Divide execution time array into blocks and get the maximum 
    # value of each block. Store the maximum values in e_time_max array.
    # After storing sort the array. Sorted array is needed for EVT application.
    index = 0
    for x in range(0, len(e_time), block_size):
        e_time_max[index] = np.max(e_time[x : x + 10])
        index = index + 1
    
    np.sort(e_time_max)


    # Fit a generalized extreme value (GEV) distribution to the maximum values 
    # of blocks.
    # In block maxima method we fit a GEV distribtuion. During the fit operation
    # we use method of l-moments (MoLM). Fit operation is performed by the
    # help of the lmoments3 package.
    params = distr.gev.lmom_fit(e_time_max)
    fitted_gev = distr.gev(**params)


    # Calculate and plot CDF and 1-CDF.
    # This is for demonstration and test purposes.
    max_value: int = np.ceil(np.max(e_time))
    plot_array: np.array = np.arange(1, max_value + 1, 1)
    e_time_cdf = fitted_gev.cdf(plot_array)
    e_time_1_cdf = 1 - fitted_gev.cdf(plot_array)

    plt.figure(num="TimeProbe")
    plt.plot(plot_array, e_time_cdf)
    plt.title("CDF of the Fitted GEV")
    plt.xlabel("Values")
    plt.ylabel("Probability")
    plt.show()

    plt.figure(num="TimeProbe")
    plt.plot(plot_array, e_time_1_cdf)
    plt.title("1-CDF of the Fitted GEV")
    plt.xlabel("Values")
    plt.ylabel("Probability")
    plt.show()


    # Apply q-q plot method to determine the sucess of the fitted GEV.
    # Create PPF.
    percentile = np.arange(1 / block_count, 1.01, 1 / block_count)
    e_time_ppf = fitted_gev.ppf(percentile)
    
    # If there is an infinite value change it to 1
    e_time_ppf = np.where(np.isinf(e_time_ppf), 1, e_time_ppf)


    # Stack the PPF and maximum values to see whether the PPF creation is 
    # sucessful. This is for testing purposes.
    # my_stack = np.vstack((e_time_ppf, e_time_max)).T
    # print(my_stack)


    # Draw q-q plot.

    # Create data pairs of PPF and max values. Then draw pairs as plus signs.
    # X axis represents PPF and Y axis respresents maximum values.
    plt.figure(num="TimeProbe")
    plt.plot(e_time_ppf, e_time_max, marker='+', linestyle='')

    # Draw 45 degree line to help visually checking the validity of points.
    ppf_min_val = np.min(e_time_ppf)
    ppf_max_val = np.max(e_time_ppf)
    plt.axline([ppf_min_val, ppf_min_val], [ppf_max_val, ppf_max_val], color='r')
    plt.title("Q-Q Plot of the Fitted GEV")
    plt.xlabel("PPF")
    plt.ylabel("Maximum Values")
    plt.show()


    # Calculate the probability of exceeding a boundary value. The value is
    # provided by the user using -bval option. If it is not None, perform the
    # calculation.
    # P(X >= x) = 1 - F(x)
    if boundary_value != None:
        exceedence_probability = 1 - fitted_gev.cdf(boundary_value)
        print(f"The probability of exceeding {boundary_value} is", 
              exceedence_probability)



def parse_arguments() -> None:
    """Parse arguments
    
    This function creates a parser and then parses the command line arguments 
    and options and sets theglobal configuration values.


    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the command line arguments and options are not valid.
    """

    global file_name
    global block_size
    global boundary_value


    # Create a parser to parse command line options and arguments. Parser takes
    # three arguments. The first one is a positional argument which is the input 
    # csv file name that includes execution times of the analyzed program. The 
    # second one is an optional argument which is the block size. If it is not 
    # provided the default block size value is used. The third one is an
    # optional argument which is the boundary value whose exceedence probability 
    # will be calculated. If it is not provided a particular exceedence
    # probability is not calculated.
    parser = argparse.ArgumentParser(
        prog='TimeProbe',
        description='WCET Analysis Tool')
    parser.add_argument('file_name', type=str,
                    help='Input csv file name that includes execution times.')
    parser.add_argument('-bsize', type=int,
                    help='The block size that is used in the block maxima '
                         'method. The block size value must be a positive '
                         'integer.')
    parser.add_argument('-bval', type=int,
                    help='The boundary value whose exceeding probability will '
                         'be calculated. The boundary value must be a positive '
                         'integer.')
    args = parser.parse_args()


    # Set the file name value.
    # First check the validity of user entered the file name value. If it is a 
    # valid value set it. Otherwise raise exception. Providing a valid file
    # name is compulsory.
    if args.file_name == None or isinstance(args.file_name, str) == False:
        raise ValueError("Please enter a valid file name for input csv file.")
    else:        
        file_name = args.file_name
    print(f"File Name = {file_name}")


    # Set the block size value.
    # First check the validity of user entered the block size value. If it is a 
    # valid value set it. Otherwise raise exception. If the value is not 
    # provided don't set it and use the default one. The default value of the 
    # block size is set globally.
    if args.bsize != None:
        if isinstance(args.bsize, int) == False or args.bsize <= 0:
            raise ValueError("Please enter a valid positive integer value for "
                             "block size or don't provide a value. If a value "
                             "is not the program uses default value.")
        else:
            block_size = args.bsize
    print(f"Block Size = {block_size}")


    
    # Set the boundary value.
    # First check the validity of user entered the boundary value. If it is a 
    # valid value set it. If it is not valid raise error. If the value is not
    # provided don't set it. Setting this value is optional.
    if args.bval != None:
        if isinstance(args.bval, int) == False or args.bval <= 0:
            raise ValueError("Please enter a valid positive integer value for "
                             "boundary value or don't provide a value. Setting "
                             "this value is optional.")
        else:
            boundary_value = args.bval    
    print(f"Boundary Value = {boundary_value}")



def main() -> None:
    """Main function

    Returns
    -------
    None
    """

    parse_arguments()


    # Array of execution times of the real-time program.
    # The type of the array is floating point.
    e_time = np.array

    # Read the execution times from e_time.csv file and and store them in
    # e_time array.
    e_time = read_data_file()


    # Perform WCET analysis on the data. After performing the analysis, 
    # the "fitted_gev" variable represents the probability distribution of the 
    # WCETs of the program. Then any proability calculation can be performed
    # using fitted_gev distribution.
    calc_wcet(e_time)




if __name__=="__main__":
    """Entry point

    Returns
    -------
    None
    """

    main()

"""Generate Sample Data for TimeProbe

This program generates sample data for testing TimeProbe, a WCET analyzer.
The program generates 1000 sample execution times using a uniform distribution. 
The times are between 1 and 100 and they are in floating point number format. 
Generated values are saved in e_time.csv file in the current working directory.
The program also includes an option to create samples using a gumbel 
distribution.

"""


import numpy as np
import csv

def main() -> None:
    """Main function

    Parameters
    ----------
    param1 : --
        Description


    Returns
    -------
    param1 : --
        Description
    """


    # Draw 1000 samples from uniform distribution.
    e_time_array = np.random.default_rng().uniform(1, 100, 1000)

    # Draw 1000 samples from a gumbel distribution.
    # rng = np.random.default_rng()
    # mu, beta = 2.0, 1.0 # location and scale
    # e_time_array = rng.gumbel(mu, beta, 1000)    

    # Save the values to the e_time.csv file.
    with open('./execution_times.csv', 'w', encoding='UTF8') as data_file:
        writer = csv.writer(data_file)
        writer.writerow(e_time_array)


    # This is for testing purposes.
    # Read the values of the e_time.csv and print.
    with open('./execution_times.csv', 'r', encoding='UTF8') as data_file:
        reader = csv.reader(data_file)
        for row in reader:
            print(row)
            my_array = np.asarray(row)

    print(my_array)

    my_array1 = my_array.astype(np.float64)
    e_time = np.around(my_array1, decimals=2)
    print(e_time)




if __name__=="__main__":
    """Entry point
    """
    main()
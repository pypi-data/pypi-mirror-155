import math
import numpy as np
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Binomial(Distribution):

    """ Binomial distribution class for calculating and 
    visualizing a Binomial distribution.

    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) the total number of trials

    """

    def __init__(self, prob=.5, size=20): 

        self.n = size
        self.p = prob
        
        Distribution.__init__(self, mu = self.calculate_mean(), sigma=self.calculate_stdev()) 

    def calculate_mean(self):
        """Method to calculate the mean of the data set.
        Args: 
            None
        
        Returns: 
            float: mean of the data set
        """
        mu = self.p * self.n
        self.mean = mu

        return mu

    def calculate_stdev(self):

        """Method to calculate the standard deviation of the data set.
        
        Args: 
            sample (bool): whether the data represents a sample or population
        
        Returns: 
            float: standard deviation of the data set
    
        """
        sigma = np.sqrt(self.n * self.p * (1 - self.p))
        self.stdev = sigma

        return sigma

    def replace_stats_with_data(self):
    
        """Function to calculate p and n from the data set
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """   
        self.n = len(self.data)
        self.p = np.mean(self.data)
        self.calculate_mean()
        self.calculate_stdev()

        return self.p, self.n


    def plot_bar(self):
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        Args:
            None
        Returns:
            None
        """

        plt.hist(self.data, bins=2)
        plt.title('Histogram of Data')
        plt.title(f'Binomial distribution`s histogram: n = {self.n}; p = {self.p}')
        plt.xlabel('data')
        plt.ylabel('count')     


    def plot_bar_pdf(self):
        """
        Method to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
        """
       
        x = []
        y = []
        
        # calculate the x values to visualize
        for i in range(self.n):
            k=i+1
            x.append(k)
            y.append(self.pdf(self, k))

        # make the plots
        fig, axes = plt.subplots(2,sharex=True)
        fig.subplots_adjust(hspace=.5)
        axes[0].hist(self.data, density=True)
        axes[0].set_title('Normed Histogram of Data')
        axes[0].set_ylabel('Density')

        axes[1].plot(x, y)
        axes[1].set_title('Normal Distribution for \n Sample Mean and Sample Standard Deviation')
        axes[0].set_ylabel('Density')
        plt.show()

        return x, y

    def pdf(self, k):
        """Probability density function calculator for the Binomial distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """
        tests = np.random.choice([1,0], size=[int(1e7),self.n], p=[self.p, (1-self.p)])
        # sums of all tests
        test_sums = tests.sum(axis=1)
        # proportion of tests that produced exactly one head
        prob = (test_sums == k).mean()
        
        return prob

    def __add__(self, other):
        
        """Magic method to add together two Binomial distributions
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise

        p = self.p
        n = self.n + other.n

        result = Binomial(prob=p, size=n)
       
        return result

    def __repr__(self):
    
        """Magic method to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Binomial
        
        """
        return f"mean {self.mean}, standard deviation {self.stdev}, p {self.p}, n {self.n}"

    # def read_data_file(self, file_name):
    #     """Function to read in data from a txt file. The txt file should have one number (float) per line. The numbers are stored in the data attribute. After reading the file, the mean and standard deviation are calculated
    #     Args:
    #         file_name (string): name of a file to read from
    #     Returns:
    #         None
    #     """
    #     Distribution.read_data_file(self, file_name)

    #     p,n = self.replace_stats_with_data()

    #     self.__init__(p,n)
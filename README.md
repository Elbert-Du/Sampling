# Sampling
The code here is used for generating a small, representative sample of the entire population space assuming you have the population pdf.

The problem of creating a small, representative sample is a problem with many practical applications. It is very difficult to analyze large datasets, so we can only analyze a smaller sample. However, when a sample is significantly smaller than the original data set, we lose a significant portion of information about the original population. As such, we need to create an efficient way to take small samples that are very representative of the original data set.

The easiest way to generate the population and sample distributions for this algorithm is to bin the data, and then the values of the pdfs is simply the proportion of the values in each bin. A more complicated, but probably more accurate method to generate the pdfs is to use kernel density estimations. You could also generate the pdfs through parametric methods such as assuming the distribution is gaussian and computing the mean and variance. Be careful though, when you generate the pdf using different methods, you may also want to change which distance metric you're using.


Moving on to the code:
sampling_knapsack.py contains the code for the Kolmogorov-Smirnov version of the code run on 1-d data. Because Kolmogorov-Smirnov does not scale up to multidimensional data well, this code is only useful for the 1-d case.

sampling_knapsack.ipynb contains the code for the single dimensional case so one can see how it was built into the multidimensional case. It also contains more metrics for the distance to show that the distance metrics are interchangable: it is just that some work better than others depending on the data and how it was represented.

Finally, the pdf file contains pseudocode for the functions since that is easier to read and understand than the python code.

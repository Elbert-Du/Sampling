"""
Helper functions
This is a function that takes values from the CDF and computes the maximum deviation from the target distribution.
This is the Kolmogorov-Smirnov test statistic
"""
def closeness(distribution, overallCDF):
    deviation = 0
    maxDeviation = 0
    normFactor = distribution[numJumps-1]
    for i, value in enumerate(distribution):
        if abs(value/normFactor - overallCDF[i]) > maxDeviation:
            maxDeviation = abs(value/normFactor - overallCDF[i])
    return maxDeviation

#This computes the 2-sided p value of the Kolmogorov-Smirnov test statistic. i doesn't have to be as large as 1000 since it converges
#quickly most of the time.
def compute_p_value(deviation):
    if deviation == 0:
        return 1
    else:
        infSum = 0
        for i in range(1,1000):
            infSum += math.exp(-(2*i-1)**2*math.pi**2/(8*deviation**2))
        return 1-math.sqrt(2*math.pi)/deviation*infSum

#This function calculates the overall CDF when you give it a bunch of cdfs.
#It assumes the functions are normalized. It is a combined cdf representing the cdf of the entire population.
def CDF(x):
    value = 0
    for func in p:
        value += func(x)
    return value/n

#This is the global variable representing the overall CDF that is used in the main function to calculate the distance between the current
#CDF and the overall CDF.
discreteCDF = np.zeros((numJumps,))
for i in range(numJumps):
    discreteCDF[i] = CDF(i*jumpSize+domain[0])
    
    
"""
Main function:
This is extremely good for large data sets because it can run fast, and will produce results that are far better than a
simple random sample as long as the parameters are adjusted correctly.
Furthermore, if you adjust the parameters correctly (using trial and error), you will be able to produce a sample with a distribution
nearly identical to that of the population.
To adjust the parameters, it's better to have a large significance level as then you will accept more objects and the code will terminate
more quickly.

Inputs:
w is a vector of the weights for each of the cdfs. Normally this would correspond to the number of objects that constitute this cdf.
n is the number of cdfs
p is a vector of cdf: this is currently written for them to be functions, but it can easily be modified so that it corresponds to the
value of the cdf at discrete intervals or the sample elements (using the scipy kstest implementation)
maxWeight is the maximum weight that you can have in your sample.

Note that each object we are considering right now is a collection of elements rather than a single element. They don't have to be grouped
intelligently, although groupings that create a larger variety of cdfs tend to work better.

"""
sampleProportion = 0.5 #Customize this to choose the size of the random sample that we add onto
significanceLevel = 0.9999 #Customize this to choose how much each object must improve our sample by in order to be added.

def choose_sample(w, n, p, maxWeight):
    totalWeight = 0
    currentCDF = np.zeros((numJumps,))
    contents = dict()
    #first, we take a simple random sample that has weight at most maxWeight*sampleProportion. It should be somewhat similar to the
    #population density. We will then build on this to improve the sample for our final distribution.
    while True:
        i = np.random.randint(0,n)
        if i not in contents:
            if totalWeight + w[i] > maxWeight*sampleProportion:
                break
            else:
                contents[i] = 1
                totalWeight += w[i]
                for j in range(numJumps):
                    currentCDF[j] += w[i]*(p[i](jumpSize*j+domain[0]))
    #Now, we add objects to this sample to try to correct it and make it closer to the population density
    #Here, we add 1 object at a time. This time, we just take anything that decreases the deviation by a significant amount, defined by
    #significanceLevel. This causes the algorithm to go much faster than anything that does a lot of comparisons.
    currentDeviation = closeness(currentCDF, discreteCDF)
    pairAdded = True
    numIts=0
    while pairAdded:
        counter = 0
        for i, weight in enumerate(w):
            if i not in contents and totalWeight+w[i] <= maxWeight:
                tempCDF = copy.deepcopy(currentCDF)
                for j in range(numJumps):
                    tempCDF[j] += w[i]*(p[i](jumpSize*j+domain[0]))
                tempDeviation = closeness(tempCDF, discreteCDF)
                if tempDeviation <= significanceLevel*currentDeviation:
                    currentDeviation = tempDeviation
                    totalWeight += w[i]
                    contents[i] = 1
                    currentCDF = tempCDF
                    counter += 1
                    if totalWeight == maxWeight:
                        return contents, currentDeviation, currentCDF, totalWeight, numIts
        if counter == 0:
            pairAdded = False
        numIts += 1
    
    
    return contents, currentDeviation, currentCDF, totalWeight, numIts

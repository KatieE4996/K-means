# -*- coding: utf-8 -*-
"""
Created on Wed May 20 13:29:57 2020

@author: Katie Easlon
"""

import numpy as np 

def kmeans(n,row):
    # =============================================================================
    #     Step 1: Call to initalize.
    #     Step 2: Execute while loop, which will continue until the clusters stop changing.
    #     Step 3: Use the Elbow Method (wcss), to find the sum of squares for each K so that the optimal K
    #     is found.
    # =============================================================================
    initalize(n, row)
    
    cont = True
    it_max = 100
    check = 1
    while check <= it_max:
        cont = update_clusters(n,row)
        if cont == False:
            break
        update_centroids(n,row)
        check += 1
    wcss(n, row)    
    
def initalize(n, row):
    # =============================================================================
    #     Step 1: Assign all data points to a cluster 
    #     Step 2: Call update_centroids to define the k[n] centroids based
    #     on the clusters array
    # =============================================================================
    global clusters, centroids 
    col = len(data[row])
    clusters = np.zeros([col], dtype= np.int)
    
    for i in range(k[n]):
        clusters[i] = i
    for i in range(i, col):
        clusters[i] = np.random.randint(0, k[n])
        
    centroids = np.zeros([k[n]], dtype = np.float64) 
    update_centroids(n, row)

def update_clusters(n, row):
    #==============================================================================
    #     Clusters is an array that holds the IDS corresponding with 0-(k-1) so that
    #     the original data isn't modified
    #
    #     Step 1: Copy the old clusters into an array called new_clusters
    #     Step 2: Calculate the Euclidean distance (Ed) from each centroid
    #     (e.g. the mean or center of the cluster)
    #     Step 3: The smallest Ed is noted and the corresponding ID is saved
    #     into new_clusters
    #     Step 4: Check if new_clusters == clusters. If it does equal then return False (K-means is done)
    #     Step 5: Check that there is cluster data
    #     Step 6: Save the new_cluster array into cluster array and return True
    #==============================================================================
    col = len(data[row])
    
    new_clusters = np.copy(clusters)
    edistances = np.zeros([k[n]], dtype = np.float64)
    
    for i in range(col):
        for j in range(k[n]):
            edistances[j] = e_distances(j, row, i) #calulates and stores each Euclidian Distance for every centroid and data
        c_id = np.argmin(edistances)
        new_clusters[i] = c_id
    
    if np.array_equal(clusters, new_clusters): #checks if the clusters are equal 
        return False
    
    counts = np.zeros([k[n]], dtype = np.int)    
    for i in range(col):
        cent = clusters[i]
        counts[cent] += 1
        
    for j in range(k[n]):
        if counts[j] == 0:
            return False
        
    for l in range(col):
        clusters[l] = new_clusters[l]
    return True
    
def e_distances(n, row, col):
    #==============================================================================
    #     This method named e_distances is used to assign a data point to the appropriate
    #     centroid or mean of a cluster
    #
    #     Formula is sqrt((x[i] - m[i])^2)
    #
    #     This is calculated for data point at each K
    #     Method is called in update clusters 
    #==============================================================================
    sum = 0.0
    sum += (data[row][col]-centroids[n]) ** 2
    return np.sqrt(sum)
    
def update_centroids(n, row):
    # =============================================================================
    #     This method named update_centoids finds the centroid (mean or average) of each cluster
    # =============================================================================
    counter = np.zeros([k[n]], dtype = np.int)
    new_centroids = np.zeros([k[n]], dtype = np.float64)
    col = len(data[row])
    
    for i in range(col):
        cent_id = clusters[i]
        counter[cent_id]+=1
        new_centroids[cent_id] += data[row][i]
    for j in range(k[n]):
        new_centroids[j] /= counter[j]
    
    for x in range(k[n]):
        centroids[x] = new_centroids[x]
        
        
def wcss(n, row):
    #==============================================================================
    #     This method calculates the best K using sum of squared distances
    #
    #     Step 1: Save the centroids into an array so that the datapoint corresponds
    #     with the cluster that centroid is in.
    #     Step 2: Calculate the sum of squared distances for the whole set by
    #     doing so for each data point to is centroid
    #       Formula (x[i] - centroid[i])^2 + (x[j] - centroid[j])^2
    #     Step 3: Save the sums into wcss_sum
    #==============================================================================
    global centroid_wcss
    col = len(data[row])
    centroid_wcss = np.zeros([col], dtype = np.float64)
    i = 0
    j = 0
    
    while i < col:
        while j < k[n]:
            if clusters[i] == j:
                centroid_wcss[i] = centroids[j]
            j += 1
        i += 1
        if j == k[n]:
            j = 0
    
    l = 0
    m = 0
    sum = 0.0
    
    while l < col: 
        while m < k[n]:
            if centroids[m] == centroid_wcss[l]:
                sum += (data[row][l] - centroids[m])**2
            m +=1
        wcss_sum[n] = sum
        l += 1
        if m == k[n]:
            m = 0
            sum = 0.0


def optimized_k(row):
    #==============================================================================
    #      This method called optimized_k will sift through the data, when the sum is greater than its predecessor
    #      then the predecessor is the optimal K
    #==============================================================================   
    l = 0
    m = l + 1
    for y in range(len(wcss_sum)):
        if m < len(wcss_sum):
            if wcss_sum[l] > wcss_sum[m]:
                l+=1
                m+=1
            else:
                opt_K[row] = k[l]
                
def file_write():
    #==============================================================================
    #      This mehtod writes the opt_K into a new text file
    #
    #      Note: Orginal filename was manually entered.  If possible implementation from
    #       file_read() by passing in a variable name
    #==============================================================================
    f = open("output.txt", "w")
    f.write("0.txt\n")
    for x in opt_K:
        np.savetxt(f, opt_K)
    f.close()      
    
               
def file_read():
    # =============================================================================
    #     This method reads the txt file and saves the entire file into a numpy array
    #
    #     Note: To make the code work with the parameters of the interview, the file was
    #       saved in the work environment and the program uses the filename indicated.  
    #       In a production implementation this should be optimized to use a variable that would be passed in upon execution.
    # =============================================================================
    global data #will hold all datasets from the file

    with open ("0.txt", "r") as f: 
        lis = [[float(x) for x in line.split()] for line in f]
        
    f.close()
    data = np.asarray(lis)
       
def main():
    #==============================================================================
    #    Step 1: Initalize the k, wcss_sum, and opt_K arrays
    #    Step 2: Calls read file, which loads the file into the data array
    #    Step 3: Start a while loop to preform Kmeans for each dataset at each K
    #    Step 4: Calls file_write to output the results
    #
    #    Note: with large datasets the program takes about 12-20 minutes to execute.
    #       Multiple instances of the code could be executed in parallel.
    #       Code could be further improved to provide flexibility of limiting execution of selected datasets
    #       using a file to pass in desired dataset.
    #==============================================================================
    global k, wcss_sum, opt_K
    n = [2,3,4,5,6,7,8,9,10] #k is the number of clusters 
    k = np.asarray(n)
    wcss_sum = np.zeros([len(k)], dtype = np.float64)
      
    
    file_read() 
    opt_K = np.zeros([len(data)], dtype= np.int)
    i = 0
    j = 0
    
    while i < len(data):
        while j < len(k):
            kmeans(j, i)
            j += 1
        optimized_k(i)
        i += 1
        if j == len(k):
            j = 0
            
    file_write()        
    
    
main()
      
        

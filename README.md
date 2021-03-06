# Spark / MLlib performance test

This code is intended to measure the ability of MLlib algorithms to scale on a Spark architecture, using PySpark. The algorithm used for these tests is k-means.

## Code

The code is split in 4 files : 
* Learning phase of k-means, which builds a re-usable model (```kmeans_learning.py```)
* Execution phase of k-means, which predicts a cluster for some vectors (```kmeans_prediction.py```) 
* Supervision of learning, which runs the learning script several times with a variable dataset size (```supervise_learning.py```)
* Supervision of execution, which runs the execution script several times with a variable dataset size (```supervise_prediction.py```)

## Execution

An example of setup for the version 2.3.2 of Spark on Debian can be found in ```server-setup.sh```, but should be adapted with your paths and Spark version

Only the supervisor scripts should be run directly, their usage is detailed in the comments of each scripts, here are two examples :

```bash
python3 supervise_learning.py kmeans_learning.py 80000 2000000 3 KMeansModel localhost input.txt
python3 supervise_prediction.py kmeans_prediction.py 20000 500000 3 KMeansModel1500000 localhost input.txt
```

## Dataset used

The dataset used is too large for git, but it can be downloaded here :

https://julien-emmanuel.com/s/household_power_consumption.csv.gz

(Originally taken from the [UC Irvine Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/individual+household+electric+power+consumption))

It represents the electric consumption of a house for approximately 3 years measured daily. We manually removed the header line, and then split it into a learning and prediction dataset using the script ```delete_date_data.py``` (additionally the dates and missing values where removed from the dataset to be processable by k-means).

## Methodology

Each algorithm is ran several times using variable sized datasets (specified as input parameters in the supervisor script). Each dataset is also processed several times so that an average can be done on the results to have a more precise value (this is also a parameter of the supervisor script). 

The execution time are stored in a file in a folder called ```out```, and the models in a ```models``` folder for the learning algorithms (both folders must exist before starting the scripts).

The quality of the clustering was computed using the Within Set Sum of Squared Errors method (this error was divided by the dataset size in the graphs).

## Architecture and results

These tests have been run on 5 different configuration, with 1 master machine and 1 to 5 worker machines. 

Each machine had the same characteristics (2 x Intel Xeon X5670 ; 6 cores/CPU ; 96 GB RAM ; running on Debian).

The results are located in the ```result``` folder, using the following convention : 

M**X**W**Y** Where X is the number of master node (so always 1), and Y the number of worker nodes

## Comments on results

Graphs on results are also stored in the ```result``` folder in pdf form. What we can observe is that with more workers the learning phase can be sped up a bit by using 2 or 3 workers, but after that we don't manage to get any more improvement in performance. We can also see that no matter what the dataset size and number of workers is, the execution time never gets below 6 seconds, which might be explained by caching effects which are only efficient after a certain quantity of data have been processed.

The execution phase is always very fast (1/100th to 1/50th of a millisecond, even with quite large datasets), so we get the same results no matter how many workers we use (which might be explained by the fact that each machine is already quite powerful on its own, and don't even use 100% CPU with 1 worker configuration)

We can also see that the clustering globally gets more precise as we increase the dataset size, but is still quite varying, which can probably be explained by the fact that k-means is randomly initialized and that k is chosen quite arbitrarily too.

## Additional algorithms

We tried to use our measurements on a different algorithm ([BisectingKMeans](https://spark.apache.org/docs/2.2.0/mllib-clustering.html#bisecting-k-means)), but its implementation seems incomplete for the Python library (it isn't possible to save / load a model), so we abandoned this path and concentrated on the main k-means algorithm.
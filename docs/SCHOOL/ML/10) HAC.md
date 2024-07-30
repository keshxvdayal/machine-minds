- Stands for Hierarchal Agglomerative Clustering



<br><br><br>



# How it works

<br>

Suppose we have the following data:
![Screenshot 2024-01-23 at 7.07.27 PM.png](../../_resources/Screenshot%202024-01-23%20at%207.07.27%20PM.png)

What we do is we merge the closest 2 points in a cluster like so:
![Screenshot 2024-01-23 at 7.08.08 PM.png](../../_resources/Screenshot%202024-01-23%20at%207.08.08%20PM.png)

And we keep doing that until we reach the desired number of clusters (or some other criteria). We also have the ability to merge clusters like so:
![Screenshot 2024-01-23 at 7.09.52 PM.png](../../_resources/Screenshot%202024-01-23%20at%207.09.52%20PM.png)
![Screenshot 2024-01-23 at 7.10.06 PM.png](../../_resources/Screenshot%202024-01-23%20at%207.10.06%20PM.png)

So ultimately, if we had the number of clusters = 3, we will end up with the following clusters:
![Screenshot 2024-01-23 at 7.12.14 PM.png](../../_resources/Screenshot%202024-01-23%20at%207.12.14%20PM.png)



<br><br><br>



# Determining distance b/w clusters
There are various ways to measure distance b/w clusters. These different ways/methods are called the various "linkage types"

<br>

### 1) Single linkage
This will be the distance between the two closest points of the clusters. A pro is that it can help in ensuring a clear separation of the clusters that have any points within certain distances of one another, so that it can have clear boundaries. A con is that it would not be able to separate out cleanly if theres some noise between the two different clusters, meaning it would be easily skewed by certain outliers falling close to certain clusters
![Screenshot 2024-01-23 at 7.22.03 PM.png](../../_resources/Screenshot%202024-01-23%20at%207.22.03%20PM.png)

<br>

### 2) Complete linkage
Similar to single linkage, but this will take the maximum distance instead of the minimum distance, ie the distance between the two farthest points. A pro of this method is that it will do a much better job of separating out the clusters if theres a bit of noise or overlapping points of the two clusters, unlike single linkage. But a con of this method is that it can tend to break apart larger existing clusters dependent on where that maximum distance of the different points may end up lying
![Screenshot 2024-01-23 at 7.29.50 PM.png](../../_resources/Screenshot%202024-01-23%20at%207.29.50%20PM.png)

<br>

### 3) Average linkage
Or we can just take the averages of the clusters (sort of like centroids) and measure the distance between them. It is sort of a neutral method when compared to single and complete linkage, meaning it has both their pros and cons but to a less extend 
![Screenshot 2024-01-23 at 7.32.48 PM.png](../../_resources/Screenshot%202024-01-23%20at%207.32.48%20PM.png)

<br>

### 4) Ward linkage
Marge based on inertia. So when merging, it will merge the clusters which would minimise that inertia value. (Remember, intertia is the sum of squared distances from each point (x~i~) to its cluster's centroid (C~k~))



<br><br><br>



# Using cluster distance to stop
Rather than using number of clusters as a criteria to stop, we can use the cluster distance as a criteria to stop. We can set a threshold and keep pairing points/clusters until we can make sure that the distance b/w all the clusters is atleast that amount

<br>

So suppose we are at this point:
![Screenshot 2024-01-23 at 7.17.52 PM.png](../../_resources/Screenshot%202024-01-23%20at%207.17.52%20PM.png)
![Screenshot 2024-01-23 at 7.18.07 PM.png](../../_resources/Screenshot%202024-01-23%20at%207.18.07%20PM.png)

<br>

We will keep clustering until we ensure that the distance of all the clusters exceed that threshold, like so:
![Screenshot 2024-01-23 at 7.19.17 PM.png](../../_resources/Screenshot%202024-01-23%20at%207.19.17%20PM.png)
![Screenshot 2024-01-23 at 7.19.27 PM.png](../../_resources/Screenshot%202024-01-23%20at%207.19.27%20PM.png)



<br><br><br>



# Code

```python
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html
from sklearn.cluster import AgglomerativeClustering

model = AgglomerativeClustering(n_clusters=3, metric='euclidean', linkage='ward')
model.fit(X1)
y_predict = model.predict(X2)
```




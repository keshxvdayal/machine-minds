- Depending on the starting positions of the centroids, their end positions can be different



<br><br><br>



# How it works

Suppose we have the following data:
![Screenshot 2024-01-21 at 3.02.29 PM.png](../../_resources/Screenshot%202024-01-21%20at%203.02.29%20PM.png)

What we will do is we will first pick two random points (ie "centroids"), for example:
![Screenshot 2024-01-21 at 3.03.36 PM.png](../../_resources/Screenshot%202024-01-21%20at%203.03.36%20PM.png)

Then we try to predict what cluster each point belongs to (based on distance to the centroids), like so:
![Screenshot 2024-01-21 at 3.05.42 PM.png](../../_resources/Screenshot%202024-01-21%20at%203.05.42%20PM.png)

Then we move each centroid to its cluster's mean/center, like so:
![Screenshot 2024-01-21 at 3.06.58 PM.png](../../_resources/Screenshot%202024-01-21%20at%203.06.58%20PM.png)

So lets do the prediction step again with the new centroids
![Screenshot 2024-01-21 at 3.07.49 PM.png](../../_resources/Screenshot%202024-01-21%20at%203.07.49%20PM.png)

We then move the centroids to the center/mean of their cluster and do the prediction again, and we keep doing that until the centroids dont move anymore, ie they are in the center/mean of their cluster. So we will end up with something like:
![Screenshot 2024-01-21 at 3.09.45 PM.png](../../_resources/Screenshot%202024-01-21%20at%203.09.45%20PM.png)

<br>

If there were 3 centroids, the result might have been:
![Screenshot 2024-01-21 at 3.12.39 PM.png](../../_resources/Screenshot%202024-01-21%20at%203.12.39%20PM.png)



<br><br><br>



# Performance metric(s)
- These helps us select the right number of clusters
- To find the best model, initiate the model multiple times (with diff configs) and take the model with the best score

<br>

### Inertia
- Sum of squared distances from each point (x~i~) to its cluster's centroid (C~k~)
- Smaller value corresponds to tighter cluster
- Value sensitive to the number of points in the cluster
![Screenshot 2024-01-21 at 11.16.16 PM.png](../../_resources/Screenshot%202024-01-21%20at%2011.16.16%20PM.png)

<br>

### Distortion
- Same as inertia, but takes average instead of sum
- Average of the squared distances from each point (x~i~) to its cluster's centroid (C~k~)
- Smaller value corresponds to tighter cluster
- Doesn't generally increase when more points are added (relative to inertia)
![Screenshot 2024-01-21 at 11.18.13 PM.png](../../_resources/Screenshot%202024-01-21%20at%2011.18.13%20PM.png)

<br>

### Elbow method
- Value decreases with increasing K. Just think like if we will have a cluster for every single data point, the inertia/distortion would be 0

![Screenshot 2024-01-21 at 11.28.43 PM.png](../../_resources/Screenshot%202024-01-21%20at%2011.28.43%20PM.png)
So in the above graph, the best value for `k` will be 4, since there will be diminishing returns after that



<br><br><br>



# Code

```python
from sklearn.cluster import KMeans

model = KMeans(n_clusters=3, init='k-means++')
model.fit(X1)
y_predict = model.predict(X2)

# Can also be used in batch mode with `MiniBatchKMeans`
from sklearn.cluster import MiniBatchKMeans
```

<br>

The elbow method can be done like:

```python
perfs = {}
Ks = list(range(2,11))

for k in Ks:
    model = KMeans(n_clusters=k)
    model.fit(X)
    perfs[k] = model.inertia_
```





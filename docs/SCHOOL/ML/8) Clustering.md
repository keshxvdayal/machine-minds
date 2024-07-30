- Part of unsupervised learning, meaning we have data points with unknown outcomes (labels)
- Some common use cases of clustering are:
  - Classification
  - Anomaly/outlier detection
  - Customer segregation
  - Improve supervised learning models. For example, by training different models for clusters rather than training a model for the whole data



<br><br><br>



# Distance metrics
- "Distance" between two points can be measured in various ways
- Choice of our distance metric is incredibly important during clustering
- Each metric has its strengths, weaknesses, and use cases

<br>

### Manhattan / city block (L1)

The concept here is that "you cannot walk between two points directly, you have to turn at a corner first"

|Δx| + |Δy|

<br>

### Euclidean (L2)

The most common and easy to understand method, basically how we were taught in school to calculate distance between two points. It works on the pythagorus theorem and calculates the literal distances between the points. It is useful for coordinate based measurements. It is more sensitive (compared to cosine) to the curse of dimensionality

sqrt(Δx^2^ + Δy^2^)

<br>

### Cosine
Here we draw lines/vectors of the two points and take the cosine of the angle between them. It remains insensitive to the scaling in respect to the origin. Meaning the distance will remain same even if a point is moved back/forward on the line. It is better for data such as text where the location of occurrence in less important. It is more robust/insensitive (compared to euclidean) to the curse of dimensionality
<center>

![Screenshot 2024-01-22 at 6.10.14 PM.png](../../_resources/Screenshot%202024-01-22%20at%206.10.14%20PM.png)</center>

<br>

### Jaccard
Useful for sets (like word occurrences)


<center>

![Screenshot 2024-01-22 at 6.15.18 PM.png](../../_resources/Screenshot%202024-01-22%20at%206.15.18%20PM.png)

![Screenshot 2024-01-22 at 6.16.08 PM.png](../../_resources/Screenshot%202024-01-22%20at%206.16.08%20PM.png)

</center>



<br><br><br>



# Comparisons

("Ward" means the HAC algo with ward linkage)
<center>

![Screenshot 2024-01-27 at 6.28.20 PM.png](../../_resources/Screenshot%202024-01-27%20at%206.28.20%20PM.png)

![Screenshot 2024-01-27 at 6.37.45 PM.png](../../_resources/Screenshot%202024-01-27%20at%206.37.45%20PM.png)

</center>

<br>

### 1) K-Means
- MiniBatch is fast
- Gotta finetune the `n_clu` hyperparameter (can use that elbow method)
- Tends to find even sized clusters
- Bad with non-spherical cluster shapes

<br>

### 2) Mean shift
- We dont have to guess `n_clu`
- Can find uneven clusters
- Slow with a lot of data
- Does a good job of finding a lot of clusters (if they exist)
- Does not do a great job of finding weird shapes
- Uses euclidean distances only

<br>

### 3) HAC (ward)
- Useful for getting a "full hierarchal tree", meaning how some groups are maybe sub groups of others
- Gotta finetune the `n_clu` hyperparameter
- Can find uneven cluster sizes
- A lot of distance metrics and linkage options (may make it difficult to finetune)
- Can be slow to calculate (as number of observations increase)

<br>

### 4) DBSCAN
- "Can get the best of both worlds, if the right parameters are chosen"
- Gotta finetune the `epsilon` and `n_clu` hyperparameters
- Can find uneven sized clusters
- Various distance metrics
- Can handle tons of data and weird shapes
- Too small epsilon is not trustworthy (as it will result in too many clusters)
- Does not do well with clusters of different densities
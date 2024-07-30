- Used to classify stuff
- It is very sensitive to unrelated features. Unlike regression, we cannot fit unrelated features into the model and then expect it to filter out them itself. We have to perform EDA and or use common sense to see which features are related
- Scaling is extremely important
- https://archive.ics.uci.edu/ml/datasets/Car+Evaluation
- **Pros:**
  - Simple to implement
  - Adapts well as new data is introduced
  - Easy to interpret (meaning it makes intuitive sense to the decision makers, ie it provides results or predictions in a way that is easily understandable)
- **Cons:**
  - Slow to predict, cause a LOT of distances have to be calculated
  - Can require a lot of memory
  - When there are many labels, KNN can start to break down cause of the curse of dimensionality



<br><br><br>



# How it works

So we plant all the datapoints on a scatter plot, and each point is associated with a "class". Our aim is to determine which class a new point belongs to. We do that by finding the nearest points to that point. Suppose we have 3 classes (red, blue, and green), and various points are plotted like this:

![Screenshot 2023-05-22 at 7.50.16 PM.png](../../_resources/Screenshot%202023-05-22%20at%207.50.16%20PM.png)

and we need to find the class of this black point:

![Screenshot 2023-05-22 at 7.51.04 PM.png](../../_resources/Screenshot%202023-05-22%20at%207.51.04%20PM.png)

What we will do is calculate the distances between the black point and all the other points on the graph, select the nearest `k` (hyperparameter) number of points (ie points having the lowest distance), and checking which class most of those points have. We usually calculate the distance between two points using the sqrt( (Δ𝑥)^2^ + (Δy)^2^ ) formula. `k` is usually set to be a small odd number. It is odd to avoid ties, and is small because in situations like these:

![Screenshot 2023-05-22 at 8.05.13 PM.png](../../_resources/Screenshot%202023-05-22%20at%208.05.13%20PM.png)

If we set `k` to 11, then the black (unclassified) point will not be classified as red, because red will never be the majority no matter how close the unclassified is to the red cluster



<br><br><br>



# Distance/Similarity measurements

"Distance" between two points can be measured in various ways. The ones most popular in practice are:

<br>

### Manhattan (L1)

The concept here is that "you cannot walk between two points directly, you have to turn at a corner first"

|Δx| + |Δy|

<br>

### Euclidean (L2)

The most common and easy to understand method, basically how we were taught in school to calculate distance between two points. It works on the pythagorus theorem and calculates the literal distances between the points

sqrt(Δx^2^ + Δy^2^)


<br><br><br>



# Why scaling is important

Suppose we have two features (no. of services & data usage in GB), where no. of services ranges from 0-5 and the data usage ranges from 0-60. The graph looks something like this:

<center>

![Screenshot 2023-09-09 at 4.34.38 AM.png](../../_resources/Screenshot%202023-09-09%20at%204.34.38%20AM.png)</center>

which when zoomed in shows this

<center>

![Screenshot 2023-09-09 at 4.35.57 AM.png](../../_resources/Screenshot%202023-09-09%20at%204.35.57%20AM.png)</center>

So here, although the class matters more on the number of services, this feature will have a minimised impact and little effect on the prediction

So after min-max scaling (the common scaling approach when using KNN, since it basically makes all dimensions have equal length), the graph will look something like:

<center>

![Screenshot 2023-09-09 at 4.40.03 AM.png](../../_resources/Screenshot%202023-09-09%20at%204.40.03%20AM.png)</center>

Now both the features will have an equal influence on our model






<br><br><br>


# Decision boundary

It is basically a visual representation of like, what class will a portion of the graph be classified as. Basically for every pixel, which class would it belong to (as predicted by our model). For eg:

<center>

![Screenshot 2023-09-09 at 4.17.55 AM.png](../../_resources/Screenshot%202023-09-09%20at%204.17.55%20AM.png)</center>



<br><br><br>



# Choosing the right value of `k`

- The right value depends on which error metric is most important
- To find the best value of `k`, a common approach is the "elbow method" approach, where kinks in the curve of the error (as a function of `k`) is emphasised

<center>

![Screenshot 2023-09-09 at 4.22.58 AM.png](../../_resources/Screenshot%202023-09-09%20at%204.22.58%20AM.png)</center>



<br><br><br>



# Using KNN for regression

Regression can in theory be performed with KNN. We basically find the average of the labels of the `k` nearest neighbours

- If `k`=1, the model will act as a line graph
- If `k`>1, the model will basically act as a smoothing function
- If `k`=no. of points, the model will just calculate the mean of all the y values

<center>

![Screenshot 2023-09-09 at 4.46.33 AM.png](../../_resources/Screenshot%202023-09-09%20at%204.46.33%20AM.png)</center>








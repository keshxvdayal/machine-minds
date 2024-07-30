- Stands for Principal Component Analysis
- It is very sensitive to scaling, so we should scale our dataset prior to applying it
- MUST SCALE DATA


<br><br><br>



# How it works

<br>

Suppose we have the following dataset. As we can see, the two features are very correlated
![Screenshot 2024-01-29 at 2.00.37 AM.png](../../_resources/Screenshot%202024-01-29%20at%202.00.37%20AM.png)

What we can do is we can consider this line and project the points onto it, like so:
<center>

![Screenshot 2024-01-29 at 2.02.05 AM.png](../../_resources/Screenshot%202024-01-29%20at%202.02.05%20AM.png)

![Screenshot 2024-01-29 at 2.02.20 AM.png](../../_resources/Screenshot%202024-01-29%20at%202.02.20%20AM.png)

</center>

<br>

We can think of his transformation as "the scaled addition" of both the columns. So we now have only one column, which was created as the combination of the two original columns
<center>

![Screenshot 2024-01-29 at 2.04.55 AM.png](../../_resources/Screenshot%202024-01-29%20at%202.04.55%20AM.png)</center>




<br><br><br>



# Maths behind this
First we gotta understand what a "right singular vector" is. These are basically the lines on which we will project our data. Using linear algebra, we can find the "primary right singular vector" and the "secondary right singular vector". They both are perpendicular to other. So they might like look so:

<center>

![Screenshot 2024-01-29 at 2.11.45 AM.png](../../_resources/Screenshot%202024-01-29%20at%202.11.45%20AM.png)</center>

<br>

We use SVD (single value decomposition) to find these vectors



<br><br><br>



# Nonlinear PCA (ie KPCA)
- Stands for "Kernel Principal Component Analysis"
- Here we basically apply a kernel (like the ones in SVMs) to "flatten" out the data

For example, normal PCA cannot be used on this dataset:

<center>

![Screenshot 2024-01-29 at 11.56.50 PM.png](../../_resources/Screenshot%202024-01-29%20at%2011.56.50%20PM.png)</center>

So we use KPCA projection to come up with a "linearly separable"

<center>

![Screenshot 2024-01-29 at 11.58.22 PM.png](../../_resources/Screenshot%202024-01-29%20at%2011.58.22%20PM.png)

![Screenshot 2024-01-29 at 11.59.03 PM.png](../../_resources/Screenshot%202024-01-29%20at%2011.59.03%20PM.png)

</center>






<br><br><br>



# Code

```python
from sklearn.decomposition import PCA, KernelPCA

model = PCA(n_components=3) # n_components in the number of features end data should have
X_trans = model.fit_transform(X_orig)

model = KernelPCA(n_components=3, kernel='rbf', gamma=1.0)
X_trans = model.fit_transform(X_orig)
```
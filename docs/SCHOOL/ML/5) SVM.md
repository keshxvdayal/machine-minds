- Scaling is extremely important (https://stats.stackexchange.com/questions/65094/why-scaling-is-important-for-the-linear-svm-classification)



<br><br><br>



# How it works

So basically we plot a "hyperplane" (ie an (n-1)-dimensional object where n is the total number of dimensions, which in most cases will be the number of features) to divide the clusters. A hyperplane should have equal distances to the closet points of different classes. So for example, in a dataset like

<center>

![Screenshot 2023-09-10 at 11.50.45 AM.png](../../_resources/Screenshot%202023-09-10%20at%2011.50.45%20AM.png)</center>

There can be the following hyperplanes:

<center>

![Screenshot 2023-09-10 at 11.51.10 AM.png](../../_resources/Screenshot%202023-09-10%20at%2011.51.10%20AM.png)

![Screenshot 2023-09-10 at 11.51.37 AM.png](../../_resources/Screenshot%202023-09-10%20at%2011.51.37%20AM.png)</center>


The optimal (ie best) hyperplane would be the hyperplane with the highest **margin**, ie the distance to the closet points of different classes

However, this approach can sometimes overfit when dealing with outliers. For example,

<center>

![Screenshot 2023-09-10 at 11.52.08 AM.png](../../_resources/Screenshot%202023-09-10%20at%2011.52.08%20AM.png)</center>



<br><br><br>



# Kernels

Sometimes, the data looks like

<center>

![Screenshot 2023-09-10 at 12.01.36 PM.png](../../_resources/Screenshot%202023-09-10%20at%2012.01.36%20PM.png)</center>

In cases like these we use a "kernel", ie essentially a function which takes in the features as inputs and adds another feature (ie the output of the function), sort of how we added polynomial features in polynomial regression in case there was any correlation between them and the label. So w can use a kernel f(x~1~,x~2~)->x~3~ on the above graph so that it can be transformed into:

<center>

![Screenshot 2023-09-10 at 12.35.53 PM.png](../../_resources/Screenshot%202023-09-10%20at%2012.35.53%20PM.png)</center>

Another example:

<center>

![Screenshot 2023-09-13 at 3.28.56 PM.png](../../_resources/Screenshot%202023-09-13%20at%203.28.56%20PM.png)</center>





<br><br><br>



# Soft margin

A margin is basically a distance to the closet points of different classes. In real world datasets, we cannot find a hyperplane which perfectly divides the data (cause of areas on the graph where both classes collide), so we sometimes use a "soft margin", ie a margin where points of any class can exist. For eg:

<center>

![Screenshot 2023-09-13 at 3.08.25 PM.png](../../_resources/Screenshot%202023-09-13%20at%203.08.25%20PM.png)

![Screenshot 2023-09-13 at 3.12.34 PM.png](../../_resources/Screenshot%202023-09-13%20at%203.12.34%20PM.png)

</center>



<br><br><br>



# Regularisation/Error function


![Screenshot 2023-09-13 at 3.13.34 PM.png](../../_resources/Screenshot%202023-09-13%20at%203.13.34%20PM.png)

Here the first term refers to amount of misclassifications of training data by our hyperplane (hinge loss?), and the second term is inversely proportional to the margin, so we gotta minimise both the terms



<br><br><br>



# Hyperparamaters

`kernel`
`penalty` (Which regularisation method we want to use, ie L1, L2, or elastic net)
`c` Lower c value means more regularisation and a simpler model






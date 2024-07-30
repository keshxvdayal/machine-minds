Useful for binary classification. Should NOT be used for regression

If we will use simple linear regression, it can misclassify data (cause of points/outliers far away) like so:

<center>

![Screenshot 2023-08-24 at 6.51.13 PM.png](../../_resources/Screenshot%202023-08-24%20at%206.51.13%20PM.png)</center>

So we need to weight the samples (that are far away) much lower. Thats where the logistic function (ie sigmoid function) comes into play



<br><br><br>



# Sigmoid function

It looks as follows:

<center>

![Screenshot 2023-08-24 at 6.55.04 PM.png](../../_resources/Screenshot%202023-08-24%20at%206.55.04%20PM.png)

![Screenshot 2023-08-24 at 6.57.41 PM.png](../../_resources/Screenshot%202023-08-24%20at%206.57.41%20PM.png)


</center>

So rather than the slope being `mx+b`, it is 1 / (1 + e^-(mx+b)^) 

1 / (1 + e^-(mx+b)^) can be further represented as

<center>

![Screenshot 2023-08-24 at 7.01.10 PM.png](../../_resources/Screenshot%202023-08-24%20at%207.01.10%20PM.png)</center>

and the odds ratio can further be represented as

<center>

![Screenshot 2023-08-24 at 7.02.53 PM.png](../../_resources/Screenshot%202023-08-24%20at%207.02.53%20PM.png)</center>



<br><br><br>



# One vs all

This is a method used when we are not dealing with binary classes. Here, for every class, we put that class's points in a separate class and all the other points in another class

So for example, suppose we have 3 classes (a,b,c). So first, we will train a model with all points of `a` being put in `class1` and points of `b` and `c` being put in `class2`. This model will represent the probability that a given point will be of the `a` class. Similarly, we will train two more models, one representing the probability of a point being of class `b` and the other representing the probability of a point being of class `c`. We will then make our final prediction based on which model gave us the highest probability

For example, in a dataset like this:

<center>

![Screenshot 2023-08-24 at 7.13.43 PM.png](../../_resources/Screenshot%202023-08-24%20at%207.13.43%20PM.png)</center>

We end up with the following models:

<center>

(blue vs purple+pink)
![Screenshot 2023-08-24 at 7.14.46 PM.png](../../_resources/Screenshot%202023-08-24%20at%207.14.46%20PM.png)

(purple vs blue+pink)
![Screenshot 2023-08-24 at 7.15.30 PM.png](../../_resources/Screenshot%202023-08-24%20at%207.15.30%20PM.png)

(pink vs blue+purple)
![Screenshot 2023-08-24 at 7.16.02 PM.png](../../_resources/Screenshot%202023-08-24%20at%207.16.02%20PM.png)

</center>



<br><br><br>



# Code

In code, we can pass hyper parameters like `penalty`, `c`, and `solver`

`penalty` is wether we want to use l1, l2, or elastic net regularisation

`c` is the inverse of λ

There is also the `LogisticRegressionCV` class which tunes regularisation parameters via cross validation

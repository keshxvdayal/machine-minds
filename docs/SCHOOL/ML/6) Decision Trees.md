- A "decision stump" is just a decision tree with only one split, so like a single if-else statement. These trees are sometimes also referred to as "weak learners"

**Pros:**
- Easy to interpret and implement
- Able to handle any data category (binary, ordinal, and continuous)
- No preprocessing or scaling required
**Cons:**
- Vulnerable to having high variance, tends to overfit. Variance can be reduced by "pruning" or by having a "max depth" that the tree can have, or the `max_features` hyperparameter. We can prune trees on the following basis:
  - classification error threshold
  - minimum amount of classes in a node

<br>

### Hyperparameters
- `max_features`: It controls the maximum number of features that the decision tree algorithm considers when looking for the best split at each node in the tree. This hyperparameter can be useful for controlling the complexity of the tree and preventing overfitting. It can be set to the following values:
  - `None` **(default):** In this case, the algorithm considers all features at every split. This can lead to deep trees and may result in overfitting if you have a large number of features.
  - **Integer value:** You can specify an integer value `max_features=k`, where `k` is an integer less than the total number of features in your dataset. The algorithm will consider a random subset of `k` features at each split. This is known as "Random Feature Subsets" or "Random Subspace Method." It helps reduce overfitting and can speed up the training process. Setting `max_features` to a smaller value is often useful when you have a large number of features
  - **Float value:** You can specify a float value `max_features=f`, where `f` is in the range (0, 1). The algorithm will consider a fraction `f` of the total number of features at each split. For example, setting `max_features=0.5` means it will consider half of the features at each split
  - `auto` **or** `sqrt`**:** It is equivalent to setting `max_features` to the square root of the total number of features. It's a common choice for classification problems
  - `log2`**:** It is equivalent to setting `max_features` to the base-2 logarithm of the total number of features
  - `onethird`**:** It is equivalent to setting `max_features` to one-third of the total number of features





<br><br><br>





# How it works

<center>

![Screenshot 2023-09-17 at 12.44.01 AM.png](../../_resources/Screenshot%202023-09-17%20at%2012.44.01%20AM.png)</center>

| Outlook  | Temperature | Play Tennis |
|----------|-------------|-------------|
| Sunny    | Hot         | No          |
| Sunny    | Mild        | No          |
| Overcast | Hot         | Yes         |
| Rainy    | Mild        | Yes         |
| Rainy    | Cool        | No          |
| Overcast | Cool        | Yes         |
| Sunny    | Mild        | No          |
| Rainy    | Hot         | No          |
| Sunny    | Cool        | Yes         |
| Overcast | Mild        | Yes         |
| Rainy    | Mild        | Yes         |
| Overcast | Hot         | Yes         |
| Sunny    | Hot         | No          |

```
Outlook
├── Sunny
│   ├── Temperature
│       ├── Hot: No
│       ├── Mild: No
│       └── Cool: Yes
├── Overcast: Yes
└── Rainy
    ├── Temperature
        ├── Hot: No
        ├── Mild: Yes
        └── Cool: Yes
```





<br><br><br>





# Algorithm

Remember, we want the possibility of homogenous (ie only one class per leaf) splits, but not actually result in homogenous splits cause else the model will overfit

Decisions trees will seek to split up the dataset into two datasets at every step, for which the decision is going to be easier, and then continue to iterate. We can keep iterating till:

- Leaf nodes are pure (ie only one class remains) (will overfit)
- Till a maximum depth is reached
- A performance metric (like accuracy) is achieved

<center>

![Screenshot 2023-10-01 at 4.13.03 PM.png](../../_resources/Screenshot%202023-10-01%20at%204.13.03%20PM.png)</center>

<br>

### Splitting based on accuracy

To find the best split at a step. The best split is the split that maximises the information gained from the split

Information gained is defined by E(t) = 1 - max[ p(i/t) ]

<center>

![Screenshot 2023-10-01 at 4.04.27 PM.png](../../_resources/Screenshot%202023-10-01%20at%204.04.27%20PM.png)
Error of parent = 1-(8/12) = 0.3333
Error of left child = 1-(2/4) = 9.5
Error of right child = 1-(6/8) = 0.25

</center>

So in the above example, no information is gained because the classification error doesn't change. If this was the best split available, then we should stop splitting

<br>

### Splitting based on entropy

<center>

![Screenshot 2023-10-01 at 4.10.19 PM.png](../../_resources/Screenshot%202023-10-01%20at%204.10.19%20PM.png)

![Screenshot 2023-10-01 at 4.11.58 PM.png](../../_resources/Screenshot%202023-10-01%20at%204.11.58%20PM.png)

![Screenshot 2023-10-01 at 4.12.14 PM.png](../../_resources/Screenshot%202023-10-01%20at%204.12.14%20PM.png)

![Screenshot 2023-10-01 at 4.12.29 PM.png](../../_resources/Screenshot%202023-10-01%20at%204.12.29%20PM.png)

![Screenshot 2023-10-01 at 4.14.38 PM.png](../../_resources/Screenshot%202023-10-01%20at%204.14.38%20PM.png)

</center>

Since the entropy has decreased by 0.0441, it means that information has been gained, and splitting can further occur

<br>

### Classification error vs Entropy

<center>

![Screenshot 2023-10-01 at 4.17.56 PM.png](../../_resources/Screenshot%202023-10-01%20at%204.17.56%20PM.png)</center>

Entropy can produce more information gain as

<center>

![Screenshot 2023-10-01 at 4.20.20 PM.png](../../_resources/Screenshot%202023-10-01%20at%204.20.20%20PM.png)

![Screenshot 2023-10-01 at 4.20.37 PM.png](../../_resources/Screenshot%202023-10-01%20at%204.20.37%20PM.png)

</center>

In entropy, average of children will be lower than the parent

<br>

### Gini index

- Default metric used in `from sklearn.tree.DecisionTreeClassifier`
- Easier to compute since it doesn't contain logarithm

<center>

![Screenshot 2023-10-01 at 6.57.08 PM.png](../../_resources/Screenshot%202023-10-01%20at%206.57.08%20PM.png)


![Screenshot 2023-10-01 at 7.00.15 PM.png](../../_resources/Screenshot%202023-10-01%20at%207.00.15%20PM.png)

</center>





<br><br><br>





# Regression trees

We can use the same logic for regression. Here, the leaves will be averages of the members that satisfy the conditions. So our "regression line" for a 2D space can look something like

<center>

![Screenshot 2023-09-17 at 12.49.14 AM.png](../../_resources/Screenshot%202023-09-17%20at%2012.49.14%20AM.png)</center>

(Here, we can see that the model with depth=5 is overfit)




- Stands for Multi-Dimensional Scaling
- Doesnt focus on maintaining overall variance
- The goal is to maintain the geometric distances b/w each point



<br><br><br>



<center>

![Screenshot 2024-01-30 at 12.04.20 AM.png](../../_resources/Screenshot%202024-01-30%20at%2012.04.20%20AM.png)</center>



<br><br><br>



```python
from sklearn.decomposition import MDS

model = MDS(n_components=2)
X_trans = model.fit_transform(X_orig)
```
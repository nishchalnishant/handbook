# Dimensionality Reduction

Dimensionality reduction refers to techniques for reducing the number of input variables in a dataset.

## Principal Component Analysis (PCA)

PCA is a dimensionality-reduction method that is often used to reduce the dimensionality of large data sets, by transforming a large set of variables into a smaller one that still contains most of the information in the large set.

### Key Concepts
*   **Principal Components**: New variables that are constructed as linear combinations or mixtures of the initial variables.
*   **Eigenvalues**: They indicate the amount of variance carried by each principal component.

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
```

# Classification

Classification is a type of supervised learning where the output variable is a category, such as "red" or "blue" or "disease" and "no disease".

## Logistic Regression

Despite its name, Logistic Regression is a classification algorithm. It is used to estimate discrete values (Binary values like 0/1, yes/no, true/false) based on a given set of independent variables.

### Sigmoid Function

It maps predicted values to probabilities.

$$ S(z) = \frac{1} {1 + e^{-z}} $$

## Support Vector Machines (SVM)

SVMs are powerful classifiers that work by finding a hyperplane that best divides a dataset into two classes.

1.  **Margin**: The distance between the hyperplane and the nearest data point from either class.
2.  **Support Vectors**: The data points that are closest to the hyperplane.

!!! warning "Computational Cost"
    SVMs can be computationally expensive on very large datasets.

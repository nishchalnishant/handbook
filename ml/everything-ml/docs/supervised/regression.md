# Regression

Regression analysis is a set of statistical processes for estimating the relationships between a dependent variable (often called the 'outcome variable') and one or more independent variables (often called 'predictors', 'covariates', or 'features').

## Linear Regression

Linear regression attempts to model the relationship between two variables by fitting a linear equation to observed data.

### Equation

The equation for simple linear regression is:

$$ y = \beta_0 + \beta_1X + \epsilon $$

Where:
*   $y$ is the predicted value.
*   $\beta_0$ is the y-intercept.
*   $\beta_1$ is the slope.
*   $X$ is the input feature.

### Code Example

```python
import numpy as np
from sklearn.linear_model import LinearRegression

# Sample data
X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
y = np.dot(X, np.array([1, 2])) + 3

# Model training
reg = LinearRegression().fit(X, y)

print(f"Score: {reg.score(X, y)}")
print(f"Coefficients: {reg.coef_}")
print(f"Intercept: {reg.intercept_}")
```

## Polynomial Regression

If the data points clearly do not follow a linear trend, it might be better to fit a polynomial equation.

!!! note
    Polynomial regression is still considered linear regression because the coefficients are linear.

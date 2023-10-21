1. The risk of a categorical feature tells us if a group that has the feature will have the condition we model. For churn, values lower than 1.0 indicate low risk of churning, whereas values higher than 1.0 indicate high risk of churning. It tells us which features are important for predicting the target variable and helps us better understand the problem we’re solving.

2. Mutual information measures the degree of (in)dependence between a categorical variable and the target. It's a good way of determining important features: the higher the mutual information is, the more important the feature.

3. Correlation measures the dependence between two numerical variables, and it can be used for determining if a numerical feature is useful for predicting the target variable.

4. One-hot encoding gives us a way to represent categorical variables as numbers. Without it, it wouldn’t be possible to easily use these variables in a model. Machine learning models typically expect all input variables to be numeric, so having an encoding scheme is crucial if we want to use categorical features in modeling.

5. We can implement one-hot encoding by using DictVectorizer from Scikit-learn. It automatically detects categorical variables and applies the one-hot encoding scheme to them while leaving numerical variables intact. It's very convenient to use and doesn’t require a lot of coding on our side.

6. Logistic regression is a linear model, just like linear regression. The difference is that logistic regression has an extra step at the end: it applies the sigmoid function to convert the scores to probabilities (a number between zero and one). That allows us to use it for classification. The output is the probability of belonging to a positive class (churn, in our case).

7. When the data is prepared, training logistic regression is very simple: we use the LogisticRegression class from Scikit-learn and invoke the fit function.

8. The model outputs probabilities, not hard predictions. To binarize the output, we cut the predictions at a certain threshold. If the probability is greater than or equal to 0.5, we predict True (churn), and False (no churn) otherwise. This allows us to use the model for solving our problem: predicting customers who churn.

9. The weights of the logistic regression model are easy to interpret and explain, especially when it comes to the categorical variables encoded using the one-hot encoding scheme. It helps us understand the behavior of the model better and explain to others what it's doing and how it's working.
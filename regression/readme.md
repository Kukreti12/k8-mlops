### Car price predictions
1. Doing simple initial exploratory analysis is important. Among other things, it helps us find out whether the data has missing values. It's not possible to train a linear regression model when there are missing values, so it's important to check our data and fill in the missing values if necessary.

2. As a part of exploratory data analysis, we need to check the distribution of the target variable. If the target distribution has a long tail, we need to apply the log transformation. Without it, we may get inaccurate and misleading predictions from the linear regression model.

3. The train/validation/test split is the best way to check our models. It gives us a way to measure the performance of the model reliably, and things like numerical instability issues won’t go unnoticed.

4. The linear regression model is based on a simple mathematical formula, and understanding this formula is the key to successful application of the model. Knowing these details helps us learn how the model works before coding it.

5. It's not difficult to implement linear regression from scratch using Python and NumPy. Doing so helps us understand that there’s no magic behind machine learning: it's simple math translated to code.

6. RMSE gives us a way to measure the predictive performance of our model on the validation set. It lets us confirm that the model is good and helps us compare multiple models to find the best one.

7. Feature engineering is the process of creating new features. Adding new features is important for improving the performance of a model. While adding new features, we always need to use the validation set to make sure that our model indeed improves. Without constant monitoring, we risk getting mediocre or very bad performance.

8. Sometimes, we face numerical instability issues that we can solve with regularization. Having a good way to validate models is crucial for spotting a problem before it's too late.

9. After the model is trained and validated, we can use it to make predictions, such as applying it to cars with unknown prices to estimate how much they may cost.
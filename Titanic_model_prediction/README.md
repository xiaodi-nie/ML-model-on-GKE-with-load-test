# Titanic Survival Classification
In this part, we used the [Titanic dataset](https://www.kaggle.com/c/titanic/data) and created a classification model using the Random Forests algorithm.  
<br>
This dataset contains 891 training samples and 418 test samples with 11 features.  
<br>
There are mainly 6 steps in the process of creating models: 
1. Analyzing feature contributions 
2. Data preprocessing (processing missing data and standardizing features)
3. Applying Random Forests to the model and evaluating performance using cross-validation and *Out of Bag (OOB)* score. 
4. Analyzing feature importance for Random Forests and tuning parameters
5. Repeating step 3 using the tuned parameters
6. Save the final model in a .joblib file  
<br>
The final model has a 92.26% training accuracy and 82.38% OOB score.
<br>
All code, analysis, and model evaluations are presented in the .ipynb file.

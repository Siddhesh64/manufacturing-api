import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os
import numpy as np

print("1. Loading Data...")
df = pd.read_csv('manufacturing_dataset_1000_samples (1).csv')

# --- EDA (Exploratory Data Analysis) ---
print("2. Creating EDA Graphs for your presentation...")
if not os.path.exists('graphs'):
    os.makedirs('graphs')

# Graph 1: Let's see how Temperature affects Parts Per Hour
plt.figure(figsize=(8, 5))
sns.scatterplot(x='Injection_Temperature', y='Parts_Per_Hour', data=df, color='blue')
plt.title('Temperature vs. Parts Per Hour')
plt.savefig('graphs/temperature_vs_parts.png')
plt.close()

# Graph 2: The distribution of our Target (Parts Per Hour)
plt.figure(figsize=(8, 5))
sns.histplot(df['Parts_Per_Hour'], bins=30, kde=True, color='green')
plt.title('Distribution of Parts Per Hour')
plt.savefig('graphs/target_distribution.png')
plt.close()
print("Graphs saved in the 'graphs' folder!")

# --- PREPROCESSING & TRAINING ---
print("3. Preparing Data and Training Linear Regression...")
# Target is now Parts_Per_Hour!
X = df.drop(columns=['Parts_Per_Hour', 'Timestamp']) 
y = df['Parts_Per_Hour'] 

numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
text_features = X.select_dtypes(include=['object']).columns

numeric_rules = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())]) # Scaling is required for Linear Regression!

text_rules = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

cleaner = ColumnTransformer(
    transformers=[
        ('num', numeric_rules, numeric_features),
        ('cat', text_rules, text_features)])

# Using Linear Regression now!
ai_model = Pipeline(steps=[('preprocessor', cleaner),
                           ('brain', LinearRegression())])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
ai_model.fit(X_train, y_train)

# --- EVALUATION ---
# Calculating the exact metrics asked for in your document
predictions = ai_model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, predictions)

print(f"\n--- Model Report ---")
print(f"MSE (Mean Squared Error): {mse:.2f}")
print(f"RMSE (Root Mean Squared Error): {rmse:.2f}")
print(f"Accuracy (R2 Score): {r2:.2f}")
print("--------------------\n")

# Save the model
if not os.path.exists('model'):
    os.makedirs('model')
joblib.dump(ai_model, 'model/linear_model.pkl')
print("Success! Your Linear Regression model is saved.")
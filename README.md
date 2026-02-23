# 🏭 Manufacturing Equipment Output Prediction

**Live Project Link:** [https://manufacturing-api-am66.onrender.com/docs](https://manufacturing-api-am66.onrender.com/docs)

## 📌 Project Overview
In the manufacturing industry, predicting how many parts a machine can produce per hour is critical for planning schedules and finding machines that need maintenance. 

This is an end-to-end Data Science and Machine Learning project. I built an Artificial Intelligence model to predict the hourly output (`Parts_Per_Hour`) of injection molding machines based on their operating conditions (like temperature, pressure, and cycle time). 

To make this useful for a real business, I deployed the model as a backend API using **FastAPI**, packaged it securely using **Docker**, and hosted it live on the cloud.

## 🛠️ Technology Stack
* **Machine Learning:** Python, Scikit-Learn, Pandas, NumPy
* **Data Visualization:** Matplotlib, Seaborn (for Exploratory Data Analysis)
* **Backend API:** FastAPI, Uvicorn
* **Deployment:** Docker, Render (Cloud Platform)

## 🧠 The Machine Learning Pipeline
I built a fully automated data processing pipeline. Here is step-by-step how the AI works:

1. **Exploratory Data Analysis (EDA):** Analyzed 1,000 records of machine data to find trends between temperature, pressure, and the final output.
2. **Data Cleaning (Imputation):** Used `SimpleImputer` to automatically fill in any missing numerical data with the mean, and missing text data with the most frequent value.
3. **Feature Scaling:** Used `StandardScaler` to bring all numerical values to the same scale, which is required for accurate Linear Regression.
4. **Categorical Encoding:** Used `OneHotEncoder` to convert text data (like "Day/Night Shift" or "Machine Type A/B") into a mathematical format (1s and 0s).
5. **Model Training:** Trained a **Linear Regression** model because the target variable (`Parts_Per_Hour`) is a continuous numerical value.

**Model Performance:**
* The model was evaluated using standard regression metrics: Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and R-Squared (R2) Score to ensure high accuracy before deployment.

## 🚀 Deployment Architecture
A machine learning model is only useful if other applications can access it. 

1. **FastAPI:** I created a RESTful API. This allows factory software or web dashboards to send a CSV file of machine data to the server and instantly receive predictions back in JSON format.
2. **Docker:** I containerized the entire project. This means the Python environment, the API code, and the trained model are locked inside a single container. This guarantees the application will run perfectly on any computer without "version conflicts" or missing installations.
3. **Cloud Hosting:** The Docker container is currently live and hosted on Render.

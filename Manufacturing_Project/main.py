from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import pandas as pd
import joblib
import io

# Create the FastAPI app
app = FastAPI(title="Manufacturing Output Predictor API")

# Load our saved Linear Regression model
model = joblib.load('model/linear_model.pkl')

# 1. This creates a very simple webpage just to upload the file
@app.get("/", response_class=HTMLResponse)
async def main_page():
    return """
    <html>
        <head><title>Predict Output</title></head>
        <body style="font-family: Arial; padding: 50px;">
            <h2>Upload Manufacturing CSV to predict Parts Per Hour</h2>
            <form action="/predict" enctype="multipart/form-data" method="post">
                <input name="file" type="file" accept=".csv">
                <input type="submit" value="Predict with AI">
            </form>
        </body>
    </html>
    """

# 2. This is the API endpoint that does the actual math
@app.post("/predict")
async def predict_output(file: UploadFile = File(...)):
    # Read the uploaded CSV file
    contents = await file.read()
    input_data = pd.read_csv(io.BytesIO(contents))
    
    # Remove columns we shouldn't predict with
    if 'Parts_Per_Hour' in input_data.columns:
        input_data = input_data.drop(columns=['Parts_Per_Hour'])
    if 'Timestamp' in input_data.columns:
        input_data = input_data.drop(columns=['Timestamp'])
        
    # Make predictions
    predictions = model.predict(input_data)
    
    # Return the first 10 predictions just to keep the screen clean
    results = predictions.tolist()
    
    return {"Message": "Success!", "Predictions are": results}
# 🎓 Study Abroad Cost Estimator

A machine learning web app that estimates the total cost of studying
(tuition + rent) by country, city, university, program and level.

## Features
- Dropdowns: country → city → university → program → level
- Predicted total cost with tuition and rent breakdown
- Charts comparing universities in a city and cities in a country

## Dataset
International Education Costs (Kaggle, by Adil Shamim).
Total_cost = Tuition_USD + Rent_USD

## Results
1              Model    MAE     R2
2      Random Forest   2655  0.934
1      Decision Tree   3045  0.874
0  Linear Regression  12279  0.252

## Run locally
    pip install -r requirements.txt
    python -m streamlit run app.py

## Limitations
- Predictions only work for universities in the dataset.
- Total cost is tuition + rent only (no visa or insurance).

## Screenshots
![Cost estimate](screenshots/estimate.png)
![Universities in a city](screenshots/city_universities.png)
![Cities in a country](screenshots/country_cities.png)
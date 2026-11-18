import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Study Abroad Cost Estimator", page_icon="🎓", layout="wide")

model = joblib.load('model.pkl')
encoders = joblib.load('encoders.pkl')
cols = joblib.load('columns.pkl')
ref = pd.read_csv('reference.csv')

st.title("🎓 Study Abroad Cost Estimator")

# ---------- Sidebar selections ----------
st.sidebar.header("Choose your options")

country = st.sidebar.selectbox("Country", sorted(ref['Country'].unique()))
country_df = ref[ref['Country'] == country]

city = st.sidebar.selectbox("City", sorted(country_df['City'].unique()))
city_df = country_df[country_df['City'] == city]

uni = st.sidebar.selectbox("University", sorted(city_df['University'].unique()))
uni_df = city_df[city_df['University'] == uni]

program = st.sidebar.selectbox("Program", sorted(uni_df['Program'].unique()))
prog_df = uni_df[uni_df['Program'] == program]

level = st.sidebar.selectbox("Level", sorted(prog_df['Level'].unique()))
sel = prog_df[prog_df['Level'] == level]

# ---------- Tabs ----------
tab1, tab2, tab3 = st.tabs(["💰 Cost estimate", "🏫 Universities in this city", "🌆 Cities in this country"])

with tab1:
    if st.button("Estimate total cost"):
        row = sel.iloc[[0]].copy()
        X = row.copy()
        for col in encoders:
            X[col] = encoders[col].transform(X[col])
        X = X[cols]
        predicted = model.predict(X)[0]

        c1, c2, c3 = st.columns(3)
        c1.metric("Predicted total cost", f"${predicted:,.0f}")
        c2.metric("Tuition", f"${row['Tuition_USD'].iloc[0]:,.0f}")
        c3.metric("Rent", f"${row['Rent_USD'].iloc[0]:,.0f}")

        st.subheader("Cost breakdown")
        breakdown = pd.DataFrame(
            {"Cost (USD)": [row['Tuition_USD'].iloc[0], row['Rent_USD'].iloc[0]]},
            index=["Tuition", "Rent"]
        )
        st.bar_chart(breakdown)
        st.caption(f"{uni}, {city}, {country} | {program} ({level}) | Duration: {row['Duration_Years'].iloc[0]} years")

with tab2:
    st.subheader(f"Universities in {city}: tuition + rent")
    comp = city_df.groupby('University')[['Tuition_USD', 'Rent_USD']].mean()
    comp = comp.assign(Total=comp.sum(axis=1)).sort_values('Total')
    st.bar_chart(comp[['Tuition_USD', 'Rent_USD']])
    st.dataframe(comp.round(0).astype(int).sort_values('Total'))

with tab3:
    st.subheader(f"Cities in {country}: tuition + rent")
    comp2 = country_df.groupby('City')[['Tuition_USD', 'Rent_USD']].mean()
    comp2 = comp2.assign(Total=comp2.sum(axis=1)).sort_values('Total')
    st.bar_chart(comp2[['Tuition_USD', 'Rent_USD']])
    st.dataframe(comp2.round(0).astype(int).sort_values('Total'))
    
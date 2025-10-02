import streamlit as st
import pandas as pd
import joblib

# ---- Load Model and Training Columns ----
model = joblib.load("model.joblib")            # your trained RFC model
train_columns = joblib.load("train_columns.pkl")  # list of columns after pd.get_dummies during training
le = joblib.load("le.joblib")

st.title("🏏 IPL Match Winner Prediction")

# ---- Teams ----
teams = [
    'Royal Challengers Bangalore','Kings XI Punjab','Delhi Daredevils',
    'Mumbai Indians','Kolkata Knight Riders','Rajasthan Royals',
    'Deccan Chargers','Chennai Super Kings','Kochi Tuskers Kerala',
    'Pune Warriors','Sunrisers Hyderabad','Gujarat Lions',
    'Rising Pune Supergiants','Rising Pune Supergiant','Delhi Capitals',
    'Punjab Kings','Lucknow Super Giants','Gujarat Titans',
    'Royal Challengers Bengaluru'
]

# ---- Venues ----
venues = [
    "M Chinnaswamy Stadium","Punjab Cricket Association Stadium, Mohali",
    "Feroz Shah Kotla","Wankhede Stadium","Eden Gardens",
    "Sawai Mansingh Stadium","Rajiv Gandhi International Stadium, Uppal",
    "MA Chidambaram Stadium, Chepauk","Dr DY Patil Sports Academy",
    "Newlands","St George's Park","Kingsmead","SuperSport Park",
    "Buffalo Park","New Wanderers Stadium","De Beers Diamond Oval",
    "OUTsurance Oval","Brabourne Stadium","Sardar Patel Stadium, Motera",
    "Barabati Stadium","Brabourne Stadium, Mumbai",
    "Vidarbha Cricket Association Stadium, Jamtha",
    "Himachal Pradesh Cricket Association Stadium","Nehru Stadium",
    "Holkar Cricket Stadium",
    "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium",
    "Subrata Roy Sahara Stadium",
    "Maharashtra Cricket Association Stadium",
    "Shaheed Veer Narayan Singh International Stadium",
    "JSCA International Stadium Complex","Sheikh Zayed Stadium",
    "Sharjah Cricket Stadium","Dubai International Cricket Stadium",
    "Punjab Cricket Association IS Bindra Stadium, Mohali",
    "Saurashtra Cricket Association Stadium","Green Park",
    "M.Chinnaswamy Stadium",
    "Punjab Cricket Association IS Bindra Stadium",
    "Rajiv Gandhi International Stadium",
    "MA Chidambaram Stadium",
    "Arun Jaitley Stadium",
    "MA Chidambaram Stadium, Chepauk, Chennai",
    "Wankhede Stadium, Mumbai",
    "Narendra Modi Stadium, Ahmedabad",
    "Arun Jaitley Stadium, Delhi",
    "Zayed Cricket Stadium, Abu Dhabi",
    "Dr DY Patil Sports Academy, Mumbai",
    "Maharashtra Cricket Association Stadium, Pune",
    "Eden Gardens, Kolkata",
    "Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh",
    "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow",
    "Rajiv Gandhi International Stadium, Uppal, Hyderabad",
    "M Chinnaswamy Stadium, Bengaluru",
    "Barsapara Cricket Stadium, Guwahati",
    "Sawai Mansingh Stadium, Jaipur",
    "Himachal Pradesh Cricket Association Stadium, Dharamsala",
    "Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur",
    "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam"
]

# ---- Streamlit Inputs ----
venue = st.selectbox("Select Venue", venues)
team1 = st.selectbox("Select Team 1", teams)
team2 = st.selectbox("Select Team 2", [t for t in teams if t != team1])
toss_winner = st.selectbox("Select Toss Winner", [team1, team2])

# ---- Predict ----
if st.button("Predict Winner"):
    # Create raw input DataFrame
    input_df = pd.DataFrame({
        'venue': [venue],
        'team1': [team1],
        'team2': [team2],
        'toss_winner': [toss_winner]
    })

    # One-hot encode
    input_encoded = pd.get_dummies(input_df)

    # Reindex to match training columns
    input_encoded = input_encoded.reindex(columns=train_columns, fill_value=0)

    # Predict winner
    prediction = model.predict(input_encoded)[0]

    # Predict probabilities
    proba = model.predict_proba(input_encoded)[0]
    team_labels = model.classes_

    st.subheader("🏆 Predicted Winner")
    st.success(le.inverse_transform([prediction]))
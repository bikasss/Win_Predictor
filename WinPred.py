import streamlit as st
from time import sleep
import pandas as pd
import pickle




st.title("Second Innings Win Prediction")


pickle_in = open("model_pipe.pkl","rb")
classifier = pickle.load(pickle_in)

#target
target = st.number_input("Target",min_value = 0, max_value = 500)
#batting team score
Score = st.number_input("Score",min_value = 0, max_value = 500)
#current over
Overs = st.number_input("Over",min_value = 1, max_value = 20)
#wicket
Wicket = st.number_input("Wicket",min_value = 0, max_value = 10)
run_left = target - Score
wicket_left = 10 - Wicket
Ball_left = 120 - Overs*6


crr = Score/Overs

if Ball_left == 0:
    rrr = 0
else:
    rrr = ((target-Score)*6)/Ball_left

won = 2

if run_left <= 0:
    won = 1
elif (Ball_left <=0 or wicket_left <=0 ) and run_left > 0 :
    won = 0
Team = [
    'Chennai Super Kings',
    'Delhi Capitals',
    'Mumbai Indians',
    'Kolkata Knight Riders',
    'Kings XI Punjab',
    'Rajasthan Royals',
    'Royal Challengers Bangalore',
    'Sunrisers Hyderabad'
]

Batting = st.selectbox("Batting Team",Team)


Bowling  = st.selectbox("Bowling Team",Team)

c = [
    'Hyderabad',
    'Pune',
    'Rajkot',
    'Indore',
    'Bangalore',
    'Mumbai',
    'Delhi',
    'Kolkata',
    'Chandigarh',
    'Kanpur',
    'Chennai',
    'Jaipur',
    'Cape Town',
    'Ahmedabad',
    'Nagpur',
    'Dharamsala',
    'Kochi',
    'Visakhapatnam',
    'Cuttack',
    'Dharamsala',
    'Raipur',
    'Ranchi',
    'Mohali'

]

city = st.selectbox("City",c)



to_add = {'batting_team':Batting,'bowling_team':Bowling, 'city':city, 'runs_left':run_left,'balls_left':Ball_left, 'wickets':wicket_left,'total_runs_x':target,'crr':crr,'rrr':rrr}
to_add = pd.DataFrame(to_add,index=[0])



def winProb(inst):
    win_prob = classifier.predict_proba(to_add)
    Re = win_prob.T[1]*100
    win = int(Re[0])
    return win

st.markdown("""
<style>
.stProgress > div > div > div > div {
    background-color: green;
}
</style>
""", unsafe_allow_html=True)

progress = st.progress(0)
if st.button('Predict'):


    if won == 2:
        ww = winProb(to_add)
    elif won ==1:
        ww = 100
    else:
        ww = 0

    

    progress.progress(ww)

    st.write(f'{Batting} chances of winning: {ww}%')










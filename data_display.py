import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import pyrebase

st.set_page_config(page_title='Garissa Township Consituency By-Election',page_icon='fm.png', layout = "wide")
st.title("Garissa Township MP Seat Race")
firebaseConfig = {
  "apiKey": "AIzaSyCqMdmrITPM8x4PdMqP5T9Hcmmj5IJPH6M",
  "authDomain": "demoapp-607db.firebaseapp.com",
  "databaseURL": "https://demoapp-607db-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "demoapp-607db",
  "storageBucket": "demoapp-607db.appspot.com",
  "messagingSenderId": "641799333572",
  "appId": "1:641799333572:web:fd402ab5271f9fa4d6cb91",
  "measurementId": "G-KPVXQKZ7KK"
}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
all_votes = db.child('votes').order_by_key().get()
info = []
for vote in all_votes:
	values = vote.val()
	# print(values)
	info.append(values)
# st.write(info)
df = pd.DataFrame(info,columns=['time','ward','pollingStation','registerdVoters','rejected','rejectedObj','disputed','valid','dekow','jofle','osman'])
# st.write(df)
df['time'] = pd.to_datetime(df['time'])
df = df.sort_values(by='time',ascending=False)
reg = 53765
r1,r2= st.columns(2)
r1.write(f"<h4 style ='margin-top:50px;'>Total Number of Registered Voters in Garissa Township are : {reg}<h4>",unsafe_allow_html=True)
turnout = df[['rejected','disputed','valid','rejectedObj']]
turnout = turnout.astype({"rejected":"int","disputed":"int","valid":"int","rejectedObj":"int"})
# st.write(turnout['valid'].sum())
# total_valid = turnout['valid'].sum()
re_turnout = turnout[['rejected','disputed','valid','rejectedObj']].sum()
final_turnout = re_turnout.sum()
# st.write(re_turnout)
r2.write("<h4 style ='margin-top:50px;'>The percentage Turnout Voters in Garissa Township is : {:.2f}%<h4>".format((final_turnout/reg)*100),unsafe_allow_html=True)
c1,c2,c3,c4,c5 = st.columns(5)
c1.write(f'<strong >Total Turnout: {final_turnout}</strong>',unsafe_allow_html=True)
c5.write(f'<strong >Total Votes Rejection Objected: {re_turnout[3]}</strong>',unsafe_allow_html=True)
c4.write(f'<strong >Total Votes Valid: {re_turnout[2]}</strong>',unsafe_allow_html=True)
c3.write(f'<strong >Total Votes Disputed: {re_turnout[1]}</strong>',unsafe_allow_html=True)
c2.write(f'<strong >Total Votes Rejected: {re_turnout[0]}</strong>',unsafe_allow_html=True)

major,jofle,osman = st.columns(3)
major_data,jofle_data,osman_data = st.columns(3)
major_per,jofle_per,osman_per = st.columns(3)

major.image('major.png')
osman.image('osman.jpg')
jofle.image('jofle.jpg')

candidates_votes = df[['dekow','jofle','osman']]
candidates_votes = candidates_votes.astype({"dekow":"int","jofle":"int","osman":"int"})
votes4dekow=candidates_votes['dekow'].sum()
votes4jofle=candidates_votes['jofle'].sum()
votes4osman=candidates_votes['osman'].sum()

major_data.write(f"Total Votes: {votes4dekow}")
jofle_data.write(f"Total Votes: {votes4jofle}")
osman_data.write(f"Total Votes: {votes4osman}")

def calculate(vote4each):
  percentage_f = (vote4each/re_turnout[2]) * 100
  return percentage_f
major_per.write('Total Percentage: {:.2f}%'.format(calculate(votes4dekow)))
jofle_per.write('Total Percentage: {:.2f}%'.format(calculate(votes4jofle)))
osman_per.write('Total Percentage: {:.2f}%'.format(calculate(votes4osman)))
# total = calculate(votes4osman)+calculate(votes4jofle)+calculate(votes4dekow)
# st.write(total)
graph1,graph2=st.columns(2)
data = [['MAJOR',votes4dekow],['JOFLE',votes4jofle],['OSMAN',votes4osman]]
jabir = pd.DataFrame(data,columns=['Candidate','Votes'] )
jabir= jabir.sort_values(by='Votes', ascending=False)
bar_chart = px.bar(jabir,
                    x='Candidate',
                    y='Votes',
                    text='Votes',
                    orientation='v',
                    color_discrete_sequence = ['#62B6B7'],
                    template='plotly_white')
graph1.plotly_chart(bar_chart)
#bar chart
checkvotes = [votes4dekow,votes4jofle,votes4osman]
pie_chart = px.pie(jabir, title = "Votes for Each Candidate", values=checkvotes,names=['dekow','jofle','osman'])
graph2.plotly_chart(pie_chart)
st.dataframe(df,width=int(1900))

##checking who is leading
hv=np.max(checkvotes)
hv5=np.min(checkvotes)
("---")
if hv == votes4dekow:
  checkvote1 = [votes4jofle,votes4osman]
  hv1=np.max(checkvote1)
  major_per.write(f"<strong style='color:#99004d;'>You are ahead by : {votes4dekow-hv1} votes</strong>",unsafe_allow_html=True)
elif hv == votes4jofle:
  checkvote1 = [votes4dekow,votes4osman]
  hv1=np.max(checkvote1)
  jofle_per.write(f"<strong style='color:#99004d;'>You are ahead by : {votes4jofle-hv1} votes</strong>",unsafe_allow_html=True)
else:
  checkvote1 = [votes4dekow,votes4jofle]
  hv1=np.max(checkvote1)
  osman_per.write(f"<strong style='color:#99004d;'>You are ahead by : {votes4osman-hv1} votes</strong>",unsafe_allow_html=True)
















style = '''
<style>
.e16nr0p30{
	margin-top:-100px;
}
footer{
  visibility:hidden;
}
</style>
'''
st.markdown(style,unsafe_allow_html=True)

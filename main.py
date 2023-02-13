import streamlit as st
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from sentida import Sentida
SV = Sentida()

col1, col2 = st.columns(2)

with col1:
   st.title('Hjem fra Rubrik')

with col2:
   st.image('https://vigeur.dk/img/logo/metalogo.png', width=250)

st.write('Hvor positive er vores rubrikker?')
option = st.selectbox(
    'Forside',
    ('Vigeur', 'Nordjyske', 'LigeHer.nu'), label_visibility="hidden")

match option:
    case "Vigeur":
        url='https://www.vigeur.dk'
        hlStyle = 'h2'
        classFilter = {'class':'article-teaser__heading'}
      
    case "Nordjyske":
        url='https://www.nordjyske.dk'
        hlStyle = 'div'
        classFilter = {'class':'dre-item__alt-title--md'}
      
    case "LigeHer.nu":
        url='https://www.ligeher.nu'
        hlStyle = 'h2'
        classFilter = {'class':'card-title'}

#Lad os hente de overskrifter
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
headlines = soup.find('body').find_all(hlStyle, classFilter)

#print(headlines)
#print('Vigeur ... ok')

#Finde sentiment på hver og stoppe dem i et array
headlinesSenti = []

for x in headlines:
    rubrik = x.text.strip()
    
    sentiment = SV.sentida(
        text = rubrik,
        output = 'mean',
        normal = False)
    
    headlinesSenti.append({'HL':rubrik, 'S':sentiment})
    #print(rubrik + '\n' + str(round(sentiment, 2)) + '\n')

dfRubrik = pd.DataFrame(headlinesSenti)

#renser dubletter
#print(dfRubrik.describe())
dfRubrik.drop_duplicates(inplace=True)

#få gennemsnittet for alle rubrikkers sentiment
sentiMean = dfRubrik['S'].mean()

st.subheader('Forsidens gennemsnit lige nu: ' + str(round(sentiMean, 2)))
 
# Dataframe and Chart display section
st.subheader('Rubrikker og deres sentiment')
st.dataframe(dfRubrik) 

st.write('**Om Hjem fra Rubrik**')
st.write('Henter alle rubrikker fra en af nævnte forsider, kører en sentiment-analyse på dem og udstiller dem, samt gennemsnittet.')
st.write('En rubrik med overvejende negative ord, vil have et lavt/negativt tal, en mere postiv rubrik vil have en højere/positiv værdi')
st.write('TB, 2023')

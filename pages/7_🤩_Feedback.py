import streamlit_authenticator as stauth
import streamlit as st
from Stocky_DB_2 import credintials

SSF=credintials()
name=st.text_input('Please Enter Name')
feedback=st.text_area('Please Give your Feedback')
submit=st.button("Submit")
if submit:
    SSF.get_feedback(name,feedback)
    st.success('Thank you for your valuable feedback')

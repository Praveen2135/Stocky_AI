import streamlit_authenticator as stauth
import streamlit as st
from Stocky_DB_2 import credintials
from streamlit_option_menu import option_menu
from telegram_bot import get_feedback



SSF=credintials()
name=st.text_input('Please Enter Name')
feedback=st.text_area('Please Give your Feedback')
submit=st.button("Submit")
if submit:
    SSF.get_feedback(name,feedback)
    get_feedback(user_name=name,feedback=feedback)
    st.success('Thank you for your valuable feedback')

try:
    if st.session_state == {}:
        st.session_state['authentication_status'] = ""
except:
    pass

# Admin Panil
try:
    if st.session_state['username']=='praveen':

        selected = option_menu(
            menu_title=None,
            options=['Users','Feedback'],
            icons=["projector-fill","terminal"],
            orientation='horizontal',
            styles={'nav-link':{'font-size':'15px'}})
    
        if selected=="Users":
            df = SSF.get_users_data()
            st.table(df)
    
        elif selected=="Feedback":
            df=SSF.get_feedback_data()
            st.table(df)
            
except:
    pass
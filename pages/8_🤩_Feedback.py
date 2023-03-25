import streamlit_authenticator as stauth
import streamlit as st
from Stocky_DB_2 import credintials,StockyDb,All_other_FX
from streamlit_option_menu import option_menu
from telegram_bot import get_feedback
from yahoo_fin.stock_info import *



SSF=credintials()
SSD=StockyDb()
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
    if st.session_state['username']=='ADMIN USER ID':

        selected = option_menu(
            menu_title=None,
            options=['Users','Feedback','Dash Board'],
            icons=["projector-fill","terminal"],
            orientation='horizontal',
            styles={'nav-link':{'font-size':'15px'}})
    
        if selected=="Users":
            df = SSF.get_users_data()
            st.table(df)
    
        elif selected=="Feedback":
            df=SSF.get_feedback_data()
            st.table(df)

        elif selected=='Dash Board':
            t_select=st.selectbox('Select Ticker',options=SSD.get_all_ticker())
            SAA=All_other_FX()
            new_df= pd.DataFrame(SAA.Dash_board_df(t_select))
            chat_df = new_df[['open','Actual open','close','Actual close','high','Actual high','low','Actual low']]
            st.line_chart(data=chat_df)

            
except:
    pass

import streamlit_authenticator as stauth
import streamlit as st
import Stocky_DB_2
import bcrypt

if st.session_state == {}:
    st.session_state['authentication_status'] = ""

cred = Stocky_DB_2.credintials()
trans = Stocky_DB_2.Portfolio()
STU = Stocky_DB_2.Store_price()

#u_names,u_details = credintials.credintials_get()

#creden = {"usernames":u_details}

credentials= cred.credintials_get()

select=st.radio("",options=('Sing In','Sing Up'))

preauthorized='melsby@gmail.com'
authenticator = stauth.Authenticate(credentials,'some_cookie_name','some_signature_key',30,preauthorized)

if select =='Sing In':

    name, authentication_status, username = authenticator.login('Login', 'main')
    st.session_state.user_name = name

    if authentication_status:
        authenticator.logout('Logout', 'sidebar')
        st.write(f'Welcome *{name}*')
        st.write('For Log Out Please come back here')
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')

    if st.session_state['authentication_status'] == True:
        T_user=st.text_input("Please enter the UserName as per Telegram , To have accsse Stocky AI throught Telegram")
        T_S=st.button('Submit')
        if T_S:
            STU.put_tele_user(T_user,st.session_state['username'])
            st.success("Its Done")


elif select=='Sing Up':
    try:
        if authenticator.register_user('Register user', preauthorization=False):
            user_name = next(iter(reversed(credentials["usernames"])))
            cred.credintials_update(credentials)
            cred.creat_portfolio(user_name)
            trans.Demo_Trans(user_name)
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)
        


import streamlit_authenticator as stauth
import streamlit as st

creden = {"usernames":{'praveen':{'name':'Praveen Kumar','password':'$2b$12$f3FHtJKI64LUWzhPRiEvU.VOQfwzwfy0mVD.JJU6fkYzTbz5AptKu'},'chinnu':{'name':'Chinnu',"passwords":'$2b$12$jwTggAP1K4hHPi9AzAnv4u61F5BrkgeTKGlOo3VOjUKrWh52.lO9q'}}}

with st.form("Register", clear_on_submit=True):
    email=st.text_input("E-mail")
    name=st.text_input("Name")
    user_name=st.text_input("User Name")
    password=st.text_input("Password")
    re_password=st.text_input("Re-enter Password")
    R_submit=st.form_submit_button("Submit")
    if R_submit :
        if len(email) and len(name) and len(user_name) and len(password) > 0:
            if user_name not in creden['usernames'].keys():
                if password == re_password:
                    hash_password = stauth.Hasher(password).generate()
                    creden['usernames']={user_name:{'name':name,'password':hash_password,}}
                    print(creden)
                else:
                    st.warning("Please Enter same password in both Password and Re-enter Password")
            else:
                st.warning("User Name already exist, Please select uniqe User Name")
        else:
            st.warning("Please fill all the details")


    
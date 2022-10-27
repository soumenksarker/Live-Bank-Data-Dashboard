import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import numpy as np
import sqlite3
import time

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)


conn = sqlite3.connect('dat.db')
c=conn.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT,password TEXT)')
def add_userdata(username, password):
    c.execute('INSERT INTO usertable(username, password) VALUES (?,?)',(username, password))
    conn.commit()
def login_user(username, password):
    c.execute('SELECT * FROM usertable WHERE username=? AND password=?', (username, password))
    data = c.fetchall()
    return data
def view_all_users():
    c.execute('SELECT * FROM usertable')
    data = c.fetchall()
    return data
st.subheader("SignUp to get access ...")
choice = option_menu(menu_title=None,
options= ["Login","SignUp"], 
icons=['Houses','book'],
menu_icon="cast",
default_index=0,
#orientation="horizontal"
)

st.title("Simple Chatbot for fun!")
if choice == "Login":
    #st.session_state.history=[]
    st.subheader("Login Section")
    username = st.text_input("User Name")
    password = st.text_input("Password", type='password')
    if st.checkbox("Login"):
        create_usertable()
        result=login_user(username, password)
        if result:
            # read csv from a github repo
            dataset_url = "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv"

            # read csv from a URL
            @st.experimental_memo
            def get_data() -> pd.DataFrame:
                return pd.read_csv(dataset_url)

            df = get_data()

            # dashboard title
            st.title("Real-Time / Live Data Science Dashboard")

            # top-level filters
            job_filter = st.selectbox("Select the Job", pd.unique(df["job"]))

            # creating a single-element container
            placeholder = st.empty()

            # dataframe filter
            df = df[df["job"] == job_filter]

            # near real-time / live feed simulation
            for seconds in range(200):

                df["age_new"] = df["age"] * np.random.choice(range(1, 5))
                df["balance_new"] = df["balance"] * np.random.choice(range(1, 5))

                # creating KPIs
                avg_age = np.mean(df["age_new"])

                count_married = int(
                    df[(df["marital"] == "married")]["marital"].count()
                    + np.random.choice(range(1, 30))
                )

                balance = np.mean(df["balance_new"])

                with placeholder.container():

                    # create three columns
                    kpi1, kpi2, kpi3 = st.columns(3)

                    # fill in those three columns with respective metrics or KPIs
                    kpi1.metric(
                        label="Age ⏳",
                        value=round(avg_age),
                        delta=round(avg_age) - 10,
                    )

                    kpi2.metric(
                        label="Married Count 💍",
                        value=int(count_married),
                        delta=-10 + count_married,
                    )

                    kpi3.metric(
                        label="A/C Balance ＄",
                        value=f"$ {round(balance,2)} ",
                        delta=-round(balance / count_married) * 100,
                    )

                    # create two columns for charts
                    fig_col1, fig_col2 = st.columns(2)
                    with fig_col1:
                        st.markdown("### First Chart")
                        fig = px.density_heatmap(
                            data_frame=df, y="age_new", x="marital"
                        )
                        st.write(fig)

                    with fig_col2:
                        st.markdown("### Second Chart")
                        fig2 = px.histogram(data_frame=df, x="age_new")
                        st.write(fig2)

                    st.markdown("### Detailed Data View")
                    st.dataframe(df)
                    time.sleep(1)
elif choice == "SignUp":
    st.subheader("Register Here!")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type='password')
    if st.button("SignUp"):
        create_usertable()
        add_userdata(new_user, new_password)
        st.success("You have successfully created a valid Account")
        st.info("Please Login...")

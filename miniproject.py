import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

# Define your password
password = "2401"

# Sidebar menu
menu = st.sidebar.radio("Menu", ["Home", "Prediction Price"])

# Password protection
st.image("famous-diamonds.jpg", width=500)
st.title("Welcome to Analyst World...")
password_input = st.text_input("Enter Password:", type="password")
access_granted = False  # Initialize access as denied

if password_input == password:
    st.success("Access granted.")
    access_granted = True  # Set access as granted

if access_granted:
    if menu == "Home":

        # Set the title of your Streamlit app
        st.title("Excel/CSV File Viewer")

        # Create a file uploader widget to allow users to upload files
        uploaded_file_home = st.file_uploader("Upload a CSV or Excel file (Home)", type=["csv", "xlsx"])

        # Check if a file has been uploaded
        if uploaded_file_home is not None:
            if uploaded_file_home.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                # Excel file (XLSX)
                df_home = pd.read_excel(uploaded_file_home)
            else:
                # CSV file
                df_home = pd.read_csv(uploaded_file_home)
                st.write(df_home)

        st.header("Statistical Summary Of Dataframe")

        if st.checkbox("Statistics"):
            st.table(df_home.describe())

        if st.checkbox("Correlation Graph"):
            st.subheader("Correlation Graph")
            fig, ax = plt.subplots(figsize=(5, 2.5))
            sns.heatmap(df_home.corr(), annot=True, cmap="coolwarm")
            st.pyplot(fig)

        st.title("Graphs")
        Graph = st.selectbox("Different Types Of Graphs", ["Scatter Plot", "Bar Graph", "Stacked Bar Graph", "Histogram", "Pie Chart"])
        if Graph == "Scatter Plot":
            if "Carat" in df_home.columns and "Price" in df_home.columns:
                value = st.slider("Filter Data Using Carat", 0, 50)
                Data = df_home.loc[df_home["Carat"] >= value]
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.scatterplot(data=Data, x="Carat", y="Price", hue="Cut")
                st.pyplot(fig)
            else:
                st.warning("The 'Carat' column does not exist in the DataFrame.")
        if Graph == "Bar Graph":
            fig, ax = plt.subplots(figsize=(3.5, 2))
            sns.barplot(x="Cut", y=df_home.Cut.index, data=df_home)
            st.pyplot(fig)

        if Graph == "Stacked Bar Graph":
            if "Clarity" in df_home.columns and "Qty" in df_home.columns:
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.barplot(x="Clarity", y="Qty", data=df_home)
                for p in ax.patches:
                    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', fontsize=12, color='black', xytext=(0, 1),
                                textcoords='offset points')
                st.pyplot(fig)
            else:
                st.warning("The 'clarity' or 'Qty' column does not exist in the DataFrame.")

        if Graph == "Histogram":
            if "color" in df_home.columns and "Price" in df_home.columns:
                fig, ax = plt.subplots(figsize=(5, 3))
                sns.histplot(data=df_home, x="color", y="price", bins=10)
                ax.set_xlabel("Color")
                ax.set_ylabel("Price")
                for p in ax.patches:
                    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', fontsize=12, color='black', xytext=(0, 5),
                                textcoords='offset points')
                st.pyplot(fig)
            else:
                st.warning("The 'color' or 'price' column does not exist in the DataFrame.")

        if Graph == "Pie Chart":
            if "Cut" in df_home.columns:
                cut_counts = df_home['Cut'].value_counts()
                fig, ax = plt.subplots()
                ax.pie(cut_counts, labels=cut_counts.index, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                st.pyplot(fig)

    if menu == "Prediction Price":
        st.title("Price Prediction for Diamonds")
        st.title("Excel/CSV File Viewer")
        uploaded_file_prediction = st.file_uploader("Upload a CSV or Excel file (Prediction)", type=["csv", "xlsx"])

        if uploaded_file_prediction is not None:
            if uploaded_file_prediction.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                df_prediction = pd.read_excel(uploaded_file_prediction)
            else:
                df_prediction = pd.read_csv(uploaded_file_prediction)
                st.write(df_prediction)

            lr = LinearRegression()
            x = np.array(df_prediction["carat"]).reshape(-1, 1)
            y = np.array(df_prediction["price"]).reshape(-1, 1)
            lr.fit(x, y)

            st.header("Diamond Price Prediction")

            carat_input = st.number_input("Enter Carat Value (0.10 - 10.0):", 0.10, 10.0, step=0.20)

            if st.button("Predict Price"):
                carat_input = np.array(carat_input).reshape(1, -1)
                predicted_price = lr.predict(carat_input)[0][0]

                # Modify this scaling factor based on your actual data and model
                scaling_factor = 1000
                predicted_price_in_dollars = predicted_price * scaling_factor

                st.success(f"Predicted Price: ${predicted_price_in_dollars:.2f}")

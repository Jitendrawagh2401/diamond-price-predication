import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
from sklearn.linear_model import LinearRegression

# Sidebar menu
menu = st.sidebar.radio("Menu", ["Home", "Predication Price"])

if menu == "Home":
    # Title
    st.title("Web App using Streamlit")

    # Image
    st.image("skyalab.jpg", width=500)

    # Title
    st.title("Case Study on Diamond Dataset")

    # Set the title of your Streamlit app
    st.title("Excel/CSV File Viewer")

    # Create a file uploader widget to allow users to upload files
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Use Pandas to read the data from the uploaded file
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            # Excel file (XLSX)
            df = pd.read_excel(uploaded_file)
        else:
            # CSV file
            df = pd.read_csv(uploaded_file)
            st.write(df)

# Statistical Summary Of Dataframe
    st.header("Statistical Summary Of Dataframe")
    if st.checkbox("Statistics"):
        st.table(df.describe())

    # Correlation graph
    if st.checkbox("Correlation Graph"):
        st.subheader("Correlation Graph")
        fig, ax = plt.subplots(figsize=(5, 2.5))
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
        st.pyplot(fig)
        # Filter out non-numeric columns from the DataFrame
    numeric_df = df.select_dtypes(include=[float, int])

    # Check if the filtered DataFrame is not empty
    if not numeric_df.empty:
        # Create a heatmap for the correlation matrix of the numeric DataFrame
        st.subheader("Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
        st.pyplot(fig)
    else:
        st.warning("No numeric columns found in the DataFrame for correlation analysis.")
    st.title("Graphs")
    Graph = st.selectbox("Different Types Of Graphs", ["Scatter Plot", "Bar Graph","Stacked Bar Graph", "Histogram", "Pie Chart"])
    if Graph == "Scatter Plot":
        if "carat" in df.columns and "price" in df.columns:
            value = st.slider("Filter Data Using Carat", 0, 50)
            Data=df.loc[df["carat"] >= value]
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.scatterplot(data=Data, x="carat", y="price", hue="cut")
            st.pyplot(fig)
        else:
            st.warning("The 'Carat' column does not exist in the DataFrame.")
    if Graph == "Bar Graph":
        fig,ax = plt.subplots(figsize=(3.5,2))
        sns.barplot(x="cut",y=df.cut.index,data=df)
        st.pyplot(fig)

    if Graph == "Stacked Bar Graph":
            if "clarity" in df.columns and "qty" in df.columns:
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.barplot(x="clarity", y="qty", data=df)
                # Add data labels (annotations) to the bars
                for p in ax.patches:
                    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', fontsize=12, color='black', xytext=(0, 5),
                                textcoords='offset points')
                st.pyplot(fig)
            else:
                st.warning("The 'clarity' or 'qty' column does not exist in the DataFrame.")

    if Graph == "Histogram":
         if "color" in df.columns and "price" in df.columns:
                fig, ax = plt.subplots(figsize=(5, 3))
                sns.histplot(data=df, x="color", y="price", bins=10)  # Use appropriate number of bins
                ax.set_xlabel("Color")
                ax.set_ylabel("Price")

                # Add data labels (counts) above each bar
                for p in ax.patches:
                    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', fontsize=12, color='black', xytext=(0, 5),
                                textcoords='offset points')

                st.pyplot(fig)
         else:
                st.warning("The 'color' or 'price' column does not exist in the DataFrame.")

    if Graph == "Pie Chart":
         if "cut" in df.columns:
                # Count the number of occurrences of each category in the 'cut' column
                cut_counts = df['cut'].value_counts()

                # Create a pie chart
                fig, ax = plt.subplots()
                ax.pie(cut_counts, labels=cut_counts.index, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                st.pyplot(fig)
         else:
                st.warning("The 'cut' column does not exist in the DataFrame.")

if menu=="Predication Price":
    st.title("Predication Price of Diamond")

    lr=LinearRegression()
    X=np.array(df["carat"]).reshape(-1,1)
    y=np.array(df["price"]).reshape(-1,1)
    lr.fit (x,y)
    value=st.number_input("carat",0.10,10.0,step=0.20)
    value=np.array(value).reshape(1,-1)
    Predication=lr.predict(value)[0]
    if st.button("Price Predication"):
        st.write(f"{Predication}")

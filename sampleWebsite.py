import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# st.write("hello world")
# st.write({"key": ["value"]})
# st.write("change is added")

st.title("Simple Data Dashboard")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None: # checks if the file is not empty
    df = pd.read_csv(uploaded_file)
    # st.write("File uploaded...")

    st.subheader("Data Preview")
    st.write(df.head(5))

    st.subheader("Data Summary")
    st.write(df.describe())

    st.subheader("Filtered Data")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select column to filter by", columns)
    unique_values = df[selected_column].unique()
    selected_value = st.selectbox("Select value to filter by", unique_values)

    filtered_df = df[df[selected_column] == selected_value]
    st.write(filtered_df)

    st.subheader("Plot Data")
    x_column = st.selectbox("Select x-axis column", columns)
    y_column = st.selectbox("Select y-axis column", columns)

    if st.button("generate lot"): # if the button is pressed
        st.line_chart(filtered_df.set_index(x_column)[y_column])
else:
    st.write("Waiting for file to be uploaded ... ")
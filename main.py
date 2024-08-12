from pymongo import MongoClient
import streamlit as st
# Replace with your MongoDB connection string
client = MongoClient("mongodb+srv://Ayushi:Anuja%40108@cluster0.aikbkzz.mongodb.net/")
db = client["MovieRS"]
collection = db["pklsmov"]

def fetch_data():
    return list(collection.find())

def main():
    st.title("MongoDB Streamlit App")

    # Fetch data from MongoDB
    data = fetch_data()

    # Display data in Streamlit
    st.write("Data from MongoDB:")
    st.write(data[1:10])

if __name__ == "__main__":
    main()
'''
import streamlit as st
from pymongo import MongoClient

# MongoDB connection setup

# Streamlit app
st.title('Insert Data into MongoDB')

# Form to input data
with st.form(key='data_form'):
    name = st.text_input('Name')
    age = st.number_input('Age', min_value=0)
    address = st.text_input('Address')

    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        # Insert data into MongoDB
        data = {
            'name': name,
            'age': age,
            'address': address
        }
        collection.insert_one(data)
        st.success('Data inserted successfully!')

# Optional: Display the data in the collection
st.subheader('Data in Collection:')
data = collection.find()
for doc in data:
    st.write(doc)

'''

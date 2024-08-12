from pymongo import MongoClient
import streamlit as st
# Replace with your MongoDB connection string
@st.cache_resource
def init_connection():
    return MongoClient("mongodb+srv://st.secrets.mongo.username:st.secrets.mongo.password@host/")

client = init_connection()

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
    db = client.MovieRS
    items = db.pklsmov.find()
    items = list(items)  # make hashable for st.cache_data
    return items



def main():
    st.title("MongoDB Streamlit App")

    # Fetch data from MongoDB
    data = get_data()

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

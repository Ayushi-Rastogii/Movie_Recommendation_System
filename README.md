# Movie Recommendation System
The Movie Recommendation System is a project that presents a Disney+ Hotstar clone for the look and feel of the website with enhanced functionality. It provides recommendations based on the selected movie in the "Recommendations for You" section. By clicking on the "More Like This" button, users receive suggestions for movies with similar genres, themes, and ideas. This functionality is powered by a machine learning model over [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) 

## Deployment Link
The project is deployed using **[Vercel](https://vercel.com/)**. You can access the deployed website [here](https://movie-recommendation-system-mou64oicm-ayushi-rastogiis-projects.vercel.app/)

## Technologies Used

- **[HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)**: For designing the structure of frontend website
- **[CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)**: For styling the movie posters and overall layout of the website.
- **[JAVASCRIPT](https://developer.mozilla.org/en-US/docs/Web/JavaScript)**: For providing interactivity to "More like this" button and select box for choosing the movie as input for recommendation system
- **[Flask](https://flask.palletsprojects.com/en/3.0.x/)**: For servicing the requests as the backend web framework.
- **[MongoDB Atlas](https://www.mongodb.com/)**: For servicing the database requests of recommendation system. It stores the processed dataframe created by applying machine learning over the dataset.
- **[Machine Learning](https://www.nltk.org/)**: The project uses text-vectorisation method for assigning values to tags created from TMDB dataset for each record. It then uses cosine-similarity data for the queried movie to determine other closest degree vectors. These vectors are actually the representation of other records in dataset and therefore closest vectors detemine and returns the most similar movies.   

## Installation Instructions

1. **Clone the repository**
   ```bash
    git clone https://github.com/Ayushi-Rastogii/Movie_Recommendation_System.git
   ```
2. **create the virtual environment and install the necessary packages using pip:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Preparing Machine Learning model:**
Run the mlmodel.ipynb file. On running the file, similarity.csv and movies.csv files are created as output.
4. **Setting up MongoDB Atlas:** From Mongodb atlas, get the connection string by logging into cloud mongodb account. The [connection strings](https://www.mongodb.com/docs/manual/reference/connection-string/) can be found using connect->shell->connection string on the landing page of the logged in cloud mongodb. Install [mongosh](https://www.mongodb.com/docs/mongodb-shell/) and run following commands:
   ```bash
   mongosh "mongodb+srv://<username>:<password>@<host address of mongodb cluster >.mongodb.net/"
   ```
5. **Create database and collections:** Run the following commands on terminal to insert all the records from movie.csv and similarity.csv to the collections of MovieRS database, pklsmov,pklsim respectively  :
   ```bash
   mongoimport --uri "mongodb+srv://<username>:<password>@<host address of mongodb cluster >.mongodb.net/MovieRS" --collection pklsmov --type csv --headerline --file </path/to/movie.csv/file>
   mongoimport --uri "mongodb+srv://<username>:<password>@<host address of mongodb cluster >.mongodb.net/MovieRS" --collection pklsim --type csv --headerline --file </path/to/similarity.csv/file>
   ```
6. ** Create .env file:** Save the username and password in following format:
   ```dotenv
   username=<username>
   password=<password>
   ```
7. **Running the app:** Activate virtual environment using **source .venv/bin/activate**, if .venv is not activated. Run the app using following command:
   ```bash
    python run.py
   ```
8. **Testing the recommendation system:** Check the frontend and respective web functionality by clicking on "Running on" link on the terminal. This will redirect to the webpage of Disney+Hotstar clone. Select a movie in right side select box of "Recommendation For You" section and click on "More Like This" to see the posters of the recommended movies under the same section.

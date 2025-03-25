from flask import Flask, render_template, url_for, request
import numpy as numpy
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pandas as pandas
import requests
import pickle


top_20_books = pickle.load(open('top-20-books.pkl', 'rb'))
books_pt = pickle.load(open('books_pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
knn = pickle.load(open('knn.pkl', 'rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", 
                           book_name = list(top_20_books['Book-Title'].values),
                           author=list(top_20_books['Book-Author'].values),
                           image=list(top_20_books['Image-URL-M'].values),
                           rating=list(top_20_books['avg-rating'].values))
    
@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    # Ensure the book exists in books_pt
    if user_input not in books_pt.index:
        print(f"Error: '{user_input}' not found in dataset.")
        return f"Error: '{user_input}' not found in dataset."

    # Store recommendations
    rec_books = []

    # Get nearest neighbors
    distance, book_info = knn.kneighbors([books_pt.loc[user_input]])

    # Extract recommended books and distances, excluding the first one (which is the input book itself)
    recom_book_info = books_pt.iloc[book_info[0][1:]].index.to_list()
    
    data = []
    # Append book names with distances
    for r in zip(recom_book_info):
        item = []
        temp_df = books[books['Book-Title'] == r[0]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)

    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
    
    


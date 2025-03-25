from flask import Flask, render_template, url_for
import pandas as pandas
import pickle


top_20_books = pickle.load(open('top-20-books.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", 
                           book_name = list(top_20_books['Book-Title'].values),
                           author=list(top_20_books['Book-Author'].values),
                           image=list(top_20_books['Image-URL-M'].values),
                           rating=list(top_20_books['avg-rating'].values))

if __name__ == "__main__":
    app.run(debug=True)
    
    


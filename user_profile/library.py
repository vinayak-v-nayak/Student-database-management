
from flask import Flask, render_template, request ,redirect, url_for,flash
import mysql.connector
from flask import Blueprint
from db.db_connect import get_db
import requests


library_route = Blueprint('library', __name__)

mydb=get_db()
mycursor = mydb.cursor()



@library_route.route('/library')
def library():
    # Google Books API endpoint
    api_url = 'https://www.googleapis.com/books/v1/volumes'

    # Get the user's query from the URL parameters
    query = request.args.get('q', 'python')  # Default query is 'python'

    # Set up parameters for the API request
    params = {'q': query}

    # Make the API request
    response = requests.get(api_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract relevant information about each book
        books = []
        for item in data.get('items', []):
            volume_info = item.get('volumeInfo', {})
            title = volume_info.get('title', 'Unknown Title')
            authors = ', '.join(volume_info.get('authors', ['Unknown Author']))
            description = volume_info.get('description', 'No description available')
            thumbnail = volume_info.get('imageLinks', {}).get('thumbnail', '')
            link = volume_info.get('infoLink', '')  # Link to the book
    
            # Create a dictionary for each book
            book = {
                'title': title,
                'authors': authors,
                'description': description,
                'thumbnail': thumbnail,
                'link': link  # Add the link to the book dictionary
            }
            books.append(book)

        # Render the library template with the list of books
        return render_template('library.html', books=books)
    else:
        # If the request was not successful, return an error message
        return f"Error: Unable to fetch books. Status code: {response.status_code}"

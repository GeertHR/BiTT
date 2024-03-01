import webbrowser
from flask import Flask, render_template
from helpfunctions import *

# Start a Flask web environment on localhost, retrieve information from logi.xml_data,
# render HTML in index.html, and display the data.
def display_table_data():
    app = Flask(__name__)

    @app.route('/')
    def display_table():
        # Initialize the cursor to the data warehouse
        db_cursor = OTDWH()

        # Define the SQL query to retrieve data
        query = 'SELECT * FROM logi.xml_data'
        db_cursor.execute(query)
        rows = db_cursor.fetchall()
        db_cursor.close()

        # Prepare the table data for rendering
        table_data = []
        for row in rows:
            table_data.append({
                'ID': row[0],
                'Domain': row[1],
                'ReportName': row[2],
                'ServerName': row[3],
                'PathName': row[4],
                'DateCreated': row[5],
                'DateModified': row[6],
                'ModifiedBy': row[7],
                'DataLayerID': row[8],
                'ConnectionID': row[9],
                'ServerConnection': row[16],
                'Query': row[10],
                'DataHash': row[11],
                'Object': row[12],
                'DateExtracted': row[13],
                'ValidFrom': row[14],
                'ValidTo': row[15]
            })

        # Render the HTML template with the table data
        return render_template('index.html', table_data=table_data)

    return app

if __name__ == '__main__':
    # Open the default web browser to view the application
    webbrowser.open('http://localhost:5000')

    # Start the Flask app to display the table data
    app = display_table_data()
    app.run()
from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load data from the Excel file
excel_file = 'dataframe.xlsx'  # Use the new dummy data file
jobs_data = pd.read_excel(excel_file)

@app.route('/')
def index():
    # Get unique cluster IDs for dropdown
    cluster_ids = jobs_data['Cluster ID'].unique()

    return render_template('index.html', clusters=cluster_ids)

@app.route('/get_table_data', methods=['POST'])
def get_table_data():
    try:
        # Get selected cluster and records per page from the request
        selected_cluster = request.form['selectedCluster']
        records_per_page = request.form['recordsPerPage']

        # Convert to int if necessary
        selected_cluster = int(selected_cluster) if selected_cluster.isdigit() else None
        records_per_page = int(records_per_page) if records_per_page.isdigit() else None

        # Filter data based on selected cluster
        if selected_cluster is not None:
            filtered_data = jobs_data[jobs_data['Cluster ID'] == selected_cluster]
        else:
            filtered_data = jobs_data.copy()  # Show all data if no cluster is selected

        # Get the total number of pages
        total_pages = (len(filtered_data) + records_per_page - 1) // records_per_page

        # Get the current page number from the request
        current_page = int(request.form['currentPage'])

        # Calculate the start and end indices for the current page
        start_index = (current_page - 1) * records_per_page
        end_index = start_index + records_per_page

        # Get data for the current page
        page_data = filtered_data.iloc[start_index:end_index]

        # Convert the page data to a list of dictionaries for easier rendering in the HTML template
        table_data = page_data.to_dict(orient='records')

        # Prepare the response data
        response_data = {
            'tableData': table_data,
            'totalPages': total_pages
        }

        return jsonify(response_data)

    except Exception as e:
        # Handle exceptions and return an error response
        response_data = {
            'error': str(e)
        }
        return jsonify(response_data), 500

@app.route('/job_details', methods=['GET'])
def job_details():
    job_name = request.args.get('Job Name')

    # Retrieve job details from the Excel file (replace this with your actual data retrieval)
    job_details = jobs_data[jobs_data['Job Name'] == job_name].to_dict(orient='records')

    # Prepare the response data
    response_data = {
        'jobDetails': job_details
    }

    return jsonify(response_data)

# New route for the search function
@app.route('/search_function', methods=['POST'])
def search_function():
    try:
        search_term = request.form['searchTerm']

        # Filter data based on the search term (modify this based on your criteria)
        search_results = jobs_data[jobs_data['Job Name'].str.contains(search_term, case=False)]

        # Convert the search results to a list of dictionaries for easier rendering in the HTML template
        search_data = search_results[['Job Name', 'Cluster ID']].to_dict(orient='records')

        # Prepare the response data
        response_data = {
            'searchData': search_data
        }

        return jsonify(response_data)

    except Exception as e:
        # Handle exceptions and return an error response
        response_data = {
            'error': str(e)
        }
        return jsonify(response_data), 500
if __name__ == '__main__':
    app.run(debug=True)

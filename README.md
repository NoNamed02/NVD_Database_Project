<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NVD Project - README</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            max-width: 800px;
            margin: auto;
        }
        h1, h2, h3 {
            color: #333;
        }
        pre, code {
            background-color: #eaeaea;
            padding: 10px;
            border-radius: 5px;
            display: block;
            margin-bottom: 10px;
            overflow-x: auto;
        }
        .code-block {
            background-color: #272822;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            overflow-x: auto;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>NVD Project - README</h1>
    <p>This project is designed to download, parse, and store National Vulnerability Database (NVD) data locally using Python.</p>

    <h2>✅ Features</h2>
    <ul>
        <li>Download NVD JSON data for specific years or a range of years.</li>
        <li>Parse the downloaded data and store it in a SQLite database.</li>
        <li>Display stored data based on severity level (e.g., CRITICAL, HIGH, MEDIUM, LOW).</li>
        <li>Sort and limit data based on publication date.</li>
        <li>Search by specific CVE ID.</li>
    </ul>

    <h2>✅ Requirements</h2>
    <p>Python 3.x and SQLite</p>

    <h3>Required Python Libraries:</h3>
    <pre class="code-block">
pip install requests pandas
    </pre>

    <h2>✅ Directory Structure</h2>
    <pre class="code-block">
nvd_project/
│── env/                   # Virtual environment folder
│── nvd_data.db            # SQLite database file
│── download_and_populate.py # Main script to download and populate the database
│── view_data.py           # Script to view and query data
│── database.py            # Script to create the SQLite database
│── README.html            # Project documentation (HTML)
    </pre>

    <h2>✅ Setup and Installation</h2>
    <p>Clone the repository:</p>
    <pre class="code-block">
git clone &lt;repository-url&gt;
cd nvd_project
    </pre>

    <p>Create and activate a virtual environment:</p>
    <pre class="code-block">
python -m venv env
.\env\Scripts\activate    # Windows
source env/bin/activate   # macOS/Linux
    </pre>

    <p>Install the required libraries:</p>
    <pre class="code-block">
pip install requests pandas
    </pre>

    <p>Create the SQLite database:</p>
    <pre class="code-block">
python database.py
    </pre>

    <h2>✅ Data Download and Population</h2>
    <p>Run the main script to download and populate the NVD data:</p>
    <pre class="code-block">
python download_and_populate.py
    </pre>

    <p>Example Input:</p>
    <pre class="code-block">
Enter start year (e.g., 2002): 2020
Enter end year (e.g., 2023): 2023
    </pre>

    <h2>✅ Viewing Data</h2>
    <p>To query and view the data, run:</p>
    <pre class="code-block">
python view_data.py
    </pre>

    <p>Options:</p>
    <ul>
        <li>1. View all data in ascending order by date.</li>
        <li>2. View all data in descending order by date.</li>
        <li>3. Filter by severity level (CRITICAL, HIGH, MEDIUM, LOW, UNKNOWN).</li>
        <li>4. Limit the number of records displayed.</li>
    </ul>

    <h2>✅ Deleting the Virtual Environment</h2>
    <p>To remove the virtual environment:</p>
    <pre class="code-block">
deactivate
rmdir /S /Q env   # Windows
rm -rf env         # macOS/Linux
    </pre>

    <h2>✅ Future Improvements</h2>
    <ul>
        <li>Implement advanced filtering and search functionalities.</li>
        <li>Add data visualization using matplotlib or seaborn.</li>
        <li>Implement error logging and data validation.</li>
        <li>Optimize the database by adding indexes on key fields.</li>
    </ul>

    <h2>✅ License</h2>
    <p>This project is licensed under the MIT License.</p>
</div>

</body>
</html>

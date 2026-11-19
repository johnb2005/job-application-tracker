# Job Application Tracker

A web-based application developed using **Python, Flask, MySQL, HTML, CSS, and Jinja2** to help users organize job opportunities, track applications, manage professional contacts, and identify jobs that match their technical skills.

The application integrates a relational MySQL database with a Flask backend and a browser-based user interface.

## Features

### 1. Company Management

Supports Create, Read, Update, and Delete (CRUD) operations for companies.

Users can:
- Add companies with their name, industry, website, location, and notes.
- View all companies stored in the database.
- Edit existing company information.
- Delete company records.

### 2. Job Management

Allows users to manage job opportunities associated with companies.

Job records include:
- Job title and associated company
- Job type
- Minimum and maximum salary
- Job posting URL
- Date posted
- Job requirements stored in JSON format

Users can add, view, edit, and delete job records.

### 3. Application Tracking

Tracks job applications and their progress through the hiring process.

Supported application statuses include:
- Applied
- Screening
- Interview
- Offer
- Rejected
- Withdrawn

Each application can store an application date, resume version, cover letter status, and interview information.

Full CRUD functionality is supported.

### 4. Contact Management

Allows users to maintain professional contacts associated with companies.

Contact information includes:
- Contact name
- Company
- Job title
- Email address
- Phone number
- LinkedIn URL
- Notes

Users can add, view, edit, and delete contacts.

### 5. Dashboard

The dashboard provides an overview of job application activity.

It displays:
- Total applications
- Active applications
- Applications in the interview stage
- Applications with offers
- Five most recent applications
- Application counts grouped by status

Dashboard statistics are generated using SQL queries involving aggregate functions, JOIN operations, and GROUP BY.

### 6. Job Matching

The Job Match feature compares user-entered technical skills against requirements stored in the Jobs table.

Users enter their skills as a comma-separated list, and the application:

1. Retrieves job requirements from MySQL.
2. Normalizes skill names for comparison.
3. Identifies matching and missing skills.
4. Calculates a match percentage.
5. Ranks jobs from highest to lowest match.

The matching percentage is calculated using:

**Match Percentage = (Number of Matched Skills / Total Required Skills) × 100**

For example, if a job requires Python, SQL, Flask, and Docker, and the user knows Python, SQL, and Flask, the match percentage is 75%.

The matching algorithm uses Python sets to compare skills and eliminate duplicates.

This is a rule-based matching system rather than a machine learning model.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming and matching logic |
| Flask | Web framework and HTTP request handling |
| MySQL | Relational database |
| MySQL Connector/Python | Database connectivity |
| HTML | Page structure and forms |
| CSS | User interface styling |
| Jinja2 | Dynamic HTML rendering and template inheritance |
| python-dotenv | Loading environment variables |
| Git and GitHub | Version control and source code management |


## Installation and Setup

### Prerequisites

Before running the application, make sure you have:

- Python 3 installed
- MySQL Server installed and running
- Git installed
- A terminal and web browser

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace the placeholder URL with the actual GitHub repository URL.

### Step 2: Create a Virtual Environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

The project uses the following primary dependencies:

- Flask
- mysql-connector-python
- python-dotenv

Additional dependencies are included in `requirements.txt`.

### Step 4: Set Up the MySQL Database

Log in to MySQL using MySQL Workbench or the MySQL command-line client.

Create the database:

```sql
CREATE DATABASE IF NOT EXISTS job_tracker_final;
USE job_tracker_final;
```
execute schema.sql to create the required tables and relationships.

For example, from the project directory:

```bash
mysql -u root -p job_tracker_final < schema.sql
```

Ensure that the schema matches the tables expected by the Flask application.

### Step 5: Configure Environment Variables

Create a `.env` file in the project root.

Configure the database credentials using the environment variable names expected by `database.py`.

For example, if the connection code uses these names:

```dotenv
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=job_tracker_final
```

Replace the example values with your local MySQL configuration.
### Step 6: Run the Application

With the virtual environment activated, execute:

```bash
python app.py
```

Open the following address in your browser:

http://127.0.0.1:5000

If your Flask application does not define a route for `/`, navigate directly to:

http://127.0.0.1:5000/dashboard

## Testing and Validation

The application was developed and tested incrementally.

CRUD operations were tested as each feature was implemented, and database changes were independently verified using MySQL Workbench.

Testing included:
- Adding new database records through HTML forms.
- Retrieving and displaying stored records.
- Updating existing records.
- Deleting records.
- Verifying database changes in MySQL Workbench.
- Checking SQL queries used by the dashboard.
- Testing navigation and form rendering in the browser.
- Reviewing responsive layout and table formatting.

## Future Improvements

Potential enhancements include:

- User authentication and individual user accounts.
- Search and filtering for companies, jobs, and applications.
- Visual charts for application statistics.
- More advanced skill matching using synonyms and weighted requirements.
- Interview reminders and follow-up notifications.
- Deployment to a hosted environment.


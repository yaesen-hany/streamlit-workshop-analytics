# Training Center Data Analysis

A multi-page Streamlit dashboard for monitoring training center operations. It enables program managers to track learner enrollment, evaluate satisfaction scores, and audit operational costs across tracks and cities.

## Table of Contents

1. [Features](#features)
2. [Data Cleaning](#data-cleaning)
3. [Project Structure](#project-structure)
4. [Dataset Requirements](#dataset-requirements)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Calculation Methodology](#calculation-methodology)
8. [Technology Stack](#technology-stack)
9. [Notes](#notes)
10. [License](#license)

## Features

The application consists of four pages, accessible from the sidebar:

- **Overview**: Introduction to the platform, a comparison of raw and cleaned data, executive KPIs (total learners, average rating, total investment), dataset summary, and the calculation methodology.
- **Dataset Explorer**: Interactive filtering by track, city, status, date range, and maximum budget per workshop. Results are displayed as a dataframe, a status count table, and an editable data grid.
- **Insights**: Summary metrics, an attendance trend over time (line chart), a learners comparison by track, city, or status (bar chart), the highest rated track, the city with the most learners, and a list of courses with low ratings or high costs.
- **Feedback**: A form for submitting a name, a rating (1 to 5), and comments. Submissions are stored in the session and displayed in a table.

## Data Cleaning

The `clean_data()` function applies the following steps:

| Step | Description |
|------|-------------|
| Date parsing | Converts the `date` column to datetime format |
| Duplicate removal | Drops duplicate rows and resets the index |
| City | Fills missing values using forward fill |
| Cost, Rating, Learners | Fills missing values with the column median |

## Project Structure

```
.
├── app.py                      # Main Streamlit application
├── training_center_data.csv    # Dataset (required)
├── photo.jpg                   # Image displayed on the Overview page (required)
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Dataset Requirements

The file `training_center_data.csv` must contain at least the following columns:

| Column | Description |
|--------|-------------|
| `date` | Workshop date |
| `city` | City where the workshop took place |
| `cost` | Workshop cost |
| `rating` | Average participant rating (out of 5) |
| `learners` | Number of enrolled learners |
| `status` | Workshop status (e.g., `Ongoing`) |
| `track` | Training track |
| `course` | Course name |

The `status` column is used to count active tracks, which are identified by the value `Ongoing`.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate        # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` file should contain:

   ```
   streamlit
   pandas
   ```

## Usage

Run the application from the project directory:

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`.

## Calculation Methodology

The average rating is calculated across all valid course reviews as follows:

```
Average Rating = Total Ratings / Total Workshops
```

## Technology Stack

- Python
- Streamlit
- Pandas

## Notes

- Feedback entries are stored in `st.session_state` and are cleared when the session ends or the page is refreshed.
- The files `training_center_data.csv` and `photo.jpg` must be located in the same directory as `app.py`.

## License

This project is intended for educational purposes. A license (for example, MIT) may be added if the project is to be distributed publicly.

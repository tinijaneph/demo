from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel

app = FastAPI(title=“Employee Dashboard Agent - Prototype”)

# Initialize Vertex AI

PROJECT_ID = os.getenv(“PROJECT_ID”, “prj-9bb5-hrna-lh-dev-8d1c”)
LOCATION = “us-central1”
vertexai.init(project=PROJECT_ID, location=LOCATION)

# ============================================================================

# SAMPLE DATA - Embedded in Application

# ============================================================================

def get_sample_employees():
“”“Generate sample employee data”””
return pd.DataFrame([
{“employee_id”: “emp001”, “name”: “John Doe”, “age”: 32, “job_title”: “Software Engineer”, “siglum”: “AAB”, “office”: “Herndon”, “hire_date”: “2020-01-15”, “salary”: 85000, “department”: “Engineering”},
{“employee_id”: “emp002”, “name”: “Jane Smith”, “age”: 28, “job_title”: “Data Analyst”, “siglum”: “AAB”, “office”: “Herndon”, “hire_date”: “2021-03-20”, “salary”: 75000, “department”: “Analytics”},
{“employee_id”: “emp003”, “name”: “Mike Johnson”, “age”: 45, “job_title”: “Senior Manager”, “siglum”: “XYZ”, “office”: “Seattle”, “hire_date”: “2015-06-10”, “salary”: 120000, “department”: “Management”},
{“employee_id”: “emp004”, “name”: “Sarah Williams”, “age”: 35, “job_title”: “Product Manager”, “siglum”: “AAB”, “office”: “Herndon”, “hire_date”: “2019-08-05”, “salary”: 95000, “department”: “Product”},
{“employee_id”: “emp005”, “name”: “Tom Brown”, “age”: 29, “job_title”: “Software Engineer”, “siglum”: “DEF”, “office”: “New York”, “hire_date”: “2022-01-10”, “salary”: 82000, “department”: “Engineering”},
{“employee_id”: “emp006”, “name”: “Lisa Garcia”, “age”: 41, “job_title”: “Director”, “siglum”: “AAB”, “office”: “Herndon”, “hire_date”: “2017-04-15”, “salary”: 140000, “department”: “Leadership”},
{“employee_id”: “emp007”, “name”: “David Lee”, “age”: 33, “job_title”: “Data Scientist”, “siglum”: “XYZ”, “office”: “Seattle”, “hire_date”: “2020-09-01”, “salary”: 98000, “department”: “Analytics”},
{“employee_id”: “emp008”, “name”: “Emma Wilson”, “age”: 26, “job_title”: “Junior Developer”, “siglum”: “DEF”, “office”: “New York”, “hire_date”: “2023-02-14”, “salary”: 68000, “department”: “Engineering”},
{“employee_id”: “emp009”, “name”: “Chris Martinez”, “age”: 38, “job_title”: “Senior Engineer”, “siglum”: “AAB”, “office”: “Herndon”, “hire_date”: “2018-07-22”, “salary”: 105000, “department”: “Engineering”},
{“employee_id”: “emp010”, “name”: “Amy Chen”, “age”: 31, “job_title”: “Product Designer”, “siglum”: “DEF”, “office”: “New York”, “hire_date”: “2021-11-03”, “salary”: 88000, “department”: “Design”},
{“employee_id”: “emp011”, “name”: “Robert Taylor”, “age”: 44, “job_title”: “VP Engineering”, “siglum”: “AAB”, “office”: “Herndon”, “hire_date”: “2016-03-12”, “salary”: 165000, “department”: “Leadership”},
{“employee_id”: “emp012”, “name”: “Maria Rodriguez”, “age”: 30, “job_title”: “UX Researcher”, “siglum”: “XYZ”, “office”: “Seattle”, “hire_date”: “2021-05-18”, “salary”: 82000, “department”: “Design”},
{“employee_id”: “emp013”, “name”: “James Anderson”, “age”: 36, “job_title”: “DevOps Engineer”, “siglum”: “DEF”, “office”: “New York”, “hire_date”: “2019-10-25”, “salary”: 92000, “department”: “Engineering”},
{“employee_id”: “emp014”, “name”: “Patricia Moore”, “age”: 39, “job_title”: “HR Manager”, “siglum”: “AAB”, “office”: “Herndon”, “hire_date”: “2018-01-08”, “salary”: 88000, “department”: “HR”},
{“employee_id”: “emp015”, “name”: “Michael White”, “age”: 27, “job_title”: “Marketing Analyst”, “siglum”: “XYZ”, “office”: “Seattle”, “hire_date”: “2022-06-15”, “salary”: 72000, “department”: “Marketing”},
])

def get_sample_time_tracking():
“”“Generate sample time tracking data”””
base_date = datetime.now() - timedelta(days=30)
data = []

```
employees = ["emp001", "emp002", "emp003", "emp004", "emp005", "emp006", "emp007", "emp008", "emp009", "emp010"]
work_types = ["Development", "Meetings", "Analysis", "Planning", "Design", "Management", "Testing"]

for day in range(30):
    current_date = base_date + timedelta(days=day)
    for emp_id in employees:
        if current_date.weekday() < 5:  # Weekdays only
            hours = round(7 + (hash(f"{emp_id}{day}") % 4) * 0.5, 1)  # 7-9 hours
            work_type = work_types[hash(f"{emp_id}{day}") % len(work_types)]
            data.append({
                "employee_id": emp_id,
                "date": current_date.strftime("%Y-%m-%d"),
                "hours": hours,
                "work_type": work_type
            })

return pd.DataFrame(data)
```

# ============================================================================

# HTML FRONTEND

# ============================================================================

@app.get(”/”, response_class=HTMLResponse)
async def home():
“”“Landing page with query interface”””
html_content = “””
<!DOCTYPE html>
<html>
<head>
<title>Employee Dashboard AI Agent - Prototype</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
font-family: ‘Segoe UI’, Tahoma, Geneva, Verdana, sans-serif;
background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
min-height: 100vh;
padding: 20px;
}
.container {
max-width: 1400px;
margin: 0 auto;
}
.header {
text-align: center;
color: white;
margin-bottom: 40px;
}
.header h1 {
font-size: 2.5em;
margin-bottom: 10px;
}
.badge {
display: inline-block;
background: rgba(255, 255, 255, 0.2);
padding: 5px 15px;
border-radius: 20px;
font-size: 0.9em;
margin-top: 10px;
}
.query-box {
background: rgba(255, 255, 255, 0.95);
border-radius: 15px;
padding: 30px;
margin-bottom: 30px;
box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}
.input-group {
display: flex;
gap: 15px;
margin-bottom: 20px;
}
input[type=“text”] {
flex: 1;
padding: 15px 20px;
font-size: 16px;
border: 2px solid #ddd;
border-radius: 8px;
transition: border-color 0.3s;
}
input[type=“text”]:focus {
outline: none;
border-color: #2a5298;
}
button {
padding: 15px 40px;
font-size: 16px;
font-weight: bold;
background: #2a5298;
color: white;
border: none;
border-radius: 8px;
cursor: pointer;
transition: background 0.3s;
}
button:hover {
background: #1e3c72;
}
.examples {
display: flex;
gap: 10px;
flex-wrap: wrap;
}
.example-chip {
padding: 8px 15px;
background: #e8f0fe;
border-radius: 20px;
font-size: 14px;
cursor: pointer;
transition: background 0.3s;
}
.example-chip:hover {
background: #d2e3fc;
}
.dashboard-container {
background: rgba(30, 60, 114, 0.95);
border-radius: 15px;
padding: 30px;
min-height: 400px;
box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}
.loading {
text-align: center;
color: white;
font-size: 18px;
padding: 50px;
}
.spinner {
border: 4px solid rgba(255,255,255,0.3);
border-top: 4px solid white;
border-radius: 50%;
width: 50px;
height: 50px;
animation: spin 1s linear infinite;
margin: 20px auto;
}
@keyframes spin {
0% { transform: rotate(0deg); }
100% { transform: rotate(360deg); }
}
.error {
background: #fee;
color: #c33;
padding: 15px;
border-radius: 8px;
margin-top: 10px;
}
.info-banner {
background: rgba(255, 193, 7, 0.2);
border-left: 4px solid #ffc107;
color: white;
padding: 15px;
border-radius: 5px;
margin-bottom: 20px;
}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>🤖 Employee Dashboard AI Agent</h1>
<p>Ask questions about employee data in natural language</p>
<div class="badge">📊 Prototype Mode - Using Sample Data</div>
</div>

```
        <div class="info-banner">
            <strong>ℹ️ Demo Mode:</strong> This prototype uses sample employee data for demonstration. 
            Real data integration will be added after approval.
        </div>
        
        <div class="query-box">
            <div class="input-group">
                <input type="text" id="queryInput" placeholder="e.g., Show me attrition dashboard or hours worked in Herndon office" />
                <button onclick="generateDashboard()">Generate Dashboard</button>
            </div>
            
            <div class="examples">
                <strong style="margin-right: 10px;">Try these:</strong>
                <span class="example-chip" onclick="setQuery('Show me attrition dashboard')">📊 Attrition dashboard</span>
                <span class="example-chip" onclick="setQuery('Hours worked in Herndon office')">⏰ Hours in Herndon</span>
                <span class="example-chip" onclick="setQuery('Employee demographics by office')">👥 Demographics</span>
                <span class="example-chip" onclick="setQuery('Show AAB siglum statistics')">📈 AAB stats</span>
                <span class="example-chip" onclick="setQuery('Compare offices')">🔍 Compare offices</span>
                <span class="example-chip" onclick="setQuery('Show engineering department')">💻 Engineering team</span>
            </div>
        </div>
        
        <div id="dashboardContainer" class="dashboard-container">
            <div style="text-align: center; color: rgba(255,255,255,0.6); padding: 100px 20px;">
                <h2 style="margin-bottom: 15px;">👆 Enter a query above to get started</h2>
                <p>The AI will analyze your request and generate an appropriate dashboard</p>
                <p style="margin-top: 20px; font-size: 0.9em;">
                    Sample dataset includes: 15 employees across 3 offices (Herndon, Seattle, New York)<br>
                    with 30 days of time tracking data
                </p>
            </div>
        </div>
    </div>

    <script>
        function setQuery(text) {
            document.getElementById('queryInput').value = text;
        }
        
        async function generateDashboard() {
            const query = document.getElementById('queryInput').value;
            if (!query) {
                alert('Please enter a query');
                return;
            }
            
            const container = document.getElementById('dashboardContainer');
            container.innerHTML = '<div class="loading"><div class="spinner"></div>Analyzing your query and generating dashboard...</div>';
            
            try {
                const response = await fetch('/generate-dashboard', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    container.innerHTML = `<div class="error">Error: ${data.error}</div>`;
                } else {
                    container.innerHTML = data.html;
                }
            } catch (error) {
                container.innerHTML = `<div class="error">Error: ${error.message}</div>`;
            }
        }
        
        document.getElementById('queryInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                generateDashboard();
            }
        });
    </script>
</body>
</html>
"""
return HTMLResponse(content=html_content)
```

@app.post(”/generate-dashboard”)
async def generate_dashboard(request: Request):
“”“Main endpoint that processes natural language query”””
try:
body = await request.json()
user_query = body.get(“query”, “”)

```
    # Step 1: Parse query using Gemini
    parsed_query = await parse_query_with_ai(user_query)
    
    # Step 2: Get sample data
    employees_df = get_sample_employees()
    time_df = get_sample_time_tracking()
    
    # Step 3: Filter and process data based on query
    filtered_data = filter_data(parsed_query, employees_df, time_df)
    
    # Step 4: Generate dashboard visualizations
    dashboard_html = generate_dashboard_html(parsed_query, filtered_data)
    
    return JSONResponse(content={
        "success": True,
        "html": dashboard_html,
        "query_interpretation": parsed_query
    })
    
except Exception as e:
    return JSONResponse(content={
        "error": str(e)
    }, status_code=500)
```

async def parse_query_with_ai(user_query: str) -> dict:
“”“Use Gemini to understand user intent”””

```
model = GenerativeModel("gemini-1.5-flash-002")

prompt = f"""You are an AI assistant that interprets employee data queries.
```

User Query: “{user_query}”

Available data:

- employees: employee_id, name, age, job_title, siglum, office, hire_date, salary, department
- time_tracking: employee_id, date, hours, work_type

Available offices: Herndon, Seattle, New York
Available siglums: AAB, XYZ, DEF
Available departments: Engineering, Analytics, Management, Product, Leadership, Design, HR, Marketing

Parse this query and return ONLY a JSON object (no markdown, no explanation) with:
{{
“dashboard_type”: “attrition” | “hours” | “demographics” | “department” | “general”,
“filters”: {{“office”: “value”, “siglum”: “value”, “department”: “value”, etc}},
“focus”: “brief description of what to show”
}}

Examples:
“Show me attrition dashboard” -> {{“dashboard_type”: “attrition”, “filters”: {{}}, “focus”: “employee turnover and tenure”}}
“Hours worked in Herndon” -> {{“dashboard_type”: “hours”, “filters”: {{“office”: “Herndon”}}, “focus”: “time tracking in Herndon”}}
“Engineering department” -> {{“dashboard_type”: “department”, “filters”: {{“department”: “Engineering”}}, “focus”: “engineering team overview”}}
“””

```
response = model.generate_content(prompt)
result_text = response.text.strip()

# Remove markdown code blocks if present
if result_text.startswith("```"):
    result_text = result_text.split("```")[1]
    if result_text.startswith("json"):
        result_text = result_text[4:]

return json.loads(result_text.strip())
```

def filter_data(parsed_query: dict, employees_df: pd.DataFrame, time_df: pd.DataFrame) -> dict:
“”“Filter data based on parsed query”””

```
filters = parsed_query.get("filters", {})

# Filter employees
filtered_employees = employees_df.copy()
for key, value in filters.items():
    if key in filtered_employees.columns:
        filtered_employees = filtered_employees[filtered_employees[key] == value]

# Filter time tracking
employee_ids = filtered_employees['employee_id'].tolist()
filtered_time = time_df[time_df['employee_id'].isin(employee_ids)]

return {
    "employees": filtered_employees,
    "time_tracking": filtered_time
}
```

def generate_dashboard_html(parsed_query: dict, data: dict) -> str:
“”“Generate HTML with Plotly charts”””

```
dashboard_type = parsed_query.get("dashboard_type", "general")
employees_df = data["employees"]
time_df = data["time_tracking"]

figures = []

if employees_df.empty:
    return """
    <div style="color: white; text-align: center; padding: 50px;">
        <h2>No data found for this query</h2>
        <p>Try adjusting your filters or query</p>
    </div>
    """

if dashboard_type == "attrition":
    # Calculate tenure
    employees_df['hire_date'] = pd.to_datetime(employees_df['hire_date'])
    employees_df['tenure_years'] = (datetime.now() - employees_df['hire_date']).dt.days / 365.25
    
    # Employee count by office
    fig1 = go.Figure(data=[
        go.Bar(
            x=employees_df.groupby('office').size().index,
            y=employees_df.groupby('office').size().values,
            marker_color='rgba(100, 200, 255, 0.8)',
            name='Employee Count'
        )
    ])
    fig1.update_layout(
        title="Employees by Office",
        paper_bgcolor='rgba(30, 60, 114, 0.8)',
        plot_bgcolor='rgba(20, 40, 80, 0.5)',
        font=dict(color='white', size=14),
        height=400,
        xaxis_title="Office",
        yaxis_title="Count"
    )
    figures.append(fig1.to_html(full_html=False, include_plotlyjs='cdn'))
    
    # Distribution by siglum (pie chart)
    siglum_counts = employees_df['siglum'].value_counts()
    fig2 = go.Figure(data=[
        go.Pie(
            labels=siglum_counts.index,
            values=siglum_counts.values,
            hole=0.4,
            marker=dict(colors=['#5DADE2', '#85C1E9', '#AED6F1', '#D6EAF8'])
        )
    ])
    fig2.update_layout(
        title="Distribution by Siglum",
        paper_bgcolor='rgba(30, 60, 114, 0.8)',
        font=dict(color='white', size=14),
        height=400
    )
    figures.append(fig2.to_html(full_html=False, include_plotlyjs=False))
    
    # Average tenure by office
    tenure_by_office = employees_df.groupby('office')['tenure_years'].mean()
    fig3 = go.Figure(data=[
        go.Bar(
            x=tenure_by_office.index,
            y=tenure_by_office.values,
            marker_color='rgba(255, 180, 100, 0.8)',
            name='Avg Tenure (Years)'
        )
    ])
    fig3.update_layout(
        title="Average Tenure by Office",
        paper_bgcolor='rgba(30, 60, 114, 0.8)',
        plot_bgcolor='rgba(20, 40, 80, 0.5)',
        font=dict(color='white', size=14),
        height=400,
        xaxis_title="Office",
        yaxis_title="Years"
    )
    figures.append(fig3.to_html(full_html=False, include_plotlyjs=False))
    
elif dashboard_type == "hours":
    if not time_df.empty:
        # Total hours by employee
        hours_by_emp = time_df.groupby('employee_id')['hours'].sum().sort_values(ascending=False).head(10)
        emp_names = employees_df.set_index('employee_id').loc[hours_by_emp.index]['name']
        
        fig1 = go.Figure(data=[
            go.Bar(
                x=emp_names.values,
                y=hours_by_emp.values,
                marker_color='rgba(100, 200, 255, 0.8)'
            )
        ])
        fig1.update_layout(
            title=f"Top 10 Employees by Hours Worked (Last 30 Days)",
            paper_bgcolor='rgba(30, 60, 114, 0.8)',
            plot_bgcolor='rgba(20, 40, 80, 0.5)',
            font=dict(color='white', size=14),
            height=500,
            xaxis_title="Employee",
            yaxis_title="Total Hours"
        )
        figures.append(fig1.to_html(full_html=False, include_plotlyjs='cdn'))
        
        # Hours by work type
        hours_by_type = time_df.groupby('work_type')['hours'].sum().sort_values(ascending=False)
        fig2 = go.Figure(data=[
            go.Pie(
                labels=hours_by_type.index,
                values=hours_by_type.values,
                marker=dict(colors=px.colors.sequential.Blues)
            )
        ])
        fig2.update_layout(
            title="Hours Distribution by Work Type",
            paper_bgcolor='rgba(30, 60, 114, 0.8)',
            font=dict(color='white', size=14),
            height=400
        )
        figures.append(fig2.to_html(full_html=False, include_plotlyjs=False))
    
elif dashboard_type == "demographics" or dashboard_type == "department":
    # Age distribution
    fig1 = go.Figure(data=[
        go.Histogram(
            x=employees_df['age'],
            marker_color='rgba(100, 200, 255, 0.8)',
            nbinsx=10
        )
    ])
    fig1.update_layout(
        title="Age Distribution",
        paper_bgcolor='rgba(30, 60, 114, 0.8)',
        plot_bgcolor='rgba(20, 40, 80, 0.5)',
        font=dict(color='white', size=14),
        height=400,
        xaxis_title="Age",
        yaxis_title="Count"
    )
    figures.append(fig1.to_html(full_html=False, include_plotlyjs='cdn'))
    
    # Employees by department
    dept_counts = employees_df['department'].value_counts()
    fig2 = go.Figure(data=[
        go.Bar(
            x=dept_counts.index,
            y=dept_counts.values,
            marker_color='rgba(100, 200, 255, 0.8)'
        )
    ])
    fig2.update_layout(
        title="Employees by Department",
        paper_bgcolor='rgba(30, 60, 114, 0.8)',
        plot_bgcolor='rgba(20, 40, 80, 0.5)',
        font=dict(color='white', size=14),
        height=400,
        xaxis_title="Department",
        yaxis_title="Count"
    )
    figures.append(fig2.to_html(full_html=False, include_plotlyjs=False))

else:  # general
    # Office distribution
    office_counts = employees_df['office'].value_counts()
    fig = px.bar(
        x=office_counts.index,
        y=office_counts.values,
        title="Employee Distribution by Office"
    )
    fig.update_layout(
        paper_bgcolor='rgba(30, 60, 114, 0.8)',
        plot_bgcolor='rgba(20, 40, 80, 0.5)',
        font=dict(color='white', size=14),
        height=500,
        xaxis_title="Office",
        yaxis_title="Count"
    )
    figures.append(fig.to_html(full_html=False, include_plotlyjs='cdn'))

# Combine all figures
charts_html = "\n".join(figures)

# Summary stats
stats_html = f"""
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px;">
    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; text-align: center;">
        <h3 style="color: #5DADE2; font-size: 2.5em; margin-bottom: 10px;">{len(employees_df)}</h3>
        <p style="color: white;">Employees</p>
    </div>
    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; text-align: center;">
        <h3 style="color: #85C1E9; font-size: 2.5em; margin-bottom: 10px;">{employees_df['office'].nunique()}</h3>
        <p style="color: white;">Offices</p>
    </div>
    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; text-align: center;">
        <h3 style="color: #AED6F1; font-size: 2.5em; margin-bottom: 10px;">{employees_df['department'].nunique()}</h3>
        <p style="color: white;">Departments</p>
    </div>
    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; text-align: center;">
        <h3 style="color: #D6EAF8; font-size: 2.5em; margin-bottom: 10px;">${employees_df['salary'].mean():,.0f}</h3>
        <p style="color: white;">Avg Salary</p>
    </div>
</div>
"""

return f"""
<div style="color: white;">
    <h2 style="margin-bottom: 20px; text-align: center;">
        📊 {parsed_query.get('focus', 'Dashboard').title()}
    </h2>
    
    {stats_html}
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 20px;">
        {charts_html}
    </div>
    
    <div style="margin-top: 30px; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 10px;">
        <h3>📝 Query Interpretation:</h3>
        <pre style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 5px; overflow:
```

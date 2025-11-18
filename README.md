https://claude.ai/public/artifacts/1b9917c7-4002-4d56-9d8a-163f3de95d54

# Employee Dashboard AI Agent

## Complete Deployment Guide - 3 Hour Timeline

**Project Goal:** Build an AI-powered dashboard agent that interprets natural language queries and generates interactive employee data visualizations.

**Total Time:** 3 Hours  
**Cost:** ~$5-10 for testing (free tier covers most)  
**Result:** Live web application with URL to share

-----

## Prerequisites

- ✅ Google Cloud account (create at https://cloud.google.com)
- ✅ Employee data files ready (CSV or Excel format)
- ✅ Chrome or Firefox browser
- ✅ No local installation needed - everything in cloud!

-----

# HOUR 1: Setup & Data Upload (60 minutes)

## Step 1: Create GCP Project (10 minutes)

### 1.1 Access Google Cloud Console

1. Open browser and go to: **https://console.cloud.google.com**
1. Sign in with your Google account
1. If prompted, accept terms of service

### 1.2 Create New Project

1. Click **“Select a project”** dropdown at the top of the page (next to “Google Cloud” logo)
1. Click **“NEW PROJECT”** button (top right of popup)
1. Fill in:
- **Project name:** `employee-dashboard-agent`
- **Location:** Leave as default (or select your organization)
1. Click **“CREATE”** button
1. Wait ~30 seconds for project creation
1. **Important:** Note your Project ID (appears below project name, something like `employee-dashboard-agent-123456`)

### 1.3 Enable Billing (Required)

1. Click hamburger menu (☰) → **“Billing”**
1. If no billing account exists:
- Click **“Link a billing account”**
- Click **“CREATE BILLING ACCOUNT”**
- Enter payment information (won’t be charged in free tier)
1. Link billing account to your project

-----

## Step 2: Enable Required APIs (10 minutes)

### 2.1 Navigate to APIs & Services

1. In the search bar at the very top of the page, type: **“APIs & Services”**
1. Click **“APIs & Services”** from results
1. Click **”+ ENABLE APIS AND SERVICES”** (big blue button at top)

### 2.2 Enable Each API (Do this 5 times, once for each API)

For each API below:

1. Type the API name in the search box
1. Click on the API from results
1. Click **“ENABLE”** button
1. Wait ~10 seconds until it shows “API enabled”
1. Click back arrow to return to API Library

**APIs to Enable:**

1. ✅ **Vertex AI API** (for AI capabilities)
1. ✅ **Cloud Run API** (for deploying application)
1. ✅ **Cloud Build API** (for building container)
1. ✅ **BigQuery API** (for data storage)
1. ✅ **Artifact Registry API** (for container storage)

-----

## Step 3: Open Cloud Shell (5 minutes)

### 3.1 Activate Cloud Shell

1. Look at the top-right corner of the Google Cloud Console
1. Find the **Cloud Shell icon** (looks like `>_` terminal symbol)
1. Click it
1. A terminal window opens at the bottom of your screen
1. Wait ~20 seconds for it to initialize
1. You’ll see a command prompt like: `yourname@cloudshell:~ $`

### 3.2 Set Your Project

In Cloud Shell terminal, type:

```bash
gcloud config set project employee-dashboard-agent
```

(Replace with your actual Project ID if different)

Press Enter. You should see: `Updated property [core/project]`

-----

## Step 4: Create BigQuery Dataset (5 minutes)

### 4.1 Using Cloud Shell Commands

In Cloud Shell terminal, copy and paste:

```bash
# Create the dataset
bq mk --dataset employee_data
```

Press Enter. You should see: `Dataset 'your-project:employee_data' successfully created`

### 4.2 Verify Dataset Creation

1. In the search bar at top, type: **“BigQuery”**
1. Click **“BigQuery”** to open BigQuery Studio
1. In the left panel (Explorer), expand your project name
1. You should see **“employee_data”** dataset listed

-----

## Step 5: Upload Your Data Files (30 minutes)

### 5.1 Prepare Your Data Files

Before uploading, make sure your files:

- ✅ Are in CSV or Excel format
- ✅ Have clear column headers in the first row
- ✅ Have consistent data types in each column
- ✅ Are less than 100MB each (for easy upload)

**Recommended tables to create:**

- `employees` - Employee master data (names, departments, hire dates, etc.)
- `time_tracking` - Hours worked, dates, projects
- `attendance` - Attendance records (optional)
- Any other relevant data you have

### 5.2 Upload Files to BigQuery

**For Each Data File, Follow These Steps:**

#### Method A: Upload via BigQuery Console (Easiest)

1. **Open BigQuery:**
- Search “BigQuery” in top search bar
- Click to open BigQuery Studio
1. **Start Upload:**
- In left panel, find your project → `employee_data` dataset
- Click the **three dots (⋮)** next to `employee_data`
- Select **“Create table”**
1. **Configure Upload:**
- **Source:**
  - Select **“Upload”**
  - Click **“Browse”** button
  - Select your file (e.g., `employees.csv`)
  - **File format:** Select your format (CSV, XLSX, etc.)
- **Destination:**
  - **Project:** (auto-filled)
  - **Dataset:** `employee_data`
  - **Table:** Enter meaningful name (e.g., `employees`, `time_tracking`)
- **Schema:**
  - ✅ Check **“Auto detect”** (BigQuery will figure out columns)
  - OR manually define if you know exact structure
- Click **“CREATE TABLE”** (bottom of page)
1. **Wait for Upload:**
- Progress bar appears
- Takes 10-60 seconds depending on file size
- Success message appears when done
1. **Verify Upload:**
- Click on your new table in left panel
- Click **“PREVIEW”** tab
- You should see your data
1. **Repeat for All Files:**
- Upload each CSV/Excel file as a separate table
- Common tables: `employees`, `time_tracking`, `attendance`, etc.

#### Method B: Upload via Cloud Shell (For Larger Files)

1. **Upload File to Cloud Shell:**
- In Cloud Shell toolbar, click **three dots (⋮)** menu
- Select **“Upload”**
- Choose your CSV file
- Wait for upload (shows progress)
- File is now in your home directory (`~/`)
1. **Load to BigQuery:**
   
   ```bash
   # For CSV files
   bq load \
     --source_format=CSV \
     --autodetect \
     employee_data.employees \
     ~/employees.csv
   
   bq load \
     --source_format=CSV \
     --autodetect \
     employee_data.time_tracking \
     ~/time_tracking.csv
   ```
1. **For Excel Files:**
   
   ```bash
   # Install pandas to convert Excel
   pip3 install pandas openpyxl
   
   # Convert Excel to CSV
   python3 << 'EOF'
   import pandas as pd
   df = pd.read_excel('~/your_file.xlsx')
   df.to_csv('~/converted.csv', index=False)
   EOF
   
   # Then load the CSV
   bq load --source_format=CSV --autodetect \
     employee_data.your_table ~/converted.csv
   ```

### 5.3 Document Your Data Structure

**IMPORTANT:** Write down your table structure for next steps.

For each table you created, note:

```
Table Name: employees
Columns:
- employee_id (STRING)
- name (STRING)
- age (INTEGER)
- job_title (STRING)
- department (STRING)
- siglum (STRING)
- office_location (STRING)
- hire_date (DATE)
- salary (FLOAT)

Table Name: time_tracking
Columns:
- employee_id (STRING)
- date (DATE)
- hours_worked (FLOAT)
- work_type (STRING)
- project_code (STRING)
```

### 5.4 Verify All Data Loaded

In BigQuery, run this query to check:

```sql
-- See all your tables
SELECT table_name, row_count 
FROM employee_data.__TABLES__
```

Click **“RUN”** button. You should see all your tables with row counts.

-----

# HOUR 2: Build Application (60 minutes)

## Step 6: Create Project Structure (10 minutes)

### 6.1 Create Directories in Cloud Shell

In Cloud Shell terminal, run:

```bash
# Create project folders
mkdir -p ~/dashboard-agent/app
cd ~/dashboard-agent

# Verify structure
ls -la
```

### 6.2 Open Cloud Shell Editor

1. In Cloud Shell toolbar, click **“Open Editor”** button (pencil icon)
1. A code editor opens
1. You’ll see your files in left panel
1. Navigate to `dashboard-agent` folder

-----

## Step 7: Create Configuration Files (15 minutes)

### 7.1 Create requirements.txt

1. In Cloud Shell Editor, **right-click** on `dashboard-agent` folder
1. Select **“New File”**
1. Name it: `requirements.txt`
1. Copy and paste this content:

```txt
fastapi==0.104.1
uvicorn==0.24.0
google-cloud-aiplatform==1.38.0
google-cloud-bigquery==3.13.0
plotly==5.18.0
pandas==2.1.3
jinja2==3.1.2
python-multipart==0.0.6
```

1. Save: **Ctrl+S** (Windows/Linux) or **Cmd+S** (Mac)

### 7.2 Create Dockerfile

1. In `dashboard-agent` folder, create new file: `Dockerfile`
1. Copy and paste:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

1. Save the file

-----

## Step 8: Create Main Application (35 minutes)

### 8.1 Create main.py File

1. In Cloud Shell Editor, **right-click** on the `app` folder
1. Select **“New File”**
1. Name it: `main.py`

### 8.2 Customize Application Code for Your Data

**CRITICAL:** You need to update the code to match YOUR data structure.

Use the Python code from the artifact I provided earlier (“AI Dashboard Agent - Main Application”), but make these changes:

#### Find the `parse_query_with_ai` function and update this section:

**BEFORE (example):**

```python
Available data:
- employees table: employee_id, name, age, job_title, siglum, office, hire_date
- time_tracking table: employee_id, date, hours, work_type
```

**AFTER (use YOUR actual columns):**

```python
Available data:
- employees table: [LIST YOUR ACTUAL COLUMNS]
- time_tracking table: [LIST YOUR ACTUAL COLUMNS]
- [ANY OTHER TABLES YOU HAVE]
```

#### Update the SQL queries in `fetch_data_from_bigquery` function:

Replace table names and column names with YOUR actual structure.

For example, if your employee table has `department` instead of `siglum`, change:

```python
# FROM:
e.siglum

# TO:
e.department
```

### 8.3 Complete main.py Content

Copy the full application code, make your customizations, and paste into `main.py`.

**Key sections to customize:**

1. Line ~90: Update `Available data` with your actual columns
1. Line ~150-200: Update SQL queries with your table/column names
1. Line ~250-300: Update filters to match your data categories

### 8.4 Save and Verify

1. Save `main.py`: **Ctrl+S** or **Cmd+S**
1. In Cloud Shell terminal, verify file exists:
   
   ```bash
   ls -la ~/dashboard-agent/app/main.py
   ```
1. Check syntax (should show no errors):
   
   ```bash
   python3 -m py_compile ~/dashboard-agent/app/main.py
   ```

-----

# HOUR 3: Deploy & Test (60 minutes)

## Step 9: Build Docker Container (15 minutes)

### 9.1 Navigate to Project Directory

In Cloud Shell terminal:

```bash
cd ~/dashboard-agent
```

### 9.2 Get Project ID

```bash
export PROJECT_ID=$(gcloud config get-value project)
echo "Project ID: $PROJECT_ID"
```

Copy your Project ID - you’ll need it!

### 9.3 Create Artifact Registry Repository

```bash
gcloud artifacts repositories create dashboard-agent \
  --repository-format=docker \
  --location=us-central1 \
  --description="Dashboard Agent Docker Repository"
```

Wait for: `Created repository [dashboard-agent]`

### 9.4 Build Container Image

**This takes 7-10 minutes - be patient!**

```bash
gcloud builds submit \
  --tag us-central1-docker.pkg.dev/$PROJECT_ID/dashboard-agent/agent:v1 \
  --timeout=20m
```

You’ll see:

- Uploading files
- Building steps (Step 1/X, Step 2/X…)
- Final message: `SUCCESS`

☕ **Get coffee while this runs!**

### 9.5 Troubleshooting Build Errors

**If build fails:**

1. **Check file structure:**
   
   ```bash
   ls -la ~/dashboard-agent/
   # Should show: Dockerfile, requirements.txt, app/
   
   ls -la ~/dashboard-agent/app/
   # Should show: main.py
   ```
1. **Check Python syntax:**
   
   ```bash
   python3 -m py_compile ~/dashboard-agent/app/main.py
   ```
1. **View detailed error logs:**
- Click the Cloud Build link in the error message
- OR go to: Cloud Console → “Cloud Build” → “History”
- Click on failed build to see details

-----

## Step 10: Deploy to Cloud Run (10 minutes)

### 10.1 Deploy Application

In Cloud Shell terminal:

```bash
gcloud run deploy dashboard-agent \
  --image us-central1-docker.pkg.dev/$PROJECT_ID/dashboard-agent/agent:v1 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=$PROJECT_ID \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10
```

### 10.2 Confirm Deployment Settings

You’ll be asked:

- **Allow unauthenticated invocations?** Type: `y` (yes)

Wait ~2-3 minutes for deployment.

### 10.3 Get Your Application URL

When complete, you’ll see:

```
Service [dashboard-agent] revision [dashboard-agent-00001-xxx] has been deployed
Service URL: https://dashboard-agent-xxxxx-uc.a.run.app
```

**🎉 COPY THIS URL!** This is your live application!

### 10.4 Alternative: Get URL Anytime

```bash
gcloud run services describe dashboard-agent \
  --region us-central1 \
  --format='value(status.url)'
```

-----

## Step 11: Test Your Prototype (20 minutes)

### 11.1 Open Your Application

1. **Open the Service URL** in a new browser tab
1. You should see the landing page with:
- Title: “🤖 Employee Dashboard AI Agent”
- Search box
- Example queries

### 11.2 Test Queries

Try these queries based on YOUR data:

**Basic Queries:**

- “Show me attrition dashboard”
- “Employee demographics by office”
- “Show me [YOUR_OFFICE_NAME] office statistics”

**Filtered Queries:**

- “Hours worked in [YOUR_LOCATION]”
- “Show [YOUR_SIGLUM/DEPARTMENT] employees”
- “Time tracking for [YOUR_CATEGORY]”

**Custom Queries:**

- “Compare [LOCATION_A] vs [LOCATION_B]”
- “Show trends by [YOUR_FIELD]”

### 11.3 What to Look For

✅ **Success indicators:**

- Query is interpreted correctly (check “Query Interpretation” section)
- Visualizations appear (charts, graphs)
- Data matches your uploaded files
- No error messages

❌ **If you see errors:**

- Note the error message
- Check logs (see troubleshooting below)

### 11.4 Take Screenshots for Demo

Capture:

1. Landing page
1. Example query + resulting dashboard
1. Different dashboard types
1. Query interpretation section (shows AI understanding)

-----

## Step 12: Troubleshooting (15 minutes)

### 12.1 View Application Logs

**In Cloud Shell:**

```bash
# View recent logs
gcloud run services logs read dashboard-agent \
  --region us-central1 \
  --limit 50
```

**In Console:**

1. Go to: Cloud Run → Services → dashboard-agent
1. Click **“LOGS”** tab
1. Look for errors in red

### 12.2 Common Issues & Fixes

#### Issue: “Permission denied” errors

**Fix:** Grant permissions to service account

```bash
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID \
  --format='value(projectNumber)')

# Grant BigQuery access
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/bigquery.dataViewer"

# Grant Vertex AI access
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/aiplatform.user"

# Redeploy
gcloud run services update dashboard-agent --region us-central1
```

#### Issue: “Table not found” errors

**Fix:** Check table names in your code match BigQuery

```bash
# List your actual tables
bq ls employee_data

# Update main.py with correct table names
# Then rebuild and redeploy
```

#### Issue: “Model not found” (Vertex AI)

**Fix:** Change to a different model

1. Edit `app/main.py`
1. Find line: `model = GenerativeModel("gemini-1.5-flash-002")`
1. Change to: `model = GenerativeModel("gemini-pro")`
1. Rebuild and redeploy:
   
   ```bash
   gcloud builds submit \
     --tag us-central1-docker.pkg.dev/$PROJECT_ID/dashboard-agent/agent:v1
   
   gcloud run deploy dashboard-agent \
     --image us-central1-docker.pkg.dev/$PROJECT_ID/dashboard-agent/agent:v1 \
     --region us-central1
   ```

#### Issue: Application is slow or times out

**Fix:** Increase resources

```bash
gcloud run services update dashboard-agent \
  --region us-central1 \
  --memory 4Gi \
  --cpu 4 \
  --timeout 540
```

#### Issue: BigQuery queries fail

**Fix:** Test queries directly in BigQuery

1. Go to BigQuery console
1. Test your queries manually
1. Fix any SQL errors
1. Update main.py with corrected queries

### 12.3 Redeploy After Fixes

Whenever you make code changes:

```bash
cd ~/dashboard-agent

# Rebuild
gcloud builds submit \
  --tag us-central1-docker.pkg.dev/$PROJECT_ID/dashboard-agent/agent:v1

# Redeploy
gcloud run deploy dashboard-agent \
  --image us-central1-docker.pkg.dev/$PROJECT_ID/dashboard-agent/agent:v1 \
  --region us-central1
```

-----

# Post-Deployment: Prepare for Demo

## Step 13: Create Demo Materials

### 13.1 Document Your Prototype

Create a one-page summary:

**What We Built:**

- AI-powered dashboard generator
- Natural language query interface
- Real employee data integration
- Professional visualizations

**Tech Stack:**

- Google Cloud Platform
- Vertex AI (Gemini) for NLP
- BigQuery for data warehouse
- Cloud Run for serverless hosting
- Python + FastAPI backend

**Capabilities Demonstrated:**

- Query interpretation
- Dynamic SQL generation
- Multi-dashboard types
- Filtered analysis
- Real-time visualization

### 13.2 Prepare Demo Script

**Opening (1 minute):**
“Currently, creating HR dashboards requires technical SQL knowledge and manual report building. Let me show you a solution…”

**Demo Flow (5 minutes):**

1. Open application URL
1. Show query box: “This accepts natural language”
1. Type: “Show me attrition dashboard”
1. Highlight:
- AI interpretation
- Automatic query generation
- Instant visualization
1. Try filtered query: “Hours worked in Herndon office”
1. Show customization: “Compare departments”

**Closing (2 minutes):**
“This prototype demonstrates feasibility. With full development, we can:

- Connect directly to MyPulse (no uploads)
- Add 20+ dashboard types
- Implement role-based access
- Schedule automated reports
- Export to PDF/PowerPoint”

### 13.3 Anticipated Questions

**Q: How accurate is the AI?**
A: Show the “Query Interpretation” section - it explains its understanding. We can fine-tune prompts for 95%+ accuracy.

**Q: Can it handle complex queries?**
A: Yes - demonstrate multi-filter query like “Show AAB employees in Herndon with over 40 hours”

**Q: What about data security?**
A: All data stays in our GCP project. We can add:

- Row-level security
- Role-based access control
- Audit logging
- Data masking for sensitive fields

**Q: How much will full implementation cost?**
A: Estimate ~$200-500/month for production (scales with usage)

**Q: Can we add more data sources?**
A: Yes - we can connect: MyPulse, Workday, ADP, custom databases, Excel files, etc.

-----

# Expansion Roadmap

## Phase 1: Enhanced Prototype (Month 1)

- Connect to MyPulse API
- Add 10 pre-built dashboard templates
- Implement user authentication
- Add export to PDF

## Phase 2: Production Ready (Month 2-3)

- Role-based access control
- Scheduled dashboard delivery
- Email alerts for anomalies
- Historical trend analysis
- Mobile responsive design

## Phase 3: Advanced Features (Month 4-6)

- Predictive analytics
- Natural language insights
- Recommendation engine
- Integration with Slack/Teams
- Custom dashboard builder

## Phase 4: Enterprise Scale (Month 6+)

- Multi-tenant architecture
- Data governance framework
- Advanced security compliance
- API for other systems
- White-label options

-----

# Cost Breakdown

## Prototype Phase (Current)

- **BigQuery:** Free tier (1TB queries/month)
- **Cloud Run:** Free tier (2M requests/month)
- **Vertex AI:** ~$0.001 per query
- **Storage:** ~$1/month
- **Estimated Total:** $5-20/month for testing

## Production Phase (After Deployment)

- **BigQuery:** ~$50-100/month (depends on data size)
- **Cloud Run:** ~$50-150/month (scales with users)
- **Vertex AI:** ~$50-100/month (query volume)
- **Monitoring/Logging:** ~$20/month
- **Estimated Total:** $200-500/month

-----

# Maintenance & Updates

## Daily Monitoring

1. Check Cloud Run logs for errors
1. Monitor query response times
1. Review user feedback

## Weekly Tasks

1. Review most common queries
1. Add new query patterns if needed
1. Update dashboard templates
1. Check data freshness

## Monthly Updates

1. Update to latest Gemini model
1. Optimize BigQuery queries
1. Review costs and usage
1. Implement user feature requests

-----

# Support & Resources

## GCP Documentation

- **BigQuery:** https://cloud.google.com/bigquery/docs
- **Cloud Run:** https://cloud.google.com/run/docs
- **Vertex AI:** https://cloud.google.com/vertex-ai/docs

## Getting Help

1. **Cloud Console Support:** Click “?” icon → “Support”
1. **Community:** https://stackoverflow.com/questions/tagged/google-cloud-platform
1. **Status:** https://status.cloud.google.com

## Useful Commands Reference

```bash
# View service status
gcloud run services describe dashboard-agent --region us-central1

# View logs
gcloud run services logs read dashboard-agent --region us-central1

# Update service
gcloud run services update dashboard-agent --region us-central1

# Delete service (cleanup)
gcloud run services delete dashboard-agent --region us-central1

# View BigQuery tables
bq ls employee_data

# Query data
bq query --use_legacy_sql=false 'SELECT * FROM employee_data.employees LIMIT 10'

# Check costs
gcloud billing accounts list
```

-----

# Success Checklist

## Before Demo

- ✅ Application URL accessible
- ✅ All test queries work
- ✅ Screenshots captured
- ✅ Demo script prepared
- ✅ Questions anticipated
- ✅ Backup plan ready (show screenshots if live demo fails)

## During Demo

- ✅ Explain problem statement clearly
- ✅ Show live application
- ✅ Demonstrate multiple query types
- ✅ Highlight AI interpretation
- ✅ Discuss expansion possibilities
- ✅ Address security/cost questions

## After Demo

- ✅ Gather feedback
- ✅ Document requested features
- ✅ Create project timeline
- ✅ Estimate full development cost
- ✅ Plan Phase 1 implementation

-----

# Quick Reference Card

## Your Application Details

**Project ID:** ________________________

**Service URL:** ________________________

**Region:** us-central1

**BigQuery Dataset:** employee_data

**Tables Created:**

- -----
- -----
- -----

## Key Commands

**View logs:**

```bash
gcloud run services logs read dashboard-agent --region us-central1
```

**Redeploy:**

```bash
cd ~/dashboard-agent
gcloud builds submit --tag us-central1-docker.pkg.dev/$PROJECT_ID/dashboard-agent/agent:v1
gcloud run deploy dashboard-agent --image us-central1-docker.pkg.dev/$PROJECT_ID/dashboard-agent/agent:v1 --region us-central1
```

**Check data:**

```bash
bq query --use_legacy_sql=false 'SELECT COUNT(*) FROM employee_data.employees'
```

-----

# Congratulations! 🎉

You’ve successfully built and deployed an AI-powered dashboard agent!

**What you’ve accomplished:**
✅ Built a cloud-native application
✅ Integrated AI/ML capabilities
✅ Created interactive visualizations
✅ Deployed to production environment
✅ Demonstrated enterprise feasibility

**Next steps:**

1. Demo to stakeholders
1. Gather requirements
1. Plan full implementation
1. Scale to production

-----

**Document Version:** 1.0  
**Last Updated:** November 2024  
**Author:** Claude (Anthropic)  
**Support Contact:** [Your contact information]

-----

# Notes Section

Use this space to track your customizations and learnings:

**My Data Structure:**

```
[Write your table schemas here]
```

**Custom Queries That Work Well:**

```
[Document successful queries]
```

**Issues Encountered:**

```
[Track problems and solutions]
```

**Feature Requests:**

```
[Note what stakeholders want to add]
```

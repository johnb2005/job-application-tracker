from flask import Flask, render_template, request, redirect, url_for, flash
from database import JobTrackerDB
from mysql.connector import Error
import json

app = Flask(__name__)
app.secret_key = "development-only-change-me"


@app.route("/companies", methods=["GET", "POST"])
def companies():
    db = JobTrackerDB()

    if not db.connect():
        return "Database connection failed", 500

    try:
        if request.method == "POST":

            company_name = request.form.get("company_name", "").strip()
            industry = request.form.get("industry", "").strip()
            website = request.form.get("website", "").strip()
            city = request.form.get("city", "").strip()
            state = request.form.get("state", "").strip()
            notes = request.form.get("notes", "").strip()

            # Validate required fields
            if not company_name:
                flash("Company name is required.")
                return redirect(url_for("companies"))

            # Insert the new company
            db.add_company(
                company_name,
                industry,
                website,
                city,
                state,
                notes
            )

            flash("Company added successfully!")
            return redirect(url_for("companies"))

        # GET request: retrieve existing companies
        company_list = db.get_all_companies()

        return render_template(
            "companies.html",
            companies=company_list
        )

    finally:
        db.disconnect()






@app.route("/companies/edit/<int:company_id>", methods=["GET", "POST"])
def edit_company(company_id):
    db = JobTrackerDB()

    if not db.connect():
        return "Database connection failed", 500

    try:
        # Retrieve the company being edited
        company = db.get_company_by_id(company_id)

        if company is None:
            return "Company not found", 404

        if request.method == "POST":

            # Collect updated information from the HTML form
            company_data = {
                "company_name": request.form.get("company_name", "").strip(),
                "industry": request.form.get("industry", "").strip(),
                "website": request.form.get("website", "").strip(),
                "city": request.form.get("city", "").strip(),
                "state": request.form.get("state", "").strip(),
                "notes": request.form.get("notes", "").strip()
            }

            # Validate required fields
            if not company_data["company_name"]:
                flash("Company name is required.")
                return redirect(url_for("edit_company", company_id=company_id))

            # Update the database
            db.update_company(company_id, company_data)

            flash("Company updated successfully!")

            return redirect(url_for("companies"))

        # GET request: display existing company information
        return render_template("edit_company.html", company=company)

    finally:
        db.disconnect()


@app.route("/companies/delete/<int:company_id>", methods=["POST"])
def delete_company(company_id):
    db = JobTrackerDB()

    if not db.connect():
        flash("Database connection failed.", "error")
        return redirect(url_for("companies"))

    try:
        deleted_rows = db.delete_company(company_id)

        if deleted_rows == 1:
            flash("Company deleted successfully!", "success")
        else:
            flash("Company not found.", "error")

    except Error as e:
        if e.errno == 1451:
            flash(
            "Cannot delete this company because it has associated jobs. "
            "Please remove or reassign those jobs first."
        )
        else:
            print(f"Error deleting company: {e}")
            flash("An unexpected error occurred while deleting the company.")

    finally:
        db.disconnect()

    return redirect(url_for("companies"))


@app.route("/jobs", methods=["GET", "POST"])
def jobs():
    db = JobTrackerDB()

    if not db.connect():
        return "Database connection failed", 500

    try:
        if request.method == "POST":

            company_id = request.form.get("company_id", "").strip() or None
            job_title = request.form.get("job_title", "").strip()
            job_type = request.form.get("job_type", "").strip() or None
            salary_min = request.form.get("salary_min", "").strip() or None
            salary_max = request.form.get("salary_max", "").strip() or None
            job_url = request.form.get("job_url", "").strip() or None
            date_posted = request.form.get("date_posted", "").strip() or None
            requirements = request.form.get("requirements", "").strip() or None

            if not job_title:
                flash("Job title is required")
                return redirect(url_for("jobs"))

            if job_type not in (
                None, "Full-time", "Part-time",
                "Contract", "Internship"
            ):
                flash("Invalid job type")
                return redirect(url_for("jobs"))

            try:
                company_id = int(company_id) if company_id else None
                salary_min = int(salary_min) if salary_min else None
                salary_max = int(salary_max) if salary_max else None

            except ValueError:
                flash("Company ID and salary values must be valid numbers")
                return redirect(url_for("jobs"))

            # Convert requirements text into a valid JSON string
            if requirements is not None:
                requirements = json.dumps(requirements)

            try:
                db.add_job(
                    company_id,
                    job_title,
                    job_type,
                    salary_min,
                    salary_max,
                    job_url,
                    date_posted,
                    requirements
                )

                flash("Job added successfully")
                return redirect(url_for("jobs"))

            except Error as e:
                flash(f"Error adding job: {e}")
                return redirect(url_for("jobs"))

        job_list = db.get_all_jobs()
        company_list = db.get_all_companies()

        return render_template(
            "jobs.html",
            jobs=job_list,
            companies=company_list
        )

    finally:
        db.disconnect()





@app.route("/jobs/edit/<int:job_id>", methods=["GET", "POST"])
def edit_job(job_id):
    db = JobTrackerDB()

    if not db.connect():
        return "Database connection failed", 500

    try:
        job = db.get_job_by_id(job_id)

        if job is None:
            flash("Job not found")
            return redirect(url_for("jobs"))

        if request.method == "POST":
            company_id = request.form.get("company_id", "").strip()
            job_title = request.form.get("job_title", "").strip()
            job_type = request.form.get("job_type", "").strip() or None
            salary_min = request.form.get("salary_min", "").strip()
            salary_max = request.form.get("salary_max", "").strip()
            job_url = request.form.get("job_url", "").strip() or None
            date_posted = request.form.get("date_posted", "").strip() or None
            requirements = request.form.get("requirements", "").strip()

            if not company_id or not job_title:
                flash("Company and job title are required")
                return redirect(url_for("edit_job", job_id=job_id))

            if job_type not in (
                None, "Full-time", "Part-time",
                "Contract", "Internship"
            ):
                flash("Invalid job type")
                return redirect(url_for("edit_job", job_id=job_id))

            try:
                company_id = int(company_id)
                salary_min = int(salary_min) if salary_min else None
                salary_max = int(salary_max) if salary_max else None
            except ValueError:
                flash("Please enter valid numeric values")
                return redirect(url_for("edit_job", job_id=job_id))

            if salary_min is not None and salary_min < 0:
                flash("Minimum salary cannot be negative")
                return redirect(url_for("edit_job", job_id=job_id))

            if salary_max is not None and salary_max < 0:
                flash("Maximum salary cannot be negative")
                return redirect(url_for("edit_job", job_id=job_id))

            if (salary_min is not None and salary_max is not None
                    and salary_min > salary_max):
                flash("Minimum salary cannot exceed maximum salary")
                return redirect(url_for("edit_job", job_id=job_id))

            job_values = {
                "company_id": company_id,
                "job_title": job_title,
                "job_type": job_type,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "job_url": job_url,
                "date_posted": date_posted,
                "requirements": json.dumps(requirements) if requirements else None
            }

            try:
                db.update_job(job_id, job_values)
                flash("Job updated successfully")
                return redirect(url_for("jobs"))

            except Error as e:
                print(f"Error updating job: {e}")
                flash("Unable to update job")
                return redirect(url_for("edit_job", job_id=job_id))

        company_list = db.get_all_companies()

        # MySQL Connector returns JSON columns as JSON text.
        # Convert a stored JSON string into editable plain text.
        if job["requirements"]:
            try:
                decoded = json.loads(job["requirements"])
                if isinstance(decoded, str):
                    job["requirements"] = decoded
                else:
                    job["requirements"] = json.dumps(decoded, indent=2)
            except (TypeError, ValueError):
                pass

        return render_template(
            "edit_job.html",
            job=job,
            companies=company_list
        )

    finally:
        db.disconnect()


@app.route("/jobs/delete/<int:job_id>", methods=["POST"])
def delete_job(job_id):
    db = JobTrackerDB()

    if not db.connect():
        flash("Database connection failed")
        return redirect(url_for("jobs"))

    try:
        deleted_rows = db.delete_job(job_id)

        if deleted_rows == 1:
            flash("Job deleted successfully")
        else:
            flash("Job not found")

    except Error as e:
        print(f"Error deleting job: {e}")

        if e.errno == 1451:
            flash(
                "Cannot delete this job because it has associated records, "
                "such as applications. Remove or reassign them first."
            )
        else:
            flash("An error occurred while deleting the job")

    finally:
        db.disconnect()

    return redirect(url_for("jobs"))

if __name__ == "__main__":
    app.run(debug=True)
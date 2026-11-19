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



APPLICATION_STATUSES = (
    "Applied",
    "Screening",
    "Interview",
    "Offer",
    "Rejected",
    "Withdrawn"
)


def get_application_form_data():
    job_id = request.form.get("job_id", "").strip()
    application_date = request.form.get("application_date", "").strip()
    status = request.form.get("status", "").strip()
    resume_version = request.form.get("resume_version", "").strip()
    cover_letter_sent = request.form.get("cover_letter_sent", "0")
    interview_data = request.form.get("interview_data", "").strip()

    if not job_id:
        raise ValueError("Please select a job")

    try:
        job_id = int(job_id)
        if job_id <= 0:
            raise ValueError()
    except ValueError:
        raise ValueError("Invalid job ID")

    if status and status not in APPLICATION_STATUSES:
        raise ValueError("Invalid application status")

    if len(resume_version) > 50:
        raise ValueError("Resume version cannot exceed 50 characters")

    if cover_letter_sent not in ("0", "1"):
        raise ValueError("Invalid cover letter value")

    # Store interview notes as a JSON string.
    # Validate and serialize structured JSON
    if interview_data:
        try:
            parsed_data = json.loads(interview_data)
            interview_data = json.dumps(parsed_data)
        except json.JSONDecodeError:
            raise ValueError("Interview data must contain valid JSON")
    else:
        interview_data = None

    return {
        "job_id": job_id,
        "application_date": application_date or None,
        "status": status or None,
        "resume_version": resume_version or None,
        "cover_letter_sent": int(cover_letter_sent),
        "interview_data": interview_data
    }


@app.route("/applications", methods=["GET", "POST"])
def applications():
    db = JobTrackerDB()

    if not db.connect():
        return "Database connection failed", 500

    try:
        if request.method == "POST":
            try:
                data = get_application_form_data()

                db.add_application(
                    data["job_id"],
                    data["application_date"],
                    data["status"],
                    data["resume_version"],
                    data["cover_letter_sent"],
                    data["interview_data"]
                )

                flash("Application added successfully")

            except ValueError as e:
                flash(str(e))

            except Error as e:
                print(f"Error adding application: {e}")
                flash("Unable to add application")

            return redirect(url_for("applications"))

        application_list = db.get_all_applications()
        job_list = db.get_all_jobs()

        return render_template(
            "applications.html",
            applications=application_list,
            jobs=job_list
        )

    finally:
        db.disconnect()


@app.route("/applications/edit/<int:application_id>", methods=["GET", "POST"])
def edit_application(application_id):
    db = JobTrackerDB()

    if not db.connect():
        return "Database connection failed", 500

    try:
        application = db.get_application_by_id(application_id)

        if application is None:
            flash("Application not found")
            return redirect(url_for("applications"))

        if request.method == "POST":
            try:
                application_data = get_application_form_data()

                db.update_application(
                    application_id,
                    application_data
                )

                flash("Application updated successfully")
                return redirect(url_for("applications"))

            except ValueError as e:
                flash(str(e))

            except Error as e:
                print(f"Error updating application: {e}")
                flash("Unable to update application")

            return redirect(
                url_for("edit_application", application_id=application_id)
            )

        job_list = db.get_all_jobs()

        # Convert JSON text into plain text for the textarea.
        if application["interview_data"]:
            try:
                decoded = json.loads(application["interview_data"])

                if isinstance(decoded, str):
                    application["interview_data"] = decoded
                else:
                    application["interview_data"] = json.dumps(
                        decoded, indent=2
                    )
            except (TypeError, ValueError):
                pass

        return render_template(
            "edit_application.html",
            application=application,
            jobs=job_list
        )

    finally:
        db.disconnect()


@app.route("/applications/delete/<int:application_id>", methods=["POST"])
def delete_application(application_id):
    db = JobTrackerDB()

    if not db.connect():
        flash("Database connection failed")
        return redirect(url_for("applications"))

    try:
        deleted_rows = db.delete_application(application_id)

        if deleted_rows == 1:
            flash("Application deleted successfully")
        else:
            flash("Application not found")

    except Error as e:
        print(f"Error deleting application: {e}")

        if e.errno == 1451:
            flash("Cannot delete application because it has related records")
        else:
            flash("Unable to delete application")

    finally:
        db.disconnect()

    return redirect(url_for("applications"))




def get_contact_form_data():
    company_id = request.form.get("company_id", "").strip()
    contact_name = request.form.get("contact_name", "").strip()
    title = request.form.get("title", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    linkedin_url = request.form.get("linkedin_url", "").strip()
    notes = request.form.get("notes", "").strip()

    if not contact_name:
        raise ValueError("Contact name is required")

    if len(contact_name) > 100:
        raise ValueError("Contact name cannot exceed 100 characters")

    if len(title) > 100:
        raise ValueError("Title cannot exceed 100 characters")

    if len(email) > 100:
        raise ValueError("Email cannot exceed 100 characters")

    if len(phone) > 20:
        raise ValueError("Phone cannot exceed 20 characters")

    if len(linkedin_url) > 200:
        raise ValueError("LinkedIn URL cannot exceed 200 characters")

    if company_id:
        try:
            company_id = int(company_id)

            if company_id <= 0:
                raise ValueError()

        except ValueError:
            raise ValueError("Invalid company ID")
    else:
        company_id = None

    return {
        "company_id": company_id,
        "contact_name": contact_name,
        "title": title or None,
        "email": email or None,
        "phone": phone or None,
        "linkedin_url": linkedin_url or None,
        "notes": notes or None
    }

@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    db = JobTrackerDB()

    if not db.connect():
        return "Database connection failed", 500

    try:
        if request.method == "POST":
            try:
                contact_data = get_contact_form_data()

                db.add_contact(contact_data)

                flash("Contact added successfully")

            except ValueError as e:
                flash(str(e))

            except Error as e:
                print(f"Error adding contact: {e}")
                flash("Unable to add contact")

            return redirect(url_for("contacts"))

        contact_list = db.get_all_contacts()
        company_list = db.get_all_companies()

        return render_template(
            "contacts.html",
            contacts=contact_list,
            companies=company_list
        )

    finally:
        db.disconnect()

@app.route("/contacts/edit/<int:contact_id>", methods=["GET", "POST"])
def edit_contact(contact_id):
    db = JobTrackerDB()

    if not db.connect():
        return "Database connection failed", 500

    try:
        contact = db.get_contact_by_id(contact_id)

        if contact is None:
            flash("Contact not found")
            return redirect(url_for("contacts"))

        if request.method == "POST":
            try:
                contact_data = get_contact_form_data()

                db.update_contact(contact_id, contact_data)

                flash("Contact updated successfully")
                return redirect(url_for("contacts"))

            except ValueError as e:
                flash(str(e))

            except Error as e:
                print(f"Error updating contact: {e}")
                flash("Unable to update contact")

            return redirect(
                url_for("edit_contact", contact_id=contact_id)
            )

        company_list = db.get_all_companies()

        return render_template(
            "edit_contact.html",
            contact=contact,
            companies=company_list
        )

    finally:
        db.disconnect()

@app.route("/contacts/delete/<int:contact_id>", methods=["POST"])
def delete_contact(contact_id):
    db = JobTrackerDB()

    if not db.connect():
        flash("Database connection failed")
        return redirect(url_for("contacts"))

    try:
        deleted_rows = db.delete_contact(contact_id)

        if deleted_rows == 1:
            flash("Contact deleted successfully")
        else:
            flash("Contact not found")

    except Error as e:
        print(f"Error deleting contact: {e}")

        if e.errno == 1451:
            flash(
                "Cannot delete this contact because "
                "it has associated records"
            )
        else:
            flash("Unable to delete contact")

    finally:
        db.disconnect()

    return redirect(url_for("contacts"))


@app.route("/dashboard")
def dashboard():
    db = JobTrackerDB()

    if not db.connect():
        return "Database connection failed", 500

    try:
        stats = db.get_dashboard_stats()
        recent_applications = db.get_recent_applications()
        status_counts = db.get_application_status_counts()

        return render_template(
            "dashboard.html",
            stats=stats,
            recent_applications=recent_applications,
            status_counts=status_counts
        )

    finally:
        db.disconnect()


def calculate_job_match(user_skills, job_requirements):

    # Convert JSON text into a Python object
    if isinstance(job_requirements, str):
        try:
            job_requirements = json.loads(job_requirements)
        except json.JSONDecodeError:
            return None

    # Support requirements stored as a JSON array
    # or an object containing a "skills" array
    if isinstance(job_requirements, dict):
        required_skills = job_requirements.get("skills", [])

    elif isinstance(job_requirements, list):
        required_skills = job_requirements

    else:
        return None

    # Validate that all requirements are strings
    if not isinstance(required_skills, list):
        return None

    if not all(isinstance(skill, str) for skill in required_skills):
        return None

    # Normalize capitalization and whitespace
    normalized_user_skills = {
        skill.strip().lower()
        for skill in user_skills
        if skill.strip()
    }

    normalized_required_skills = {
        skill.strip().lower()
        for skill in required_skills
        if skill.strip()
    }

    # Jobs without listed skills cannot be scored
    if not normalized_required_skills:
        return None

    matched_skills = normalized_required_skills.intersection(
        normalized_user_skills
    )

    missing_skills = normalized_required_skills.difference(
        normalized_user_skills
    )

    match_percentage = (
        len(matched_skills) / len(normalized_required_skills)
    ) * 100

    return {
        "match_percentage": round(match_percentage, 2),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills)
    }

@app.route("/job-match", methods=["GET", "POST"])
def job_match():

    results = []
    skills_input = ""
    searched = False

    if request.method == "POST":

        searched = True
        skills_input = request.form.get("skills", "").strip()

        if not skills_input:
            flash("Please enter at least one skill")
        else:
            user_skills = skills_input.split(",")

            db = JobTrackerDB()

            if not db.connect():
                return "Database connection failed", 500

            try:
                jobs = db.get_jobs_for_matching()

                for job in jobs:

                    match = calculate_job_match(
                        user_skills,
                        job["requirements"]
                    )

                    if match is None:
                        continue

                    results.append({
                        "job_id": job["job_id"],
                        "job_title": job["job_title"],
                        "company_name": job["company_name"],
                        "job_type": job["job_type"],
                        "match_percentage": match["match_percentage"],
                        "matched_skills": match["matched_skills"],
                        "missing_skills": match["missing_skills"]
                    })

                # Highest match percentage first
                results.sort(
                    key=lambda job: job["match_percentage"],
                    reverse=True
                )

            finally:
                db.disconnect()

    return render_template(
        "job_match.html",
        results=results,
        skills_input=skills_input,
        searched=searched
    )


if __name__ == "__main__":
    app.run(debug=True)
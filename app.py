from flask import Flask, render_template, request, redirect, url_for, flash
from database import JobTrackerDB

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
        print(f"Error deleting company: {e}")

        if e.errno == 1451:
            flash(
                "Cannot delete this company because it has associated jobs.",
                "error"
            )
        else:
            flash("An error occurred while deleting the company.", "error")

    finally:
        db.disconnect()

    return redirect(url_for("companies"))


if __name__ == "__main__":
    app.run(debug=True)
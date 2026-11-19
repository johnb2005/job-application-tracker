import mysql.connector
import os
from mysql.connector import Error
from dotenv import load_dotenv



load_dotenv()


class JobTrackerDB:
    def __init__(self):
        self.config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME")
        }

        self.connection = None

    def connect(self):
        try:
            self.connection  = mysql.connector.connect(**self.config)
            return True

        except Error as e:
            print(f"Connection error : {e}")
            return False


    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()


# Companies table CRUD implementation 
    def get_all_companies(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("Select * FROM companies")
        return cursor.fetchall()
    
    
    def add_company(self, company_name, industry, website, city, state, notes):
        cursor = self.connection.cursor()

        try:
            query = """
            INSERT INTO companies
                (company_name, industry, website, city, state, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

            values = (company_name, industry, website, city, state, notes)

            cursor.execute(query, values)
            self.connection.commit()

            return cursor.lastrowid

        except Error:
            self.connection.rollback()
            raise

        finally:
            cursor.close()


    def update_company(self,company_id,company_data):
        cursor = self.connection.cursor()

        try:
            query = '''UPDATE companies
            SET company_name = %s,
                industry = %s,
                website = %s,
                city = %s,
                state = %s,
                notes = %s
            WHERE company_id = %s
            '''

            values = (
            company_data['company_name'],
            company_data['industry'],
            company_data['website'],
            company_data['city'],
            company_data['state'],
            company_data['notes'],
            company_id
            )
            cursor.execute(query,values)
            self.connection.commit()
            return cursor.rowcount
        

        except Error:
            self.connection.rollback()
            raise

        finally:
            cursor.close()


    def get_company_by_id(self,company_id):
        cursor = self.connection.cursor(dictionary=True)

        try:
            query = '''
        SELECT * FROM companies WHERE company_id = %s

        '''

            cursor.execute(query,(company_id,))
            return cursor.fetchone()
    
        finally:
            cursor.close()



    def delete_company(self, company_id):
        cursor = self.connection.cursor()

        try:
            query = """
            DELETE FROM companies
            WHERE company_id = %s
        """

            cursor.execute(query, (company_id,))
            self.connection.commit()

            return cursor.rowcount

        except Error:
            self.connection.rollback()
            raise

        finally:
            cursor.close()
            



    def get_all_jobs(self):
        cursor = self.connection.cursor(dictionary=True)

        try:
            query = """
            SELECT j.*, c.company_name
            FROM jobs j
            LEFT JOIN companies c
                ON j.company_id = c.company_id
            ORDER BY j.job_id
        """

            cursor.execute(query)
            return cursor.fetchall()

        finally:
            cursor.close()
    def add_job(self,company_id,job_title,job_type,salary_min,salary_max,job_url,date_posted,requirements):
        cursor = self.connection.cursor()


        try:
            query = '''
            INSERT INTO jobs (company_id,job_title,job_type,salary_min,salary_max,job_url,date_posted,requirements)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            '''

            values = (company_id,job_title,job_type,salary_min,salary_max,job_url,date_posted,requirements)
            
            cursor.execute(query,values)
            self.connection.commit()

            return cursor.lastrowid

        except Error:
            self.connection.rollback()
            raise

        finally:
            cursor.close()     

    def update_job(self,job_id,job_values):
        cursor = self.connection.cursor()

        try:
            query = '''
            UPDATE jobs
            
            SET company_id = %s,
                job_title = %s,
                job_type = %s,
                salary_min = %s,
                salary_max = %s,
                job_url = %s,
                date_posted = %s,
                requirements = %s

            WHERE job_id = %s

        '''       

            values = (
                job_values["company_id"],
                job_values["job_title"],
                job_values["job_type"],
                job_values["salary_min"],
                job_values["salary_max"],
                job_values["job_url"],
                job_values["date_posted"],
                job_values["requirements"],
                job_id




            )
            cursor.execute(query,values)
            self.connection.commit()
            return cursor.rowcount

        except Error:
            self.connection.rollback()
            raise
        
        finally:
            cursor.close()


    def get_job_by_id(self, job_id):
        cursor = self.connection.cursor(dictionary=True)

        try:
            query = """
            SELECT *
            FROM jobs
            WHERE job_id = %s
        """

            cursor.execute(query, (job_id,))
            return cursor.fetchone()

        finally:
            cursor.close()

    def delete_job(self, job_id):
        cursor = self.connection.cursor()

        try:
            query = """
            DELETE FROM jobs
            WHERE job_id = %s
        """

            cursor.execute(query, (job_id,))
            self.connection.commit()

            return cursor.rowcount

        except Error:
            self.connection.rollback()
            raise

        finally:
            cursor.close()


# Applications CRUD

    def get_all_applications(self):
        cursor = self.connection.cursor(dictionary=True)

        try:
            query = """
            SELECT
                a.*,
                j.job_title,
                c.company_name
            FROM applications a
            LEFT JOIN jobs j
                ON a.job_id = j.job_id
            LEFT JOIN companies c
                ON j.company_id = c.company_id
            ORDER BY a.application_id
        """

            cursor.execute(query)
            return cursor.fetchall()

        finally:
            cursor.close()


    def get_application_by_id(self, application_id):
        cursor = self.connection.cursor(dictionary=True)

        try:
            query = """
            SELECT *
            FROM applications
            WHERE application_id = %s
        """

            cursor.execute(query, (application_id,))
            return cursor.fetchone()

        finally:
            cursor.close()


    def add_application(
        self, job_id, application_date, status,
        resume_version, cover_letter_sent, interview_data
):
        cursor = self.connection.cursor()

        try:
            query = """
            INSERT INTO applications
            (job_id, application_date, status,
             resume_version, cover_letter_sent, interview_data)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

            values = (
            job_id,
            application_date,
            status,
            resume_version,
            cover_letter_sent,
            interview_data
        )

            cursor.execute(query, values)
            self.connection.commit()
            return cursor.lastrowid

        except Error:
            self.connection.rollback()
            raise

        finally:
            cursor.close()


    def update_application(self, application_id, application_data):
        cursor = self.connection.cursor()

        try:
            query = """
            UPDATE applications
            SET job_id = %s,
                application_date = %s,
                status = %s,
                resume_version = %s,
                cover_letter_sent = %s,
                interview_data = %s
            WHERE application_id = %s
        """

            values = (
            application_data["job_id"],
            application_data["application_date"],
            application_data["status"],
            application_data["resume_version"],
            application_data["cover_letter_sent"],
            application_data["interview_data"],
            application_id
        )

            cursor.execute(query, values)
            self.connection.commit()
            return cursor.rowcount

        except Error:
            self.connection.rollback()
            raise

        finally:
            cursor.close()


    def delete_application(self, application_id):
        cursor = self.connection.cursor()

        try:
            query = """
            DELETE FROM applications
            WHERE application_id = %s
        """

            cursor.execute(query, (application_id,))
            self.connection.commit()
            return cursor.rowcount

        except Error:
            self.connection.rollback()
            raise

        finally:
            cursor.close()

    # Contacts CRUD

    def get_all_contacts(self):
        cursor = self.connection.cursor(dictionary=True)

        try:
            query = """
                SELECT ct.*, c.company_name
                FROM contacts ct
                LEFT JOIN companies c
                    ON ct.company_id = c.company_id
                ORDER BY ct.contact_id
            """

            cursor.execute(query)
            return cursor.fetchall()

        finally:
            cursor.close()


    def get_contact_by_id(self, contact_id):
        cursor = self.connection.cursor(dictionary=True)

        try:
            query = """
                SELECT *
                FROM contacts
                WHERE contact_id = %s
            """

            cursor.execute(query, (contact_id,))
            return cursor.fetchone()

        finally:
            cursor.close()


    def add_contact(self, contact_data):
        cursor = self.connection.cursor()

        try:
            query = """
                INSERT INTO contacts
                (company_id, contact_name, title,
                 email, phone, linked_in_url, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                contact_data["company_id"],
                contact_data["contact_name"],
                contact_data["title"],
                contact_data["email"],
                contact_data["phone"],
                contact_data["linkedin_url"],
                contact_data["notes"]
            )

            cursor.execute(query, values)
            self.connection.commit()

            return cursor.lastrowid

        except Error:
            self.connection.rollback()
            raise

        finally:
            cursor.close()


    def update_contact(self, contact_id, contact_data):
        cursor = self.connection.cursor()

        try:
            query = """
                UPDATE contacts
                SET company_id = %s,
                    contact_name = %s,
                    title = %s,
                    email = %s,
                    phone = %s,
                    linked_in_url = %s,
                    notes = %s
                WHERE contact_id = %s
            """

            values = (
                contact_data["company_id"],
                contact_data["contact_name"],
                contact_data["title"],
                contact_data["email"],
                contact_data["phone"],
                contact_data["linkedin_url"],
                contact_data["notes"],
                contact_id
            )

            cursor.execute(query, values)
            self.connection.commit()

            return cursor.rowcount

        except Error:
            self.connection.rollback()
            raise

        finally:
            cursor.close()


    def delete_contact(self, contact_id):
        cursor = self.connection.cursor()

        try:
            query = """
                DELETE FROM contacts
                WHERE contact_id = %s
            """

            cursor.execute(query, (contact_id,))
            self.connection.commit()

            return cursor.rowcount

        except Error:
            self.connection.rollback()
            raise

        finally:
            cursor.close()

    def get_dashboard_stats(self):
        cursor = self.connection.cursor(dictionary=True)

        try:
            query = '''
            SELECT
            COUNT(*) AS total_applications,

            COUNT(CASE
            WHEN status IN ('Applied', 'Screening', 'Interview')
            THEN 1
            END) AS active_applications,

            COUNT(CASE
            WHEN status = 'Interview'
            THEN 1
            END) AS interviews,

            COUNT(CASE
             WHEN status = 'Offer'
            THEN 1
            END) AS offers

            FROM applications;
        '''
            cursor.execute(query)
            return cursor.fetchone()
        finally:
         cursor.close()


    def get_recent_applications(self):
        cursor = self.connection.cursor(dictionary=True)

        try:

            query = '''
            SELECT
            a.application_id,
            c.company_name,
            j.job_title,
            a.application_date,
            a.status
            FROM applications a
            JOIN jobs j ON a.job_id = j.job_id
            JOIN companies c ON j.company_id = c.company_id
            ORDER BY a.application_date DESC, a.application_id DESC
            LIMIT 5;        

            '''

            cursor.execute(query)

            return cursor.fetchall()

        finally:
            cursor.close()

    def get_application_status_counts(self):
        cursor = self.connection.cursor(dictionary=True)

        try:
            query = '''
            SELECT status, COUNT(*) AS total
            FROM applications
            GROUP BY status
            ORDER BY total DESC;
            '''

            cursor.execute(query)
            return cursor.fetchall()

        finally:
            cursor.close()

    
    def get_jobs_for_matching(self):
        cursor = self.connection.cursor(dictionary=True)

        try:
            query = """
            SELECT
                j.job_id,
                j.job_title,
                j.job_type,
                j.requirements,
                c.company_name
            FROM jobs j
            LEFT JOIN companies c
                ON j.company_id = c.company_id
            ORDER BY j.job_id
        """

            cursor.execute(query)
            return cursor.fetchall()

        finally:
            cursor.close()

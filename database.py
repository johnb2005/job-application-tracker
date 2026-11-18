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
        cursor.execute("SELECT * FROM jobs")
        return cursor.fetchall()

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


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
            






            



    def get_all_jobs(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT job_id,company_id,job_title FROM jobs")
        return cursor.fetchall()






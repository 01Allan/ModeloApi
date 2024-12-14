import mysql.connector
from mysql.connector import Error
from app.services.logger import logger

def save_prediction_to_db(data):
    try:
        connection = mysql.connector.connect(
            host="your_freesqldatabase_host",
            user="your_username",
            password="your_password",
            database="your_database_name"
        )
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO predictions (
            CustomerID, Age, Gender, Tenure, Usage_Frequency, 
            Support_Calls, Payment_Delay, Subscription_Type, 
            Contract_Length, Total_Spend, Last_Interaction, Churn, Probability
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data["CustomerID"], data["Age"], data["Gender"], data["Tenure"],
            data["Usage_Frequency"], data["Support_Calls"], data["Payment_Delay"],
            data["Subscription_Type"], data["Contract_Length"], data["Total_Spend"],
            data["Last_Interaction"], data["Churn"], data["Probability"]
        )
        cursor.execute(insert_query, values)
        connection.commit()
        logger.info(f"Datos guardados exitosamente en la base de datos para CustomerID: {data['CustomerID']}")
    except Exception as e:
        logger.error(f"Error al guardar en la base de datos: {e}")
        raise RuntimeError(f"Error al guardar en la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

import mysql.connector
from mysql.connector import Error
from app.services.logger import logger

def save_data_to_db(data):
    """Guarda la data inicial en la base de datos."""
    try:
        connection = mysql.connector.connect(
            host="sql3.freesqldatabase.com",
            user="sql3751784",
            password="hF9MAPva8x",
            database="sql3751784"
        )
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO predictions (
            CustomerID, Age, Gender, Tenure, Usage_Frequency,
            Support_Calls, Payment_Delay, Subscription_Type,
            Contract_Length, Total_Spend, Last_Interaction
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        for record in data:
            values = (
                record["CustomerID"], record["Age"], record["Gender"], record["Tenure"],
                record["Usage_Frequency"], record["Support_Calls"], record["Payment_Delay"],
                record["Subscription_Type"], record["Contract_Length"], record["Total_Spend"],
                record["Last_Interaction"]
            )
            cursor.execute(insert_query, values)

        connection.commit()
        logger.info("Datos guardados exitosamente.")
    except Exception as e:
        logger.error(f"Error al guardar en la base de datos: {e}")
        raise RuntimeError(f"Error al guardar en la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fetch_data_from_db(batch_size=100):
    """Recupera los datos guardados para predicciones en batches."""
    try:
        connection = mysql.connector.connect(
            host="sql3.freesqldatabase.com",
            user="sql3751784",
            password="hF9MAPva8x",
            database="sql3751784"
        )
        cursor = connection.cursor(dictionary=True)

        query = f"SELECT * FROM predictions LIMIT {batch_size}"
        cursor.execute(query)
        records = cursor.fetchall()
        logger.info(f"{len(records)} registros recuperados para predicción.")
        return records
    except Exception as e:
        logger.error(f"Error al recuperar datos desde la base de datos: {e}")
        raise RuntimeError(f"Error al recuperar datos desde la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def save_predictions_to_db(predictions):
    """Guarda las predicciones en la base de datos."""
    try:
        connection = mysql.connector.connect(
            host="sql3.freesqldatabase.com",
            user="sql3751784",
            password="hF9MAPva8x",
            database="sql3751784"
        )
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO predictions (
            CustomerID, Churn, Probability
        ) VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            Churn=VALUES(Churn), Probability=VALUES(Probability)
        """
        for prediction in predictions:
            values = (
                prediction["CustomerID"], prediction["Churn"]#, prediction["Probability"]
            )
            cursor.execute(insert_query, values)

        connection.commit()
        logger.info("Predicciones guardadas exitosamente en la base de datos.")
    except Exception as e:
        logger.error(f"Error al guardar predicciones en la base de datos: {e}")
        raise RuntimeError(f"Error al guardar predicciones en la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fetch_predictions_from_db():
    """Recupera las predicciones guardadas desde la base de datos."""
    try:
        connection = mysql.connector.connect(
            host="sql3.freesqldatabase.com",
            user="sql3751784",
            password="hF9MAPva8x",
            database="sql3751784"
        )
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM predictions"
        cursor.execute(query)
        records = cursor.fetchall()
        logger.info(f"{len(records)} predicciones recuperadas desde la base de datos.")
        return records
    except Exception as e:
        logger.error(f"Error al recuperar predicciones desde la base de datos: {e}")
        raise RuntimeError(f"Error al recuperar predicciones desde la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
"""
Script para resetear completamente la base de datos.
"""

import psycopg2

from database.connection import DATABASE_URL


def reset_database():
    """
    Resetea completamente la base de datos eliminando todas las tablas.
    """
    print("🔄 Reseteando base de datos...")

    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cursor = conn.cursor()

        # Obtener todas las tablas
        cursor.execute(
            """
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
        """
        )

        tables = cursor.fetchall()

        # Eliminar todas las tablas
        for table in tables:
            table_name = table[0]
            print(f"🗑️  Eliminando tabla: {table_name}")
            cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE")

        print("✅ Base de datos reseteada exitosamente!")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error reseteando base de datos: {e}")


if __name__ == "__main__":
    reset_database()

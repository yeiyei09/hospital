"""
Script para migrar la base de datos y crear las tablas necesarias.
"""

from sqlalchemy import text

from database.connection import create_tables, drop_tables, engine


def migrate_database():
    """
    Migra la base de datos eliminando tablas existentes y creando nuevas.
    """
    print("🔄 Iniciando migración de base de datos...")

    try:
        # Eliminar todas las tablas existentes
        print("🗑️  Eliminando tablas existentes...")
        drop_tables()

        # Crear todas las tablas con la nueva estructura
        print("🏗️  Creando nuevas tablas...")
        create_tables()

        print("✅ Migración completada exitosamente!")

    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        return False

    return True


if __name__ == "__main__":
    migrate_database()

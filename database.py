from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Change these details as per your local SQL Server setup
DATABASE_SERVER = 'localhost'  # or use your actual server name
DATABASE_NAME = 'Leave_api_learning'
# DATABASE_USERNAME = 'your_username'  # optional if using Windows auth
# DATABASE_PASSWORD = 'your_password'  # optional if using Windows auth

# Example for SQL Server with SQL Authentication:
# DATABASE_URL = f"mssql+pyodbc://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_SERVER}/{DATABASE_NAME}?driver=ODBC+Driver+17+for+SQL+Server"

# Example for Windows Authentication:
DATABASE_URL = f"mssql+pyodbc://localhost/Leave_api_learning?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&trusted_connection=yes"

engine = create_engine(DATABASE_URL, echo = True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

import sqlalchemy as db
from config.init import config

engine = db.create_engine(config('DB_URI'))
connection = engine.connect()
metadata = db.MetaData()

# Table definitions
users = db.Table("users", metadata, autoload=True, autoload_with=engine)
jobs = db.Table("jobs", metadata, autoload=True, autoload_with=engine)
job_applications = db.Table(
    "job_applications", metadata, autoload=True, autoload_with=engine)

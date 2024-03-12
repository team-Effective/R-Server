class SystemConfig:
    from dotenv import load_dotenv

    load_dotenv()
    import os

    DB_USER = os.getenv("DB_USER")
    PASSWORD = os.getenv("PASSWORD")
    HOST = os.getenv("HOST")
    DATABASE = os.getenv("DATABASE")

    DEBUG = True

    if DATABASE is not None:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{PASSWORD}@{HOST}/{DATABASE}?charset=utf8"
        )


Config = SystemConfig

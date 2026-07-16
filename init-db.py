from database import engine, Base
import models

def init_database():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_database()

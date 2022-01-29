from sqlmodel import Session
from edam.reader.models.database import SQLModel
from edam.reader.models.database import create_db_and_tables, engine


def main():
    create_db_and_tables()


if __name__ == "__main__":
    main()

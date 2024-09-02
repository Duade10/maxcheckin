from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)


class GoogleSheets(Base):
    __tablename__ = 'google_sheets'

    id = Column(Integer, primary_key=True)
    sheet_id = Column(String)
    worksheet_name = Column(String)

    def __init__(self, sheet_id, worksheet_name):
        self.sheet_id = sheet_id
        self.worksheet_name = worksheet_name

    def __repr__(self):
        return f"GoogleSheets({self.sheet_id}, {self.worksheet_name})"


Base.metadata.create_all(engine)


def update_sheet_id(sheet_id: str):
    session = Session()
    existing_sheet = session.query(GoogleSheets).filter_by(id=id).first()

    if existing_sheet:
        if existing_sheet.sheet_id == sheet_id:
            raise Exception("Sheet ID already exists")

        existing_sheet.sheet_id = sheet_id

    session.commit()
    session.close()


def create_sheet(sheet_id: str, worksheet_name: str):
    session = Session()

    existing_sheet = session.query(GoogleSheets).filter_by(worksheet_name=worksheet_name).first()
    if existing_sheet:
        raise Exception("Google Sheet already exists")

    new_sheet = GoogleSheets(sheet_id, worksheet_name)
    session.add(new_sheet)
    session.commit()
    session.close()


def get_single_sheet(sheet_id):
    pass
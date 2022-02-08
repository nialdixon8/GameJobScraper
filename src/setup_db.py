"""Database Schema

Database schema and connection functionality
"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    employer = Column(String(50))
    location = Column(String(50))
    experience = Column(String(50))
    requirements = Column(String(50))

    def __repr__(self):
        return "<Offer(title='{}', employer='{}', requirements='{}')>"\
            .format(self.title, self.employer, self.requirements)


def setup_connection():
    """ Sets up connection to the database. Currently a simple sqlite3 file. """

    engine = create_engine('sqlite:///db/temp.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


if __name__ == '__main__':
    session = setup_connection()
    # offer1 = Offer(title='Software Engineer', employer='Google', location='Leicester', experience='None', requirements='Python')
    # offer2 = Offer(title='Database Engineer', employer='Microsoft', location='Leicester', experience='None', requirements='MySQL')
    # session.add_all((offer1, offer2))
    # session.commit()
    #
    # print(session.query(Offer).all())

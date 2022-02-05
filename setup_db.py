from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    employer = Column(String(50))
    requirements = Column(String(50))

    def __repr__(self):
        return "<Offer(title='{}', employer='{}', requirements='{}')>"\
            .format(self.title, self.employer, self.requirements)


def setup_connection():
    engine = create_engine('sqlite:///:memory:', echo=False)  # temporarily using inmemory db
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


if __name__ == '__main__':
    session = setup_connection()

    offer1 = Offer(title='Software Engineer', employer='Google', requirements='Python')
    offer2 = Offer(title='Database Engineer', employer='Microsoft', requirements='MySQL')
    session.add_all((offer1, offer2))
    session.commit()

    print(session.query(Offer).all())

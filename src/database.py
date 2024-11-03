import sqlalchemy
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "sqlite:///customers.db", echo=True
)  # Create a SQLite db engine with  query logging enable
Base = sqlalchemy.orm.declarative_base()
Session = sessionmaker(bind=engine)  # Create a session

# Customer model representing 'customers' table in  db


class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True)
    firstname = Column(String, nullable=False)
    middlename = Column(String)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)  # Can be composite

    """ TO DO: Add Implement Composite Key:
     Ensure model uses a composite primary key with both id and phone columns??
    """


def init_db():
    Base.metadata.create_all(engine)


def get_session():
    return Session()


# creates a  customer record in db
def create(customer_data):
    session = get_session()
    try:
        new_customer = Customer(**customer_data)
        session.add(new_customer)
        session.commit()
        session.refresh(new_customer)
        return customer_to_dict(new_customer)
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


# get customer based on id from the db
def get_customer_by_id(id):
    session = get_session()
    try:
        customer = session.query(Customer).filter_by(id=id).first()
        if customer:
            return customer_to_dict(customer)
        else:
            return None
    finally:
        session.close()


# update/put operation
def update(id, customer_data):
    session = get_session()
    try:
        customer = session.query(Customer).filter_by(id=id).first()
        if customer:
            for key, value in customer_data.items():
                setattr(customer, key, value)
            session.commit()
            return customer_to_dict(customer)
        return None
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


# delete cusgtomer based on the id
def delete(id):
    session = get_session()
    try:
        customer = session.query(Customer).filter_by(id=id).first()
        if customer:
            session.delete(customer)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


# to print response back
def customer_to_dict(customer):
    return {
        "id": customer.id,
        "firstname": customer.firstname,
        "middlename": customer.middlename,
        "lastname": customer.lastname,
        "email": customer.email,
        "phone": customer.phone,
    }

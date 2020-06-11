from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from base import Base


#Legislators first!

class Politician(Base):
    __tablename__ = 'politicians'
    id = Column(Integer, primary_key=True)
    bioid = Column('bioid', String)
    date_of_birth = Column('date_of_birth', String)
    first_name = Column('first_name', String)
    last_name = Column('last_name', String)
    terms = relationship("Politician_Term")
    roles = relationship("Leadership_Role")

class Politician_Term(Base):
    __tablename__ = "politician_terms"
    id = Column(Integer, primary_key=True)
    polid = Column(Integer, ForeignKey("politicians.id"))
    start_date = Column('start_date', Date)
    end_date = Column('end_date', Date)
    party = Column('party', String)
    state = Column('state', String)
    legislative_body = Column('legislative_body', String)
    gender = Column('gender', String)
    district = Column('district', String)

class Leadership_Role(Base):
    __tablename__ = 'leadership_roles'
    id = Column(Integer, primary_key=True)
    polid = Column(Integer, ForeignKey("politicians.id"))
    role = Column('role', String)
    chamber = Column('chamber', String)
    start_date = Column('start_date', Date)
    end_date = Column('end_date', Date)

#Bills Next

class Bill(Base):
    __tablename__ = "bills"
    id = Column(Integer, primary_key=True)
    bill_code = Column('bill_code', String)
    bill_states = relationship("Bill_State")
    references_to = relationship("Bill_Reference")
    references_from = relationship("Bill_Reference")
    topics = relationship("Topic")
    sponsors = relationship("Sponsorship")
    topics = relationship("Bill_Topic")

class Bill_State(Base):
    __tablename__ = "bill_states"
    id = Column(Integer, primary_key=True)   
    bill_state_identifier = Column('bill_state_identifier', String)
    bill_id = Column(Integer, ForeignKey("bills.id"))
    bill_type = Column('bill_type', String)
    status_code = Column('status_code', String)
    text_location = Column('text_location', String)
    short_title = Column('short_title', String)
    official_title = Column('official_title', String)
    intro_date = Column('intro_date', Date)
    congress = Column('congress', Integer)

# Bill_ref next 

class Bill_Reference(Base):
    __tablename__ = "bill_references"
    id = Column(Integer, primary_key=True)
    to_bill = Column(Integer, ForeignKey("bills.id"))
    from_bill = Column(Integer, ForeignKey("bills.id"))

#Bill Topics

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True)
    name = Column("name", String)
    
class Bill_Topic(Base):
    __tablename__ = "bill_topics"
    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey("bills.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    calculated = Column('calculated', Boolean)

#Sponsorhip Adding

class Sponsorship(Base):
    __tablename__ = "sponsorships"
    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey("bills.id"))
    polid = Column(Integer, ForeignKey("politicians.id"))
    sponsor_type = Column('sponsor_type', String)


#Votes
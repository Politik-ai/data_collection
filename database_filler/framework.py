#!/usr/bin/env python3
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
    thomas_id = Column('thomas_id', Integer)
    date_of_birth = Column('date_of_birth', String)
    first_name = Column('first_name', String)
    last_name = Column('last_name', String)
    terms = relationship("Politician_Term")
    roles = relationship("Leadership_Role")

    def __init__(self, bioid, thomas_id, date_of_birth, first_name, last_name):
        self.bioid = bioid
        self.thomas_id = thomas_id
        self.date_of_birth = date_of_birth
        self.first_name = first_name
        self.last_name = last_name   
        

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
    district = Column('district', Integer)
    

    def __init__(self, polid, start_date, end_date, party, state, legislative_body, gender, district):
        self.polid = polid
        self.start_date = start_date
        self.end_date = end_date
        self.party = party
        self.state = state
        self.legislative_body = legislative_body
        self.gender = gender
        self.district = district    

class Leadership_Role(Base):
    __tablename__ = 'leadership_roles'
    id = Column(Integer, primary_key=True)
    polid = Column(Integer, ForeignKey("politicians.id"))
    role = Column('role', String)
    chamber = Column('chamber', String)
    start_date = Column('start_date', Date)
    end_date = Column('end_date', Date)

    def __init__(self, role, chamber, start_date, end_date, polid):
        self.role = role
        self.chamber = chamber
        self.start_date = start_date
        self.end_date = end_date
        self.polid = polid

class Bill(Base):
    __tablename__ = "bills"
    id = Column(Integer, primary_key=True)
    bill_code = Column('bill_code', String)
    status = Column('status', String)
    originating_body = Column('originating_body', String)

    #references_to_id = Column(Integer, ForeignKey("bill_references.id"))
    #references_from_id = Column(Integer, ForeignKey("bill_references.id"))
    #references_to = relationship("Bill_Reference", foreign_keys=[references_to_id])
    #references_from = relationship("Bill_Reference", foreign_keys=[references_from_id])

    sponsors = relationship("Sponsorship")
    topics = relationship("Bill_Topic")
    bill_states = relationship("Bill_State", back_populates='bill')

    def __init__(self, bill_code, status, originating_body):
        self.id = None
        self.bill_code = bill_code
        self.status = status
        self.originating_body = originating_body

class Bill_State(Base):
    __tablename__ = "bill_states"
    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey("bills.id"))
    bill = relationship("Bill", back_populates='bill_states')

    bill_state_identifier = Column('bill_state_identifier', String)
    bill_type = Column('bill_type', String)
    status_code = Column('status_code', String)
    text_location = Column('text_location', String)
    short_title = Column('short_title', String)
    official_title = Column('official_title', String)
    intro_date = Column('intro_date', Date)
    congress = Column('congress', Integer)

    def __init__(self, bill,bill_id, bill_state_identifier, bill_type, status_code, \
     text_location,short_title,official_title,intro_date,congress):
        self.bill = bill
        self.bill_id = bill_id
        self.bill_state_identifier = bill_state_identifier
        self.bill_type = bill_type
        self.status_code = status_code
        self.text_location = text_location
        self.short_title = short_title
        self.official_title = official_title
        self.intro_date = intro_date
        self.congress = congress


# Bill_ref next 
class Bill_Reference(Base):
    __tablename__ = "bill_references"
    id = Column(Integer, primary_key=True)
    to_bill_id = Column(Integer, ForeignKey("bills.id"))
    from_bill_id = Column(Integer, ForeignKey("bills.id"))

    def __init__(self, from_bill_id,to_bill_id):
        self.from_bill_id = from_bill_id
        self.to_bill_id = from_bill_id

#Bill Topics
class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True)
    name = Column("name", String)

    def __init__(self, name):
        self.name = name
    
class Bill_Topic(Base):
    __tablename__ = "bill_topics"
    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey("bills.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    calculated = Column('calculated', Boolean)

    def __init__(self,bill_id,topic_id):
        self.bill_id = bill_id
        self.topic_id = topic_id

#Sponsorhip Adding
class Sponsorship(Base):
    __tablename__ = "sponsorships"
    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey("bills.id"))
    polid = Column(Integer, ForeignKey("politicians.id"))
    sponsor_type = Column('sponsor_type', String)

    def __init__(self,bill_id,polid,sponsor_type):
        self.bill_id = bill_id
        self.polid = polid
        self.sponsor_type = sponsor_type


#Votes
class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)
    bill_state_id = Column(Integer, ForeignKey("bill_states.id"))
    vote_politicians = relationship("Vote_Politician")
    vote_date = Column('vote_date', Date)


    def __init__(self, bill_state_id, vote_date):
        self.bill_state_id = bill_state_id
        self.vote_date = vote_date


class Vote_Politician(Base):
    __tablename__ = 'vote_politicians'
    id = Column(Integer, primary_key=True)
    vote_id = Column(Integer, ForeignKey("votes.id"))
    polid = Column(Integer, ForeignKey("politicians.id"))
    """
    -2 is Present (acts towards quarum, but not yay or nay)
    -1 is Not Voting
    0 is No
    1 is Yes
    """
    response = Column('response', Integer)

    def __init__(self,vote_id,polid, response):
        self.vote_id = vote_id
        self.polid = polid
        self.response = response

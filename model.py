#!/usr/bin/python

import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base

engine = sqlalchemy.create_engine('postgresql://matching_engine:password@localhost/matching-engine')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.String,primary_key=True,index=True)
    password = sqlalchemy.Column(sqlalchemy.String)
    default_currency = sqlalchemy.Column(sqlalchemy.String,sqlalchemy.ForeignKey('assets.name'),nullable=False)
    active = sqlalchemy.Column(sqlalchemy.Boolean, default='true')
    admin = sqlalchemy.Column(sqlalchemy.Boolean, default='false')

    balance = sqlalchemy.orm.relationship("Balance", order_by="Balance.asset")

    def __repr__(self):
        return "<User: {0.id}>".format(self)


class Asset(Base):
    __tablename__ = 'assets'

    name = sqlalchemy.Column(sqlalchemy.String,primary_key=True)


class Balance(Base):
    __tablename__ = 'balances'
    __table_args__ = (sqlalchemy.PrimaryKeyConstraint('user','asset'),)

    user = sqlalchemy.Column(sqlalchemy.String,sqlalchemy.ForeignKey('users.id'),nullable=False)
    asset = sqlalchemy.Column(sqlalchemy.String,sqlalchemy.ForeignKey('assets.name'),nullable=False)
    balance = sqlalchemy.Column(sqlalchemy.Float)


class Transaction(Base):
    __tablename__ = 'transactions'

    number = sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.Sequence('transaction_number_sequence'),primary_key=True)
    user = sqlalchemy.Column(sqlalchemy.String,sqlalchemy.ForeignKey("users.id"),nullable=False)
    asset = sqlalchemy.Column(sqlalchemy.String,sqlalchemy.ForeignKey("assets.name"),nullable=False)
    amount = sqlalchemy.Column(sqlalchemy.Float)


trig_ddl = sqlalchemy.DDL("""
    CREATE OR REPLACE FUNCTION update_balance() RETURNS trigger AS '
    BEGIN
    UPDATE balances SET balance = balance + NEW.amount WHERE balances.user = NEW.user AND balances.asset = NEW.asset; 
    RETURN NEW;
    END;'
    LANGUAGE plpgsql;

    CREATE TRIGGER update_balance_trigger BEFORE INSERT
    ON transactions
    FOR EACH ROW EXECUTE PROCEDURE
    update_balance();
""")

tbl = Transaction.__table__
sqlalchemy.event.listen(tbl, 'after_create', trig_ddl.execute_if(dialect='postgresql'))

Base.metadata.create_all(engine)

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

if __name__ == "__main__":
    pass

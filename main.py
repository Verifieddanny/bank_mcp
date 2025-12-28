import os
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timezone

API_KEY = os.getenv("ARMORIQ_SECRET", "default_fallback_key_for_local_only")
API_KEY_NAME = "access_token"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Database Configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./banking.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )

# --- Models ---


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    balance = Column(Float, default=0.0)


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    amount = Column(Float)
    type = Column(String) 
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))


Base.metadata.create_all(bind=engine)

app = FastAPI(title="ArmorIQ MCP Banking Server", dependencies=[Depends(get_api_key)])

origins = [
    "http://127.0.0.1:8000/",
    "https://your-production-site.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create_account")
def create_account(name: str, initial_deposit: float = 0.0, db: Session = Depends(get_db)):
    new_account = Account(name=name, balance=initial_deposit)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return {"message": "Account created", "account_id": new_account.id}


@app.post("/deposit")
def deposit(account_id: int, amount: float, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    account.balance += amount
    txn = Transaction(account_id=account_id, amount=amount, type="deposit")
    db.add(txn)
    db.commit()
    return {"new_balance": account.balance}


@app.post("/withdraw")
def withdraw(account_id: int, amount: float, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account or account.balance < amount:
        raise HTTPException(
            status_code=400, detail="Insufficient funds or account missing")

    account.balance -= amount
    txn = Transaction(account_id=account_id, amount=amount, type="withdrawal")
    db.add(txn)
    db.commit()
    return {"new_balance": account.balance}


@app.get("/balance/{account_id}")
def get_balance(account_id: int, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"account_name": account.name, "balance": account.balance}


@app.get("/history/{account_id}")
def get_history(account_id: int, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(
        Transaction.account_id == account_id).all()
    return transactions

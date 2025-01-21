from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .main import get_factorial
from . import models, database

app = FastAPI()
factorial = get_factorial()

# Create tables
models.Base.metadata.create_all(bind=database.engine)

raise Exception

@app.get("/factorial/{input_num}")
async def get_factorial_result(input_num: int, db: Session = Depends(database.get_db)):
    if input_num < 0:
        raise HTTPException(status_code=400, detail="Input must be non-negative")
    try:
        result = factorial(input_num)
        
        # Store the result in the database
        db_result = models.FactorialResult(
            input_number=input_num,
            result=result
        )
        db.add(db_result)
        db.commit()
        
        return {"result": result}
    except RecursionError:
        raise HTTPException(status_code=400, detail="Input too large")

@app.get("/history")
async def get_history(db: Session = Depends(database.get_db)):
    results = db.query(models.FactorialResult).order_by(models.FactorialResult.created_at.desc()).all()
    return results

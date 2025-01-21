from fastapi import FastAPI, HTTPException
from main import get_factorial

app = FastAPI()
factorial = get_factorial()

@app.get("/factorial/{input_num}")
async def get_factorial_result(input_num: int):
    if input_num < 0:
        raise HTTPException(status_code=400, detail="Input must be non-negative")
    try:
        result = factorial(input_num)
        return {"result": result}
    except RecursionError:
        raise HTTPException(status_code=400, detail="Input too large")

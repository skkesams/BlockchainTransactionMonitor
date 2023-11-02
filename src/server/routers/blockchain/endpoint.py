from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os

from core.utils import log_exception, read_yaml
from src.server.routers.blockchain.handle_request import handle_request
from src.server.routers.blockchain.postprocess import postprocess

router = APIRouter()

security = HTTPBasic()


@router.post("/blockchain_data")
async def blockchain_data_request(
        rq_payload: dict = {"num_of_records": 10},
        credentials: HTTPBasicCredentials = Depends(security),
):
    username = credentials.username
    password = credentials.password

    try:
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        api_conf = read_yaml(__location__ + "/config/api_credentials.yaml")

        assert username == api_conf.get("username", "") and password == api_conf.get("password", "")

    except OSError as e:
        log_exception(e, "Error while reading api credentials")
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error",
        )

    except Exception as e:
        log_exception(e, f"Error Unauthorized")
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorized",
        )

    try:
        num_records = rq_payload.get("num_of_records", 10)
        data = await handle_request(num_records)
        output = await postprocess(data)
        return output
    except Exception as e:
        log_exception(e, "Error in Instant Report API")
        raise HTTPException(
            status_code=500,
            detail=f"Error in Instant Report API",
        )
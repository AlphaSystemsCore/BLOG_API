from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.responses import JSONResponse
from typing import Annotated, List


post_router = APIRouter(tags=["posts"])


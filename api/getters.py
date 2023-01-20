from fastapi import APIRouter, Body, Request, Response, HTTPException, status, FastAPI
from fastapi.encoders import jsonable_encoder
from typing import List

from dotenv import dotenv_values, find_dotenv

router = APIRouter()

config = dotenv_values(find_dotenv('.env'))


@router.get("/availability/{start_date}/{end_date}", response_description="Get availability", status_code=status.HTTP_200_OK)
def get_availability(start_date: str, end_date: str, request: Request):
    data = []
    #start_date = req['start_date']
    #end_date = req['end_date']

    availability = list(request.app.database[config['CACHED_COLLECTION_NAME']].find({"effective_date": {"$gt": start_date,
                                                                                                        "$lt": end_date}}, limit=100))
    if availability is not None:
        for item in availability:
            item['_id'] = str(item['_id'])

        for avail_record in availability:
            property_record = request.app.database[config['PROPERTY_COLLECTION_NAME']].find_one({"guid": avail_record['property_guid']})
            if property_record is not None:
                property_record['_id'] = str(property_record['_id'])
                data.append({"property": property_record, "availability": avail_record})

    if data is not None:
        return {"message": f"Found data for date range {start_date} to {end_date}", "data": data}
    return {"message": f"No data found for date range {start_date} to {end_date}", "data": data}
import requests
from typing import Generator, Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import SessionLocal
from app.db.models import BtcUsdPrice, Leads


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_application() -> FastAPI:
    application = FastAPI(
        title='Fetch api',
        debug=False,
        version='0.1.0',
    )

    # Set all CORS enabled origins
    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.get('/leads/')
    def get_leads(

            db: Session = Depends(get_db),
            limit: Optional[int] = 20,
            offset: Optional[int] = 0
    ):
        return db.execute(select(Leads).order_by('id').offset(offset).limit(limit)).scalars().fetchall()

    @application.get('/leads/bulk-save/')
    def bulk_save_leads(
            db: Session = Depends(get_db),
    ):
        data = [{"phone_work": '1234456', "first_name": 'xxxx', "last_name": 'zzzzzzz'}]
        objs_in = [
            Leads(phone_work=obj.get('phone_work'), first_name=obj.get('first_name'), last_name=obj.get('last_name'))
            for obj in data
        ]

        # bulk save the models
        db.bulk_save_objects(objs_in)
        db.commit()
        return True

    @application.get('/btc-usd-price/')
    def get_btc_usd_price(
            db: Session = Depends(get_db),
            limit: Optional[int] = 20,
            offset: Optional[int] = 0
    ):
        return db.execute(select(BtcUsdPrice).order_by('id').offset(offset).limit(limit)).scalars().fetchall()

    @application.get('/btc-usd-price/')
    def bulk_save_leads_btc_usd_price(
            db: Session = Depends(get_db),
    ):
        data = [{"value": 12344}, {"value": 1324, }, {"value": 45}]
        objs_in = [
            BtcUsdPrice(value=obj.get('value'))
            for obj in data
        ]

        # bulk save the models
        db.bulk_save_objects(objs_in)
        db.commit()
        return True

    # @application.get('/leads/fetch/')
    # def fetch_api(
    #         db: Session = Depends(get_db)
    # ):
    #     # Define the Suite CRM URL and API endpoint URL
    #
    #     suite_crm_url = 'https://suitecrmdemo.dtbc.eu'
    #     api_endpoint_url = '/service/v4/rest.php/module/Leads'
    #     # Define the headers for the API request with the username and password
    #     headers = {'Content-Type': 'application/json'}
    #     data = {'grant_type': 'password', 'username': 'Demo', 'password': 'Demo'}
    #     response = requests.post(suite_crm_url + '/Api/access_token', headers=headers, data=data)
    #     access_token = response.json()['access_token']
    #     headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    #
    #     # Make the API request to fetch leads
    #     response = requests.get(suite_crm_url + api_endpoint_url, headers=headers)
    #
    #     # Check the response status code and content
    #     if response.status_code == 200:
    #         leads_data = response.json()
    #         # Do something with the leads data
    #     else:
    #         raise HTTPException(status_code=400, detail='Error fetching leads: ' + response.text)
    #     # price = BtcUsdPrice(amount=leads_data.get('data').get('amount'))
    #     # db.add(price)
    #     # db.commit()
    #     # return price
    #     return {}
    # return application


app = get_application()

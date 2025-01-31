import json

import requests
from app.config import constants, settings
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependecies.exceptions import RequestExternalAPIFailed
from ..schemas.imei_schema import ImeiInfo

HEADERS = {
    'Authorization': f'Bearer {settings.IMEI_CHECK_TOKEN}',
    'Content-Type': 'application/json',
}


async def validate_imei_schema(data: dict) -> ImeiInfo:
    print(data)
    
    data = data['properties']
    model = ImeiInfo(
        device_name=data['deviceName'] if 'deviceName' in data else None,
        image=data['image'] if 'image' in data else None,
        imei=data['imei'] if 'imei' in data else None,
        meid=data['meid'] if 'meid' in data else None,
        imei2=data['imei2'] if 'imei2' in data else None,
        serial=data['serial'] if 'serial' in data else None,
        est_purchase_date=data['estPurchaseDate'] if 'estPurchaseDate' in data else None,
        sim_lock=data['simLock'] if 'simLock' in data else None,
        warranty_status=data['warrantyStatus'] if 'warrantyStatus' in data else None,
        technical_support=data['technicalSupport'] if 'technicalSupport' in data else None,
        model_desc=data['modelDesc'] if 'modelDesc' in data else None,
        purchase_country=data['purchaseCountry'] if 'purchaseCountry' in data else None,
        apple_region=data['appleRegion'] if 'appleRegion' in data else None,
        fmi_on=data['fmiOn'] if 'fmiOn' in data else None,
        lost_mode=data['lostMode'] if 'lostMode' in data else None,
        repair_coverage=data['repairCoverage'] if 'repairCoverage' in data else None,
        demo_unit=data['demoUnit'] if 'demoUnit' in data else None,
        refurbished=data['refurbished'] if 'refurbished' in data else None,
        usa_block_status=data['usaBlockStatus'] if 'usaBlockStatus' in data else None,
        network=data['network'] if 'network' in data else None,
    )
    
    print(model)
    
    return model


async def check_imei(imei: str):
    body = {
        'deviceId': imei,
        'serviceId': constants.IMEI_SERVICE_ID
    }
    body = json.dumps(body)
    
    response = requests.post(
        url=constants.IMEI_BASE_URL,
        headers=HEADERS,
        data=body
    )
    response_json = json.loads(response.text)
    
    if response_json['status'] in ['failed', 'unsuccessful']:
        raise RequestExternalAPIFailed
    
    model = await validate_imei_schema(response_json)
    return model
    
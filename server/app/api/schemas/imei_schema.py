from pydantic import BaseModel, Field
from typing import Optional, Annotated


class ImeiInfo(BaseModel):
    device_name: Optional[str]
    image: Optional[str]
    imei: Optional[str]
    meid: Optional[str]
    imei2: Optional[str]
    serial: Optional[str]
    est_purchase_date: Optional[int]
    sim_lock: Optional[bool]
    warranty_status: Optional[str]
    technical_support: Optional[bool]
    model_desc: Optional[str]
    purchase_country: Optional[str]
    apple_region: Optional[str]
    fmi_on: Optional[bool]
    lost_mode: Optional[bool]
    repair_coverage: Optional[str | bool]
    demo_unit: Optional[bool]
    refurbished: Optional[bool]
    usa_block_status: Optional[str]
    network: Optional[str]


class ImeiCheck(BaseModel):
    imei: Annotated[str, Field(min_length=8, max_length=15)]
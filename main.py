from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Simple in-memory ban storage — replace with DB for production
banned_userids = set()
banned_ips = set()
banned_hwids = set()

class BanRequest(BaseModel):
    userId: Optional[int] = None
    ip: Optional[str] = None
    hwid: Optional[str] = None
    reason: Optional[str] = None

class CheckRequest(BaseModel):
    userId: Optional[int] = None
    ip: Optional[str] = None
    hwid: Optional[str] = None

@app.post("/ban")
async def ban(data: BanRequest):
    if data.userId:
        banned_userids.add(data.userId)
    if data.ip:
        banned_ips.add(data.ip)
    if data.hwid:
        banned_hwids.add(data.hwid)
    print(f"Banned: UserId={data.userId}, IP={data.ip}, HWID={data.hwid}, Reason={data.reason}")
    return {"success": True}

@app.post("/unban")
async def unban(data: BanRequest):
    if data.userId:
        banned_userids.discard(data.userId)
    if data.ip:
        banned_ips.discard(data.ip)
    if data.hwid:
        banned_hwids.discard(data.hwid)
    print(f"Unbanned: UserId={data.userId}, IP={data.ip}, HWID={data.hwid}")
    return {"success": True}

@app.post("/check")
async def check(data: CheckRequest):
    banned = False
    if data.userId and data.userId in banned_userids:
        banned = True
    if data.ip and data.ip in banned_ips:
        banned = True
    if data.hwid and data.hwid in banned_hwids:
        banned = True
    return {"banned": banned}

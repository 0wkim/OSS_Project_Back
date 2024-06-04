from fastapi import FastAPI, APIRouter, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI()

# CORS 설정
origins = ["http://127.0.0.1:5501", "http://52.71.126.245"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIRouter 인스턴스 생성
router = APIRouter()

# 방명록 데이터를 저장할 리스트
guestbook_entries = []

class GuestbookEntry(BaseModel):
    name: str
    message: str
    timestamp: datetime

# 방명록 데이터 반환
@router.get('/guestbook', response_model=List[GuestbookEntry])
def get_guestbook_entries():
    return guestbook_entries

# 방명록 엔트리리 추가
@router.post('/guestbook', response_model=GuestbookEntry)
def add_guestbook_entry(entry: GuestbookEntry):
    if not entry.name or not entry.message:
        raise HTTPException(status_code=400, detail="Name and message are required")
    
    entry.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    guestbook_entries.append(entry)
    return entry

# 방명록 엔트리 삭제
@router.delete('/guestbook/{index}', response_model=GuestbookEntry)
def delete_guestbook_entry(index: int = Path(..., description="The index of the guestbook entry to delete")):
    if 0 <= index < len(guestbook_entries):
        return guestbook_entries.pop(index)
    else:
        raise HTTPException(status_code=400, detail="Invalid index")

# 라우터 등록
app.include_router(router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=80)
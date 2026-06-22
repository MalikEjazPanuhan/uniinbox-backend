from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from src.core.database import get_db
from src.models.user import User
from src.models.channel import Channel
from src.schemas.channel import ChannelCreate, ChannelUpdate, ChannelResponse
from src.api.deps import get_current_user

router = APIRouter(prefix="/channels", tags=["channels"])

@router.post("/", response_model=ChannelResponse)
async def connect_channel(
    channel_data: ChannelCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if channel with same name exists
    existing = db.query(Channel).filter(
        Channel.user_id == current_user.id,
        Channel.channel_name == channel_data.channel_name,
        Channel.channel_type == channel_data.channel_type,
        Channel.is_active == True
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Channel with this name and type already exists"
        )
    
    channel = Channel(
        user_id=current_user.id,
        channel_type=channel_data.channel_type,
        channel_name=channel_data.channel_name,
        config=channel_data.config,
        sync_enabled=channel_data.sync_enabled,
        sync_frequency=channel_data.sync_frequency,
        monitored_folders=channel_data.monitored_folders,
        excluded_folders=channel_data.excluded_folders
    )
    
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return channel

@router.get("/", response_model=List[ChannelResponse])
async def get_channels(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Channel).filter(
        Channel.user_id == current_user.id,
        Channel.is_active == True
    ).all()

@router.get("/{channel_id}", response_model=ChannelResponse)
async def get_channel(
    channel_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    channel = db.query(Channel).filter(
        Channel.id == channel_id,
        Channel.user_id == current_user.id
    ).first()
    
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    return channel

@router.put("/{channel_id}", response_model=ChannelResponse)
async def update_channel(
    channel_id: uuid.UUID,
    channel_data: ChannelUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    channel = db.query(Channel).filter(
        Channel.id == channel_id,
        Channel.user_id == current_user.id
    ).first()
    
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    update_dict = channel_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(channel, key, value)
    
    db.commit()
    db.refresh(channel)
    return channel

@router.delete("/{channel_id}")
async def delete_channel(
    channel_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    channel = db.query(Channel).filter(
        Channel.id == channel_id,
        Channel.user_id == current_user.id
    ).first()
    
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    channel.is_active = False
    db.commit()
    return {"message": "Channel disconnected successfully"}

@router.post("/{channel_id}/sync")
async def sync_channel(
    channel_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    channel = db.query(Channel).filter(
        Channel.id == channel_id,
        Channel.user_id == current_user.id
    ).first()
    
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    # Trigger sync task (will be implemented with Celery)
    # For now, just update last_sync
    from datetime import datetime
    channel.last_sync = datetime.utcnow()
    db.commit()
    
    return {"message": "Sync started successfully", "channel_id": str(channel_id)}


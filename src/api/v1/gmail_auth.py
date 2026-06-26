from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from google_auth_oauthlib.flow import Flow
import logging

from src.core.database import get_db
from src.core.config import settings
from src.models.user import User
from src.models.channel import Channel
from src.api.deps import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth/gmail", tags=["gmail"])

@router.get("/auth-url")
async def get_gmail_auth_url(
    current_user: User = Depends(get_current_user),
):
    """Generate the Gmail OAuth URL for the user to authorize."""
    if not settings.GMAIL_CLIENT_ID or not settings.GMAIL_CLIENT_SECRET:
        raise HTTPException(
            status_code=500,
            detail="Gmail client ID or secret not configured on the server."
        )

    try:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": settings.GMAIL_CLIENT_ID,
                    "client_secret": settings.GMAIL_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [settings.GMAIL_REDIRECT_URI]
                }
            },
            scopes=[
                "https://www.googleapis.com/auth/gmail.readonly",
                "https://www.googleapis.com/auth/gmail.send",
                "https://www.googleapis.com/auth/gmail.compose"
            ],
            redirect_uri=settings.GMAIL_REDIRECT_URI
        )

        auth_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )

        return {"auth_url": auth_url, "state": state}
    except Exception as e:
        logger.error(f"Error generating Gmail auth URL: {e}")
        raise HTTPException(status_code=500, detail="Could not generate authorization URL.")

@router.get("/callback")
async def gmail_callback(
    request: Request,
    code: str,
    state: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle the OAuth callback from Google after user authorization."""
    logger.info(f"Gmail callback received for user: {current_user.email}")

    if not settings.GMAIL_CLIENT_ID or not settings.GMAIL_CLIENT_SECRET:
        raise HTTPException(
            status_code=500,
            detail="Gmail client ID or secret not configured."
        )

    try:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": settings.GMAIL_CLIENT_ID,
                    "client_secret": settings.GMAIL_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [settings.GMAIL_REDIRECT_URI]
                }
            },
            scopes=[
                "https://www.googleapis.com/auth/gmail.readonly",
                "https://www.googleapis.com/auth/gmail.send",
                "https://www.googleapis.com/auth/gmail.compose"
            ],
            redirect_uri=settings.GMAIL_REDIRECT_URI
        )

        flow.fetch_token(code=code)
        credentials = flow.credentials

        logger.info(f"Token received: {bool(credentials.token)}")
        logger.info(f"Refresh token received: {bool(credentials.refresh_token)}")

        if not credentials or not credentials.token:
            raise HTTPException(status_code=400, detail="Failed to obtain access token from Google.")

        # Delete any existing Gmail channel for this user
        db.query(Channel).filter(
            Channel.user_id == current_user.id,
            Channel.channel_type == "gmail"
        ).delete()

        # Create new channel with tokens
        new_channel = Channel(
            user_id=current_user.id,
            channel_type="gmail",
            channel_name="Gmail",
            access_token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_expiry=credentials.expiry,
            is_active=True,
            config={}
        )
        db.add(new_channel)
        db.commit()

        logger.info(f"Gmail OAuth successful! Token saved for user: {current_user.email}")
        logger.info(f"Channel ID: {new_channel.id}")

        return {"message": "Gmail connected successfully!", "success": True}

    except Exception as e:
        logger.error(f"Error in Gmail OAuth callback: {e}")
        db.rollback()
        raise HTTPException(status_code=400, detail=f"OAuth callback failed: {str(e)}")

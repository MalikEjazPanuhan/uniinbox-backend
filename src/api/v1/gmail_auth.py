from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import json
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

        # In a production app, you should store the 'state' in the user's session
        # to prevent CSRF attacks. For simplicity in this guide, we are not implementing that.
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
            detail="Gmail client ID or secret not configured on the server."
        )

    try:
        # Recreate the flow with the same configuration
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

        # Fetch the access token using the authorization code
        flow.fetch_token(code=code)
        credentials = flow.credentials

        if not credentials or not credentials.token:
            raise HTTPException(status_code=400, detail="Failed to obtain access token from Google.")

        # Save or update the Gmail channel for this user
        existing_channel = db.query(Channel).filter(
            Channel.user_id == current_user.id,
            Channel.channel_type == "gmail"
        ).first()

        if existing_channel:
            # Update existing channel with new tokens
            existing_channel.access_token = credentials.token
            existing_channel.refresh_token = credentials.refresh_token
            existing_channel.token_expiry = credentials.expiry
            existing_channel.is_active = True
            logger.info(f"Updated existing Gmail channel for user: {current_user.email}")
        else:
            # Create a new channel
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
            logger.info(f"Created new Gmail channel for user: {current_user.email}")

        db.commit()
        logger.info(f"Gmail OAuth flow successful for user: {current_user.email}")

        # You can redirect to a success page or return a JSON response
        # For a frontend application, a redirect is often best.
        return {"message": "Gmail connected successfully!"}

    except Exception as e:
        logger.error(f"Error in Gmail OAuth callback: {e}")
        db.rollback()
        raise HTTPException(status_code=400, detail=f"OAuth callback failed: {str(e)}")

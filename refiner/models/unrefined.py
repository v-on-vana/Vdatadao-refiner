from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class Contributor(BaseModel):
    wallet_address: str
    email: str
    name: str
    locale: str


class Profile(BaseModel):
    username: str
    display_name: str
    email: str
    account_type: str
    date_of_birth: str
    phone_confirmed: bool
    private_account: bool


class Metrics(BaseModel):
    posts_count: int
    following_count: int
    follower_count: int
    likes_given_count: int
    comments_count: int
    account_age_days: int
    total_interactions: int
    has_story_activity: bool


class Following(BaseModel):
    username: str
    followed_at: int


class LikeGiven(BaseModel):
    target_username: str
    count: int
    last_activity: int


class PostCreated(BaseModel):
    creation_timestamp: int
    title: str
    source_app: str
    has_photo: bool
    has_camera_metadata: bool


class CommentMade(BaseModel):
    timestamp: int
    target_username: str


class Activities(BaseModel):
    following_list: List[Following]
    likes_given: List[LikeGiven]
    posts_created: List[PostCreated]
    comments_made: List[CommentMade]


class Security(BaseModel):
    last_login: int
    contact_syncing: bool
    has_shared_live_video: bool


class RawExportData(BaseModel):
    note: str
    
    class Config:
        extra = "allow"


class FolderStructure(BaseModel):
    metaFolderId: str
    instagramFolderId: str
    instagramFolderName: str


class PrivacySettings(BaseModel):
    contains_pii: bool
    anonymization_level: str
    retention_policy: str


class InstagramMetadata(BaseModel):
    version: str
    schema_version: str
    source: str
    collection_date: str
    data_type: str
    processing_timestamp: int
    extraction_completeness: float
    folder_structure: FolderStructure
    privacy_settings: PrivacySettings
    quality_score: float
    data_freshness: float


class InstagramData(BaseModel):
    platform: str
    source_type: str
    extraction_method: str
    profile: Profile
    metrics: Metrics
    activities: Activities
    security: Security
    raw_export_data: RawExportData


class InstagramExport(BaseModel):
    contribution_id: str
    contributor: Contributor
    data: InstagramData
    metadata: InstagramMetadata
    created_at: str
    updated_at: str

from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    ForeignKey,
    DateTime,
    Text,
    JSON,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class InstagramUser(Base):
    __tablename__ = "instagram_users"

    contribution_id = Column(String, primary_key=True)
    wallet_address = Column(String, nullable=False)
    contributor_email = Column(String, nullable=False)
    contributor_name = Column(String, nullable=False)
    contributor_locale = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    profiles = relationship("InstagramProfile", back_populates="user")
    metrics = relationship("InstagramMetric", back_populates="user")
    followings = relationship("InstagramFollowing", back_populates="user")
    likes = relationship("InstagramLike", back_populates="user")
    posts = relationship("InstagramPost", back_populates="user")
    comments = relationship("InstagramComment", back_populates="user")
    security = relationship("InstagramSecurity", back_populates="user")
    export_metadata = relationship("InstagramExportMetadata", back_populates="user")


class InstagramProfile(Base):
    __tablename__ = "instagram_profiles"

    profile_id = Column(Integer, primary_key=True, autoincrement=True)
    contribution_id = Column(
        String, ForeignKey("instagram_users.contribution_id"), nullable=False
    )
    username = Column(String, nullable=False)
    display_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    account_type = Column(String, nullable=False)
    date_of_birth = Column(String, nullable=False)
    phone_confirmed = Column(Boolean, nullable=False)
    private_account = Column(Boolean, nullable=False)

    user = relationship("InstagramUser", back_populates="profiles")


class InstagramMetric(Base):
    __tablename__ = "instagram_metrics"

    metric_id = Column(Integer, primary_key=True, autoincrement=True)
    contribution_id = Column(
        String, ForeignKey("instagram_users.contribution_id"), nullable=False
    )
    posts_count = Column(Integer, nullable=False)
    following_count = Column(Integer, nullable=False)
    follower_count = Column(Integer, nullable=False)
    likes_given_count = Column(Integer, nullable=False)
    comments_count = Column(Integer, nullable=False)
    account_age_days = Column(Integer, nullable=False)
    total_interactions = Column(Integer, nullable=False)
    has_story_activity = Column(Boolean, nullable=False)

    user = relationship("InstagramUser", back_populates="metrics")


class InstagramFollowing(Base):
    __tablename__ = "instagram_followings"

    following_id = Column(Integer, primary_key=True, autoincrement=True)
    contribution_id = Column(
        String, ForeignKey("instagram_users.contribution_id"), nullable=False
    )
    username = Column(String, nullable=False)
    followed_at = Column(DateTime, nullable=False)

    user = relationship("InstagramUser", back_populates="followings")


class InstagramLike(Base):
    __tablename__ = "instagram_likes"

    like_id = Column(Integer, primary_key=True, autoincrement=True)
    contribution_id = Column(
        String, ForeignKey("instagram_users.contribution_id"), nullable=False
    )
    target_username = Column(String, nullable=False)
    count = Column(Integer, nullable=False)
    last_activity = Column(DateTime, nullable=False)

    user = relationship("InstagramUser", back_populates="likes")


class InstagramPost(Base):
    __tablename__ = "instagram_posts"

    post_id = Column(Integer, primary_key=True, autoincrement=True)
    contribution_id = Column(
        String, ForeignKey("instagram_users.contribution_id"), nullable=False
    )
    creation_timestamp = Column(DateTime, nullable=False)
    title = Column(String, nullable=False)
    source_app = Column(String, nullable=False)
    has_photo = Column(Boolean, nullable=False)
    has_camera_metadata = Column(Boolean, nullable=False)

    user = relationship("InstagramUser", back_populates="posts")


class InstagramComment(Base):
    __tablename__ = "instagram_comments"

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    contribution_id = Column(
        String, ForeignKey("instagram_users.contribution_id"), nullable=False
    )
    timestamp = Column(DateTime, nullable=False)
    target_username = Column(String, nullable=False)

    user = relationship("InstagramUser", back_populates="comments")


class InstagramSecurity(Base):
    __tablename__ = "instagram_security"

    security_id = Column(Integer, primary_key=True, autoincrement=True)
    contribution_id = Column(
        String, ForeignKey("instagram_users.contribution_id"), nullable=False
    )
    last_login = Column(DateTime, nullable=False)
    contact_syncing = Column(Boolean, nullable=False)
    has_shared_live_video = Column(Boolean, nullable=False)

    user = relationship("InstagramUser", back_populates="security")


class InstagramExportMetadata(Base):
    __tablename__ = "instagram_export_metadata"

    metadata_id = Column(Integer, primary_key=True, autoincrement=True)
    contribution_id = Column(
        String, ForeignKey("instagram_users.contribution_id"), nullable=False
    )
    version = Column(String, nullable=False)
    schema_version = Column(String, nullable=False)
    source = Column(String, nullable=False)
    collection_date = Column(DateTime, nullable=False)
    data_type = Column(String, nullable=False)
    processing_timestamp = Column(Integer, nullable=False)
    extraction_completeness = Column(Float, nullable=False)
    meta_folder_id = Column(String, nullable=False)
    instagram_folder_id = Column(String, nullable=False)
    instagram_folder_name = Column(String, nullable=False)
    contains_pii = Column(Boolean, nullable=False)
    anonymization_level = Column(String, nullable=False)
    retention_policy = Column(String, nullable=False)
    quality_score = Column(Float, nullable=False)
    data_freshness = Column(Float, nullable=False)
    platform = Column(String, nullable=False)
    source_type = Column(String, nullable=False)
    extraction_method = Column(String, nullable=False)
    raw_export_note = Column(Text, nullable=True)
    raw_export_data_json = Column(JSON, nullable=True)

    user = relationship("InstagramUser", back_populates="export_metadata")

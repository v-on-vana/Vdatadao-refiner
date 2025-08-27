from typing import Dict, Any, List
from refiner.models.refined import Base
from refiner.transformer.base_transformer import DataTransformer
from refiner.models.refined import (
    InstagramUser,
    InstagramProfile,
    InstagramMetric,
    InstagramFollowing,
    InstagramLike,
    InstagramPost,
    InstagramComment,
    InstagramSecurity,
    InstagramExportMetadata,
)
from refiner.models.unrefined import InstagramExport
from refiner.utils.date import parse_timestamp
from refiner.utils.pii import mask_email, mask_full_name, mask_username, mask_wallet_address, mask_birth_date, process_raw_export_safely
from datetime import datetime


class InstagramTransformer(DataTransformer):
    """
    Transformer for Instagram Meta Export data.
    """

    def transform(self, data: Dict[str, Any]) -> List[Base]:
        """
        Transform raw Instagram data into SQLAlchemy model instances.

        Args:
            data: Dictionary containing Instagram export data

        Returns:
            List of SQLAlchemy model instances
        """
        unrefined_data = InstagramExport.model_validate(data)

        models = []

        created_at = datetime.fromisoformat(
            unrefined_data.created_at.replace("Z", "+00:00")
        )
        updated_at = datetime.fromisoformat(
            unrefined_data.updated_at.replace("Z", "+00:00")
        )

        user = InstagramUser(
            contribution_id=unrefined_data.contribution_id,
            wallet_address=mask_wallet_address(unrefined_data.contributor.wallet_address),
            contributor_email=mask_email(unrefined_data.contributor.email),
            contributor_name=mask_full_name(unrefined_data.contributor.name),
            contributor_locale=unrefined_data.contributor.locale,
            created_at=created_at,
            updated_at=updated_at,
        )
        models.append(user)

        profile = InstagramProfile(
            contribution_id=unrefined_data.contribution_id,
            username=mask_username(unrefined_data.data.profile.username),
            display_name=mask_full_name(unrefined_data.data.profile.display_name),
            email=mask_email(unrefined_data.data.profile.email),
            account_type=unrefined_data.data.profile.account_type,
            date_of_birth=mask_birth_date(unrefined_data.data.profile.date_of_birth),
            phone_confirmed=unrefined_data.data.profile.phone_confirmed,
            private_account=unrefined_data.data.profile.private_account,
        )
        models.append(profile)

        metrics = InstagramMetric(
            contribution_id=unrefined_data.contribution_id,
            posts_count=unrefined_data.data.metrics.posts_count,
            following_count=unrefined_data.data.metrics.following_count,
            follower_count=unrefined_data.data.metrics.follower_count,
            likes_given_count=unrefined_data.data.metrics.likes_given_count,
            comments_count=unrefined_data.data.metrics.comments_count,
            account_age_days=unrefined_data.data.metrics.account_age_days,
            total_interactions=unrefined_data.data.metrics.total_interactions,
            has_story_activity=unrefined_data.data.metrics.has_story_activity,
        )
        models.append(metrics)

        for following in unrefined_data.data.activities.following_list:
            following_record = InstagramFollowing(
                contribution_id=unrefined_data.contribution_id,
                username=mask_username(following.username),
                followed_at=parse_timestamp(following.followed_at),
            )
            models.append(following_record)

        for like in unrefined_data.data.activities.likes_given:
            like_record = InstagramLike(
                contribution_id=unrefined_data.contribution_id,
                target_username=mask_username(like.target_username),
                count=like.count,
                last_activity=parse_timestamp(like.last_activity),
            )
            models.append(like_record)

        for post in unrefined_data.data.activities.posts_created:
            post_record = InstagramPost(
                contribution_id=unrefined_data.contribution_id,
                creation_timestamp=parse_timestamp(post.creation_timestamp),
                title=post.title,
                source_app=post.source_app,
                has_photo=post.has_photo,
                has_camera_metadata=post.has_camera_metadata,
            )
            models.append(post_record)

        for comment in unrefined_data.data.activities.comments_made:
            comment_record = InstagramComment(
                contribution_id=unrefined_data.contribution_id,
                timestamp=parse_timestamp(comment.timestamp),
                target_username=mask_username(comment.target_username),
            )
            models.append(comment_record)

        security = InstagramSecurity(
            contribution_id=unrefined_data.contribution_id,
            last_login=parse_timestamp(unrefined_data.data.security.last_login),
            contact_syncing=unrefined_data.data.security.contact_syncing,
            has_shared_live_video=unrefined_data.data.security.has_shared_live_video,
        )
        models.append(security)

        collection_date = datetime.fromisoformat(
            unrefined_data.metadata.collection_date.replace("Z", "+00:00")
        )

        cleaned_raw_data = None
        if unrefined_data.data.raw_export_data:
            raw_export_dict = unrefined_data.data.raw_export_data.model_dump()
            note = raw_export_dict.pop('note', '')
            if raw_export_dict:
                cleaned_raw_data = process_raw_export_safely(raw_export_dict)
        
        metadata = InstagramExportMetadata(
            contribution_id=unrefined_data.contribution_id,
            version=unrefined_data.metadata.version,
            schema_version=unrefined_data.metadata.schema_version,
            source=unrefined_data.metadata.source,
            collection_date=collection_date,
            data_type=unrefined_data.metadata.data_type,
            processing_timestamp=unrefined_data.metadata.processing_timestamp,
            extraction_completeness=unrefined_data.metadata.extraction_completeness,
            meta_folder_id=unrefined_data.metadata.folder_structure.metaFolderId,
            instagram_folder_id=unrefined_data.metadata.folder_structure.instagramFolderId,
            instagram_folder_name=unrefined_data.metadata.folder_structure.instagramFolderName,
            contains_pii=unrefined_data.metadata.privacy_settings.contains_pii,
            anonymization_level=unrefined_data.metadata.privacy_settings.anonymization_level,
            retention_policy=unrefined_data.metadata.privacy_settings.retention_policy,
            quality_score=unrefined_data.metadata.quality_score,
            data_freshness=unrefined_data.metadata.data_freshness,
            platform=unrefined_data.data.platform,
            source_type=unrefined_data.data.source_type,
            extraction_method=unrefined_data.data.extraction_method,
            raw_export_note=unrefined_data.data.raw_export_data.note,
            raw_export_data_json=cleaned_raw_data,
        )
        models.append(metadata)

        return models

from sqlmodel import Session, select
from typing import List, Optional
from ..models.task import Tag, TagCreate, TagUpdate
from fastapi import HTTPException


class TagService:
    """Service class for managing tags."""

    def create_tag(self, db: Session, tag_data: TagCreate) -> Tag:
        """Create a new tag."""
        # Check if tag already exists for this user
        existing_tag = db.exec(
            select(Tag).where(Tag.name == tag_data.name).where(Tag.user_id == tag_data.user_id)
        ).first()
        
        if existing_tag:
            raise HTTPException(status_code=400, detail=f"Tag '{tag_data.name}' already exists for this user")
        
        tag = Tag.model_validate(tag_data)
        db.add(tag)
        db.commit()
        db.refresh(tag)
        return tag

    def get_tags_by_user(self, db: Session, user_id: int) -> List[Tag]:
        """Get all tags for a specific user."""
        tags = db.exec(select(Tag).where(Tag.user_id == user_id)).all()
        return tags

    def get_tag_by_id(self, db: Session, tag_id: str) -> Optional[Tag]:
        """Get a tag by its ID."""
        tag = db.get(Tag, tag_id)
        return tag

    def update_tag(self, db: Session, tag_id: str, tag_data: TagUpdate) -> Optional[Tag]:
        """Update an existing tag."""
        tag = db.get(Tag, tag_id)
        if not tag:
            return None
        
        update_data = tag_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tag, field, value)
        
        db.add(tag)
        db.commit()
        db.refresh(tag)
        return tag

    def delete_tag(self, db: Session, tag_id: str) -> bool:
        """Delete a tag by its ID."""
        tag = db.get(Tag, tag_id)
        if not tag:
            return False
        
        db.delete(tag)
        db.commit()
        return True

    def get_tag_by_name_and_user(self, db: Session, name: str, user_id: int) -> Optional[Tag]:
        """Get a tag by its name and user ID."""
        tag = db.exec(
            select(Tag).where(Tag.name == name).where(Tag.user_id == user_id)
        ).first()
        return tag
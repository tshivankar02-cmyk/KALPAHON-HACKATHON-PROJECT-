from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # INFLUENCER | BRAND
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    campaigns = db.relationship("Campaign", back_populates="brand", cascade="all, delete-orphan")
    applications = db.relationship("Application", back_populates="influencer", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "bio": self.bio,
            "created_at": self.created_at.isoformat(),
        }


class Campaign(db.Model):
    __tablename__ = "campaigns"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    brand = db.relationship("User", back_populates="campaigns")
    applications = db.relationship("Application", back_populates="campaign", cascade="all, delete-orphan")

    def to_dict(self, include_applications=False):
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "budget": self.budget,
            "brand_id": self.brand_id,
            "brand_name": self.brand.name if self.brand else "Unknown",
            "application_count": len(self.applications),
            "created_at": self.created_at.isoformat(),
        }
        if include_applications:
            data["brand_bio"] = self.brand.bio if self.brand else None
            data["applications"] = [a.to_dict() for a in self.applications]
        return data


class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    influencer_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    pitch_text = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="PENDING", nullable=False)  # PENDING | ACCEPTED | REJECTED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    influencer = db.relationship("User", back_populates="applications")
    campaign = db.relationship("Campaign", back_populates="applications")

    def to_dict(self):
        return {
            "id": self.id,
            "influencer_id": self.influencer_id,
            "influencer_name": self.influencer.name if self.influencer else "Unknown",
            "influencer_bio": self.influencer.bio if self.influencer else None,
            "campaign_id": self.campaign_id,
            "campaign_title": self.campaign.title if self.campaign else "Unknown",
            "campaign_budget": self.campaign.budget if self.campaign else 0,
            "pitch_text": self.pitch_text,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }

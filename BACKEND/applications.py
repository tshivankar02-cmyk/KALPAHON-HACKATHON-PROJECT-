from flask import Blueprint, request, jsonify
from models import db, Campaign, Application
from utils import jwt_required, role_required

applications_bp = Blueprint("applications", __name__)


@applications_bp.route("/applications", methods=["POST"])
@jwt_required
@role_required("INFLUENCER")
def create_application(current_user):
    d = request.get_json(silent=True) or {}
    campaign_id = d.get("campaign_id")
    pitch_text = (d.get("pitch_text") or "").strip()
    if not campaign_id or not pitch_text:
        return jsonify({"message": "campaign_id and pitch_text are required", "code": 400}), 400
    if not Campaign.query.get(campaign_id):
        return jsonify({"message": "Campaign not found", "code": 404}), 404
    if Application.query.filter_by(influencer_id=current_user.id, campaign_id=campaign_id).first():
        return jsonify({"message": "You have already applied to this campaign", "code": 409}), 409
    a = Application(influencer_id=current_user.id, campaign_id=campaign_id, pitch_text=pitch_text)
    db.session.add(a)
    db.session.commit()
    return jsonify(a.to_dict()), 201


@applications_bp.route("/applications/my", methods=["GET"])
@jwt_required
def my_applications(current_user):
    if current_user.role == "INFLUENCER":
        apps = Application.query.filter_by(influencer_id=current_user.id).order_by(Application.created_at.desc()).all()
    else:
        ids = [c.id for c in current_user.campaigns]
        if not ids:
            return jsonify([])
        apps = Application.query.filter(Application.campaign_id.in_(ids)).order_by(Application.created_at.desc()).all()
    return jsonify([a.to_dict() for a in apps])


@applications_bp.route("/applications/<int:aid>/status", methods=["PATCH"])
@jwt_required
@role_required("BRAND")
def update_status(current_user, aid):
    d = request.get_json(silent=True) or {}
    status = d.get("status")
    if status not in ("ACCEPTED", "REJECTED"):
        return jsonify({"message": "status must be ACCEPTED or REJECTED", "code": 400}), 400
    a = Application.query.get_or_404(aid)
    if a.campaign.brand_id != current_user.id:
        return jsonify({"message": "You can only update applications for your own campaigns", "code": 403}), 403
    a.status = status
    db.session.commit()
    return jsonify(a.to_dict())

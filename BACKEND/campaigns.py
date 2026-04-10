from flask import Blueprint, request, jsonify
from models import db, User, Campaign, Application
from utils import jwt_required, role_required

campaigns_bp = Blueprint("campaigns", __name__)


@campaigns_bp.route("/campaigns/stats", methods=["GET"])
def stats():
    return jsonify({
        "total_campaigns": Campaign.query.count(),
        "total_applications": Application.query.count(),
        "total_budget": db.session.query(db.func.sum(Campaign.budget)).scalar() or 0,
        "total_brands": User.query.filter_by(role="BRAND").count(),
        "total_influencers": User.query.filter_by(role="INFLUENCER").count(),
    })


@campaigns_bp.route("/campaigns", methods=["GET"])
def list_campaigns():
    campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
    return jsonify([c.to_dict() for c in campaigns])


@campaigns_bp.route("/campaigns", methods=["POST"])
@jwt_required
@role_required("BRAND")
def create_campaign(current_user):
    d = request.get_json(silent=True) or {}
    title = (d.get("title") or "").strip()
    description = (d.get("description") or "").strip()
    budget = d.get("budget")
    if not title or not description or budget is None:
        return jsonify({"message": "title, description, and budget are required", "code": 400}), 400
    if not isinstance(budget, (int, float)) or budget <= 0:
        return jsonify({"message": "budget must be a positive number", "code": 400}), 400
    c = Campaign(title=title, description=description, budget=float(budget), brand_id=current_user.id)
    db.session.add(c)
    db.session.commit()
    return jsonify(c.to_dict()), 201


@campaigns_bp.route("/campaigns/<int:cid>", methods=["GET"])
def get_campaign(cid):
    c = Campaign.query.get_or_404(cid)
    return jsonify(c.to_dict(include_applications=True))


@campaigns_bp.route("/campaigns/<int:cid>", methods=["DELETE"])
@jwt_required
def delete_campaign(current_user, cid):
    c = Campaign.query.get_or_404(cid)
    if c.brand_id != current_user.id:
        return jsonify({"message": "You can only delete your own campaigns", "code": 403}), 403
    db.session.delete(c)
    db.session.commit()
    return jsonify({"message": "Campaign deleted"})

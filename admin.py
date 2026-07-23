"""Admin dashboard blueprint — login-protected CRUD for every piece of
content shown on the public site, plus a contact-message inbox.

Kept as one file (rather than a package) to match the project's existing
flat layout (app.py, config.py, data.py, forms.py, icons.py all sit at the
repo root). The generic list/form templates mean adding a new manageable
entity only needs a handful of routes here, not a new template each time.
"""
import os
import uuid
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image
from werkzeug.utils import secure_filename

from admin_forms import (
    ApproachStepForm,
    AvatarUploadForm,
    ChangePasswordForm,
    CoreValueForm,
    LoginForm,
    ProjectForm,
    SectorForm,
    ServiceForm,
    SiteSettingsForm,
    SkillGroupForm,
    StatForm,
    ValuePropForm,
)
from models import (
    AdminUser,
    ApproachStep,
    ContactMessage,
    CoreValue,
    Project,
    Sector,
    Service,
    SiteSetting,
    SkillGroup,
    Stat,
    ValueProp,
    db,
)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin", template_folder="templates/admin")

LOCKOUT_THRESHOLD = 5
LOCKOUT_MINUTES = 15


@admin_bp.context_processor
def inject_admin_globals():
    if current_user.is_authenticated:
        return {"unread_count": ContactMessage.query.filter_by(is_read=False).count()}
    return {"unread_count": 0}


def save_upload(file_storage, prefix="img"):
    """Save an uploaded image under static/uploads and return its path
    relative to the static folder (e.g. "uploads/abc123.png"), or None."""
    if not file_storage or not hasattr(file_storage, "filename") or not file_storage.filename:
        return None
    ext = file_storage.filename.rsplit(".", 1)[-1].lower() if "." in file_storage.filename else ""
    if ext not in current_app.config["ALLOWED_UPLOAD_EXTENSIONS"]:
        return None

    # Verify the upload is genuinely an image before it ever touches disk —
    # a renamed non-image (or a malformed/corrupt one) would otherwise
    # either land straight in static/ or crash the request. Pillow can raise
    # a variety of exception types for bad image data (UnidentifiedImageError,
    # OSError, SyntaxError, ValueError...) depending on the format and what's
    # wrong with it — since any parse failure here just means "reject this
    # upload", catch broadly rather than trying to enumerate every case.
    try:
        file_storage.stream.seek(0)
        Image.open(file_storage.stream).verify()
        file_storage.stream.seek(0)
    except Exception:
        return None

    filename = secure_filename(f"{prefix}-{uuid.uuid4().hex[:10]}.{ext}")
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)
    file_storage.save(os.path.join(upload_dir, filename))
    return f"uploads/{filename}"


def admin_login_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        return view(*args, **kwargs)
    return wrapped


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data.strip()).first()
        now = datetime.now(timezone.utc)

        if user and user.locked_until and user.locked_until.replace(tzinfo=timezone.utc) > now:
            minutes_left = int((user.locked_until.replace(tzinfo=timezone.utc) - now).total_seconds() // 60) + 1
            flash(f"Too many failed attempts. Try again in {minutes_left} minute(s).", "danger")
        elif user and user.check_password(form.password.data):
            user.failed_attempts = 0
            user.locked_until = None
            user.last_login_at = now
            db.session.commit()
            login_user(user, remember=False)
            flash("Welcome back.", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("admin.dashboard"))
        else:
            if user:
                user.failed_attempts = (user.failed_attempts or 0) + 1
                if user.failed_attempts >= LOCKOUT_THRESHOLD:
                    user.locked_until = now + timedelta(minutes=LOCKOUT_MINUTES)
                db.session.commit()
            flash("Invalid username or password.", "danger")

    return render_template("admin/login.html", form=form)


@admin_bp.route("/logout", methods=["POST"])
@admin_login_required
def logout():
    logout_user()
    flash("You've been logged out.", "info")
    return redirect(url_for("admin.login"))


@admin_bp.route("/password", methods=["GET", "POST"])
@admin_login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash("Current password is incorrect.", "danger")
        elif form.new_password.data != form.confirm_password.data:
            flash("New password and confirmation don't match.", "danger")
        else:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash("Password updated.", "success")
            return redirect(url_for("admin.dashboard"))
    return render_template("admin/form.html", form=form, title="Change Password", submit_label="Update Password", back_url=url_for("admin.dashboard"))


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
@admin_bp.route("/")
@admin_login_required
def dashboard():
    counts = {
        "projects": Project.query.count(),
        "sectors": Sector.query.count(),
        "services": Service.query.count(),
        "skill_groups": SkillGroup.query.count(),
        "messages": ContactMessage.query.count(),
        "unread_messages": ContactMessage.query.filter_by(is_read=False).count(),
    }
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    return render_template("admin/dashboard.html", counts=counts, recent_messages=recent_messages)


# ---------------------------------------------------------------------------
# Site settings
# ---------------------------------------------------------------------------
@admin_bp.route("/settings", methods=["GET", "POST"])
@admin_login_required
def settings():
    row = SiteSetting.get()
    form = SiteSettingsForm(obj=row)
    avatar_form = AvatarUploadForm()
    if form.validate_on_submit():
        form.populate_obj(row)
        db.session.commit()
        flash("Site settings saved.", "success")
        return redirect(url_for("admin.settings"))
    return render_template(
        "admin/settings.html", form=form, avatar_form=avatar_form,
        title="Site Settings", avatar_path=row.AVATAR_IMAGE,
    )


@admin_bp.route("/settings/avatar", methods=["POST"])
@admin_login_required
def update_avatar():
    form = AvatarUploadForm()
    if form.validate_on_submit():
        uploaded = save_upload(form.image.data, prefix="avatar")
        if uploaded:
            row = SiteSetting.get()
            row.AVATAR_IMAGE = uploaded
            db.session.commit()
            flash("Avatar updated.", "success")
        else:
            flash("Couldn't save that image — check the file type.", "danger")
    else:
        flash("Please choose an image to upload.", "danger")
    return redirect(url_for("admin.settings"))


# --- Stats ---
@admin_bp.route("/stats")
@admin_login_required
def stats_list():
    items = Stat.query.order_by(Stat.order).all()
    columns = [("Value", "value", "text"), ("Label", "label", "text"), ("Order", "order", "text")]
    return render_template("admin/list.html", items=items, columns=columns, title="Hero Stats",
                            add_url=url_for("admin.stat_new"), edit_endpoint="admin.stat_edit",
                            delete_endpoint="admin.stat_delete")


@admin_bp.route("/stats/new", methods=["GET", "POST"])
@admin_login_required
def stat_new():
    form = StatForm()
    if form.validate_on_submit():
        item = Stat()
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash("Stat added.", "success")
        return redirect(url_for("admin.stats_list"))
    return render_template("admin/form.html", form=form, title="New Stat", submit_label="Create", back_url=url_for("admin.stats_list"))


@admin_bp.route("/stats/<int:item_id>/edit", methods=["GET", "POST"])
@admin_login_required
def stat_edit(item_id):
    item = db.session.get(Stat, item_id) or abort(404)
    form = StatForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash("Stat updated.", "success")
        return redirect(url_for("admin.stats_list"))
    return render_template("admin/form.html", form=form, title="Edit Stat", submit_label="Save Changes", back_url=url_for("admin.stats_list"))


@admin_bp.route("/stats/<int:item_id>/delete", methods=["POST"])
@admin_login_required
def stat_delete(item_id):
    item = db.session.get(Stat, item_id) or abort(404)
    db.session.delete(item)
    db.session.commit()
    flash("Stat deleted.", "info")
    return redirect(url_for("admin.stats_list"))


# --- Value props ---
@admin_bp.route("/value-props")
@admin_login_required
def value_props_list():
    items = ValueProp.query.order_by(ValueProp.order).all()
    columns = [("Icon", "icon", "icon"), ("Title", "title", "text"), ("Order", "order", "text")]
    return render_template("admin/list.html", items=items, columns=columns, title="Why Us (Value Props)",
                            add_url=url_for("admin.value_prop_new"), edit_endpoint="admin.value_prop_edit",
                            delete_endpoint="admin.value_prop_delete")


@admin_bp.route("/value-props/new", methods=["GET", "POST"])
@admin_login_required
def value_prop_new():
    form = ValuePropForm()
    if form.validate_on_submit():
        item = ValueProp()
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash("Value prop added.", "success")
        return redirect(url_for("admin.value_props_list"))
    return render_template("admin/form.html", form=form, title="New Value Prop", submit_label="Create", back_url=url_for("admin.value_props_list"))


@admin_bp.route("/value-props/<int:item_id>/edit", methods=["GET", "POST"])
@admin_login_required
def value_prop_edit(item_id):
    item = db.session.get(ValueProp, item_id) or abort(404)
    form = ValuePropForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash("Value prop updated.", "success")
        return redirect(url_for("admin.value_props_list"))
    return render_template("admin/form.html", form=form, title="Edit Value Prop", submit_label="Save Changes", back_url=url_for("admin.value_props_list"))


@admin_bp.route("/value-props/<int:item_id>/delete", methods=["POST"])
@admin_login_required
def value_prop_delete(item_id):
    item = db.session.get(ValueProp, item_id) or abort(404)
    db.session.delete(item)
    db.session.commit()
    flash("Value prop deleted.", "info")
    return redirect(url_for("admin.value_props_list"))


# --- Core values ---
@admin_bp.route("/core-values")
@admin_login_required
def core_values_list():
    items = CoreValue.query.order_by(CoreValue.order).all()
    columns = [("Title", "title", "text"), ("Order", "order", "text")]
    return render_template("admin/list.html", items=items, columns=columns, title="Core Values",
                            add_url=url_for("admin.core_value_new"), edit_endpoint="admin.core_value_edit",
                            delete_endpoint="admin.core_value_delete")


@admin_bp.route("/core-values/new", methods=["GET", "POST"])
@admin_login_required
def core_value_new():
    form = CoreValueForm()
    if form.validate_on_submit():
        item = CoreValue()
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash("Core value added.", "success")
        return redirect(url_for("admin.core_values_list"))
    return render_template("admin/form.html", form=form, title="New Core Value", submit_label="Create", back_url=url_for("admin.core_values_list"))


@admin_bp.route("/core-values/<int:item_id>/edit", methods=["GET", "POST"])
@admin_login_required
def core_value_edit(item_id):
    item = db.session.get(CoreValue, item_id) or abort(404)
    form = CoreValueForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash("Core value updated.", "success")
        return redirect(url_for("admin.core_values_list"))
    return render_template("admin/form.html", form=form, title="Edit Core Value", submit_label="Save Changes", back_url=url_for("admin.core_values_list"))


@admin_bp.route("/core-values/<int:item_id>/delete", methods=["POST"])
@admin_login_required
def core_value_delete(item_id):
    item = db.session.get(CoreValue, item_id) or abort(404)
    db.session.delete(item)
    db.session.commit()
    flash("Core value deleted.", "info")
    return redirect(url_for("admin.core_values_list"))


# --- Approach steps ---
@admin_bp.route("/process")
@admin_login_required
def approach_steps_list():
    items = ApproachStep.query.order_by(ApproachStep.order).all()
    columns = [("Title", "title", "text"), ("Order", "order", "text")]
    return render_template("admin/list.html", items=items, columns=columns, title="How Projects Run (Process)",
                            add_url=url_for("admin.approach_step_new"), edit_endpoint="admin.approach_step_edit",
                            delete_endpoint="admin.approach_step_delete")


@admin_bp.route("/process/new", methods=["GET", "POST"])
@admin_login_required
def approach_step_new():
    form = ApproachStepForm()
    if form.validate_on_submit():
        item = ApproachStep()
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash("Step added.", "success")
        return redirect(url_for("admin.approach_steps_list"))
    return render_template("admin/form.html", form=form, title="New Process Step", submit_label="Create", back_url=url_for("admin.approach_steps_list"))


@admin_bp.route("/process/<int:item_id>/edit", methods=["GET", "POST"])
@admin_login_required
def approach_step_edit(item_id):
    item = db.session.get(ApproachStep, item_id) or abort(404)
    form = ApproachStepForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash("Step updated.", "success")
        return redirect(url_for("admin.approach_steps_list"))
    return render_template("admin/form.html", form=form, title="Edit Process Step", submit_label="Save Changes", back_url=url_for("admin.approach_steps_list"))


@admin_bp.route("/process/<int:item_id>/delete", methods=["POST"])
@admin_login_required
def approach_step_delete(item_id):
    item = db.session.get(ApproachStep, item_id) or abort(404)
    db.session.delete(item)
    db.session.commit()
    flash("Step deleted.", "info")
    return redirect(url_for("admin.approach_steps_list"))


# --- Services ---
@admin_bp.route("/services")
@admin_login_required
def services_list():
    items = Service.query.order_by(Service.order).all()
    columns = [("Icon", "icon", "icon"), ("Title", "title", "text"), ("Slug", "slug", "code"), ("Order", "order", "text")]
    return render_template("admin/list.html", items=items, columns=columns, title="Services",
                            add_url=url_for("admin.service_new"), edit_endpoint="admin.service_edit",
                            delete_endpoint="admin.service_delete")


@admin_bp.route("/services/new", methods=["GET", "POST"])
@admin_login_required
def service_new():
    form = ServiceForm()
    if form.validate_on_submit():
        item = Service()
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash("Service added.", "success")
        return redirect(url_for("admin.services_list"))
    return render_template("admin/form.html", form=form, title="New Service", submit_label="Create", back_url=url_for("admin.services_list"))


@admin_bp.route("/services/<int:item_id>/edit", methods=["GET", "POST"])
@admin_login_required
def service_edit(item_id):
    item = db.session.get(Service, item_id) or abort(404)
    form = ServiceForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash("Service updated.", "success")
        return redirect(url_for("admin.services_list"))
    return render_template("admin/form.html", form=form, title="Edit Service", submit_label="Save Changes", back_url=url_for("admin.services_list"))


@admin_bp.route("/services/<int:item_id>/delete", methods=["POST"])
@admin_login_required
def service_delete(item_id):
    item = db.session.get(Service, item_id) or abort(404)
    db.session.delete(item)
    db.session.commit()
    flash("Service deleted.", "info")
    return redirect(url_for("admin.services_list"))


# --- Skill groups ---
@admin_bp.route("/skills")
@admin_login_required
def skill_groups_list():
    items = SkillGroup.query.order_by(SkillGroup.order).all()
    columns = [("Icon", "icon", "icon"), ("Title", "title", "text"), ("Skills", "skills", "count"), ("Order", "order", "text")]
    return render_template("admin/list.html", items=items, columns=columns, title="Skills",
                            add_url=url_for("admin.skill_group_new"), edit_endpoint="admin.skill_group_edit",
                            delete_endpoint="admin.skill_group_delete")


@admin_bp.route("/skills/new", methods=["GET", "POST"])
@admin_login_required
def skill_group_new():
    form = SkillGroupForm()
    if form.validate_on_submit():
        item = SkillGroup()
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash("Skill group added.", "success")
        return redirect(url_for("admin.skill_groups_list"))
    return render_template("admin/form.html", form=form, title="New Skill Group", submit_label="Create", back_url=url_for("admin.skill_groups_list"))


@admin_bp.route("/skills/<int:item_id>/edit", methods=["GET", "POST"])
@admin_login_required
def skill_group_edit(item_id):
    item = db.session.get(SkillGroup, item_id) or abort(404)
    form = SkillGroupForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash("Skill group updated.", "success")
        return redirect(url_for("admin.skill_groups_list"))
    return render_template("admin/form.html", form=form, title="Edit Skill Group", submit_label="Save Changes", back_url=url_for("admin.skill_groups_list"))


@admin_bp.route("/skills/<int:item_id>/delete", methods=["POST"])
@admin_login_required
def skill_group_delete(item_id):
    item = db.session.get(SkillGroup, item_id) or abort(404)
    db.session.delete(item)
    db.session.commit()
    flash("Skill group deleted.", "info")
    return redirect(url_for("admin.skill_groups_list"))


# --- Sectors ---
@admin_bp.route("/sectors")
@admin_login_required
def sectors_list():
    items = Sector.query.order_by(Sector.order).all()
    columns = [("Icon", "icon", "icon"), ("Title", "title", "text"), ("Proven", "proven", "bool"), ("Order", "order", "text")]
    return render_template("admin/list.html", items=items, columns=columns, title="Sectors",
                            add_url=url_for("admin.sector_new"), edit_endpoint="admin.sector_edit",
                            delete_endpoint="admin.sector_delete")


@admin_bp.route("/sectors/new", methods=["GET", "POST"])
@admin_login_required
def sector_new():
    form = SectorForm()
    if form.validate_on_submit():
        uploaded = save_upload(form.image.data, prefix="sector")
        item = Sector()
        form.populate_obj(item)
        item.image = uploaded  # form.image is a FileField — never store its raw data
        db.session.add(item)
        db.session.commit()
        flash("Sector added.", "success")
        return redirect(url_for("admin.sectors_list"))
    return render_template("admin/form.html", form=form, title="New Sector", submit_label="Create", back_url=url_for("admin.sectors_list"))


@admin_bp.route("/sectors/<int:item_id>/edit", methods=["GET", "POST"])
@admin_login_required
def sector_edit(item_id):
    item = db.session.get(Sector, item_id) or abort(404)
    form = SectorForm(obj=item)
    if form.validate_on_submit():
        existing_image = item.image
        uploaded = save_upload(form.image.data, prefix="sector")
        form.populate_obj(item)
        item.image = uploaded or existing_image  # keep current image unless a new one was uploaded
        db.session.commit()
        flash("Sector updated.", "success")
        return redirect(url_for("admin.sectors_list"))
    return render_template("admin/form.html", form=form, title="Edit Sector", submit_label="Save Changes",
                            back_url=url_for("admin.sectors_list"), image_path=item.image)


@admin_bp.route("/sectors/<int:item_id>/delete", methods=["POST"])
@admin_login_required
def sector_delete(item_id):
    item = db.session.get(Sector, item_id) or abort(404)
    db.session.delete(item)
    db.session.commit()
    flash("Sector deleted.", "info")
    return redirect(url_for("admin.sectors_list"))


# --- Projects ---
@admin_bp.route("/projects")
@admin_login_required
def projects_list():
    items = Project.query.order_by(Project.order).all()
    columns = [
        ("Title", "title", "text"),
        ("Category", "category_label", "text"),
        ("Featured", "featured", "bool"),
        ("Confidential", "confidential", "bool"),
        ("Order", "order", "text"),
    ]
    return render_template("admin/list.html", items=items, columns=columns, title="Projects",
                            add_url=url_for("admin.project_new"), edit_endpoint="admin.project_edit",
                            delete_endpoint="admin.project_delete")


@admin_bp.route("/projects/new", methods=["GET", "POST"])
@admin_login_required
def project_new():
    form = ProjectForm()
    if form.validate_on_submit():
        uploaded = save_upload(form.image.data, prefix=form.slug.data)
        item = Project()
        form.populate_obj(item)
        item.image = uploaded  # form.image is a FileField — never store its raw data
        db.session.add(item)
        db.session.commit()
        flash("Project added.", "success")
        return redirect(url_for("admin.projects_list"))
    return render_template("admin/form.html", form=form, title="New Project", submit_label="Create", back_url=url_for("admin.projects_list"))


@admin_bp.route("/projects/<int:item_id>/edit", methods=["GET", "POST"])
@admin_login_required
def project_edit(item_id):
    item = db.session.get(Project, item_id) or abort(404)
    form = ProjectForm(obj=item)
    if form.validate_on_submit():
        existing_image = item.image
        uploaded = save_upload(form.image.data, prefix=form.slug.data)
        form.populate_obj(item)
        item.image = uploaded or existing_image  # keep current image unless a new one was uploaded
        db.session.commit()
        flash("Project updated.", "success")
        return redirect(url_for("admin.projects_list"))
    return render_template("admin/form.html", form=form, title="Edit Project", submit_label="Save Changes",
                            back_url=url_for("admin.projects_list"), image_path=item.image)


@admin_bp.route("/projects/<int:item_id>/delete", methods=["POST"])
@admin_login_required
def project_delete(item_id):
    item = db.session.get(Project, item_id) or abort(404)
    db.session.delete(item)
    db.session.commit()
    flash("Project deleted.", "info")
    return redirect(url_for("admin.projects_list"))


# ---------------------------------------------------------------------------
# Contact messages inbox
# ---------------------------------------------------------------------------
@admin_bp.route("/messages")
@admin_login_required
def messages_list():
    items = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin/messages_list.html", items=items, title="Contact Messages")


@admin_bp.route("/messages/<int:item_id>")
@admin_login_required
def message_detail(item_id):
    item = db.session.get(ContactMessage, item_id) or abort(404)
    if not item.is_read:
        item.is_read = True
        db.session.commit()
    return render_template("admin/message_detail.html", item=item)


@admin_bp.route("/messages/<int:item_id>/delete", methods=["POST"])
@admin_login_required
def message_delete(item_id):
    item = db.session.get(ContactMessage, item_id) or abort(404)
    db.session.delete(item)
    db.session.commit()
    flash("Message deleted.", "info")
    return redirect(url_for("admin.messages_list"))

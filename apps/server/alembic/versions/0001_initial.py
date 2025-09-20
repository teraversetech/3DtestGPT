"""initial schema

Revision ID: 0001
Revises: 
Create Date: 2024-05-01
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")

    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("plan", sa.String(length=50), nullable=False, server_default="free"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "uploads",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("owner_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("s3_key", sa.String(length=255), nullable=False),
        sa.Column("size", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("parts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "jobs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("owner_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("upload_id", sa.String(length=36), sa.ForeignKey("uploads.id"), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="queued"),
        sa.Column("progress", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("params_json", sa.JSON(), server_default=sa.text("'{}'::json")),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "artifacts",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("job_id", sa.String(length=36), sa.ForeignKey("jobs.id"), nullable=False),
        sa.Column("owner_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("glb_key", sa.String(length=255), nullable=False),
        sa.Column("usdz_key", sa.String(length=255), nullable=False),
        sa.Column("preview_key", sa.String(length=255), nullable=False),
        sa.Column("meta_json", sa.JSON(), server_default=sa.text("'{}'::json")),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "posts",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("owner_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("artifact_id", sa.String(length=36), sa.ForeignKey("artifacts.id"), nullable=False),
        sa.Column("caption", sa.Text(), nullable=False, server_default=""),
        sa.Column("tags", sa.JSON(), server_default=sa.text("'[]'::json")),
        sa.Column("visibility", sa.String(length=20), nullable=False, server_default="public"),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "likes",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("post_id", sa.String(length=36), sa.ForeignKey("posts.id"), nullable=False),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "comments",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("post_id", sa.String(length=36), sa.ForeignKey("posts.id"), nullable=False),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "scan_quotas",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("month", sa.String(length=7), nullable=False),
        sa.Column("used_scans", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("plan", sa.String(length=50), nullable=False, server_default="free"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )



def downgrade() -> None:
    op.drop_table("scan_quotas")
    op.drop_table("comments")
    op.drop_table("likes")
    op.drop_table("posts")
    op.drop_table("artifacts")
    op.drop_table("jobs")
    op.drop_table("uploads")
    op.drop_table("users")

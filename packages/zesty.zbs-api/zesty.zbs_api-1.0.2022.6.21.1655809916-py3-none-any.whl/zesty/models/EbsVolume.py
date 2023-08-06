from typing import Dict

try:
    from sqlalchemy import Column
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.dialects.postgresql import BOOLEAN, FLOAT, INTEGER, \
        JSON, TIMESTAMP, VARCHAR
except ImportError:
    raise ImportError("sqlalchemy is required by zesty.zbs-api but needs to be vendored separately. Add postgres-utils to your project's requirements that depend on zbs-api.")

Base = declarative_base()


class EbsVolume(Base):
    # TODO: Move this model into our Alembic system 
    # when a modification of this model is needed.
    __tablename__ = "disks"

    volume_id = Column(VARCHAR, primary_key=True)
    org_id = Column(VARCHAR, index=True)
    account_uuid = Column(VARCHAR, index=True)
    account_id = Column(VARCHAR, index=True)
    region = Column(VARCHAR, index=True)
    volume_type = Column(VARCHAR, index=True)
    cloud = Column(VARCHAR, index=True)
    availability_zone = Column(VARCHAR)
    create_time = Column(TIMESTAMP)
    encrypted = Column(BOOLEAN)
    size = Column(INTEGER)
    snapshot_id = Column(VARCHAR)
    state = Column(VARCHAR)
    iops = Column(INTEGER)
    tags = Column(JSON)
    attachments = Column(JSON)
    attached_to = Column(JSON)
    monthly_cost = Column(FLOAT, default=0)
    is_unused_resource = Column(INTEGER, default=0)
    unused_since = Column(VARCHAR)
    agent_installed = Column(BOOLEAN, default=False)
    _zbs_supported_os = Column(INTEGER)
    potential_savings = Column(FLOAT, default=0)

    def __init__(
            self,
            volume_aws_schema: Dict,
            account_uuid: str = None):
        if account_uuid:
            self.account_uuid = account_uuid
        else:
            self.account_uuid = volume_aws_schema["account_uuid"]

        self.volume_id = volume_aws_schema["volume_id"]
        self.org_id = volume_aws_schema["org_id"]
        self.account_id = volume_aws_schema["account_id"]
        self.cloud = volume_aws_schema["cloud"]
        self.region = volume_aws_schema["region"]
        self.volume_type = volume_aws_schema["volume_type"]
        self.availability_zone = volume_aws_schema["availability_zone"]
        self.create_time = volume_aws_schema["create_time"]
        self.encrypted = volume_aws_schema["encrypted"]
        self.size = volume_aws_schema["size"]
        self.snapshot_id = volume_aws_schema["snapshot_id"]
        self.state = volume_aws_schema["state"]
        self.iops = volume_aws_schema.get("iops", 0)
        self.tags = volume_aws_schema.get("tags", {})
        self.attachments = volume_aws_schema.get("attachments", [])
        self.attached_to = volume_aws_schema.get("attached_to", [])
        self.monthly_cost = volume_aws_schema.get("monthly_cost", 0)
        self.is_unused_resource = volume_aws_schema.get(
            "is_unused_resource", 0)
        self.unused_since = volume_aws_schema.get("unused_since", None)
        self.agent_installed = volume_aws_schema.get("agent_installed", False)
        self._zbs_supported_os = volume_aws_schema.get("_zbs_supported_os")
        self.potential_savings = volume_aws_schema.get("potential_savings", 0)

    def __repr__(self):
        return f"{self.__tablename__}:{self.volume_id}"

    def get_volume_id(self):
        return self.volume_id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

from backend_sqlalchemy.backend_app.models.findings import FindingsModel
from backend_sqlalchemy.backend_app.db import db
from flask_restful import Resource, reqparse, fields, marshal_with, abort


def get_all_findings():
    """
    Get all findings
    """
    all_findings = db.session.query(FindingsModel.FID, FindingsModel.Name, FindingsModel.Title).all()
    findings_hash = {}
    for finding in all_findings:
        findings_hash[finding.Name] = finding.FID
    print(findings_hash)


get_all_findings()
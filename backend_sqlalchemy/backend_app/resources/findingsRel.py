from backend_sqlalchemy.backend_app.models.findingsRel import FindingsRel
from backend_sqlalchemy.backend_app.models.findings import FindingsModel
from backend_sqlalchemy.backend_app.db import db
from flask_restful import Resource, reqparse, fields, marshal_with, abort

if __name__ == '__main__':
    fr = db.session.query(FindingsRel).filter(FindingsRel.FID1 == 3744).first()
    finding = db.session.query(FindingsModel).filter(FindingsModel.FID == fr.FID1).first()
    print("Total FID2= "+str(len(finding.entity_FID2)))
    for fid in finding.entity_FID2:
        print(fid)

from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Depends
from bigfastapi.db.database import get_db
from bigfastapi.models.import_progress_models import FailedImports
import sqlalchemy.orm as orm

app = APIRouter(tags=["failed_imports"],)

async def logImportError(line, error, organization_id: str, model: str, 
    db: orm.Session = Depends(get_db)):
    failedImport = FailedImports(
        id=uuid4().hex, line=line,
        model=model, error=error, organization_id=organization_id, 
        is_deleted=False, created_at= datetime.now(), 
        updated_at= datetime.now()
    )
    db.add(failedImport)
    db.commit()
    db.refresh(failedImport)

    return failedImport

async def deleteImportError(organization_id: str, model: str, 
    db: orm.Session = Depends(get_db)):

    db.query(FailedImports).filter(FailedImports.organization_id == organization_id).\
        filter(FailedImports.model == model).update({'is_deleted': True})
    db.commit()
    return

def isEmpty(imports):
    if len(imports) != 0:
        return True
    return False

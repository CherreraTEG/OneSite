from sqlalchemy.orm import Session
from app.models.user_company_permission import UserCompanyPermission

class CRUDUserCompanyPermission:
    def get_companies_for_user(self, db: Session, user_id: int):
        return db.query(UserCompanyPermission.company_id).filter(UserCompanyPermission.user_id == user_id).all()

crud_user_company_permission = CRUDUserCompanyPermission() 
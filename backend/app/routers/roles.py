from fastapi import APIRouter
from ..workflows.roles import ROLES

router = APIRouter(prefix="/api/roles", tags=["roles"])


@router.get("")
def list_roles():
    return [role.__dict__ for role in ROLES]

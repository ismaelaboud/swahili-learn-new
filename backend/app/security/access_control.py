from enum import Enum, auto
from typing import List, Dict, Any
from fastapi import HTTPException, status

class UserRole(Enum):
    GUEST = auto()
    STUDENT = auto()
    INSTRUCTOR = auto()
    ADMIN = auto()

class PermissionLevel(Enum):
    READ = auto()
    WRITE = auto()
    DELETE = auto()
    MANAGE = auto()

class AccessControl:
    """
    Centralized access control system for Swahili Learn
    Manages role-based and time-based content access
    """
    
    ROLE_PERMISSIONS: Dict[UserRole, Dict[str, List[PermissionLevel]]] = {
        UserRole.GUEST: {
            'courses': [PermissionLevel.READ],
            'lessons': [PermissionLevel.READ],
        },
        UserRole.STUDENT: {
            'courses': [PermissionLevel.READ],
            'lessons': [PermissionLevel.READ],
            'progress': [PermissionLevel.WRITE],
        },
        UserRole.INSTRUCTOR: {
            'courses': [PermissionLevel.READ, PermissionLevel.WRITE, PermissionLevel.MANAGE],
            'lessons': [PermissionLevel.READ, PermissionLevel.WRITE, PermissionLevel.MANAGE],
            'students': [PermissionLevel.READ],
        },
        UserRole.ADMIN: {
            'courses': [PermissionLevel.READ, PermissionLevel.WRITE, PermissionLevel.DELETE, PermissionLevel.MANAGE],
            'lessons': [PermissionLevel.READ, PermissionLevel.WRITE, PermissionLevel.DELETE, PermissionLevel.MANAGE],
            'users': [PermissionLevel.READ, PermissionLevel.WRITE, PermissionLevel.DELETE],
            'system': [PermissionLevel.MANAGE],
        }
    }

    @classmethod
    def check_permission(
        cls, 
        user_role: UserRole, 
        resource: str, 
        required_permission: PermissionLevel
    ) -> bool:
        """
        Check if a user role has the required permission for a specific resource
        
        :param user_role: Role of the user
        :param resource: Resource being accessed
        :param required_permission: Permission level required
        :return: Boolean indicating if access is granted
        """
        if user_role not in cls.ROLE_PERMISSIONS:
            return False
        
        resource_permissions = cls.ROLE_PERMISSIONS[user_role].get(resource, [])
        return required_permission in resource_permissions

    @classmethod
    def enforce_permission(
        cls, 
        user_role: UserRole, 
        resource: str, 
        required_permission: PermissionLevel
    ):
        """
        Enforce permission and raise HTTPException if access is denied
        
        :param user_role: Role of the user
        :param resource: Resource being accessed
        :param required_permission: Permission level required
        :raises HTTPException: If access is denied
        """
        if not cls.check_permission(user_role, resource, required_permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions to {required_permission.name.lower()} {resource}"
            )

    @classmethod
    def get_accessible_resources(
        cls, 
        user_role: UserRole, 
        resource: str
    ) -> List[PermissionLevel]:
        """
        Get list of permissions for a specific resource
        
        :param user_role: Role of the user
        :param resource: Resource to check
        :return: List of permitted actions
        """
        return cls.ROLE_PERMISSIONS.get(user_role, {}).get(resource, [])

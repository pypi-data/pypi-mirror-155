import json
from typing import Dict, List, Any

from algoralabs.permission import PermissionRequest
from algoralabs.common.functions import no_transform
from algoralabs.decorators.data import data_request, async_data_request
from algoralabs.common.requests import (
    __get_request, __put_request, __post_request, __delete_request,
    __async_get_request, __async_put_request, __async_post_request, __async_delete_request
)


def _get_permission_request_info(id: str) -> dict:
    return {
        'endpoint': f"config/permission/{id}"
    }


@data_request(transformer=no_transform)
def get_permission(id: str) -> Dict[str, Any]:
    request_info = _get_permission_request_info(id)
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_permission(id: str) -> Dict[str, Any]:
    request_info = _get_permission_request_info(id)
    return await __async_get_request(**request_info)


def _get_permission_by_resource_id_request_info(resource_id: str) -> dict:
    return {
        'endpoint': f"config/permission/resource/{resource_id}"
    }


@data_request(transformer=no_transform)
def get_permission_by_resource_id(resource_id: str) -> Dict[str, Any]:
    request_info = _get_permission_by_resource_id_request_info(resource_id)
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_permission_by_resource_id(resource_id: str) -> Dict[str, Any]:
    request_info = _get_permission_by_resource_id_request_info(resource_id)
    return await __async_get_request(**request_info)


def _get_permissions_by_resource_id_request_info(resource_id: str) -> dict:
    return {
        'endpoint': f"config/permission/resource/{resource_id}/permissions"
    }


@data_request(transformer=no_transform)
def get_permissions_by_resource_id(resource_id: str) -> List[Dict[str, Any]]:
    request_info = _get_permissions_by_resource_id_request_info(resource_id)
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_permissions_by_resource_id(resource_id: str) -> List[Dict[str, Any]]:
    request_info = _get_permissions_by_resource_id_request_info(resource_id)
    return await __async_get_request(**request_info)


def _create_permission_request_info(request: PermissionRequest) -> dict:
    return {
        'endpoint': f"config/permission",
        'json': json.loads(request.json())
    }


@data_request(transformer=no_transform)
def create_permission(request: PermissionRequest) -> Dict[str, Any]:
    request_info = _create_permission_request_info(request)
    return __put_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_create_permission(request: PermissionRequest) -> Dict[str, Any]:
    request_info = _create_permission_request_info(request)
    return await __async_put_request(**request_info)


def _update_permission_request_info(id: str, request: PermissionRequest) -> dict:
    return {
        'endpoint': f"config/permission/{id}",
        'json': json.loads(request.json())
    }


@data_request(transformer=no_transform)
def update_permission(id: str, request: PermissionRequest) -> Dict[str, Any]:
    request_info = _update_permission_request_info(id, request)
    return __post_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_update_permission(id: str, request: PermissionRequest) -> Dict[str, Any]:
    request_info = _update_permission_request_info(id, request)
    return await __async_post_request(**request_info)


def _delete_permission_request_info(id: str) -> dict:
    return {
        'endpoint': f"config/permission/{id}"
    }


@data_request(transformer=no_transform)
def delete_permission(id: str) -> None:
    request_info = _delete_permission_request_info(id)
    return __delete_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_delete_permission(id: str) -> None:
    request_info = _delete_permission_request_info(id)
    return await __async_delete_request(**request_info)

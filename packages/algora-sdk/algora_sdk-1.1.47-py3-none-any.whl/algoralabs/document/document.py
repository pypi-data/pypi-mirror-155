import json
from typing import List

from algoralabs.common.functions import no_transform
from algoralabs.document import Document, DocumentRequest, SearchDocumentRequest
from algoralabs.decorators.data import data_request, async_data_request
from algoralabs.common.requests import (
    __get_request, __put_request, __post_request, __delete_request,
    __async_get_request, __async_put_request, __async_post_request, __async_delete_request
)


def _get_document_request_info(id: str) -> dict:
    return {
        'endpoint': f"config/documents/{id}"
    }


@data_request(transformer=no_transform)
def get_document(id: str) -> Document:
    request_info = _get_document_request_info(id)
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_document(id: str) -> Document:
    request_info = _get_document_request_info(id)
    return await __async_get_request(**request_info)


def _search_documents_request_info(request: SearchDocumentRequest) -> dict:
    return {
        'endpoint': "config/documents/search",
        'json': json.loads(request.json())
    }


@data_request(transformer=no_transform)
def search_documents(request: SearchDocumentRequest) -> List[Document]:
    request_info = _search_documents_request_info(request)
    return __post_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_search_documents(request: SearchDocumentRequest) -> List[Document]:
    request_info = _search_documents_request_info(request)
    return await __async_post_request(**request_info)


def _create_document_request_info(request: DocumentRequest) -> dict:
    return {
        'endpoint': "config/documents",
        'json': json.loads(request.json())
    }


@data_request(transformer=no_transform)
def create_document(request: DocumentRequest) -> Document:
    request_info = _create_document_request_info(request)
    return __post_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_create_document(request: DocumentRequest) -> Document:
    request_info = _create_document_request_info(request)
    return await __async_post_request(**request_info)


def _update_document_request_info(id: str, request: DocumentRequest) -> dict:
    return {
        'endpoint': f"config/documents/{id}",
        'json': json.loads(request.json())
    }


@data_request(transformer=no_transform)
def update_document(id: str, request: DocumentRequest) -> Document:
    request_info = _update_document_request_info(id, request)
    return __put_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_update_document(id: str, request: DocumentRequest) -> Document:
    request_info = _update_document_request_info(id, request)
    return await __async_put_request(**request_info)


def _delete_document_request_info(id: str) -> dict:
    return {
        'endpoint': f"config/documents/{id}"
    }


@data_request(transformer=no_transform)
def delete_document(id: str) -> None:
    request_info = _delete_document_request_info(id)
    return __delete_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_delete_document(id: str) -> None:
    request_info = _delete_document_request_info(id)
    return await __async_delete_request(**request_info)

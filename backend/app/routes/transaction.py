from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Query

from app.common.enums import Tag
from app.common.exceptions import EntityNotFoundException, ActionForbiddenException, EntityNotAssociatedException
from app.common.responses import common_responses_dict
from app.core.logger import get_logger
from app.db_models import User
from app.schemas import TransactionCreate, TransactionUpdate, TransactionOut, TransactionFilters, ErrorResponse
from app.services import TransactionService, get_transaction_service
from app.services.security import get_current_user


logger = get_logger(__name__)

router = APIRouter(prefix="/transactions", tags=[Tag.transaction])


@router.get(
    "/{transaction_id}",
    response_model=TransactionOut,
    status_code=200,
    description="get one transaction by its id",
    responses={
        **common_responses_dict,
        403: {
            "description": "action forbidden",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "users can only view their own transactions"}}},
        },
        404: {
            "description": "transaction not found",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "transaction with id 100 not found"}}},
        },
    },
)
async def get_transaction(
    transaction_id: int,
    service: TransactionService = Depends(get_transaction_service),
    current_user: User = Depends(get_current_user),
) -> TransactionOut:
    logger.info(f"fetching transaction with id {transaction_id}")
    try:
        transaction = await service.get_by_id(entity_id=transaction_id, gotten_by=current_user)
        return transaction
    except ActionForbiddenException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "",
    response_model=list[TransactionOut],
    status_code=200,
    description="get all transactions with optional filters",
    responses=common_responses_dict,
)
async def get_transactions(
    filters: Annotated[TransactionFilters, Query()],
    service: TransactionService = Depends(get_transaction_service),
    current_user: User = Depends(get_current_user),
) -> list[TransactionOut]:
    logger.info(f"fetching all transactions with filters {filters}")
    transactions = await service.get_all_with_filters(filters=filters, gotten_by=current_user)
    logger.info(f"returned {len(transactions)} transactions")
    return transactions


@router.post(
    "",
    response_model=TransactionOut,
    status_code=201,
    description="create a new transaction",
    responses={
        **common_responses_dict,
        403: {
            "description": "action forbidden",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "users can only view their own transactions"}}},
        },
        404: {
            "description": "type not found",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "type with id 100 not found"}}},
        },
        409: {
            "description": "entity not assocaited",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "entity not associated: category with id 10 is not of type with id 2"}
                }
            },
        },
    },
)
async def create_transaction(
    new_transaction: TransactionCreate,
    service: TransactionService = Depends(get_transaction_service),
    current_user: User = Depends(get_current_user),
) -> TransactionOut:
    logger.info("creating a new transaction")
    try:
        transaction = await service.create(
            create_schema=new_transaction, created_by=current_user, user_id=current_user.id
        )
        return transaction
    except ActionForbiddenException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except EntityNotAssociatedException as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put(
    "/{transaction_id}",
    response_model=TransactionOut,
    status_code=200,
    description="update a transaction by its id",
    responses={
        **common_responses_dict,
        403: {
            "description": "action forbidden",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "users can only update their own transactions"}}},
        },
        404: {
            "description": "type not found",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "type with id 100 not found"}}},
        },
        409: {
            "description": "entity not assocaited",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "entity not associated: category with id 10 is not of type with id 2"}
                }
            },
        },
    },
)
async def update_transaction(
    transaction_id: int,
    updated_transaction: TransactionUpdate,
    service: TransactionService = Depends(get_transaction_service),
    current_user: User = Depends(get_current_user),
) -> TransactionOut:
    logger.info(f"updating transaction with id {transaction_id}")
    try:
        transaction = await service.update(
            entity_id=transaction_id, update_schema=updated_transaction, updated_by=current_user
        )
        return transaction
    except ActionForbiddenException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except EntityNotAssociatedException as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete(
    "/{transaction_id}",
    response_model=TransactionOut,
    status_code=200,
    description="delete transaction by its id",
    responses={
        **common_responses_dict,
        403: {
            "description": "action forbidden",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "users can only delete their own transactions"}}},
        },
        404: {
            "description": "user not found",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "transaction with id 100 not found"}}},
        },
    },
)
async def delete_transaction(
    transaction_id: int,
    service: TransactionService = Depends(get_transaction_service),
    current_user: User = Depends(get_current_user),
) -> TransactionOut:
    logger.info(f"deleting transaction with id {transaction_id}")
    try:
        transaction = await service.delete(entity_id=transaction_id, deleted_by=current_user)
        return transaction
    except ActionForbiddenException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

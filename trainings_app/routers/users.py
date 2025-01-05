from fastapi import APIRouter, HTTPException, Depends
from trainings_app.schemas.users import GetUser, CreateUser, UpdateUserPut, UpdateUserPatch
from trainings_app.db.connection import get_db
from trainings_app.repositories.user_repository import UserRepository

router = APIRouter(prefix='/users', tags=['user'])


@router.post('/', response_model=GetUser)
async def r_create_user(user: CreateUser, db=Depends(get_db)) -> GetUser:
    try:
        user_dict = user.dict()
        user_repo = UserRepository(db)
        created_user = await user_repo.create_user(user_dict)
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred. Additional info: {e}")


@router.get('/', response_model=list[GetUser])
async def r_get_active_users(db=Depends(get_db)) -> list[GetUser]:
    try:
        user_repo = UserRepository(db)
        users = await user_repo.get_active_users()
        return users
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred. Additional info: {e}")


@router.get('/deleted', response_model=list[GetUser])
async def r_get_deleted_users(db=Depends(get_db)) -> list[GetUser]:
    try:
        user_repo = UserRepository(db)
        users = await user_repo.get_deleted_users()
        return users
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred. Additional info: {e}")


@router.get('/user_id/{user_id}', response_model=GetUser)
async def r_get_user_by_id(user_id: int, db=Depends(get_db)) -> GetUser:
    try:
        user_repo = UserRepository(db)
        user = await user_repo.get_user_by_id(user_id)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred. Additional info: {e}")


@router.get('/username/{username}', response_model=GetUser)
async def r_get_user_by_username(username: str, db=Depends(get_db)) -> GetUser:
    try:
        user_repo = UserRepository(db)
        user = await user_repo.get_user_by_username(username)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred. Additional info: {e}")


@router.delete('/delete', response_model=GetUser)
async def r_delete_user(user_attr: dict, db=Depends(get_db)) -> GetUser:
    try:
        user_repo = UserRepository(db)
        user = await user_repo.delete_user(user_attr)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred. Additional info: {e}")


@router.put('/{user_id}', response_model=GetUser)
async def r_update_user_put(user_id: int, user: UpdateUserPut, db=Depends(get_db)) -> GetUser:
    try:
        user_repo = UserRepository(db)
        user = await user_repo.update_user(user_id, user.dict())
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred. Additional info: {e}")


@router.patch('/{user_id}', response_model=GetUser)
async def r_update_user_put(user_id: int, user: UpdateUserPatch, db=Depends(get_db)) -> GetUser:
    try:
        user_repo = UserRepository(db)
        user = await user_repo.update_user(user_id, user.dict(exclude_unset=True))
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred. Additional info: {e}")

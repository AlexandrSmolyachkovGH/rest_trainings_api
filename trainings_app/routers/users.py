from fastapi import APIRouter, HTTPException, Depends
from trainings_app.schemas.users import GetUser, CreateUser, UpdateUserPut, UpdateUserPatch
from trainings_app.db.connection import get_db
from trainings_app.repositories.user_repository import UserRepository

router = APIRouter(prefix='/users', tags=['user'])


@router.post('/', response_model=GetUser)
async def create_user(user: CreateUser, db=Depends(get_db)) -> GetUser:
    """
    Create new user.
    Returns a model of created user.
    """
    try:
        user_repo = UserRepository(db)
        created_user = await user_repo.create_user(user)
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred. Additional info: {e}")


@router.get('/{user_id}', response_model=u.GetUser)
async def get_all_users(user_id: int) -> u.GetUser:
    conn = get_db()
    query = 'SELECT * FROM users WHERE id = $1'
    user_record = await conn.fetchrow(query, user_id)
    if not user_record:
        return HTTPException(status_code=404, detail='User not found')
    user = u.GetUser(
        id=user_record['id'],
        username=user_record['username'],
        password_hash=user_record['password_hash'],
        email=user_record['email'],
        role=user_record['role'],
        created_at=user_record['created_at'],
        last_login=user_record['last_login'],
    )
    return user


@router.put('/{user_id}', response_model=u.GetUser)
async def update_user(user_id: int, user: u.UpdateUser) -> u.GetUser:
    conn = get_db()
    query = 'SELECT * FROM users WHERE id = $1'
    user_record = await conn.fetchrow(query, user_id)
    if not user_record:
        raise HTTPException(status_code=404, detail='User not found')
    query_update = """
            UPDATE users 
            SET username = $1, password_hash = $2, email = $3, role = $4, last_login = $5 
            WHERE id = $6
            RETURNING id, username, password_hash, email, role, created_at, last_login
        """
    user_params = (
        user.username,
        user.password_hash,
        user.email,
        user.role,
        user.last_login,
        user_id
    )


@router.delete('/')
async def delete_category():
    pass

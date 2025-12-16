from uuid import UUID

from app.database import SessionLocal
from app.models.User import User

# docker compose run --rm api python -m app.scripts.user

# 1) Select all users
def get_all_users():
    with SessionLocal() as db:
        users = db.query(User).all()
        print('get_all_users')

        if (len(users) == 0):
            print('No users')
            return

        for u in users:
            print(u.id, u.first_name, u.email, u.is_email_verified)
        print('get_all_users end')
    

# 2) Select user by email
def get_user_by_email(email: str):
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == email).first()
        print(user)

# 3) Select user by id (UUID)
def get_user_by_id(user_id: str):
    with SessionLocal() as db:
        user = db.query(User).filter(User.id == UUID(user_id)).first()
        print(user)


# 4) Delete all users
def delete_all_users():
    with SessionLocal() as db:
        deleted_count = db.query(User).delete()
        db.commit()
        print(f"Deleted {deleted_count} users")

if __name__ == "__main__":
    # examples – edit as needed
    get_all_users()
    # get_user_by_email("some_email@example.com")
    # get_user_by_id("00000000-0000-0000-0000-000000000000")
    # delete_all_users()
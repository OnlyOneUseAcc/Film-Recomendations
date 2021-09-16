from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    id: Optional[int] = Field(..., description="Аналог login, unique == True")
    name: str = Field(..., description="Имя пользователя")
    is_admin: bool = Field(..., description="Флаг, указывающий на возможности администратора")
    password: str = Field(..., description="Пароль пользователя")


if __name__ == '__main__':
    user = User(id=None, name='Алексей', is_admin=True, password='Qwerty123')
    user2 = User(id=127, name='Алексей', is_admin=True, password='Qwerty123')

    print(user.json())
    print(user2)

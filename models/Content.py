from pydantic import BaseModel, Field
from typing import Optional, List


class Content(BaseModel):
    content_id: Optional[int] = Field(..., description="ID контента")
    name: str = Field(..., description="Название контента")
    type: str = Field(..., description="Тип")
    serial_id: Optional[int] = Field(..., description="ID контента типа сериал, != None, если type == serial")
    genres: Optional[List[str]] = Field(..., description="Список жанров данного контента")
    duration: int = Field(..., description="Длительность фильма")


if __name__ == '__main__':
    a = Content(content_id=1,
                name='123',
                type='123',
                serial_id=1,
                genres=['123'],
                duration=1234)
    print(a)

    b = Content(content_id=1,
                name='123',
                type='123',
                serial_id=None,
                genres=None,
                duration=1234)
    print(b.json())
    print(f'тип поля content заданного через Field{type(a.content_id)}')

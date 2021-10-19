from pydantic import BaseModel, Field
from typing import Optional, List


class WatchHistoryUnit(BaseModel):
    user_uid: int = Field(..., description='UID пользователя, просмотревшего контент')
    content_uid: int = Field(..., description='UID контента, просмотренного пользователем')
    name: str = Field(..., description='Название единицы контента')
    duration: float = Field(..., description="Длительность просмотра в процентах")
    type: Optional[str] = Field(..., description="Тип контента")


class WatchHistory(BaseModel):
    history: Optional[List[WatchHistoryUnit]] = Field(..., description="Список просмотренных единиц")

    def append(self, unit):
        if self.history is None:
            self.history = [unit]
        else:
            self.history.append(unit)


if __name__ == '__main__':
    unit1 = WatchHistoryUnit(name='Qwerty', duration=6500, type=None)
    unit2 = WatchHistoryUnit(name='werty', duration=16500, type='serial')

    history = WatchHistory(history=None)
    history2 = WatchHistory(history=[unit1])

    history.append(unit1)
    print(history)

    history2.append(unit2)
    print(history2)





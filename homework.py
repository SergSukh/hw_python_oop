from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_HOUR: ClassVar[int] = 60
    LEN_STEP: ClassVar[float] = .65
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.LEN_STEP * self.action / Training.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = type(self).__name__
        info = InfoMessage(training_type,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIES1: ClassVar[int] = 18
    CEFF_CALORIES2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        calories = ((Running.COEFF_CALORIES1 * self.get_mean_speed()
                    - Running.CEFF_CALORIES2) * self.weight / Training.M_IN_KM
                    * (self.duration * Training.MIN_IN_HOUR))
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIES1: ClassVar[int] = .035
    CEFF_CALORIES2: ClassVar[int] = .029
    height: float

    def get_spent_calories(self) -> float:
        calories = ((SportsWalking.COEFF_CALORIES1 * self.weight
                    + (self.get_mean_speed() ** 2 // self.height)
                    * SportsWalking.CEFF_CALORIES2 * self.weight)
                    * (self.duration * Training.MIN_IN_HOUR))
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    COEFF_CALORIES1: ClassVar[int] = 1.1
    CEFF_CALORIES2: ClassVar[int] = 2
    length_pool: int
    count_pool: int

    def get_mean_speed(self) -> float:
        speed = ((self.length_pool * self.count_pool)
                 / Training.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed() + Swimming.COEFF_CALORIES1)
                    * Swimming.CEFF_CALORIES2 * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_code = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    if workout_type not in training_code:
        raise NameError('Тип занятий не предусмотрен!, Обновите программу!')
    else:
        workout = training_code[workout_type](*data)
    return workout


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
    message = InfoMessage.get_message(info)
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

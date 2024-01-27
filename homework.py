from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    INFO_MESSAGE = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.INFO_MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    HOUR_IN_MINUTE = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Дочерние классы должны реализовать это.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    action: int
    duration: float
    weight: float

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER
             * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.HOUR_IN_MINUTE
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_WALK_MULTIPLIER = 0.035
    CALORIES_MEAN_WALK_SHIFT = 0.029
    KMH_IN_MS = round(1000 / 3600, 3)
    M_IN_CM = 100

    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_WALK_MULTIPLIER
                * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MS)**2 / (self.height / self.M_IN_CM))
                * self.CALORIES_MEAN_WALK_SHIFT
                * self.weight)
                * self.duration
                * self.HOUR_IN_MINUTE)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SWIM_MULTIPLIER = 1.1
    CALORIES_MEAN_SWIM_SHIFT = 2

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SWIM_MULTIPLIER)
                * self.CALORIES_MEAN_SWIM_SHIFT
                * self.weight
                * self.duration)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    allowed_workout_type = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type not in allowed_workout_type:
        raise ValueError('Недопустимый тип тренировки.')
    return allowed_workout_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

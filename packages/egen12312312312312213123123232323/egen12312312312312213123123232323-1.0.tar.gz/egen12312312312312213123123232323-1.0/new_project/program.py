class User:

    """Базовый клас пользователя
    """
    
    def __init__(self):
        """Инициализация пользвателя
        """
        self.__login = input('login:')
        self.__password = input('password:')
    def info(self):
        """Получение информации о пользователе
        """
        pass


class Admin(User):

    """Пользователь Администратор
    """
    
    pass

class Support(User):

    """Пользователь поддержки
    """
    
    pass


def create_user(user_type):
    """Создаёт пользователя
    
    Args:
        user_type (str): Тип пользователя для создания
    
    Returns:
        TYPE: Description
    """
    return 'USER'

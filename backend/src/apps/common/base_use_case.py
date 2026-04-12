from abc import ABCMeta, abstractmethod
from collections.abc import Callable


class BaseUseCase[T](metaclass=ABCMeta):
    """This is a template of a base use case.
    All use cases in the app should follow this rule:
      * Input variables should be done at the __init__ phase
      * Use case should implement a single entrypoint without arguments
    """

    def __call__(self) -> T:
        self.validate()
        return self.act()

    def get_validators(self) -> list[Callable[[], None]]:
        return []

    def validate(self) -> None:
        validators = self.get_validators()
        for validator in validators:
            validator()

    @abstractmethod
    def act(self) -> T:
        raise NotImplementedError('Please implement in the use case.')

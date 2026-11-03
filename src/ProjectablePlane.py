from abc import ABC, abstractmethod
#strategy design pattern
class ProjectablePlane(ABC):
    """interface should implement  each shape for this project  """
    @abstractmethod
    def get_parameters(self):
        pass
    """
    method to return all the parametrs we need for the projection
    (start_a1, start_a2, vector_ab, vector_ac, height, width)
    """
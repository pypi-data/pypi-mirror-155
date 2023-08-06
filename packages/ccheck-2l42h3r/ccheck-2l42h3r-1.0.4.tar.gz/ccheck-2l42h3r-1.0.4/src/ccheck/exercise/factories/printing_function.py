"""PritingFunctionExercise factory module"""

from ccheck.domain.exercise.exercise import Exercise
from ccheck.domain.exercise.exercise_creator import ExerciseCreator
from ccheck.exercise.printing_function import PrintingFunctionExercise


class PrintingFunctionExerciseCreator(ExerciseCreator):
    """PrintingFunctionExercise factory"""

    def factory_method(self) -> Exercise:
        return PrintingFunctionExercise()

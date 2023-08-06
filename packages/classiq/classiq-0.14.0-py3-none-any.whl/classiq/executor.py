"""Executor module, implementing facilities for executing quantum programs using Classiq platform."""
import asyncio
import itertools
from typing import Any, Collection, Iterable, List, Optional, Sequence, Tuple, Union

from classiq.interface.backend.backend_preferences import BackendPreferencesTypes
from classiq.interface.executor import execution_request, result as exc_result
from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.executor.hamiltonian_minimization_problem import (
    HamiltonianMinimizationProblem,
)
from classiq.interface.executor.quantum_program import Arguments, QuantumProgram
from classiq.interface.executor.result import (
    ExecutionDetails,
    FinanceSimulationResults,
    GroverSimulationResults,
)
from classiq.interface.executor.vqe_result import VQESolverResult
from classiq.interface.generator.result import GeneratedCircuit

from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.async_utils import Asyncify, syncify_function
from classiq._internals.type_validation import validate_type
from classiq.exceptions import ClassiqExecutionError, ClassiqValueError

BatchExecutionResult = Union[ExecutionDetails, BaseException]
ProgramAndResult = Tuple[QuantumProgram, BatchExecutionResult]
BackendPreferencesProgramAndResult = Tuple[
    BackendPreferencesTypes, QuantumProgram, BatchExecutionResult
]


class Executor(metaclass=Asyncify):
    """Executor is the entry point for executing quantum programs on multiple quantum hardware vendors."""

    def __init__(
        self, preferences: Optional[ExecutionPreferences] = None, **kwargs
    ) -> None:
        """Init self.

        Args:
            preferences (): Execution preferences, such as number of shots.
        """
        self._preferences = preferences or ExecutionPreferences(**kwargs)

    @property
    def preferences(self) -> ExecutionPreferences:
        return self._preferences

    async def _execute(self, expected_type: Any, **execution_request_kwargs):
        request = execution_request.ExecutionRequest(
            preferences=self._preferences, **execution_request_kwargs
        )

        try:
            execution_result = await ApiWrapper.call_execute_task(request=request)
        except Exception as exc:
            raise ClassiqExecutionError(f"Execution failed: {exc!s}") from exc

        if execution_result.status != exc_result.ExecutionStatus.SUCCESS:
            raise ClassiqExecutionError(f"Execution failed: {execution_result.details}")

        return validate_type(
            obj=execution_result.details,
            expected_type=expected_type,
            operation="Execution",
            exception_type=ClassiqExecutionError,
        )

    async def execute_quantum_program_async(
        self,
        quantum_program: QuantumProgram,
        arguments: Optional[Arguments] = None,
    ) -> ExecutionDetails:
        kwargs = quantum_program.dict()
        if arguments:
            original_arguments = kwargs["arguments"] or {}
            kwargs["arguments"] = {**original_arguments, **arguments}

        return await self._execute(
            execution_payload=execution_request.QuantumProgramExecution(**kwargs),
            expected_type=ExecutionDetails,
        )

    async def batch_execute_quantum_program_async(
        self, quantum_programs: Collection[QuantumProgram]
    ) -> List[ProgramAndResult]:
        results = await asyncio.gather(
            *map(self.execute_quantum_program_async, quantum_programs),
            return_exceptions=True,
        )
        return list(zip(quantum_programs, results))

    async def execute_generated_circuit_async(
        self, generation_result: GeneratedCircuit
    ) -> Union[FinanceSimulationResults, GroverSimulationResults]:
        if generation_result.metadata is None:
            raise ClassiqExecutionError(
                "The execute_generated_circuit is to execute generated circuits as oracles, but "
                "the generated circuit's metadata is empty. To execute a circuit as-is, please"
                "use execute_quantum_program."
            )

        return await self._execute(
            execution_payload=execution_request.GenerationMetadataExecution(
                **generation_result.metadata.dict()
            ),
            expected_type=(FinanceSimulationResults, GroverSimulationResults),
        )

    async def execute_hamiltonian_minimization_async(
        self,
        hamiltonian_minimization_problem: HamiltonianMinimizationProblem,
    ) -> VQESolverResult:
        return await self._execute(
            execution_payload=execution_request.HamiltonianMinimizationProblemExecution(
                **hamiltonian_minimization_problem.dict()
            ),
            expected_type=VQESolverResult,
        )

    async def execute_async(
        self,
        arg: Union[GeneratedCircuit, QuantumProgram, str],
        *args,
        **kwargs,
    ):
        if isinstance(arg, GeneratedCircuit):
            if arg.metadata is not None:
                return await self.execute_generated_circuit_async(
                    arg,
                    *args,
                    **kwargs,
                )
            else:
                first_format, first_output = next(iter(arg.outputs.items()))
                program = QuantumProgram(code=first_output, syntax=first_format)
        elif isinstance(arg, QuantumProgram):
            program = arg
        elif isinstance(arg, str):
            program = QuantumProgram(code=arg)
        else:
            raise ClassiqValueError("Invalid executor input")

        return await self.execute_quantum_program_async(
            program,
            *args,
            **kwargs,
        )


async def batch_execute_multiple_backends_async(
    preferences_template: ExecutionPreferences,
    backend_preferences: Sequence[BackendPreferencesTypes],
    quantum_programs: Collection[QuantumProgram],
) -> List[BackendPreferencesProgramAndResult]:
    """
    Execute all the provided quantum programs (n) on all the provided backends (m).
    In total, m * n executions.
    The return value is a list of the following tuples:

    - An element from `backend_preferences`
    - An element from `quantum_programs`
    - The execution result of the quantum program on the backend. If the execution failed,
      the value is an exception.

    The length of the list is m * n.

    The `preferences_template` argument is used to supplement all other preferences.

    The code is equivalent to:
    ```
    for backend in backend_preferences:
        for program in quantum_programs:
            preferences = preferences_template.copy()
            preferences.backend_preferences = backend
            Executor(preferences).execute_quantum_program(program)
    ```
    """
    executors = [
        Executor(
            preferences=preferences_template.copy(
                update={"backend_preferences": backend}
            )
        )
        for backend in backend_preferences
    ]
    results = await asyncio.gather(
        *(
            executor.batch_execute_quantum_program_async(quantum_programs)
            for executor in executors
        ),
        return_exceptions=True,
    )

    def map_return_value(
        executor: Executor,
        result: Union[List[ProgramAndResult], BaseException],
    ) -> Iterable[BackendPreferencesProgramAndResult]:
        nonlocal quantum_programs
        preferences = executor.preferences.backend_preferences
        if isinstance(result, BaseException):
            return ((preferences, program, result) for program in quantum_programs)
        else:
            return (
                (preferences, program, single_result)
                for program, single_result in result
            )

    return list(
        itertools.chain.from_iterable(
            map_return_value(executor, result)
            for executor, result in zip(executors, results)
        )
    )


batch_execute_multiple_backends = syncify_function(
    batch_execute_multiple_backends_async
)

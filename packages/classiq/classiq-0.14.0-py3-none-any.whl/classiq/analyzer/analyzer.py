"""Analyzer module, implementing facilities for analyzing circuits using Classiq platform."""
import json
import webbrowser
from typing import List, Optional, Union
from urllib.parse import urljoin

import plotly.graph_objects as go

from classiq.interface.analyzer import analysis_params, result as analysis_result
from classiq.interface.backend.quantum_backend_providers import AnalyzerProviderVendor
from classiq.interface.generator import result as generator_result
from classiq.interface.server import routes

from classiq._internals import client
from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.async_utils import Asyncify
from classiq._internals.type_validation import validate_type
from classiq.exceptions import ClassiqAnalyzerError


class Analyzer(metaclass=Asyncify):
    """Analyzer is the wrapper object for all analysis capabilities."""

    def __init__(self, circuit: generator_result.GeneratedCircuit):
        """Init self.

        Args:
            circuit (): The circuit to be analyzed.
        """
        self.graph: go.Figure = None
        self.hardware_comparison_table: go.Figure = None
        if circuit.qasm is None:
            raise ValueError("Analysis requires a circuit with valid QASM code")
        self._params = analysis_params.AnalysisParams(qasm=circuit.qasm)
        self.input = circuit

    async def analyze_async(self) -> analysis_result.Analysis:
        """Runs the circuit analysis.

        Returns:
            The analysis result.
        """
        result = await ApiWrapper.call_analysis_task(self._params)

        if result.status != analysis_result.AnalysisStatus.SUCCESS:
            raise ClassiqAnalyzerError(f"Analysis failed: {result.details}")
        details = validate_type(
            obj=result.details,
            expected_type=analysis_result.Analysis,
            operation="Analysis",
            exception_type=ClassiqAnalyzerError,
        )

        dashboard_path = routes.ANALYZER_DASHBOARD
        self._open_route(path=dashboard_path)
        return details

    async def analyzer_app_async(self) -> None:
        """Opens the analyzer app with synthesis interactive results.

        Returns:
            None.
        """
        result = await ApiWrapper.call_analyzer_app(self.input)
        webbrowser.open_new_tab(urljoin(routes.ANALYZER_FULL_FE_APP, str(result.id)))

    async def get_qubits_connectivity_async(self) -> None:
        """create a network connectivity graph of the analysed circuit.

        Returns:
            None.
        """
        result = await ApiWrapper.call_graphs_task(self._params)
        self.graph = go.Figure(json.loads(result.graph))

    async def plot_qubits_connectivity_async(self) -> None:
        """plot the connectivity graph. if it has not been created it, it first creates the graph.

        Returns:
            None.
        """
        if not hasattr(self, "graph"):
            await self.get_qubits_connectivity_async()
        self.graph.show()

    async def get_hardware_comparison_table_async(
        self,
        hardware: Optional[List[Union[str, AnalyzerProviderVendor]]] = None,
    ) -> None:
        """create a comparison table between the transpiled circuits result on different hardware.
        The  comparison table included the depth, multi qubit gates count,and total gates count of the circuits.

        Args: hardware (): List of hardware (string or `AnalyzerProviderVendor`). if None, the table will include all
        the available hardware.

        Returns: None.
        """
        if hardware is None:
            hardware = list(AnalyzerProviderVendor)
        params = analysis_params.AnalysisTableParams(
            qasm=self._params.qasm, hardware=hardware
        )
        result = await ApiWrapper.call_table_graphs_task(params=params)
        self.hardware_comparison_table = go.Figure(json.loads(result.graph))

    async def plot_hardware_comparison_table_async(
        self,
    ) -> None:
        """plot the comparison table. if it has not been created it, it first creates the table using all the
        available hardware.

        Returns:
            None.
        """
        if not hasattr(self, "hardware_comparison_table"):
            await self.get_hardware_comparison_table_async()
        self.hardware_comparison_table.show()

    @staticmethod
    def _open_route(path: str) -> None:
        backend_uri = client.client().get_backend_uri()
        webbrowser.open_new_tab(f"{backend_uri}{path}")

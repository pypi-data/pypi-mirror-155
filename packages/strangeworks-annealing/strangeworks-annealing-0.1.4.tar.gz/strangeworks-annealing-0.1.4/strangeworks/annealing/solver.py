import uuid
from typing import Dict, List, Union
from strangeworks.backend.backends import Backend
from strangeworks.errors.error import StrangeworksError
from strangeworks.jobs.jobs import Job
import strangeworks
import networkx as nx
from .problem import Problem
from dwave_embedding_utilities import embed_ising, unembed_samples
from minorminer import find_embedding
from strangeworks.backend.backends import Backend
from strangeworks.jobs.jobs import Job

from dimod import (
    BinaryQuadraticModel,
    ConstrainedQuadraticModel,
    DiscreteQuadraticModel,
)


class Solver:
    def __init__(
        self,
        backend: Backend,
        params: dict,
        target_quadratic: dict = None,
        target_linear: dict = None,
        random_seed: int = None,
        chain_quadratic: dict = None,
        samples: List[Dict] = None,
    ):
        self.backend = backend
        self.params = params
        self.__target_linear = target_linear
        self.__target_quadratic = target_quadratic
        self.__chain_quadratic = chain_quadratic
        self.__random_seed = random_seed
        self.__samples = samples

    def optimize(
        self,
        problem: Union[
            Problem,
            BinaryQuadraticModel,
            ConstrainedQuadraticModel,
            DiscreteQuadraticModel,
        ],
        shots: int = 1,
        result_id: str = None,
        **kwargs,
    ) -> Job:
        # create a new result for each job unless the user specifies a result in the client
        rid = str(uuid.uuid4()) if result_id is None else result_id

        # check if backend can run annealing problems
        if self.backend.backend_type() != "annealing":
            raise StrangeworksError.invalid_argument(
                f"{self.backend.name()} is not a supported backend for annealing service"
            )

        if "dwave" in self.backend.plugin_url().lower():
            return self.__submit_to_dwave_direct(problem, shots, **kwargs)

        if not isinstance(problem, Problem):
            raise StrangeworksError.invalid_argument(
                "dimod quadratic models are valid inputs only for dwave.* backends"
            )

        data = self.backend.backend_data()
        embed = True
        if "embed" in data and data["embed"] == 0:
            embed = False
            self.__target_linear = problem.linear
            self.__target_quadratic = problem.quadratic

        # check if problem is embedded, if not embed problem
        if embed and (self.__target_linear is None or self.__target_quadratic is None):
            coupling_map = self.__get_coupling_map()
            self.embed_problem(problem, coupling_map)

        payload = {
            "target": self.backend.name(),
            "result_id": rid,
            "shots": shots,
            "backend_params": self.params,
            "kwargs": kwargs,
        }
        nq = {}
        for v in self.__target_quadratic:
            k = ",".join(map(str, v))
            nq[k] = self.__target_quadratic[v]
        qb = {}
        qb["quadratic"] = nq
        qb["linear"] = self.__target_linear
        payload["qubo"] = qb
        payload["problem_type"] = problem.problem_type

        # post to the correct plugin and return a job
        response = strangeworks.client.rest_client.post(
            url=f"{self.backend.plugin_url()}/run-annealing-job",
            json=payload,
            expected_response=200,
        )

        return Job.from_json(
            job=response,
            backend=self.backend,
            rest_client=strangeworks.client.rest_client,
        )

    def embed_problem(self, problem: Problem, coupler: dict):
        # set up problem
        problem_graph = nx.Graph()
        problem_graph.add_nodes_from(problem.linear.keys())
        problem_graph.add_edges_from(problem.quadratic.keys())

        # fetch coupling from solver
        coupler_graph = nx.Graph()
        coupler_graph.add_nodes_from(coupler["qubits"])
        coupler_graph.add_edges_from(coupler["couplers"])

        self.embedding = find_embedding(
            problem_graph, coupler_graph, random_seed=self.__random_seed
        )
        (
            self.__target_linear,
            self.__target_quadratic,
            self.__chain_quadratic,
        ) = embed_ising(
            problem.linear, problem.quadratic, self.embedding, coupler_graph
        )

    def unembed_result(self, job: Job) -> List[Dict]:
        output = job.results()
        solutions = output["solutions"]
        self.samples = unembed_samples(solutions, self.embedding)
        return self.samples

    def __get_coupling_map(self) -> dict:
        return strangeworks.client.rest_client.get(
            f"{self.backend.plugin_url()}/backend/{self.backend.name()}/coupling"
        )

    def __submit_to_dwave_direct(self, problem, shots, **kwargs) -> Job:
        supported_problem_type = (
            isinstance(problem, Problem)
            or isinstance(problem, BinaryQuadraticModel)
            or isinstance(problem, ConstrainedQuadraticModel)
            or isinstance(problem, DiscreteQuadraticModel)
        )
        if not supported_problem_type:
            raise StrangeworksError.invalid_argument(f"{type(problem)} is unsuportted")
        target = self.backend.name()
        if isinstance(problem, Problem):
            if "hybrid" in target:
                raise StrangeworksError.invalid_argument(
                    "strangeworks.annealing.Problem not a vaild input for a dwave hybrid qpu"
                )
            # todo: need to add an if no embedd then self.__target_liner = problem.linear & self.__target_quadratic = problem.quadratic
            if self.__target_linear is None or self.__target_quadratic is None:
                coupling_map = self.__get_coupling_map()
                self.embed_problem(problem, coupling_map)
            nq = {}
            for v in self.__target_quadratic:
                k = ",".join(map(str, v))
                nq[k] = self.__target_quadratic[v]
            problem_dict = {}
            problem_dict["quadratic"] = nq
            problem_dict["linear"] = self.__target_linear
            problem_dict["problem_type"] = problem.problem_type
            payload = {
                "shots": shots,
                "target": target,
                "parameters": {},
                "problem_type": problem_dict["problem_type"],
                "problem": {
                    problem_dict["problem_type"]: {
                        "linear": problem_dict["linear"],
                        "quadratic": problem_dict["quadratic"],
                    }
                },
            }
            payload["parameters"].update(kwargs)
        else:
            with problem.to_file() as f:
                files = {"file": ("dimod-quad-model", f)}
                file_res = strangeworks.client.rest_client.post(
                    url="/files", files=files
                )
                file_id = file_res["ID"]
            problem_type = type(problem).__module__ + "." + type(problem).__name__

            payload = {
                "target": target,
                "parameters": {},
                "problem_type": problem_type,
                "problem": {problem_type: {"file_id": file_id}},
            }
            payload["parameters"].update(kwargs)

        response = strangeworks.client.rest_client.post(
            url=f"{self.backend.plugin_url()}/run-annealing-job",
            json=payload,
            expected_response=200,
        )

        return Job.from_json(
            job=response,
            backend=self.backend,
            rest_client=strangeworks.client.rest_client,
        )


def get_solvers(
    selected_solver: Union[str, Solver] = None, pprint: bool = True
) -> List[Backend]:
    return strangeworks.backends_service.get_backends(
        selected_solver, pprint, filters=lambda b: b.backend_type() == "annealing"
    )


def select_solver(selected_backend: Union[str, Backend] = None, **kwargs) -> Solver:
    return Solver(
        backend=strangeworks.backends_service.select_backend(selected_backend),
        params=kwargs,
    )

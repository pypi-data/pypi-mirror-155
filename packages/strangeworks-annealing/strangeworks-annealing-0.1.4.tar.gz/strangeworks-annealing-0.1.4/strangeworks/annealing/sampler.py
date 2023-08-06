import dimod
from dimod.exceptions import BinaryQuadraticModelStructureError
from strangeworks.errors.error import StrangeworksError

import strangeworks


class SWDWaveSampler(dimod.Sampler, dimod.Structured):
    def __init__(self, solver="dwave.Advantage_system4.1") -> None:
        supported_samplers = {
            "dwave": {
                "sampler": "DWaveSampler",
            },
            "aws": {
                "sampler": "BraketDwaveSampler",
            },
        }

        # todo: this can be expensive if backends are not already loaded in mem.
        self._backend = strangeworks.backends_service.select_backend(solver)
        provider = self._backend.provider()
        if provider not in supported_samplers:
            raise StrangeworksError.invalid_argument(
                f"{solver} not supported by SWDWaveSampler"
            )

        # it could be the case that the user specified an unsported solver...
        self._solver = self._backend.name()
        self._sampler = supported_samplers[provider]["sampler"]
        url = f"{self._backend.plugin_url()}/sampler/{self._sampler}/{self._solver}"
        # todo: this can also be expensive ...
        dwave_sampler = strangeworks.client.rest_client.get(url)
        self._properties = dwave_sampler["properties"]
        self._parameters = dwave_sampler["parameters"]
        self._nodelist = dwave_sampler["nodelist"]
        self._edgelist = dwave_sampler["edgelist"]

    @property
    def properties(self):
        return self._properties

    @property
    def parameters(self):
        return self._parameters

    @property
    def nodelist(self):
        return self._nodelist

    @property
    def edgelist(self):
        return self._edgelist

    def sample(self, bqm, warnings=None, **kwargs):
        with bqm.to_file() as f:
            files = {"file": ("dimod-quad-model", f)}
            file_res = strangeworks.client.rest_client.post(url="/files", files=files)
            file_id = file_res["ID"]
        problem_type = type(bqm).__module__ + "." + type(bqm).__name__

        payload = {
            "target": self._solver,
            "parameters": {},
            "problem_type": problem_type,
            "problem": {problem_type: {"file_id": file_id}},
        }
        payload["parameters"].update(kwargs)
        if warnings:
            payload["warnings"] = warnings

        return self.__send_request(payload)

    def sample_ising(self, h, *args, **kwargs):
        J = {}
        if "J" in args:
            for v in args["J"]:
                k = ",".join(map(str, v))
                J[k] = args["J"][v]
        payload = {
            "target": self._solver,
            "parameters": {},
            "problem_type": "ising",
            "problem": {
                "ising": {
                    "linear": h,
                    "quadratic": J,
                }
            },
        }
        payload["parameters"].update(kwargs)
        return self.__send_request(payload)

    def __send_request(self, payload):
        try:
            url = f"{self._backend.plugin_url()}/sampler/{self._sampler}/sample"
            res = strangeworks.client.rest_client.post(
                url,
                json=payload,
                expected_response=200,
            )
        except StrangeworksError as e:
            if "Problem graph incompatible with solver" in e.message:
                raise BinaryQuadraticModelStructureError(e.message)
            else:
                raise e
        return dimod.SampleSet.from_serializable(res)

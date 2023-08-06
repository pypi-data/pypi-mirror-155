from pathlib import Path

from pytorch_lightning import Trainer

from lightning_app.components.python import TracerPythonScript
from lightning_app.utilities.tracer import Tracer


class PLTracerPythonScript(TracerPythonScript):
    def configure_tracer(self) -> Tracer:
        # This hook would be called everytime
        # before a Trainer `__init__` method is called.
        def trainer_pre_fn(self, *args, **kwargs):
            # Injecting `fast_dev_run` in the Trainer kwargs.
            return {}, args, kwargs

        tracer = super().configure_tracer()
        tracer.add_traced(Trainer, "__init__", pre_fn=trainer_pre_fn)
        return tracer


if __name__ == "__main__":
    comp = PLTracerPythonScript(Path(__file__).parent / "pl_script.py")
    res = comp.run()

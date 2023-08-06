from pydantic import BaseModel
from async_rundeck.proto import definitions
import inspect

for name, model in inspect.getmembers(definitions, inspect.isclass):
    if not issubclass(model, BaseModel):
        continue

    model.update_forward_refs()

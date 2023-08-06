# named-env

Class-based environment variables typed specification.

## Usage example

```python
from named_env import EnvironmentNamespace, RequiredInteger
import os


class WebApplicationEnvironmentNamespace(EnvironmentNamespace):
    WEB_SERVER_PORT = RequiredInteger()


env = WebApplicationEnvironmentNamespace()

if __name__ == "__main__":
    os.environ["WEB_SERVER_PORT"] = "80"
    print(env.WEB_SERVER_PORT)  # 80
    print(type(env.WEB_SERVER_PORT))  # int
```

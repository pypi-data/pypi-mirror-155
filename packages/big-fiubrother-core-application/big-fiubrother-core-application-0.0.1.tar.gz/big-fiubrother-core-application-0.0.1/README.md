# big-fiubrother-core-application

*big-fiubrother-core-application* module is a basic frame to be used in all the applications from the Big Fiubrother project.
This module concentrates common tasks that are needed in all the microservices, for example:
- Parsing arguments
- Loading configuration
- Starting (distributed) logging
- Handle Linux signals

## Usage

```python
from big_fiubrother_core_application import run


with run('application_name') as application:
    while not application.is_stopped():
        work()
```
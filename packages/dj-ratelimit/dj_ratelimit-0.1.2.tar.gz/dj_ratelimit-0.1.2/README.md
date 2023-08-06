# dj-ratelimit
Redis backed ratelimit implemented with leaky bucket algorithm

To install:
```commandline
pip install dj-ratelimit
```

https://pypi.org/project/dj-ratelimit/0.1.0/

### Requirements

#### V 0.1.0

- dj-ratelimit currently supported for redis backed queue using djangorestframework requests
- The following environment variables should be set:
  - ENVIRONMENT
  - DJ_RATELIMIT_REDIS_ADDRESS
  - DJ_RATELIMIT_REDIS_PORT

### Usage

```python
from dj_ratelimit.src.bucket import ratelimit


class DjangoView(APIView):
  # View Setup

  @ratelimit(rate="200/m", burst_limit=400, key_fn=custom_key_func)
  def post(self, request):
        # Request handling
```

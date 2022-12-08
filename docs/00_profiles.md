# Profiles - how to switch between local Orion and various Cloud workspaces

Prefect 2 makes it easy to **switch between environments**.

## Why Profiles?

  A single Prefect 2.0 installation can communicate with **multiple Orion APIs**, which can help you switch between development, staging, and production environments.

  As long as each profile points to a different `PREFECT_API_URL`, you can easily switch between multiple instances.

  Each profile can point to:

- a different Prefect Cloud workspace
- a different Prefect Orion API endpoint (e.g. for local development)

## How to create it?

  To create one, you can use:

    prefect profile create demo
    prefect profile use dev
    prefect cloud login # or prefect orion start

## How to switch?

  To switch between those, you can use:

    prefect profile use dev # or prod or any other profile

## Where is this file located?

```python
prefect config view --show-defaults | grep PROFILES_PATH
# PREFECT_PROFILES_PATH='~/.prefect/profiles.toml'
```

```python
cat ~/.prefect/profiles.toml
```

```toml
active = "default"

[profiles.default]
PREFECT_API_URL = "http://127.0.0.1:4200/api"
PREFECT_LOGGING_LEVEL = "DEBUG"
PREFECT_LOCAL_STORAGE_PATH = "/Users/anna/.prefect/results/local"

[profiles.docker]
PREFECT_API_URL = "http://0.0.0.0:4200/api"
PREFECT_LOGGING_LEVEL = "DEBUG"

[profiles.prod]
PREFECT_API_URL = "https://api.prefect.cloud/api/accounts/c5276cbb-62a2-4501-b64a-74d3d900d781/workspaces/5b915f84-73fc-429b-a701-79d4a247004e"
PREFECT_API_KEY = "xxx"
PREFECT_LOGGING_LEVEL = "INFO"

[profiles.integrations]
PREFECT_API_URL = "https://api.prefect.cloud/api/accounts/c5276cbb-62a2-4501-b64a-74d3d900d781/workspaces/aaeffa0e-13fa-460e-a1f9-79b53c05ab36"
PREFECT_API_KEY = "xxx"
PREFECT_LOGGING_EXTRA_LOGGERS = "Ingestion,OMetaAPI,Metadata,Profiler,Utils"
PREFECT_LOGGING_LEVEL = "INFO"
PREFECT_RESULTS_PERSIST_BY_DEFAULT = "true"

[profiles.development]
PREFECT_API_KEY = "xxx"
PREFECT_API_URL = "https://api.prefect.cloud/api/accounts/d3dfeec8-870a-476d-971a-4e3826a63e70/workspaces/7724016b-e783-4a99-aa90-6cd5813edffe"
PREFECT_LOGGING_LEVEL = "DEBUG"
```


More information about managing multiple environments with workspaces: [Settings - Prefect 2](https://docs.prefect.io/concepts/settings/?h=profiles#configuration-profiles)

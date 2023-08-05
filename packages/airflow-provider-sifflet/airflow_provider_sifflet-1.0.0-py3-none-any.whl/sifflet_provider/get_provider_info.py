import sifflet_provider


def get_provider_info():
    return {
        "package-name": "airflow-provider-sifflet",
        "name": "Sifflet",
        "description": "This package provides operators and hook that integrate Sifflet into Apache Airflow.",
        "versions": [
            sifflet_provider.__version__,
        ],
        "additional-dependencies": ["apache-airflow>=2.0.0"],
        "operators": [
            {
                "integration-name": "Sifflet Run Rule",
                "python-modules": ["sifflet_provider.operators.rule"],
            },
            {
                "integration-name": "Sifflet Ingest dbt",
                "python-modules": ["sifflet_provider.operators.dbt"],
            },
        ],
        "connection-types": [
            {
                "hook-class-name": "sifflet_provider.hooks.sifflet_hook.SiffletHook",
                "connection-type": "sifflet",
            },
        ],
    }

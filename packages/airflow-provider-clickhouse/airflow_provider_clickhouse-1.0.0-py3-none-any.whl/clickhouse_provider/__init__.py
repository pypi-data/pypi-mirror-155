
def get_provider_info():
    return {
        "package-name":            "airflow-provider-clickhouse",
        "name":                    "Clickhouse Airflow Provider",
        "description":             "Clickhouse provider for Airflow",
        "versions":                [
            "1.0.0"
        ],
        "additional-dependencies": [
            "apache-airflow>=2.2.0", "clickhouse_driver>=0.2.1", "pandas>=1.3.2"
        ],
        "integrations":            [
            {
                "integration-name": "Clickhouse",
                "external-doc-url": "https://osample.link.com",
                "tags":             [
                    "service", "clickhouse","database","airflow"
                ]
            }
        ],
        "operators":               [
            {
                "integration-name": "Clickhouse",
                "python-modules":   [
                    "clickhouse_provider.operators.clickhouse_operator.ClickhouseOperator"
                ]
            }
        ],
        "hooks":                   [
            {
                "integration-name": "Clickhouse",
                "python-modules":   [
                    "clickhouse_provider.hooks.clickhouse_hook.ClickhouseHook"
                ]
            }
        ],
	"hook-class-names": ['clickhouse_provider.hooks.clickhouse_hook.ClickhouseHook'],
        "connection-types":        [
            {
                "hook-class-name": "clickhouse_provider.hooks.clickhouse_hook.ClickhouseHook",
                "connection-type": "clickhouse"
            }
        ]
    }

import google.auth
from google.cloud import bigquery as bq


class BqQueryQueryRunner:
    def run(self, query: str):
        credentials, project_id = self._get_credentials()
        client = bq.Client(credentials=credentials, project=project_id)
        return client.query(query).result().to_dataframe()

    def _get_credentials(self):
        return google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

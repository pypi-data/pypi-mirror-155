from datetime import datetime, timedelta
import logging
import re
from typing import Optional
import aiohttp

from base64 import b64encode

from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

def get_auth_token(req) -> Optional[str]:
    auth_headers = [
        req.headers.get(key)
        for key in req.headers.keys()
        if str.lower(key) == 'authorization' and str.lower(req.headers.get(key)).startswith('bearer ')
    ]
    
    return auth_headers[0][len('bearer '):]

async def get_user_mail(token: str) -> Optional[str]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method='GET',
                url='https://graph.microsoft.com/v1.0/me',
                headers={'Authorization': f'Bearer {token}'}
            ) as response:

                user_data = await response.json()

                if 'mail' in user_data:
                    return user_data['mail']
    except Exception as e:
        print(e)

    return None

def store(package, connection_string: str, account_key: str, container_name: str):
    blob_name = f'package_{str(datetime.now()).replace(" ", "_")}.zip'

    blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(connection_string)

    containers = [c.name for c in blob_service_client.list_containers(container_name)]
    if container_name not in containers:
        blob_service_client.create_container(container_name)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(package)

    container_client = blob_service_client.get_container_client(container=container_name)
    blob_count = sum(1 for _ in container_client.list_blobs())

    sas_url = generate_blob_sas(
            account_name=blob_client.account_name,
            container_name=blob_client.container_name,
            blob_name=blob_name,
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=2)
        )

    return (f'https://{blob_client.account_name}.blob.core.windows.net/{blob_client.container_name}/{blob_name}?{sas_url}', blob_count)


async def trigger_pipeline(personal_access_token: str, organization: str, project_id: str, pipeline_id: int, package_url: str, image_name: str, version: str, author: str):
    # Create a connection to the org
    async with aiohttp.ClientSession() as session:
        async with session.request(
            method='POST',
            url=f'https://dev.azure.com/{organization}/{project_id}/_apis/pipelines/{pipeline_id}/runs?api-version=6.0-preview.1',
            headers={ 'Authorization': f'Basic {b64encode(str.encode(f":{personal_access_token}", encoding="UTF8")).decode("ascii")}' },
            json={
                'templateParameters': {
                    'package': package_url,
                    'imageName': image_name,
                    'version': version,
                    'author': author
                }
            }
        ):
            pass
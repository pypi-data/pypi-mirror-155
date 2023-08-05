import os
import glob
from typing import List
import zipfile
import azure.identity as ai
import click
import requests

@click.group()
def main():
    pass

def get_token(tenant_id: str, client_id: str) -> str:
    config = {
        "authority": "https://login.microsoftonline.com",
        'scope': 'User.ReadBasic.All'
    }

    credentials = ai.InteractiveBrowserCredential(
        authority=config['authority'],
        tenant_id=tenant_id,
        client_id=client_id
    )

    tokens = credentials.get_token(config['scope'])

    return tokens.token

def expand_patterns(patterns) -> List[str]:
    return [f for p in patterns for f in glob.glob(p, recursive=True)]

def get_ignore_list() -> List[str]:
    return expand_patterns(['__pycache__/**/*', 'build/**/*', '*.egg-info'])

def get_file_list() -> List[str]:
    ignores = set(get_ignore_list())
    
    return [file for file in expand_patterns(['**/*.py', '**/*.json', '**/*.txt']) if file not in ignores]

def build_package(files: List[str]) -> str:
    workdir = os.getcwd()

    with zipfile.ZipFile('package.zip', 'w', zipfile.ZIP_DEFLATED) as package:
        for file in files:
            package.write(os.path.join(workdir, file), file)

        return package.filename
    
def publish_package(func_base_url, func_code, token, package_path):
    with open(package_path, 'rb') as package:
        response = requests.post(
            url=f'{func_base_url}/api/player?code={func_code}',
            headers={
                'Authorization': f'Bearer {token}'
            },
            files={
                'package': package
            }
        )

        print(f'{response.status_code}: {response.text}')

@main.command()
@click.argument('tenant_id')
@click.argument('client_id')
@click.argument('func_base_url')
@click.argument('func_code')
def publish(tenant_id: str, client_id: str, func_base_url: str, func_code: str) -> None:
    token = get_token(tenant_id, client_id)

    package_path = build_package(get_file_list())

    try:
        publish_package(func_base_url, func_code, token, package_path)
    finally:
        os.remove(package_path)


if __name__ == '__main__':
    main()
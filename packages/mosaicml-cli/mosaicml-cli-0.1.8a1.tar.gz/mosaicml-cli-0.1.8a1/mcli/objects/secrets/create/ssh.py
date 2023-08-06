"""Creators for ssh secrets"""
from pathlib import Path
from typing import Callable, Optional

from mcli.models import SecretType
from mcli.objects.secrets import MCLISSHSecret
from mcli.objects.secrets.create.base import SecretCreator, SecretValidationError
from mcli.objects.secrets.create.generic import FileSecretFiller, FileSecretValidator
from mcli.utils.utils_interactive import file_prompt
from mcli.utils.utils_string_validation import ensure_rfc1123_compatibility, validate_existing_filename


class SSHSecretFiller(FileSecretFiller):
    """Interactive filler for SSH secret data
    """

    @staticmethod
    def fill_private_key(validate: Callable[[str], bool]) -> str:
        return file_prompt('Where is your private SSH key located?', validate=validate)


class SSHSecretValidator(FileSecretValidator):
    """Validation methods for SSH secret data

    Raises:
        SecretValidationError: Raised for any validation error for secret data
    """

    def validate_only_git_ssh(self) -> bool:
        for secret in self.existing_secrets:
            if secret.secret_type == SecretType.git:
                raise SecretValidationError(f'Git SSH secret already exists: {secret.name}. '
                                            'Only one Git SSH secret is allowed. Try adding the secret as an '
                                            '`ssh` secret instead using `mcli create secret ssh`')
        return True

    @staticmethod
    def validate_private_key(key_path: str) -> bool:

        if not validate_existing_filename(key_path):
            raise SecretValidationError(f'File does not exist. File path {key_path} does not exist or is not a file.')
        return True


class SSHSecretCreator(SSHSecretFiller, SSHSecretValidator):
    """Creates SSH secrets for the CLI
    """

    def create(
        self,
        name: Optional[str] = None,
        mount_path: Optional[str] = None,
        ssh_private_key: Optional[str] = None,
        git: bool = False,
    ) -> MCLISSHSecret:

        # Validate only git secret
        if git:
            self.validate_only_git_ssh()

        # Validate mount and ssh key
        if mount_path:
            self.validate_mount(mount_path)

        if ssh_private_key:
            self.validate_private_key(ssh_private_key)

        # Fill ssh private key
        if not ssh_private_key:
            ssh_private_key = self.fill_private_key(self.validate_private_key)

        # Default name based on private key path
        make_name_unique = False
        if not name:
            name = ensure_rfc1123_compatibility(Path(ssh_private_key).stem)
            make_name_unique = True

        base_creator = SecretCreator()
        secret_type = SecretType.git if git else SecretType.ssh
        secret = base_creator.create(secret_type, name=name, make_name_unique=make_name_unique)
        assert isinstance(secret, MCLISSHSecret)

        if not mount_path:
            mount_path = self.get_valid_mount_path(secret.name)
        secret.mount_path = mount_path

        with open(Path(ssh_private_key).expanduser().absolute(), 'r', encoding='utf8') as fh:
            secret.value = fh.read()

        return secret

'''
[![npm version](https://badge.fury.io/js/cdk-github.svg)](https://badge.fury.io/js/cdk-github)
[![PyPI version](https://badge.fury.io/py/cdk-github.svg)](https://badge.fury.io/py/cdk-github)
[![NuGet version](https://badge.fury.io/nu/cdkgithub.svg)](https://badge.fury.io/nu/cdkgithub)
[![release](https://github.com/wtfjoke/cdk-github/actions/workflows/release.yml/badge.svg)](https://github.com/wtfjoke/cdk-github/actions/workflows/release.yml)
![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

# CDK-GitHub

GitHub Constructs for use in [AWS CDK](https://aws.amazon.com/cdk/) .

This project aims to make GitHub's API accessible through CDK with various helper constructs to create resources in GitHub.
The target is to replicate most of the functionality of the official [Terraform GitHub Provider](https://registry.terraform.io/providers/integrations/github/latest/docs).

Internally [AWS CloudFormation custom resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) and [octokit](https://github.com/octokit/core.js) are used to manage GitHub resources (such as Secrets).

# 🔧 Installation

JavaScript/TypeScript:
`npm install cdk-github`

Python:
`pip install cdk-github`

C#
See https://www.nuget.org/packages/CdkGithub

# 📚 Constructs

This library provides the following constructs:

* [ActionSecret](API.md#actionsecret-a-nameactionsecret-idcdk-githubactionsecreta) - Creates a [GitHub Action (repository) secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository) from a given AWS Secrets Manager secret.
* [ActionEnvironmentSecret](API.md#actionenvironmentsecret-a-nameactionenvironmentsecret-idcdk-githubactionenvironmentsecreta) - Creates a [GitHub Action environment secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-an-environment) from a given AWS Secrets Manager secret.

# 🔓 Authentication

Currently the constructs only support authentication via a [GitHub Personal Access Token](https://github.com/settings/tokens/new). The token needs to be a stored in a AWS SecretsManager Secret and passed to the construct as parameter.

# 👩‍🏫 Examples

The API documentation and examples in different languages are available on [Construct Hub](https://constructs.dev/packages/cdk-github).
All (typescript) examples can be found in the folder [examples](src/examples/).

## ActionSecret

```python
import { Secret } from 'aws-cdk-lib/aws-secretsmanager';
import { ActionSecret } from 'cdk-github';

export class ActionSecretStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const sourceSecret = Secret.fromSecretNameV2(this, 'secretToStoreInGitHub', 'testcdkgithub');
    const githubTokenSecret = Secret.fromSecretNameV2(this, 'ghSecret', 'GITHUB_TOKEN');

    new ActionSecret(this, 'GitHubActionSecret', {
      githubTokenSecret,
      repositoryName: 'cdk-github',
      repositoryOwner: 'wtfjoke',
      repositorySecretName: 'aRandomGitHubSecret',
      sourceSecret,
    });
  }
}
```

## ActionEnvironmentSecret

```python
import { Secret } from 'aws-cdk-lib/aws-secretsmanager';
import { ActionEnvironmentSecret } from 'cdk-github';

export class ActionEnvironmentSecretStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const sourceSecret = Secret.fromSecretNameV2(this, 'secretToStoreInGitHub', 'testcdkgithub');
    const githubTokenSecret = Secret.fromSecretNameV2(this, 'ghSecret', 'GITHUB_TOKEN');

    new ActionEnvironmentSecret(this, 'GitHubActionEnvironmentSecret', {
      githubTokenSecret,
      environment: 'dev',
      repositoryName: 'cdk-github',
      repositoryOwner: 'wtfjoke',
      repositorySecretName: 'aRandomGitHubSecret',
      sourceSecret,
    });
  }
}
```

# 💖 Contributing

Contributions of all kinds are welcome! Check out our [contributing guide](CONTRIBUTING.md).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_secretsmanager
import constructs


class ActionEnvironmentSecret(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-github.ActionEnvironmentSecret",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        environment: builtins.str,
        github_token_secret: aws_cdk.aws_secretsmanager.ISecret,
        repository_name: builtins.str,
        repository_secret_name: builtins.str,
        source_secret: aws_cdk.aws_secretsmanager.ISecret,
        repository_owner: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param environment: (experimental) The GithHub environment name which the secret should be stored in.
        :param github_token_secret: (experimental) The AWS secret in which the OAuth GitHub (personal) access token is stored.
        :param repository_name: (experimental) The GitHub repository name.
        :param repository_secret_name: (experimental) The GitHub secret name to be stored.
        :param source_secret: (experimental) This AWS secret value will be stored in GitHub as a secret (under the name of repositorySecretName).
        :param repository_owner: (experimental) The GitHub repository owner. Default: - user account which owns the token

        :stability: experimental
        '''
        props = ActionEnvironmentSecretProps(
            environment=environment,
            github_token_secret=github_token_secret,
            repository_name=repository_name,
            repository_secret_name=repository_secret_name,
            source_secret=source_secret,
            repository_owner=repository_owner,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-github.ActionEnvironmentSecretProps",
    jsii_struct_bases=[],
    name_mapping={
        "environment": "environment",
        "github_token_secret": "githubTokenSecret",
        "repository_name": "repositoryName",
        "repository_secret_name": "repositorySecretName",
        "source_secret": "sourceSecret",
        "repository_owner": "repositoryOwner",
    },
)
class ActionEnvironmentSecretProps:
    def __init__(
        self,
        *,
        environment: builtins.str,
        github_token_secret: aws_cdk.aws_secretsmanager.ISecret,
        repository_name: builtins.str,
        repository_secret_name: builtins.str,
        source_secret: aws_cdk.aws_secretsmanager.ISecret,
        repository_owner: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param environment: (experimental) The GithHub environment name which the secret should be stored in.
        :param github_token_secret: (experimental) The AWS secret in which the OAuth GitHub (personal) access token is stored.
        :param repository_name: (experimental) The GitHub repository name.
        :param repository_secret_name: (experimental) The GitHub secret name to be stored.
        :param source_secret: (experimental) This AWS secret value will be stored in GitHub as a secret (under the name of repositorySecretName).
        :param repository_owner: (experimental) The GitHub repository owner. Default: - user account which owns the token

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "environment": environment,
            "github_token_secret": github_token_secret,
            "repository_name": repository_name,
            "repository_secret_name": repository_secret_name,
            "source_secret": source_secret,
        }
        if repository_owner is not None:
            self._values["repository_owner"] = repository_owner

    @builtins.property
    def environment(self) -> builtins.str:
        '''(experimental) The GithHub environment name which the secret should be stored in.

        :stability: experimental
        '''
        result = self._values.get("environment")
        assert result is not None, "Required property 'environment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def github_token_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''(experimental) The AWS secret in which the OAuth GitHub (personal) access token is stored.

        :stability: experimental
        '''
        result = self._values.get("github_token_secret")
        assert result is not None, "Required property 'github_token_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def repository_name(self) -> builtins.str:
        '''(experimental) The GitHub repository name.

        :stability: experimental
        '''
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_secret_name(self) -> builtins.str:
        '''(experimental) The GitHub secret name to be stored.

        :stability: experimental
        '''
        result = self._values.get("repository_secret_name")
        assert result is not None, "Required property 'repository_secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''(experimental) This AWS secret value will be stored in GitHub as a secret (under the name of repositorySecretName).

        :stability: experimental
        '''
        result = self._values.get("source_secret")
        assert result is not None, "Required property 'source_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def repository_owner(self) -> typing.Optional[builtins.str]:
        '''(experimental) The GitHub repository owner.

        :default: - user account which owns the token

        :stability: experimental
        '''
        result = self._values.get("repository_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionEnvironmentSecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionSecret(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-github.ActionSecret",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        github_token_secret: aws_cdk.aws_secretsmanager.ISecret,
        repository_name: builtins.str,
        repository_secret_name: builtins.str,
        source_secret: aws_cdk.aws_secretsmanager.ISecret,
        repository_owner: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param github_token_secret: (experimental) The AWS secret in which the OAuth GitHub (personal) access token is stored.
        :param repository_name: (experimental) The GitHub repository name.
        :param repository_secret_name: (experimental) The GitHub secret name to be stored.
        :param source_secret: (experimental) This AWS secret value will be stored in GitHub as a secret (under the name of repositorySecretName).
        :param repository_owner: (experimental) The GitHub repository owner. Default: - user account which owns the token

        :stability: experimental
        '''
        props = ActionSecretProps(
            github_token_secret=github_token_secret,
            repository_name=repository_name,
            repository_secret_name=repository_secret_name,
            source_secret=source_secret,
            repository_owner=repository_owner,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-github.ActionSecretProps",
    jsii_struct_bases=[],
    name_mapping={
        "github_token_secret": "githubTokenSecret",
        "repository_name": "repositoryName",
        "repository_secret_name": "repositorySecretName",
        "source_secret": "sourceSecret",
        "repository_owner": "repositoryOwner",
    },
)
class ActionSecretProps:
    def __init__(
        self,
        *,
        github_token_secret: aws_cdk.aws_secretsmanager.ISecret,
        repository_name: builtins.str,
        repository_secret_name: builtins.str,
        source_secret: aws_cdk.aws_secretsmanager.ISecret,
        repository_owner: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param github_token_secret: (experimental) The AWS secret in which the OAuth GitHub (personal) access token is stored.
        :param repository_name: (experimental) The GitHub repository name.
        :param repository_secret_name: (experimental) The GitHub secret name to be stored.
        :param source_secret: (experimental) This AWS secret value will be stored in GitHub as a secret (under the name of repositorySecretName).
        :param repository_owner: (experimental) The GitHub repository owner. Default: - user account which owns the token

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "github_token_secret": github_token_secret,
            "repository_name": repository_name,
            "repository_secret_name": repository_secret_name,
            "source_secret": source_secret,
        }
        if repository_owner is not None:
            self._values["repository_owner"] = repository_owner

    @builtins.property
    def github_token_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''(experimental) The AWS secret in which the OAuth GitHub (personal) access token is stored.

        :stability: experimental
        '''
        result = self._values.get("github_token_secret")
        assert result is not None, "Required property 'github_token_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def repository_name(self) -> builtins.str:
        '''(experimental) The GitHub repository name.

        :stability: experimental
        '''
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_secret_name(self) -> builtins.str:
        '''(experimental) The GitHub secret name to be stored.

        :stability: experimental
        '''
        result = self._values.get("repository_secret_name")
        assert result is not None, "Required property 'repository_secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''(experimental) This AWS secret value will be stored in GitHub as a secret (under the name of repositorySecretName).

        :stability: experimental
        '''
        result = self._values.get("source_secret")
        assert result is not None, "Required property 'source_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def repository_owner(self) -> typing.Optional[builtins.str]:
        '''(experimental) The GitHub repository owner.

        :default: - user account which owns the token

        :stability: experimental
        '''
        result = self._values.get("repository_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionSecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ActionEnvironmentSecret",
    "ActionEnvironmentSecretProps",
    "ActionSecret",
    "ActionSecretProps",
]

publication.publish()

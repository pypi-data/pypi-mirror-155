'''
# cdk-threagile

![Build](https://github.com/hupe1980/cdk-threagile/workflows/build/badge.svg)
![Release](https://github.com/hupe1980/cdk-threagile/workflows/release/badge.svg)

> Agile Threat Modeling as Code

CDK Constructs for [threatgile](https://threagile.io/)

## Installation

TypeScript/JavaScript:

```bash
npm i cdktg
```

Python:

```bash
pip install cdktg
```

## How to use

### Threat Model written in typescript:

```typescript
const project = new Project();

const model = new Model(project, 'Model Stub', {
    title: 'Model Stub',
    version: '1.0.0',
    date: '2020-03-31',
    author: new Author({
        name: 'John Doe',
    }),
    businessCriticality: BusinessCriticality.IMPORTANT,
});

const someData = new DataAsset(model, 'Some Data Asset', {
    description: 'Some Description',
    usage: Usage.BUSINESS,
    origin: 'Some Origin',
    owner: 'Some Owner',
    quantity: Quantity.MANY,
    ciaTriad: new CIATriad({
        confidentiality: Confidentiality.CONFIDENTIAL,
        integrity: Integrity.CRITICAL,
        availability: Availability.OPERATIONAL,
    }),
});

const someTrustBoundary = new TrustBoundary(model, 'Some Trust Boundary', {
    description: 'Some Description',
    type: TrustBoundaryType.NETWORK_DEDICATED_HOSTER,
});

const someTechnicalAsset = new TechnicalAsset(model, 'Some Technical Asset', {
    trustBoundary: someTrustBoundary,
    description: 'Some Description',
    type: TechnicalAssetType.PROCESS,
    usage: Usage.BUSINESS,
    humanUse: false,
    size: Size.COMPONENT,
    technology: Technology.WEB_SERVICE_REST,
    internet: false,
    machine: Machine.VIRTUAL,
    encryption: Encryption.NONE,
    owner: 'Some Owner',
    ciaTriad: new CIATriad({
        confidentiality: Confidentiality.CONFIDENTIAL,
        integrity: Integrity.CRITICAL,
        availability: Availability.CRITICAL,
    }),
    multiTenant: false,
    redundant: true,
});

someTechnicalAsset.process(someData);

const someOtherTechnicalAsset = new TechnicalAsset(model, 'Some Other Technical Asset', {
    description: 'Some Description',
    type: TechnicalAssetType.PROCESS,
    usage: Usage.BUSINESS,
    humanUse: false,
    size: Size.COMPONENT,
    technology: Technology.WEB_SERVICE_REST,
    tags: ['some-tag', 'some-other-tag'],
    internet: false,
    machine: Machine.VIRTUAL,
    encryption: Encryption.NONE,
    owner: 'Some Owner',
    ciaTriad: new CIATriad({
        confidentiality: Confidentiality.CONFIDENTIAL,
        integrity: Integrity.IMPORTANT,
        availability: Availability.IMPORTANT,
    }),
    multiTenant: false,
    redundant: true,
});

someOtherTechnicalAsset.process(someData);

const someTraffic = someTechnicalAsset.communicateWith('Some Traffic', someOtherTechnicalAsset, {
    description: 'Some Description',
    protocol: Protocol.HTTPS,
    authentication: Authentication.NONE,
    authorization: Authorization.NONE,
    vpn: false,
    ipFiltered: false,
    readonly: false,
    usage: Usage.BUSINESS,
});

someTraffic.send(someData);

const someSharedRuntime = new SharedRuntime(model, "Some Shared Runtime", {
    description: "Some Description",
});

someSharedRuntime.run(someTechnicalAsset, someOtherTechnicalAsset);

project.synth();
```

### cdktg CLI commands:

```sh
cdktg [command]

Commands:
  cdktg synth <filename>  synthesize the models
  cdktg ping              ping the api
  cdktg check             check the models
  cdktg analyse           analyze the models
  cdktg completion        generate completion script

Options:
  --help     Show help                                                 [boolean]
  --version  Show version number                                       [boolean]
```

### Analyse outputs:

```sh
dist
└── ModelStub
    ├── data-asset-diagram.png
    ├── data-flow-diagram.png
    ├── report.pdf
    ├── risks.json
    ├── risks.xlsx
    ├── stats.json
    ├── tags.xlsx
    ├── technical-assets.json
    └── threagile.yaml
```

## Example

See more complete [examples](https://github.com/hupe1980/cdk-threagile-examples).

## License

[MIT](LICENSE)
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

import constructs


class AbuseCase(metaclass=jsii.JSIIMeta, jsii_type="cdktg.AbuseCase"):
    def __init__(self, *, description: builtins.str, name: builtins.str) -> None:
        '''
        :param description: 
        :param name: 
        '''
        props = AbuseCaseProps(description=description, name=name)

        jsii.create(self.__class__, self, [props])

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="DENIAL_OF_SERVICE")
    def DENIAL_OF_SERVICE(cls) -> "AbuseCase":
        return typing.cast("AbuseCase", jsii.sget(cls, "DENIAL_OF_SERVICE"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="RANSOMWARE")
    def RANSOMWARE(cls) -> "AbuseCase":
        return typing.cast("AbuseCase", jsii.sget(cls, "RANSOMWARE"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="cdktg.AbuseCaseProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "name": "name"},
)
class AbuseCaseProps:
    def __init__(self, *, description: builtins.str, name: builtins.str) -> None:
        '''
        :param description: 
        :param name: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "description": description,
            "name": name,
        }

    @builtins.property
    def description(self) -> builtins.str:
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AbuseCaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdktg.AnnotationMetadataEntryType")
class AnnotationMetadataEntryType(enum.Enum):
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


class Annotations(metaclass=jsii.JSIIMeta, jsii_type="cdktg.Annotations"):
    '''Includes API for attaching annotations such as warning messages to constructs.'''

    @jsii.member(jsii_name="of") # type: ignore[misc]
    @builtins.classmethod
    def of(cls, scope: constructs.IConstruct) -> "Annotations":
        '''Returns the annotations API for a construct scope.

        :param scope: The scope.
        '''
        return typing.cast("Annotations", jsii.sinvoke(cls, "of", [scope]))

    @jsii.member(jsii_name="addError")
    def add_error(self, message: builtins.str) -> None:
        '''Adds an { "error":  } metadata entry to this construct.

        The toolkit will fail synthesis when errors are reported.

        :param message: The error message.
        '''
        return typing.cast(None, jsii.invoke(self, "addError", [message]))

    @jsii.member(jsii_name="addInfo")
    def add_info(self, message: builtins.str) -> None:
        '''Adds an info metadata entry to this construct.

        The CLI will display the info message when apps are synthesized.

        :param message: The info message.
        '''
        return typing.cast(None, jsii.invoke(self, "addInfo", [message]))

    @jsii.member(jsii_name="addWarning")
    def add_warning(self, message: builtins.str) -> None:
        '''Adds a warning metadata entry to this construct.

        The CLI will display the warning when an app is synthesized.
        In a future release the CLI might introduce a --strict flag which
        will then fail the synthesis if it encounters a warning.

        :param message: The warning message.
        '''
        return typing.cast(None, jsii.invoke(self, "addWarning", [message]))


class Aspects(metaclass=jsii.JSIIMeta, jsii_type="cdktg.Aspects"):
    '''Aspects can be applied to CDK tree scopes and can operate on the tree before synthesis.'''

    @jsii.member(jsii_name="of") # type: ignore[misc]
    @builtins.classmethod
    def of(cls, scope: constructs.IConstruct) -> "Aspects":
        '''Returns the ``Aspects`` object associated with a construct scope.

        :param scope: The scope for which these aspects will apply.
        '''
        return typing.cast("Aspects", jsii.sinvoke(cls, "of", [scope]))

    @jsii.member(jsii_name="add")
    def add(self, aspect: "IAspect") -> None:
        '''Adds an aspect to apply this scope before synthesis.

        :param aspect: The aspect to add.
        '''
        return typing.cast(None, jsii.invoke(self, "add", [aspect]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="all")
    def all(self) -> typing.List["IAspect"]:
        '''The list of aspects which were directly applied on this scope.'''
        return typing.cast(typing.List["IAspect"], jsii.get(self, "all"))


@jsii.enum(jsii_type="cdktg.Authentication")
class Authentication(enum.Enum):
    NONE = "NONE"
    CREDENTIALS = "CREDENTIALS"
    SESSION_ID = "SESSION_ID"
    TOKEN = "TOKEN"
    CLIENT_CERTIFICATE = "CLIENT_CERTIFICATE"
    TWO_FACTOR = "TWO_FACTOR"
    EXTERNALIZED = "EXTERNALIZED"


class Author(metaclass=jsii.JSIIMeta, jsii_type="cdktg.Author"):
    def __init__(
        self,
        *,
        name: builtins.str,
        homepage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param homepage: 
        '''
        props = AuthorProps(name=name, homepage=homepage)

        jsii.create(self.__class__, self, [props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="homepage")
    def homepage(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "homepage"))


@jsii.data_type(
    jsii_type="cdktg.AuthorProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "homepage": "homepage"},
)
class AuthorProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        homepage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param homepage: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if homepage is not None:
            self._values["homepage"] = homepage

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def homepage(self) -> typing.Optional[builtins.str]:
        result = self._values.get("homepage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuthorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdktg.Authorization")
class Authorization(enum.Enum):
    NONE = "NONE"
    TECHNICAL_USER = "TECHNICAL_USER"
    ENDUSER_IDENTITY_PROPAGATION = "ENDUSER_IDENTITY_PROPAGATION"


@jsii.enum(jsii_type="cdktg.Availability")
class Availability(enum.Enum):
    ARCHIVE = "ARCHIVE"
    OPERATIONAL = "OPERATIONAL"
    IMPORTANT = "IMPORTANT"
    CRITICAL = "CRITICAL"
    MISSION_CRITICAL = "MISSION_CRITICAL"


@jsii.enum(jsii_type="cdktg.BusinessCriticality")
class BusinessCriticality(enum.Enum):
    ARCHIVE = "ARCHIVE"
    OPERATIONAL = "OPERATIONAL"
    IMPORTANT = "IMPORTANT"
    CRITICAL = "CRITICAL"
    MISSION_CRITICAL = "MISSION_CRITICAL"


class CIATriad(metaclass=jsii.JSIIMeta, jsii_type="cdktg.CIATriad"):
    def __init__(
        self,
        *,
        availability: Availability,
        confidentiality: "Confidentiality",
        integrity: "Integrity",
        justification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability: 
        :param confidentiality: 
        :param integrity: 
        :param justification: 
        '''
        props = CIATriadProps(
            availability=availability,
            confidentiality=confidentiality,
            integrity=integrity,
            justification=justification,
        )

        jsii.create(self.__class__, self, [props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="availability")
    def availability(self) -> Availability:
        return typing.cast(Availability, jsii.get(self, "availability"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="confidentiality")
    def confidentiality(self) -> "Confidentiality":
        return typing.cast("Confidentiality", jsii.get(self, "confidentiality"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="integrity")
    def integrity(self) -> "Integrity":
        return typing.cast("Integrity", jsii.get(self, "integrity"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="justification")
    def justification(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "justification"))


@jsii.data_type(
    jsii_type="cdktg.CIATriadProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability": "availability",
        "confidentiality": "confidentiality",
        "integrity": "integrity",
        "justification": "justification",
    },
)
class CIATriadProps:
    def __init__(
        self,
        *,
        availability: Availability,
        confidentiality: "Confidentiality",
        integrity: "Integrity",
        justification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability: 
        :param confidentiality: 
        :param integrity: 
        :param justification: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "availability": availability,
            "confidentiality": confidentiality,
            "integrity": integrity,
        }
        if justification is not None:
            self._values["justification"] = justification

    @builtins.property
    def availability(self) -> Availability:
        result = self._values.get("availability")
        assert result is not None, "Required property 'availability' is missing"
        return typing.cast(Availability, result)

    @builtins.property
    def confidentiality(self) -> "Confidentiality":
        result = self._values.get("confidentiality")
        assert result is not None, "Required property 'confidentiality' is missing"
        return typing.cast("Confidentiality", result)

    @builtins.property
    def integrity(self) -> "Integrity":
        result = self._values.get("integrity")
        assert result is not None, "Required property 'integrity' is missing"
        return typing.cast("Integrity", result)

    @builtins.property
    def justification(self) -> typing.Optional[builtins.str]:
        result = self._values.get("justification")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CIATriadProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Communication(metaclass=jsii.JSIIMeta, jsii_type="cdktg.Communication"):
    def __init__(
        self,
        id: builtins.str,
        *,
        target: "TechnicalAsset",
        authentication: Authentication,
        authorization: Authorization,
        description: builtins.str,
        ip_filtered: builtins.bool,
        protocol: "Protocol",
        readonly: builtins.bool,
        usage: "Usage",
        vpn: builtins.bool,
    ) -> None:
        '''
        :param id: -
        :param target: 
        :param authentication: 
        :param authorization: 
        :param description: 
        :param ip_filtered: 
        :param protocol: 
        :param readonly: 
        :param usage: 
        :param vpn: 
        '''
        props = CommunicationProps(
            target=target,
            authentication=authentication,
            authorization=authorization,
            description=description,
            ip_filtered=ip_filtered,
            protocol=protocol,
            readonly=readonly,
            usage=usage,
            vpn=vpn,
        )

        jsii.create(self.__class__, self, [id, props])

    @jsii.member(jsii_name="receive")
    def receive(self, *assets: "DataAsset") -> None:
        '''
        :param assets: -
        '''
        return typing.cast(None, jsii.invoke(self, "receive", [*assets]))

    @jsii.member(jsii_name="send")
    def send(self, *assets: "DataAsset") -> None:
        '''
        :param assets: -
        '''
        return typing.cast(None, jsii.invoke(self, "send", [*assets]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="authentication")
    def authentication(self) -> Authentication:
        return typing.cast(Authentication, jsii.get(self, "authentication"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="authorization")
    def authorization(self) -> Authorization:
        return typing.cast(Authorization, jsii.get(self, "authorization"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ipFiltered")
    def ip_filtered(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "ipFiltered"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> "Protocol":
        return typing.cast("Protocol", jsii.get(self, "protocol"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="readonly")
    def readonly(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "readonly"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="target")
    def target(self) -> "TechnicalAsset":
        return typing.cast("TechnicalAsset", jsii.get(self, "target"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="usage")
    def usage(self) -> "Usage":
        return typing.cast("Usage", jsii.get(self, "usage"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpn")
    def vpn(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "vpn"))


@jsii.data_type(
    jsii_type="cdktg.CommunicationOptions",
    jsii_struct_bases=[],
    name_mapping={
        "authentication": "authentication",
        "authorization": "authorization",
        "description": "description",
        "ip_filtered": "ipFiltered",
        "protocol": "protocol",
        "readonly": "readonly",
        "usage": "usage",
        "vpn": "vpn",
    },
)
class CommunicationOptions:
    def __init__(
        self,
        *,
        authentication: Authentication,
        authorization: Authorization,
        description: builtins.str,
        ip_filtered: builtins.bool,
        protocol: "Protocol",
        readonly: builtins.bool,
        usage: "Usage",
        vpn: builtins.bool,
    ) -> None:
        '''
        :param authentication: 
        :param authorization: 
        :param description: 
        :param ip_filtered: 
        :param protocol: 
        :param readonly: 
        :param usage: 
        :param vpn: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "authentication": authentication,
            "authorization": authorization,
            "description": description,
            "ip_filtered": ip_filtered,
            "protocol": protocol,
            "readonly": readonly,
            "usage": usage,
            "vpn": vpn,
        }

    @builtins.property
    def authentication(self) -> Authentication:
        result = self._values.get("authentication")
        assert result is not None, "Required property 'authentication' is missing"
        return typing.cast(Authentication, result)

    @builtins.property
    def authorization(self) -> Authorization:
        result = self._values.get("authorization")
        assert result is not None, "Required property 'authorization' is missing"
        return typing.cast(Authorization, result)

    @builtins.property
    def description(self) -> builtins.str:
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_filtered(self) -> builtins.bool:
        result = self._values.get("ip_filtered")
        assert result is not None, "Required property 'ip_filtered' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def protocol(self) -> "Protocol":
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast("Protocol", result)

    @builtins.property
    def readonly(self) -> builtins.bool:
        result = self._values.get("readonly")
        assert result is not None, "Required property 'readonly' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def usage(self) -> "Usage":
        result = self._values.get("usage")
        assert result is not None, "Required property 'usage' is missing"
        return typing.cast("Usage", result)

    @builtins.property
    def vpn(self) -> builtins.bool:
        result = self._values.get("vpn")
        assert result is not None, "Required property 'vpn' is missing"
        return typing.cast(builtins.bool, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommunicationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktg.CommunicationProps",
    jsii_struct_bases=[CommunicationOptions],
    name_mapping={
        "authentication": "authentication",
        "authorization": "authorization",
        "description": "description",
        "ip_filtered": "ipFiltered",
        "protocol": "protocol",
        "readonly": "readonly",
        "usage": "usage",
        "vpn": "vpn",
        "target": "target",
    },
)
class CommunicationProps(CommunicationOptions):
    def __init__(
        self,
        *,
        authentication: Authentication,
        authorization: Authorization,
        description: builtins.str,
        ip_filtered: builtins.bool,
        protocol: "Protocol",
        readonly: builtins.bool,
        usage: "Usage",
        vpn: builtins.bool,
        target: "TechnicalAsset",
    ) -> None:
        '''
        :param authentication: 
        :param authorization: 
        :param description: 
        :param ip_filtered: 
        :param protocol: 
        :param readonly: 
        :param usage: 
        :param vpn: 
        :param target: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "authentication": authentication,
            "authorization": authorization,
            "description": description,
            "ip_filtered": ip_filtered,
            "protocol": protocol,
            "readonly": readonly,
            "usage": usage,
            "vpn": vpn,
            "target": target,
        }

    @builtins.property
    def authentication(self) -> Authentication:
        result = self._values.get("authentication")
        assert result is not None, "Required property 'authentication' is missing"
        return typing.cast(Authentication, result)

    @builtins.property
    def authorization(self) -> Authorization:
        result = self._values.get("authorization")
        assert result is not None, "Required property 'authorization' is missing"
        return typing.cast(Authorization, result)

    @builtins.property
    def description(self) -> builtins.str:
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_filtered(self) -> builtins.bool:
        result = self._values.get("ip_filtered")
        assert result is not None, "Required property 'ip_filtered' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def protocol(self) -> "Protocol":
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast("Protocol", result)

    @builtins.property
    def readonly(self) -> builtins.bool:
        result = self._values.get("readonly")
        assert result is not None, "Required property 'readonly' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def usage(self) -> "Usage":
        result = self._values.get("usage")
        assert result is not None, "Required property 'usage' is missing"
        return typing.cast("Usage", result)

    @builtins.property
    def vpn(self) -> builtins.bool:
        result = self._values.get("vpn")
        assert result is not None, "Required property 'vpn' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def target(self) -> "TechnicalAsset":
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast("TechnicalAsset", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommunicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdktg.Confidentiality")
class Confidentiality(enum.Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    RESTRICTED = "RESTRICTED"
    CONFIDENTIAL = "CONFIDENTIAL"
    STRICTLY_CONFIDENTIAL = "STRICTLY_CONFIDENTIAL"


@jsii.enum(jsii_type="cdktg.DataFormat")
class DataFormat(enum.Enum):
    JSON = "JSON"
    XML = "XML"
    SERIALIZATION = "SERIALIZATION"
    FILE = "FILE"
    CSV = "CSV"


@jsii.enum(jsii_type="cdktg.Encryption")
class Encryption(enum.Enum):
    NONE = "NONE"
    TRANSPARENT = "TRANSPARENT"
    SYMMETRIC_SHARED_KEY = "SYMMETRIC_SHARED_KEY"
    ASYMMETRIC_SHARED_KEY = "ASYMMETRIC_SHARED_KEY"
    ENDUSER_INDIVIDUAL_KEY = "ENDUSER_INDIVIDUAL_KEY"


@jsii.interface(jsii_type="cdktg.IAspect")
class IAspect(typing_extensions.Protocol):
    '''Represents an Aspect.'''

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        ...


class _IAspectProxy:
    '''Represents an Aspect.'''

    __jsii_type__: typing.ClassVar[str] = "cdktg.IAspect"

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAspect).__jsii_proxy_class__ = lambda : _IAspectProxy


@jsii.interface(jsii_type="cdktg.IManifest")
class IManifest(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="models")
    def models(self) -> typing.Mapping[builtins.str, "ModelManifest"]:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        ...


class _IManifestProxy:
    __jsii_type__: typing.ClassVar[str] = "cdktg.IManifest"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="models")
    def models(self) -> typing.Mapping[builtins.str, "ModelManifest"]:
        return typing.cast(typing.Mapping[builtins.str, "ModelManifest"], jsii.get(self, "models"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IManifest).__jsii_proxy_class__ = lambda : _IManifestProxy


@jsii.interface(jsii_type="cdktg.IModelSynthesizer")
class IModelSynthesizer(typing_extensions.Protocol):
    @jsii.member(jsii_name="synthesize")
    def synthesize(self, session: "ISynthesisSession") -> None:
        '''Synthesize the associated model to the session.

        :param session: -
        '''
        ...


class _IModelSynthesizerProxy:
    __jsii_type__: typing.ClassVar[str] = "cdktg.IModelSynthesizer"

    @jsii.member(jsii_name="synthesize")
    def synthesize(self, session: "ISynthesisSession") -> None:
        '''Synthesize the associated model to the session.

        :param session: -
        '''
        return typing.cast(None, jsii.invoke(self, "synthesize", [session]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IModelSynthesizer).__jsii_proxy_class__ = lambda : _IModelSynthesizerProxy


@jsii.interface(jsii_type="cdktg.ISynthesisSession")
class ISynthesisSession(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> "Manifest":
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        '''The output directory for this synthesis session.'''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipValidation")
    def skip_validation(self) -> typing.Optional[builtins.bool]:
        ...


class _ISynthesisSessionProxy:
    __jsii_type__: typing.ClassVar[str] = "cdktg.ISynthesisSession"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> "Manifest":
        return typing.cast("Manifest", jsii.get(self, "manifest"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        '''The output directory for this synthesis session.'''
        return typing.cast(builtins.str, jsii.get(self, "outdir"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipValidation")
    def skip_validation(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "skipValidation"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISynthesisSession).__jsii_proxy_class__ = lambda : _ISynthesisSessionProxy


@jsii.enum(jsii_type="cdktg.Integrity")
class Integrity(enum.Enum):
    ARCHIVE = "ARCHIVE"
    OPERATIONAL = "OPERATIONAL"
    IMPORTANT = "IMPORTANT"
    CRITICAL = "CRITICAL"
    MISSION_CRITICAL = "MISSION_CRITICAL"


@jsii.enum(jsii_type="cdktg.Machine")
class Machine(enum.Enum):
    PHYSICAL = "PHYSICAL"
    VIRTUAL = "VIRTUAL"
    CONTAINER = "CONTAINER"
    SERVERLESS = "SERVERLESS"


@jsii.implements(IManifest)
class Manifest(metaclass=jsii.JSIIMeta, jsii_type="cdktg.Manifest"):
    def __init__(self, version: builtins.str, outdir: builtins.str) -> None:
        '''
        :param version: -
        :param outdir: -
        '''
        jsii.create(self.__class__, self, [version, outdir])

    @jsii.member(jsii_name="fromPath") # type: ignore[misc]
    @builtins.classmethod
    def from_path(cls, dir: builtins.str) -> "Manifest":
        '''
        :param dir: -
        '''
        return typing.cast("Manifest", jsii.sinvoke(cls, "fromPath", [dir]))

    @jsii.member(jsii_name="buildManifest")
    def build_manifest(self) -> IManifest:
        return typing.cast(IManifest, jsii.invoke(self, "buildManifest", []))

    @jsii.member(jsii_name="forModel")
    def for_model(self, model: "Model") -> "ModelManifest":
        '''
        :param model: -
        '''
        return typing.cast("ModelManifest", jsii.invoke(self, "forModel", [model]))

    @jsii.member(jsii_name="writeToFile")
    def write_to_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "writeToFile", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="fileName")
    def FILE_NAME(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "fileName"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="modelsFolder")
    def MODELS_FOLDER(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "modelsFolder"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="models")
    def models(self) -> typing.Mapping[builtins.str, "ModelManifest"]:
        return typing.cast(typing.Mapping[builtins.str, "ModelManifest"], jsii.get(self, "models"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outdir"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))


class Model(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdktg.Model"):
    def __init__(
        self,
        project: constructs.Construct,
        id: builtins.str,
        *,
        author: Author,
        business_criticality: BusinessCriticality,
        version: builtins.str,
        abuse_cases: typing.Optional[typing.Sequence[AbuseCase]] = None,
        date: typing.Optional[builtins.str] = None,
        management_summary: typing.Optional[builtins.str] = None,
        questions: typing.Optional[typing.Sequence["Question"]] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param id: -
        :param author: Author of the model.
        :param business_criticality: Business criticality of the target.
        :param version: Version of the Threagile toolkit.
        :param abuse_cases: Custom abuse cases for the report.
        :param date: Date of the model.
        :param management_summary: Individual management summary for the report.
        :param questions: Custom questions for the report.
        :param title: Title of the model.
        '''
        props = ModelProps(
            author=author,
            business_criticality=business_criticality,
            version=version,
            abuse_cases=abuse_cases,
            date=date,
            management_summary=management_summary,
            questions=questions,
            title=title,
        )

        jsii.create(self.__class__, self, [project, id, props])

    @jsii.member(jsii_name="isModel") # type: ignore[misc]
    @builtins.classmethod
    def is_model(cls, x: typing.Any) -> builtins.bool:
        '''
        :param x: -
        '''
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isModel", [x]))

    @jsii.member(jsii_name="of") # type: ignore[misc]
    @builtins.classmethod
    def of(cls, construct: constructs.IConstruct) -> "Model":
        '''
        :param construct: -
        '''
        return typing.cast("Model", jsii.sinvoke(cls, "of", [construct]))

    @jsii.member(jsii_name="addAbuseCases")
    def add_abuse_cases(self, *cases: AbuseCase) -> None:
        '''
        :param cases: -
        '''
        return typing.cast(None, jsii.invoke(self, "addAbuseCases", [*cases]))

    @jsii.member(jsii_name="addOverride")
    def add_override(self, path: builtins.str, value: typing.Any) -> None:
        '''
        :param path: -
        :param value: -
        '''
        return typing.cast(None, jsii.invoke(self, "addOverride", [path, value]))

    @jsii.member(jsii_name="addQuestion")
    def add_question(
        self,
        text: builtins.str,
        answer: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param text: -
        :param answer: -
        '''
        return typing.cast(None, jsii.invoke(self, "addQuestion", [text, answer]))

    @jsii.member(jsii_name="addTag")
    def add_tag(self, tag: builtins.str) -> None:
        '''
        :param tag: -
        '''
        return typing.cast(None, jsii.invoke(self, "addTag", [tag]))

    @jsii.member(jsii_name="addTags")
    def add_tags(self, *tags: builtins.str) -> None:
        '''
        :param tags: -
        '''
        return typing.cast(None, jsii.invoke(self, "addTags", [*tags]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="author")
    def author(self) -> Author:
        return typing.cast(Author, jsii.get(self, "author"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="businessCriticality")
    def business_criticality(self) -> BusinessCriticality:
        return typing.cast(BusinessCriticality, jsii.get(self, "businessCriticality"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="date")
    def date(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "date"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="managementSummary")
    def management_summary(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managementSummary"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="synthesizer")
    def synthesizer(self) -> IModelSynthesizer:
        return typing.cast(IModelSynthesizer, jsii.get(self, "synthesizer"))

    @synthesizer.setter
    def synthesizer(self, value: IModelSynthesizer) -> None:
        jsii.set(self, "synthesizer", value)


@jsii.data_type(
    jsii_type="cdktg.ModelAnnotation",
    jsii_struct_bases=[],
    name_mapping={
        "construct_path": "constructPath",
        "level": "level",
        "message": "message",
        "stacktrace": "stacktrace",
    },
)
class ModelAnnotation:
    def __init__(
        self,
        *,
        construct_path: builtins.str,
        level: AnnotationMetadataEntryType,
        message: builtins.str,
        stacktrace: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param construct_path: 
        :param level: 
        :param message: 
        :param stacktrace: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "construct_path": construct_path,
            "level": level,
            "message": message,
        }
        if stacktrace is not None:
            self._values["stacktrace"] = stacktrace

    @builtins.property
    def construct_path(self) -> builtins.str:
        result = self._values.get("construct_path")
        assert result is not None, "Required property 'construct_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def level(self) -> AnnotationMetadataEntryType:
        result = self._values.get("level")
        assert result is not None, "Required property 'level' is missing"
        return typing.cast(AnnotationMetadataEntryType, result)

    @builtins.property
    def message(self) -> builtins.str:
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stacktrace(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("stacktrace")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelAnnotation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktg.ModelManifest",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "construct_path": "constructPath",
        "name": "name",
        "sanitized_name": "sanitizedName",
        "synthesized_model_path": "synthesizedModelPath",
        "working_directory": "workingDirectory",
    },
)
class ModelManifest:
    def __init__(
        self,
        *,
        annotations: typing.Sequence[ModelAnnotation],
        construct_path: builtins.str,
        name: builtins.str,
        sanitized_name: builtins.str,
        synthesized_model_path: builtins.str,
        working_directory: builtins.str,
    ) -> None:
        '''
        :param annotations: 
        :param construct_path: 
        :param name: 
        :param sanitized_name: 
        :param synthesized_model_path: 
        :param working_directory: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "annotations": annotations,
            "construct_path": construct_path,
            "name": name,
            "sanitized_name": sanitized_name,
            "synthesized_model_path": synthesized_model_path,
            "working_directory": working_directory,
        }

    @builtins.property
    def annotations(self) -> typing.List[ModelAnnotation]:
        result = self._values.get("annotations")
        assert result is not None, "Required property 'annotations' is missing"
        return typing.cast(typing.List[ModelAnnotation], result)

    @builtins.property
    def construct_path(self) -> builtins.str:
        result = self._values.get("construct_path")
        assert result is not None, "Required property 'construct_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sanitized_name(self) -> builtins.str:
        result = self._values.get("sanitized_name")
        assert result is not None, "Required property 'sanitized_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def synthesized_model_path(self) -> builtins.str:
        result = self._values.get("synthesized_model_path")
        assert result is not None, "Required property 'synthesized_model_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def working_directory(self) -> builtins.str:
        result = self._values.get("working_directory")
        assert result is not None, "Required property 'working_directory' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelManifest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktg.ModelProps",
    jsii_struct_bases=[],
    name_mapping={
        "author": "author",
        "business_criticality": "businessCriticality",
        "version": "version",
        "abuse_cases": "abuseCases",
        "date": "date",
        "management_summary": "managementSummary",
        "questions": "questions",
        "title": "title",
    },
)
class ModelProps:
    def __init__(
        self,
        *,
        author: Author,
        business_criticality: BusinessCriticality,
        version: builtins.str,
        abuse_cases: typing.Optional[typing.Sequence[AbuseCase]] = None,
        date: typing.Optional[builtins.str] = None,
        management_summary: typing.Optional[builtins.str] = None,
        questions: typing.Optional[typing.Sequence["Question"]] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param author: Author of the model.
        :param business_criticality: Business criticality of the target.
        :param version: Version of the Threagile toolkit.
        :param abuse_cases: Custom abuse cases for the report.
        :param date: Date of the model.
        :param management_summary: Individual management summary for the report.
        :param questions: Custom questions for the report.
        :param title: Title of the model.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "author": author,
            "business_criticality": business_criticality,
            "version": version,
        }
        if abuse_cases is not None:
            self._values["abuse_cases"] = abuse_cases
        if date is not None:
            self._values["date"] = date
        if management_summary is not None:
            self._values["management_summary"] = management_summary
        if questions is not None:
            self._values["questions"] = questions
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def author(self) -> Author:
        '''Author of the model.'''
        result = self._values.get("author")
        assert result is not None, "Required property 'author' is missing"
        return typing.cast(Author, result)

    @builtins.property
    def business_criticality(self) -> BusinessCriticality:
        '''Business criticality of the target.'''
        result = self._values.get("business_criticality")
        assert result is not None, "Required property 'business_criticality' is missing"
        return typing.cast(BusinessCriticality, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Version of the Threagile toolkit.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def abuse_cases(self) -> typing.Optional[typing.List[AbuseCase]]:
        '''Custom abuse cases for the report.'''
        result = self._values.get("abuse_cases")
        return typing.cast(typing.Optional[typing.List[AbuseCase]], result)

    @builtins.property
    def date(self) -> typing.Optional[builtins.str]:
        '''Date of the model.'''
        result = self._values.get("date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def management_summary(self) -> typing.Optional[builtins.str]:
        '''Individual management summary for the report.'''
        result = self._values.get("management_summary")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def questions(self) -> typing.Optional[typing.List["Question"]]:
        '''Custom questions for the report.'''
        result = self._values.get("questions")
        return typing.cast(typing.Optional[typing.List["Question"]], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title of the model.'''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IModelSynthesizer)
class ModelSynthesizer(metaclass=jsii.JSIIMeta, jsii_type="cdktg.ModelSynthesizer"):
    def __init__(
        self,
        model: Model,
        continue_on_error_annotations: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param model: -
        :param continue_on_error_annotations: -
        '''
        jsii.create(self.__class__, self, [model, continue_on_error_annotations])

    @jsii.member(jsii_name="synthesize")
    def synthesize(self, session: ISynthesisSession) -> None:
        '''Synthesize the associated model to the session.

        :param session: -
        '''
        return typing.cast(None, jsii.invoke(self, "synthesize", [session]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="model")
    def _model(self) -> Model:
        return typing.cast(Model, jsii.get(self, "model"))

    @_model.setter
    def _model(self, value: Model) -> None:
        jsii.set(self, "model", value)


@jsii.data_type(
    jsii_type="cdktg.OutOfScopeProps",
    jsii_struct_bases=[],
    name_mapping={"out_of_scope": "outOfScope", "justification": "justification"},
)
class OutOfScopeProps:
    def __init__(
        self,
        *,
        out_of_scope: builtins.bool,
        justification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param out_of_scope: 
        :param justification: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "out_of_scope": out_of_scope,
        }
        if justification is not None:
            self._values["justification"] = justification

    @builtins.property
    def out_of_scope(self) -> builtins.bool:
        result = self._values.get("out_of_scope")
        assert result is not None, "Required property 'out_of_scope' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def justification(self) -> typing.Optional[builtins.str]:
        result = self._values.get("justification")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OutOfScopeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Project(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdktg.Project"):
    def __init__(
        self,
        *,
        outdir: typing.Optional[builtins.str] = None,
        skip_validation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param outdir: The directory to output the threadgile model. Default: - .
        :param skip_validation: Whether to skip the validation during synthesis of the project. Default: - false
        '''
        props = ProjectProps(outdir=outdir, skip_validation=skip_validation)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="synth")
    def synth(self) -> None:
        '''Synthesizes the model to the output directory.'''
        return typing.cast(None, jsii.invoke(self, "synth", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> Manifest:
        return typing.cast(Manifest, jsii.get(self, "manifest"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        '''The output directory into which models will be synthesized.'''
        return typing.cast(builtins.str, jsii.get(self, "outdir"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipValidation")
    def skip_validation(self) -> typing.Optional[builtins.bool]:
        '''Whether to skip the validation during synthesis of the app.'''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "skipValidation"))


@jsii.data_type(
    jsii_type="cdktg.ProjectProps",
    jsii_struct_bases=[],
    name_mapping={"outdir": "outdir", "skip_validation": "skipValidation"},
)
class ProjectProps:
    def __init__(
        self,
        *,
        outdir: typing.Optional[builtins.str] = None,
        skip_validation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param outdir: The directory to output the threadgile model. Default: - .
        :param skip_validation: Whether to skip the validation during synthesis of the project. Default: - false
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if outdir is not None:
            self._values["outdir"] = outdir
        if skip_validation is not None:
            self._values["skip_validation"] = skip_validation

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''The directory to output the threadgile model.

        :default: - .
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_validation(self) -> typing.Optional[builtins.bool]:
        '''Whether to skip the validation during synthesis of the project.

        :default: - false
        '''
        result = self._values.get("skip_validation")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdktg.Protocol")
class Protocol(enum.Enum):
    UNKNOEN = "UNKNOEN"
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    WS = "WS"
    WSS = "WSS"
    REVERSE_PROXY_WEB_PROTOCOL = "REVERSE_PROXY_WEB_PROTOCOL"
    REVERSE_PROXY_WEB_PROTOCOL_ENCRYPTED = "REVERSE_PROXY_WEB_PROTOCOL_ENCRYPTED"
    MQTT = "MQTT"
    JDBC = "JDBC"
    JDBC_ENCRYPTED = "JDBC_ENCRYPTED"
    ODBC = "ODBC"
    ODBC_ENCRYPTED = "ODBC_ENCRYPTED"
    SQL_ACCESS_PROTOCOL = "SQL_ACCESS_PROTOCOL"
    SQL_ACCESS_PROTOCOL_ENCRYPTED = "SQL_ACCESS_PROTOCOL_ENCRYPTED"
    NOSQL_ACCESS_PROTOCOL = "NOSQL_ACCESS_PROTOCOL"
    NOSQL_ACCESS_PROTOCOL_ENCRYPTED = "NOSQL_ACCESS_PROTOCOL_ENCRYPTED"
    BINARY = "BINARY"
    BINARY_ENCRYPTED = "BINARY_ENCRYPTED"
    TEXT = "TEXT"
    TEXT_ENCRYPTED = "TEXT_ENCRYPTED"
    SSH = "SSH"
    SSH_TUNNEL = "SSH_TUNNEL"
    SMTP = "SMTP"
    SMTP_ENCRYPTED = "SMTP_ENCRYPTED"
    POP3 = "POP3"
    POP3_ENCRYPTED = "POP3_ENCRYPTED"
    IMAP = "IMAP"
    IMAP_ENCRYPTED = "IMAP_ENCRYPTED"
    FTP = "FTP"
    FTPS = "FTPS"
    SFTP = "SFTP"
    SCP = "SCP"
    LDAP = "LDAP"
    LDAPS = "LDAPS"
    JMS = "JMS"
    NFS = "NFS"
    SMB = "SMB"
    SMB_ENCRYPTED = "SMB_ENCRYPTED"
    LOCAL_FILE_ACCESS = "LOCAL_FILE_ACCESS"
    NRPE = "NRPE"
    XMPP = "XMPP"
    IIOP = "IIOP"
    IIOP_ENCRYPTED = "IIOP_ENCRYPTED"
    JRMP = "JRMP"
    JRMP_ENCRYPTED = "JRMP_ENCRYPTED"
    IN_PROCESS_LIBRARY_CALL = "IN_PROCESS_LIBRARY_CALL"
    CONTAINER_SPAWNING = "CONTAINER_SPAWNING"


@jsii.enum(jsii_type="cdktg.Quantity")
class Quantity(enum.Enum):
    VERY_FEW = "VERY_FEW"
    FEW = "FEW"
    MANY = "MANY"
    VERY_MANY = "VERY_MANY"


@jsii.data_type(
    jsii_type="cdktg.Question",
    jsii_struct_bases=[],
    name_mapping={"text": "text", "answer": "answer"},
)
class Question:
    def __init__(
        self,
        *,
        text: builtins.str,
        answer: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param text: 
        :param answer: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "text": text,
        }
        if answer is not None:
            self._values["answer"] = answer

    @builtins.property
    def text(self) -> builtins.str:
        result = self._values.get("text")
        assert result is not None, "Required property 'text' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def answer(self) -> typing.Optional[builtins.str]:
        result = self._values.get("answer")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Question(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Resource(
    constructs.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdktg.Resource",
):
    def __init__(
        self,
        model: constructs.Construct,
        id: builtins.str,
        *,
        description: builtins.str,
    ) -> None:
        '''
        :param model: -
        :param id: -
        :param description: 
        '''
        props = ResourceProps(description=description)

        jsii.create(self.__class__, self, [model, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))


class _ResourceProxy(Resource):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Resource).__jsii_proxy_class__ = lambda : _ResourceProxy


@jsii.data_type(
    jsii_type="cdktg.ResourceProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description"},
)
class ResourceProps:
    def __init__(self, *, description: builtins.str) -> None:
        '''
        :param description: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "description": description,
        }

    @builtins.property
    def description(self) -> builtins.str:
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Scope(metaclass=jsii.JSIIAbstractClass, jsii_type="cdktg.Scope"):
    def __init__(self, justification: typing.Optional[builtins.str] = None) -> None:
        '''
        :param justification: -
        '''
        jsii.create(self.__class__, self, [justification])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="isInScope")
    @abc.abstractmethod
    def _is_in_scope(self) -> builtins.bool:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="justification")
    def justification(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "justification"))


class _ScopeProxy(Scope):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="isInScope")
    def _is_in_scope(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "isInScope"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Scope).__jsii_proxy_class__ = lambda : _ScopeProxy


class SharedRuntime(Resource, metaclass=jsii.JSIIMeta, jsii_type="cdktg.SharedRuntime"):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param tags: 
        :param description: 
        '''
        props = SharedRuntimeProps(tags=tags, description=description)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="run")
    def run(self, *assets: "TechnicalAsset") -> None:
        '''
        :param assets: -
        '''
        return typing.cast(None, jsii.invoke(self, "run", [*assets]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tags"))


@jsii.data_type(
    jsii_type="cdktg.SharedRuntimeProps",
    jsii_struct_bases=[ResourceProps],
    name_mapping={"description": "description", "tags": "tags"},
)
class SharedRuntimeProps(ResourceProps):
    def __init__(
        self,
        *,
        description: builtins.str,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param description: 
        :param tags: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "description": description,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> builtins.str:
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SharedRuntimeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdktg.Size")
class Size(enum.Enum):
    SYSTEM = "SYSTEM"
    SERVICE = "SERVICE"
    APPLICATION = "APPLICATION"
    COMPONENT = "COMPONENT"


class TechnicalAsset(
    Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktg.TechnicalAsset",
):
    def __init__(
        self,
        scope_: constructs.Construct,
        id: builtins.str,
        *,
        cia_triad: CIATriad,
        encryption: Encryption,
        human_use: builtins.bool,
        internet: builtins.bool,
        machine: Machine,
        multi_tenant: builtins.bool,
        owner: builtins.str,
        redundant: builtins.bool,
        size: Size,
        technology: "Technology",
        type: "TechnicalAssetType",
        usage: "Usage",
        scope: typing.Optional[Scope] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        trust_boundary: typing.Optional["TrustBoundary"] = None,
        description: builtins.str,
    ) -> None:
        '''
        :param scope_: -
        :param id: -
        :param cia_triad: 
        :param encryption: 
        :param human_use: 
        :param internet: 
        :param machine: 
        :param multi_tenant: 
        :param owner: 
        :param redundant: 
        :param size: 
        :param technology: 
        :param type: 
        :param usage: 
        :param scope: 
        :param tags: 
        :param trust_boundary: 
        :param description: 
        '''
        props = TechnicalAssetProps(
            cia_triad=cia_triad,
            encryption=encryption,
            human_use=human_use,
            internet=internet,
            machine=machine,
            multi_tenant=multi_tenant,
            owner=owner,
            redundant=redundant,
            size=size,
            technology=technology,
            type=type,
            usage=usage,
            scope=scope,
            tags=tags,
            trust_boundary=trust_boundary,
            description=description,
        )

        jsii.create(self.__class__, self, [scope_, id, props])

    @jsii.member(jsii_name="communicateWith")
    def communicate_with(
        self,
        id: builtins.str,
        target: "TechnicalAsset",
        *,
        authentication: Authentication,
        authorization: Authorization,
        description: builtins.str,
        ip_filtered: builtins.bool,
        protocol: Protocol,
        readonly: builtins.bool,
        usage: "Usage",
        vpn: builtins.bool,
    ) -> Communication:
        '''
        :param id: -
        :param target: -
        :param authentication: 
        :param authorization: 
        :param description: 
        :param ip_filtered: 
        :param protocol: 
        :param readonly: 
        :param usage: 
        :param vpn: 
        '''
        options = CommunicationOptions(
            authentication=authentication,
            authorization=authorization,
            description=description,
            ip_filtered=ip_filtered,
            protocol=protocol,
            readonly=readonly,
            usage=usage,
            vpn=vpn,
        )

        return typing.cast(Communication, jsii.invoke(self, "communicateWith", [id, target, options]))

    @jsii.member(jsii_name="process")
    def process(self, *assets: "DataAsset") -> None:
        '''
        :param assets: -
        '''
        return typing.cast(None, jsii.invoke(self, "process", [*assets]))

    @jsii.member(jsii_name="store")
    def store(self, *assets: "DataAsset") -> None:
        '''
        :param assets: -
        '''
        return typing.cast(None, jsii.invoke(self, "store", [*assets]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ciaTriad")
    def cia_triad(self) -> CIATriad:
        return typing.cast(CIATriad, jsii.get(self, "ciaTriad"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="encryption")
    def encryption(self) -> Encryption:
        return typing.cast(Encryption, jsii.get(self, "encryption"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="humanUse")
    def human_use(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "humanUse"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internet")
    def internet(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "internet"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="machine")
    def machine(self) -> Machine:
        return typing.cast(Machine, jsii.get(self, "machine"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="multiTenant")
    def multi_tenant(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "multiTenant"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="redundant")
    def redundant(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "redundant"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="size")
    def size(self) -> Size:
        return typing.cast(Size, jsii.get(self, "size"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="technology")
    def technology(self) -> "Technology":
        return typing.cast("Technology", jsii.get(self, "technology"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> "TechnicalAssetType":
        return typing.cast("TechnicalAssetType", jsii.get(self, "type"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="usage")
    def usage(self) -> "Usage":
        return typing.cast("Usage", jsii.get(self, "usage"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scope")
    def scope(self) -> typing.Optional[Scope]:
        return typing.cast(typing.Optional[Scope], jsii.get(self, "scope"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tags"))


@jsii.data_type(
    jsii_type="cdktg.TechnicalAssetProps",
    jsii_struct_bases=[ResourceProps],
    name_mapping={
        "description": "description",
        "cia_triad": "ciaTriad",
        "encryption": "encryption",
        "human_use": "humanUse",
        "internet": "internet",
        "machine": "machine",
        "multi_tenant": "multiTenant",
        "owner": "owner",
        "redundant": "redundant",
        "size": "size",
        "technology": "technology",
        "type": "type",
        "usage": "usage",
        "scope": "scope",
        "tags": "tags",
        "trust_boundary": "trustBoundary",
    },
)
class TechnicalAssetProps(ResourceProps):
    def __init__(
        self,
        *,
        description: builtins.str,
        cia_triad: CIATriad,
        encryption: Encryption,
        human_use: builtins.bool,
        internet: builtins.bool,
        machine: Machine,
        multi_tenant: builtins.bool,
        owner: builtins.str,
        redundant: builtins.bool,
        size: Size,
        technology: "Technology",
        type: "TechnicalAssetType",
        usage: "Usage",
        scope: typing.Optional[Scope] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        trust_boundary: typing.Optional["TrustBoundary"] = None,
    ) -> None:
        '''
        :param description: 
        :param cia_triad: 
        :param encryption: 
        :param human_use: 
        :param internet: 
        :param machine: 
        :param multi_tenant: 
        :param owner: 
        :param redundant: 
        :param size: 
        :param technology: 
        :param type: 
        :param usage: 
        :param scope: 
        :param tags: 
        :param trust_boundary: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "description": description,
            "cia_triad": cia_triad,
            "encryption": encryption,
            "human_use": human_use,
            "internet": internet,
            "machine": machine,
            "multi_tenant": multi_tenant,
            "owner": owner,
            "redundant": redundant,
            "size": size,
            "technology": technology,
            "type": type,
            "usage": usage,
        }
        if scope is not None:
            self._values["scope"] = scope
        if tags is not None:
            self._values["tags"] = tags
        if trust_boundary is not None:
            self._values["trust_boundary"] = trust_boundary

    @builtins.property
    def description(self) -> builtins.str:
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cia_triad(self) -> CIATriad:
        result = self._values.get("cia_triad")
        assert result is not None, "Required property 'cia_triad' is missing"
        return typing.cast(CIATriad, result)

    @builtins.property
    def encryption(self) -> Encryption:
        result = self._values.get("encryption")
        assert result is not None, "Required property 'encryption' is missing"
        return typing.cast(Encryption, result)

    @builtins.property
    def human_use(self) -> builtins.bool:
        result = self._values.get("human_use")
        assert result is not None, "Required property 'human_use' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def internet(self) -> builtins.bool:
        result = self._values.get("internet")
        assert result is not None, "Required property 'internet' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def machine(self) -> Machine:
        result = self._values.get("machine")
        assert result is not None, "Required property 'machine' is missing"
        return typing.cast(Machine, result)

    @builtins.property
    def multi_tenant(self) -> builtins.bool:
        result = self._values.get("multi_tenant")
        assert result is not None, "Required property 'multi_tenant' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def owner(self) -> builtins.str:
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def redundant(self) -> builtins.bool:
        result = self._values.get("redundant")
        assert result is not None, "Required property 'redundant' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def size(self) -> Size:
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(Size, result)

    @builtins.property
    def technology(self) -> "Technology":
        result = self._values.get("technology")
        assert result is not None, "Required property 'technology' is missing"
        return typing.cast("Technology", result)

    @builtins.property
    def type(self) -> "TechnicalAssetType":
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("TechnicalAssetType", result)

    @builtins.property
    def usage(self) -> "Usage":
        result = self._values.get("usage")
        assert result is not None, "Required property 'usage' is missing"
        return typing.cast("Usage", result)

    @builtins.property
    def scope(self) -> typing.Optional[Scope]:
        result = self._values.get("scope")
        return typing.cast(typing.Optional[Scope], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def trust_boundary(self) -> typing.Optional["TrustBoundary"]:
        result = self._values.get("trust_boundary")
        return typing.cast(typing.Optional["TrustBoundary"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TechnicalAssetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdktg.TechnicalAssetType")
class TechnicalAssetType(enum.Enum):
    EXTERNAL_ENTITY = "EXTERNAL_ENTITY"
    PROCESS = "PROCESS"
    DATASTORE = "DATASTORE"


@jsii.enum(jsii_type="cdktg.Technology")
class Technology(enum.Enum):
    UNKNOWN = "UNKNOWN"
    CLIENT_SYSTEM = "CLIENT_SYSTEM"
    BROWSER = "BROWSER"
    DESKTOP = "DESKTOP"
    MOBILE_APP = "MOBILE_APP"
    DEVOPS_CLIENT = "DEVOPS_CLIENT"
    WEB_SERVER = "WEB_SERVER"
    WEB_APPLICATION = "WEB_APPLICATION"
    APPLICATION_SERVER = "APPLICATION_SERVER"
    DATABASE = "DATABASE"
    FILE_SERVER = "FILE_SERVER"
    LOCAL_FILE_SERVER = "LOCAL_FILE_SERVER"
    ERP = "ERP"
    CMS = "CMS"
    WEB_SERVICE_REST = "WEB_SERVICE_REST"
    WEB_SERVICE_SOAP = "WEB_SERVICE_SOAP"
    EJB = "EJB"
    SEARCH_INDEX = "SEARCH_INDEX"
    SEARCH_ENGINE = "SEARCH_ENGINE"
    SERVICE_REGISTRY = "SERVICE_REGISTRY"
    REVERSE_PROXY = "REVERSE_PROXY"
    LOAD_BALANCER = "LOAD_BALANCER"
    BUILD_PIPELINE = "BUILD_PIPELINE"
    SOURCECODE_REPOSITORY = "SOURCECODE_REPOSITORY"
    ARTIFACT_REGISTRY = "ARTIFACT_REGISTRY"
    CODE_INSPECTION_PLATFORM = "CODE_INSPECTION_PLATFORM"
    MONITORING = "MONITORING"
    LDAP_SERVER = "LDAP_SERVER"
    CONTAINER_PLATFORM = "CONTAINER_PLATFORM"
    BATCH_PROCESSING = "BATCH_PROCESSING"
    EVENT_LISTENER = "EVENT_LISTENER"
    IDENTITIY_PROVIDER = "IDENTITIY_PROVIDER"
    IDENTITY_STORE_LDAP = "IDENTITY_STORE_LDAP"
    IDENTITY_STORE_DATABASE = "IDENTITY_STORE_DATABASE"
    TOOL = "TOOL"
    CLI = "CLI"
    TASK = "TASK"
    FUNCTION = "FUNCTION"
    GATEWAY = "GATEWAY"
    IOT_DEVICE = "IOT_DEVICE"
    MESSAGE_QUEUE = "MESSAGE_QUEUE"
    STREAM_PROCESSING = "STREAM_PROCESSING"
    SERVICE_MESH = "SERVICE_MESH"
    DATA_LAKE = "DATA_LAKE"
    REPORT_ENGINE = "REPORT_ENGINE"
    AI = "AI"
    MAIL_SERVER = "MAIL_SERVER"
    VAULT = "VAULT"
    HASM = "HASM"
    WAF = "WAF"
    IDS = "IDS"
    IPS = "IPS"
    SCHEDULER = "SCHEDULER"
    MAINFRAME = "MAINFRAME"
    BLOCK_STORAGE = "BLOCK_STORAGE"
    LIBRARY = "LIBRARY"


class TrustBoundary(Resource, metaclass=jsii.JSIIMeta, jsii_type="cdktg.TrustBoundary"):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        type: "TrustBoundaryType",
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param type: 
        :param tags: 
        :param description: 
        '''
        props = TrustBoundaryProps(type=type, tags=tags, description=description)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addTechnicalAssets")
    def add_technical_assets(self, *assets: TechnicalAsset) -> None:
        '''
        :param assets: -
        '''
        return typing.cast(None, jsii.invoke(self, "addTechnicalAssets", [*assets]))

    @jsii.member(jsii_name="addTrustBoundary")
    def add_trust_boundary(self, boundary: "TrustBoundary") -> None:
        '''
        :param boundary: -
        '''
        return typing.cast(None, jsii.invoke(self, "addTrustBoundary", [boundary]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> "TrustBoundaryType":
        return typing.cast("TrustBoundaryType", jsii.get(self, "type"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tags"))


@jsii.data_type(
    jsii_type="cdktg.TrustBoundaryProps",
    jsii_struct_bases=[ResourceProps],
    name_mapping={"description": "description", "type": "type", "tags": "tags"},
)
class TrustBoundaryProps(ResourceProps):
    def __init__(
        self,
        *,
        description: builtins.str,
        type: "TrustBoundaryType",
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param description: 
        :param type: 
        :param tags: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "description": description,
            "type": type,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> builtins.str:
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> "TrustBoundaryType":
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("TrustBoundaryType", result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TrustBoundaryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdktg.TrustBoundaryType")
class TrustBoundaryType(enum.Enum):
    NETWORK_ON_PREM = "NETWORK_ON_PREM"
    NETWORK_DEDICATED_HOSTER = "NETWORK_DEDICATED_HOSTER"
    NETWORK_VIRTUAL_LAN = "NETWORK_VIRTUAL_LAN"
    NETWORK_CLOUD_PROVIDER = "NETWORK_CLOUD_PROVIDER"
    NETWORK_CLOUD_SECURITY_GROUP = "NETWORK_CLOUD_SECURITY_GROUP"
    NETWORK_POLICY_NAMESPACE_ISOLATION = "NETWORK_POLICY_NAMESPACE_ISOLATION"
    EXECUTION_ENVIRONMENT = "EXECUTION_ENVIRONMENT"


@jsii.enum(jsii_type="cdktg.Usage")
class Usage(enum.Enum):
    BUSINESS = "BUSINESS"
    DEVOPS = "DEVOPS"


class DataAsset(Resource, metaclass=jsii.JSIIMeta, jsii_type="cdktg.DataAsset"):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cia_triad: CIATriad,
        quantity: Quantity,
        usage: Usage,
        origin: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cia_triad: 
        :param quantity: 
        :param usage: 
        :param origin: 
        :param owner: 
        :param tags: 
        :param description: 
        '''
        props = DataAssetProps(
            cia_triad=cia_triad,
            quantity=quantity,
            usage=usage,
            origin=origin,
            owner=owner,
            tags=tags,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ciaTriad")
    def cia_triad(self) -> CIATriad:
        return typing.cast(CIATriad, jsii.get(self, "ciaTriad"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="quantity")
    def quantity(self) -> Quantity:
        return typing.cast(Quantity, jsii.get(self, "quantity"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="usage")
    def usage(self) -> Usage:
        return typing.cast(Usage, jsii.get(self, "usage"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="origin")
    def origin(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "origin"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="owner")
    def owner(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "owner"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tags"))


@jsii.data_type(
    jsii_type="cdktg.DataAssetProps",
    jsii_struct_bases=[ResourceProps],
    name_mapping={
        "description": "description",
        "cia_triad": "ciaTriad",
        "quantity": "quantity",
        "usage": "usage",
        "origin": "origin",
        "owner": "owner",
        "tags": "tags",
    },
)
class DataAssetProps(ResourceProps):
    def __init__(
        self,
        *,
        description: builtins.str,
        cia_triad: CIATriad,
        quantity: Quantity,
        usage: Usage,
        origin: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param description: 
        :param cia_triad: 
        :param quantity: 
        :param usage: 
        :param origin: 
        :param owner: 
        :param tags: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "description": description,
            "cia_triad": cia_triad,
            "quantity": quantity,
            "usage": usage,
        }
        if origin is not None:
            self._values["origin"] = origin
        if owner is not None:
            self._values["owner"] = owner
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> builtins.str:
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cia_triad(self) -> CIATriad:
        result = self._values.get("cia_triad")
        assert result is not None, "Required property 'cia_triad' is missing"
        return typing.cast(CIATriad, result)

    @builtins.property
    def quantity(self) -> Quantity:
        result = self._values.get("quantity")
        assert result is not None, "Required property 'quantity' is missing"
        return typing.cast(Quantity, result)

    @builtins.property
    def usage(self) -> Usage:
        result = self._values.get("usage")
        assert result is not None, "Required property 'usage' is missing"
        return typing.cast(Usage, result)

    @builtins.property
    def origin(self) -> typing.Optional[builtins.str]:
        result = self._values.get("origin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAssetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InScope(Scope, metaclass=jsii.JSIIMeta, jsii_type="cdktg.InScope"):
    def __init__(self, justification: typing.Optional[builtins.str] = None) -> None:
        '''
        :param justification: -
        '''
        jsii.create(self.__class__, self, [justification])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="isInScope")
    def _is_in_scope(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "isInScope"))


class OutOfScope(Scope, metaclass=jsii.JSIIMeta, jsii_type="cdktg.OutOfScope"):
    def __init__(self, justification: typing.Optional[builtins.str] = None) -> None:
        '''
        :param justification: -
        '''
        jsii.create(self.__class__, self, [justification])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="isInScope")
    def _is_in_scope(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "isInScope"))


__all__ = [
    "AbuseCase",
    "AbuseCaseProps",
    "AnnotationMetadataEntryType",
    "Annotations",
    "Aspects",
    "Authentication",
    "Author",
    "AuthorProps",
    "Authorization",
    "Availability",
    "BusinessCriticality",
    "CIATriad",
    "CIATriadProps",
    "Communication",
    "CommunicationOptions",
    "CommunicationProps",
    "Confidentiality",
    "DataAsset",
    "DataAssetProps",
    "DataFormat",
    "Encryption",
    "IAspect",
    "IManifest",
    "IModelSynthesizer",
    "ISynthesisSession",
    "InScope",
    "Integrity",
    "Machine",
    "Manifest",
    "Model",
    "ModelAnnotation",
    "ModelManifest",
    "ModelProps",
    "ModelSynthesizer",
    "OutOfScope",
    "OutOfScopeProps",
    "Project",
    "ProjectProps",
    "Protocol",
    "Quantity",
    "Question",
    "Resource",
    "ResourceProps",
    "Scope",
    "SharedRuntime",
    "SharedRuntimeProps",
    "Size",
    "TechnicalAsset",
    "TechnicalAssetProps",
    "TechnicalAssetType",
    "Technology",
    "TrustBoundary",
    "TrustBoundaryProps",
    "TrustBoundaryType",
    "Usage",
]

publication.publish()

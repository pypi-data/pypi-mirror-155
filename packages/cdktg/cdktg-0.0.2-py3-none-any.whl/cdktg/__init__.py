'''
# replace this
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


class Asset(
    constructs.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdktg.Asset",
):
    def __init__(
        self,
        model: constructs.Construct,
        id: builtins.str,
        *,
        cia_triad: "CIATriad",
        description: builtins.str,
        usage: "Usage",
    ) -> None:
        '''
        :param model: -
        :param id: -
        :param cia_triad: 
        :param description: 
        :param usage: 
        '''
        props = AssetProps(cia_triad=cia_triad, description=description, usage=usage)

        jsii.create(self.__class__, self, [model, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ciaTriad")
    def cia_triad(self) -> "CIATriad":
        return typing.cast("CIATriad", jsii.get(self, "ciaTriad"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="usage")
    def usage(self) -> "Usage":
        return typing.cast("Usage", jsii.get(self, "usage"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))


class _AssetProxy(Asset):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Asset).__jsii_proxy_class__ = lambda : _AssetProxy


@jsii.data_type(
    jsii_type="cdktg.AssetProps",
    jsii_struct_bases=[],
    name_mapping={
        "cia_triad": "ciaTriad",
        "description": "description",
        "usage": "usage",
    },
)
class AssetProps:
    def __init__(
        self,
        *,
        cia_triad: "CIATriad",
        description: builtins.str,
        usage: "Usage",
    ) -> None:
        '''
        :param cia_triad: 
        :param description: 
        :param usage: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cia_triad": cia_triad,
            "description": description,
            "usage": usage,
        }

    @builtins.property
    def cia_triad(self) -> "CIATriad":
        result = self._values.get("cia_triad")
        assert result is not None, "Required property 'cia_triad' is missing"
        return typing.cast("CIATriad", result)

    @builtins.property
    def description(self) -> builtins.str:
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def usage(self) -> "Usage":
        result = self._values.get("usage")
        assert result is not None, "Required property 'usage' is missing"
        return typing.cast("Usage", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdktg.AssetType")
class AssetType(enum.Enum):
    EXTERNAL_ENTITY = "EXTERNAL_ENTITY"
    PROCESS = "PROCESS"
    DATASTORE = "DATASTORE"


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

    @jsii.member(jsii_name="received")
    def received(self, *assets: "DataAsset") -> None:
        '''
        :param assets: -
        '''
        return typing.cast(None, jsii.invoke(self, "received", [*assets]))

    @jsii.member(jsii_name="sent")
    def sent(self, *assets: "DataAsset") -> None:
        '''
        :param assets: -
        '''
        return typing.cast(None, jsii.invoke(self, "sent", [*assets]))

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


class DataAsset(Asset, metaclass=jsii.JSIIMeta, jsii_type="cdktg.DataAsset"):
    def __init__(
        self,
        model: constructs.Construct,
        id: builtins.str,
        *,
        quantity: "Quantity",
        origin: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        cia_triad: CIATriad,
        description: builtins.str,
        usage: "Usage",
    ) -> None:
        '''
        :param model: -
        :param id: -
        :param quantity: 
        :param origin: 
        :param owner: 
        :param cia_triad: 
        :param description: 
        :param usage: 
        '''
        props = DataAssetProps(
            quantity=quantity,
            origin=origin,
            owner=owner,
            cia_triad=cia_triad,
            description=description,
            usage=usage,
        )

        jsii.create(self.__class__, self, [model, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="quantity")
    def quantity(self) -> "Quantity":
        return typing.cast("Quantity", jsii.get(self, "quantity"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="origin")
    def origin(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "origin"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="owner")
    def owner(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "owner"))


@jsii.data_type(
    jsii_type="cdktg.DataAssetProps",
    jsii_struct_bases=[AssetProps],
    name_mapping={
        "cia_triad": "ciaTriad",
        "description": "description",
        "usage": "usage",
        "quantity": "quantity",
        "origin": "origin",
        "owner": "owner",
    },
)
class DataAssetProps(AssetProps):
    def __init__(
        self,
        *,
        cia_triad: CIATriad,
        description: builtins.str,
        usage: "Usage",
        quantity: "Quantity",
        origin: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cia_triad: 
        :param description: 
        :param usage: 
        :param quantity: 
        :param origin: 
        :param owner: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cia_triad": cia_triad,
            "description": description,
            "usage": usage,
            "quantity": quantity,
        }
        if origin is not None:
            self._values["origin"] = origin
        if owner is not None:
            self._values["owner"] = owner

    @builtins.property
    def cia_triad(self) -> CIATriad:
        result = self._values.get("cia_triad")
        assert result is not None, "Required property 'cia_triad' is missing"
        return typing.cast(CIATriad, result)

    @builtins.property
    def description(self) -> builtins.str:
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def usage(self) -> "Usage":
        result = self._values.get("usage")
        assert result is not None, "Required property 'usage' is missing"
        return typing.cast("Usage", result)

    @builtins.property
    def quantity(self) -> "Quantity":
        result = self._values.get("quantity")
        assert result is not None, "Required property 'quantity' is missing"
        return typing.cast("Quantity", result)

    @builtins.property
    def origin(self) -> typing.Optional[builtins.str]:
        result = self._values.get("origin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAssetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


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


class Model(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdktg.Model"):
    def __init__(
        self,
        *,
        author: Author,
        business_criticality: BusinessCriticality,
        title: builtins.str,
        version: builtins.str,
        date: typing.Optional[datetime.datetime] = None,
    ) -> None:
        '''
        :param author: Author of the model.
        :param business_criticality: Business criticality of the target.
        :param title: Title of the model.
        :param version: Version of the Threagile toolkit.
        :param date: Date of the model.
        '''
        props = ModelProps(
            author=author,
            business_criticality=business_criticality,
            title=title,
            version=version,
            date=date,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="synth")
    def synth(self, outdir: typing.Optional[builtins.str] = None) -> None:
        '''Synthesizes the model to the output directory.

        :param outdir: -
        '''
        return typing.cast(None, jsii.invoke(self, "synth", [outdir]))

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
    def date(self) -> typing.Optional[datetime.datetime]:
        return typing.cast(typing.Optional[datetime.datetime], jsii.get(self, "date"))


@jsii.data_type(
    jsii_type="cdktg.ModelProps",
    jsii_struct_bases=[],
    name_mapping={
        "author": "author",
        "business_criticality": "businessCriticality",
        "title": "title",
        "version": "version",
        "date": "date",
    },
)
class ModelProps:
    def __init__(
        self,
        *,
        author: Author,
        business_criticality: BusinessCriticality,
        title: builtins.str,
        version: builtins.str,
        date: typing.Optional[datetime.datetime] = None,
    ) -> None:
        '''
        :param author: Author of the model.
        :param business_criticality: Business criticality of the target.
        :param title: Title of the model.
        :param version: Version of the Threagile toolkit.
        :param date: Date of the model.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "author": author,
            "business_criticality": business_criticality,
            "title": title,
            "version": version,
        }
        if date is not None:
            self._values["date"] = date

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
    def title(self) -> builtins.str:
        '''Title of the model.'''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Version of the Threagile toolkit.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def date(self) -> typing.Optional[datetime.datetime]:
        '''Date of the model.'''
        result = self._values.get("date")
        return typing.cast(typing.Optional[datetime.datetime], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


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


@jsii.enum(jsii_type="cdktg.Size")
class Size(enum.Enum):
    SYSTEM = "SYSTEM"
    SERVICE = "SERVICE"
    APPLICATION = "APPLICATION"
    COMPONENT = "COMPONENT"


class TechnicalAsset(Asset, metaclass=jsii.JSIIMeta, jsii_type="cdktg.TechnicalAsset"):
    def __init__(
        self,
        model: constructs.Construct,
        id: builtins.str,
        *,
        asset_type: AssetType,
        encryption: Encryption,
        human_use: builtins.bool,
        internet: builtins.bool,
        machine: Machine,
        multi_tenant: builtins.bool,
        owner: builtins.str,
        redundant: builtins.bool,
        size: Size,
        technology: "Technology",
        scope: typing.Optional[Scope] = None,
        trust_boundary: typing.Optional["TrustBoundary"] = None,
        cia_triad: CIATriad,
        description: builtins.str,
        usage: "Usage",
    ) -> None:
        '''
        :param model: -
        :param id: -
        :param asset_type: 
        :param encryption: 
        :param human_use: 
        :param internet: 
        :param machine: 
        :param multi_tenant: 
        :param owner: 
        :param redundant: 
        :param size: 
        :param technology: 
        :param scope: 
        :param trust_boundary: 
        :param cia_triad: 
        :param description: 
        :param usage: 
        '''
        props = TechnicalAssetProps(
            asset_type=asset_type,
            encryption=encryption,
            human_use=human_use,
            internet=internet,
            machine=machine,
            multi_tenant=multi_tenant,
            owner=owner,
            redundant=redundant,
            size=size,
            technology=technology,
            scope=scope,
            trust_boundary=trust_boundary,
            cia_triad=cia_triad,
            description=description,
            usage=usage,
        )

        jsii.create(self.__class__, self, [model, id, props])

    @jsii.member(jsii_name="communicatedWith")
    def communicated_with(
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

        return typing.cast(Communication, jsii.invoke(self, "communicatedWith", [id, target, options]))

    @jsii.member(jsii_name="processed")
    def processed(self, *assets: DataAsset) -> None:
        '''
        :param assets: -
        '''
        return typing.cast(None, jsii.invoke(self, "processed", [*assets]))

    @jsii.member(jsii_name="stored")
    def stored(self, *assets: DataAsset) -> None:
        '''
        :param assets: -
        '''
        return typing.cast(None, jsii.invoke(self, "stored", [*assets]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="assetType")
    def asset_type(self) -> AssetType:
        return typing.cast(AssetType, jsii.get(self, "assetType"))

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
    @jsii.member(jsii_name="scope")
    def scope(self) -> typing.Optional[Scope]:
        return typing.cast(typing.Optional[Scope], jsii.get(self, "scope"))


@jsii.data_type(
    jsii_type="cdktg.TechnicalAssetProps",
    jsii_struct_bases=[AssetProps],
    name_mapping={
        "cia_triad": "ciaTriad",
        "description": "description",
        "usage": "usage",
        "asset_type": "assetType",
        "encryption": "encryption",
        "human_use": "humanUse",
        "internet": "internet",
        "machine": "machine",
        "multi_tenant": "multiTenant",
        "owner": "owner",
        "redundant": "redundant",
        "size": "size",
        "technology": "technology",
        "scope": "scope",
        "trust_boundary": "trustBoundary",
    },
)
class TechnicalAssetProps(AssetProps):
    def __init__(
        self,
        *,
        cia_triad: CIATriad,
        description: builtins.str,
        usage: "Usage",
        asset_type: AssetType,
        encryption: Encryption,
        human_use: builtins.bool,
        internet: builtins.bool,
        machine: Machine,
        multi_tenant: builtins.bool,
        owner: builtins.str,
        redundant: builtins.bool,
        size: Size,
        technology: "Technology",
        scope: typing.Optional[Scope] = None,
        trust_boundary: typing.Optional["TrustBoundary"] = None,
    ) -> None:
        '''
        :param cia_triad: 
        :param description: 
        :param usage: 
        :param asset_type: 
        :param encryption: 
        :param human_use: 
        :param internet: 
        :param machine: 
        :param multi_tenant: 
        :param owner: 
        :param redundant: 
        :param size: 
        :param technology: 
        :param scope: 
        :param trust_boundary: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cia_triad": cia_triad,
            "description": description,
            "usage": usage,
            "asset_type": asset_type,
            "encryption": encryption,
            "human_use": human_use,
            "internet": internet,
            "machine": machine,
            "multi_tenant": multi_tenant,
            "owner": owner,
            "redundant": redundant,
            "size": size,
            "technology": technology,
        }
        if scope is not None:
            self._values["scope"] = scope
        if trust_boundary is not None:
            self._values["trust_boundary"] = trust_boundary

    @builtins.property
    def cia_triad(self) -> CIATriad:
        result = self._values.get("cia_triad")
        assert result is not None, "Required property 'cia_triad' is missing"
        return typing.cast(CIATriad, result)

    @builtins.property
    def description(self) -> builtins.str:
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def usage(self) -> "Usage":
        result = self._values.get("usage")
        assert result is not None, "Required property 'usage' is missing"
        return typing.cast("Usage", result)

    @builtins.property
    def asset_type(self) -> AssetType:
        result = self._values.get("asset_type")
        assert result is not None, "Required property 'asset_type' is missing"
        return typing.cast(AssetType, result)

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
    def scope(self) -> typing.Optional[Scope]:
        result = self._values.get("scope")
        return typing.cast(typing.Optional[Scope], result)

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


class TrustBoundary(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktg.TrustBoundary",
):
    def __init__(
        self,
        model: constructs.Construct,
        id: builtins.str,
        *,
        description: builtins.str,
        type: "TrustBoundaryType",
    ) -> None:
        '''
        :param model: -
        :param id: -
        :param description: 
        :param type: 
        '''
        props = TrustBoundaryProps(description=description, type=type)

        jsii.create(self.__class__, self, [model, id, props])

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
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> "TrustBoundaryType":
        return typing.cast("TrustBoundaryType", jsii.get(self, "type"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))


@jsii.data_type(
    jsii_type="cdktg.TrustBoundaryProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class TrustBoundaryProps:
    def __init__(self, *, description: builtins.str, type: "TrustBoundaryType") -> None:
        '''
        :param description: 
        :param type: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "description": description,
            "type": type,
        }

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
    "Asset",
    "AssetProps",
    "AssetType",
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
    "InScope",
    "Integrity",
    "Machine",
    "Model",
    "ModelProps",
    "OutOfScope",
    "OutOfScopeProps",
    "Protocol",
    "Quantity",
    "Scope",
    "Size",
    "TechnicalAsset",
    "TechnicalAssetProps",
    "Technology",
    "TrustBoundary",
    "TrustBoundaryProps",
    "TrustBoundaryType",
    "Usage",
]

publication.publish()

'''
[![NPM version](https://badge.fury.io/js/cdk-aws-iotfleetwise.svg)](https://badge.fury.io/js/cdk-aws-iotfleetwise)
[![PyPI version](https://badge.fury.io/py/cdk-aws-iotfleetwise.svg)](https://badge.fury.io/py/cdk-aws-iotfleetwise)
[![release](https://github.com/aws-samples/cdk-aws-iotfleetwise/actions/workflows/release.yml/badge.svg)](https://github.com/aws-samples/cdk-aws-iotfleetwise/actions/workflows/release.yml)

# cdk-aws-iotfleetwise

L2 CDK construct to provision AWS IoT Fleetwise

# Install

### Typescript

```sh
npm install cdk-aws-iotfleetwise
```

[API Reference](doc/api-typescript.md)

#### Python

```sh
pip install cdk-aws-iotfleetwise
```

[API Reference](doc/api-python.md)

# Sample

```python
import { SignalCatalog,
         VehicleModel,
         Vehicle,
         Campaign,
         CanVehicleInterface,
         CanVehicleSignal,
         SignalCatalogBranch,
         TimeBasedCollectionScheme
         } from 'cdk-aws-iotfleetwise';

const signalCatalog = new SignalCatalog(stack, 'SignalCatalog', {
  database,
  table,
  role,
  nodes: [
    new SignalCatalogBranch('Vehicle', 'Vehicle'),
    new SignalCatalogSensor('EngineTorque', 'Vehicle.EngineTorque', 'DOUBLE'),
  ],
});

const model_a = new VehicleModel(stack, 'ModelA', {
  signalCatalog,
  name: 'modelA',
  description: 'Model A vehicle',
  networkInterfaces: [new CanVehicleInterface('1', 'vcan0')],
  signals: [
    new CanVehicleSignal('EngineTorque', 'Vehicle.EngineTorque', '1',
      401, // messageId
      1.0, // factor
      true, // isBigEndian
      false, // isSigned
      8, // lenght
      0.0, // offset
      9), // startBit
  ],
});

const vin100 = new Vehicle(stack, 'vin100', {
  vehicleId: 'vin100',
  vehicleModel: model_a,
  createIotThing: true
});

new Campaign(stack, 'Campaign', {
  name: 'TimeBasedCampaign',
  target: vin100,
  collectionScheme: new TimeBasedCollectionScheme(cdk.Duration.seconds(10)),
  signals: [
    new CampaignSignal('Vehicle.EngineTorque'),
  ],
});
```

## Getting started

To deploy a simple end-to-end example you can use the following commands

```sh
yarn install
projen && projen build
npx cdk -a lib/integ.full.js deploy
```

The deploy takes about 15 mins mostly due to compilation of the IoT FleetWise agent in the
EC2 instance that simulate the vehicle. Once deploy is finshed, approve the campaign with the command:

```sh
aws iotfleetwise update-campaign --campaign-name FwTimeBasedCampaign --action APPROVE
```

and data will start to show up in the Timestream table.

## TODO

Warning: this construct should be considered at alpha stage and is not feature complete.

* Apply the least priviledge principle to roles
* Implement updates for all the custom resources
* Conditional campaigns

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more
information.

## License

This code is licensed under the MIT-0 License. See the LICENSE file.
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

import aws_cdk
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_logs
import aws_cdk.aws_timestream
import constructs


class Campaign(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.Campaign",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        collection_scheme: "CollectionScheme",
        name: builtins.str,
        signals: typing.Sequence["CampaignSignal"],
        target: "Vehicle",
        auto_approve: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param collection_scheme: 
        :param name: 
        :param signals: 
        :param target: 
        :param auto_approve: 
        '''
        props = CampaignProps(
            collection_scheme=collection_scheme,
            name=name,
            signals=signals,
            target=target,
            auto_approve=auto_approve,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="target")
    def target(self) -> "Vehicle":
        return typing.cast("Vehicle", jsii.get(self, "target"))


@jsii.data_type(
    jsii_type="cdk-aws-iotfleetwise.CampaignProps",
    jsii_struct_bases=[],
    name_mapping={
        "collection_scheme": "collectionScheme",
        "name": "name",
        "signals": "signals",
        "target": "target",
        "auto_approve": "autoApprove",
    },
)
class CampaignProps:
    def __init__(
        self,
        *,
        collection_scheme: "CollectionScheme",
        name: builtins.str,
        signals: typing.Sequence["CampaignSignal"],
        target: "Vehicle",
        auto_approve: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param collection_scheme: 
        :param name: 
        :param signals: 
        :param target: 
        :param auto_approve: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "collection_scheme": collection_scheme,
            "name": name,
            "signals": signals,
            "target": target,
        }
        if auto_approve is not None:
            self._values["auto_approve"] = auto_approve

    @builtins.property
    def collection_scheme(self) -> "CollectionScheme":
        result = self._values.get("collection_scheme")
        assert result is not None, "Required property 'collection_scheme' is missing"
        return typing.cast("CollectionScheme", result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signals(self) -> typing.List["CampaignSignal"]:
        result = self._values.get("signals")
        assert result is not None, "Required property 'signals' is missing"
        return typing.cast(typing.List["CampaignSignal"], result)

    @builtins.property
    def target(self) -> "Vehicle":
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast("Vehicle", result)

    @builtins.property
    def auto_approve(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("auto_approve")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CampaignProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CampaignSignal(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.CampaignSignal",
):
    def __init__(
        self,
        name: builtins.str,
        max_sample_count: typing.Optional[jsii.Number] = None,
        minimum_sampling_interval: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''
        :param name: -
        :param max_sample_count: -
        :param minimum_sampling_interval: -
        '''
        jsii.create(self.__class__, self, [name, max_sample_count, minimum_sampling_interval])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toObject", []))


class CollectionScheme(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.CollectionScheme",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toObject", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scheme")
    def _scheme(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.get(self, "scheme"))

    @_scheme.setter
    def _scheme(self, value: typing.Mapping[typing.Any, typing.Any]) -> None:
        jsii.set(self, "scheme", value)


class Fleet(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.Fleet",
):
    '''The fleet of vehicles.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        fleet_id: builtins.str,
        signal_catalog: "SignalCatalog",
        description: typing.Optional[builtins.str] = None,
        vehicles: typing.Optional[typing.Sequence["Vehicle"]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param fleet_id: 
        :param signal_catalog: 
        :param description: 
        :param vehicles: 
        '''
        props = FleetProps(
            fleet_id=fleet_id,
            signal_catalog=signal_catalog,
            description=description,
            vehicles=vehicles,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fleetId")
    def fleet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fleetId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="signalCatalog")
    def signal_catalog(self) -> "SignalCatalog":
        return typing.cast("SignalCatalog", jsii.get(self, "signalCatalog"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vehicles")
    def vehicles(self) -> typing.Optional[typing.List["Vehicle"]]:
        return typing.cast(typing.Optional[typing.List["Vehicle"]], jsii.get(self, "vehicles"))


@jsii.data_type(
    jsii_type="cdk-aws-iotfleetwise.FleetProps",
    jsii_struct_bases=[],
    name_mapping={
        "fleet_id": "fleetId",
        "signal_catalog": "signalCatalog",
        "description": "description",
        "vehicles": "vehicles",
    },
)
class FleetProps:
    def __init__(
        self,
        *,
        fleet_id: builtins.str,
        signal_catalog: "SignalCatalog",
        description: typing.Optional[builtins.str] = None,
        vehicles: typing.Optional[typing.Sequence["Vehicle"]] = None,
    ) -> None:
        '''Interface.

        :param fleet_id: 
        :param signal_catalog: 
        :param description: 
        :param vehicles: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "fleet_id": fleet_id,
            "signal_catalog": signal_catalog,
        }
        if description is not None:
            self._values["description"] = description
        if vehicles is not None:
            self._values["vehicles"] = vehicles

    @builtins.property
    def fleet_id(self) -> builtins.str:
        result = self._values.get("fleet_id")
        assert result is not None, "Required property 'fleet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signal_catalog(self) -> "SignalCatalog":
        result = self._values.get("signal_catalog")
        assert result is not None, "Required property 'signal_catalog' is missing"
        return typing.cast("SignalCatalog", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vehicles(self) -> typing.Optional[typing.List["Vehicle"]]:
        result = self._values.get("vehicles")
        return typing.cast(typing.Optional[typing.List["Vehicle"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FleetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkFileDefinition(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.NetworkFileDefinition",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toObject", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="definition")
    def _definition(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.get(self, "definition"))

    @_definition.setter
    def _definition(self, value: typing.Mapping[typing.Any, typing.Any]) -> None:
        jsii.set(self, "definition", value)


class SignalCatalog(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.SignalCatalog",
):
    '''The Signal Catalog represents the list of all signals that you want to collect from all the vehicles.

    The AWS IoT Fleetwise preview can only support a single Signal Catalog per account.
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        database: aws_cdk.aws_timestream.CfnDatabase,
        nodes: typing.Sequence["SignalCatalogNode"],
        role: aws_cdk.aws_iam.Role,
        table: aws_cdk.aws_timestream.CfnTable,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param database: 
        :param nodes: 
        :param role: 
        :param table: 
        :param description: 
        :param name: 
        '''
        props = SignalCatalogProps(
            database=database,
            nodes=nodes,
            role=role,
            table=table,
            description=description,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambdaLayer")
    def lambda_layer(self) -> aws_cdk.aws_lambda.LayerVersion:
        return typing.cast(aws_cdk.aws_lambda.LayerVersion, jsii.get(self, "lambdaLayer"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambdaRole")
    def lambda_role(self) -> aws_cdk.aws_iam.Role:
        return typing.cast(aws_cdk.aws_iam.Role, jsii.get(self, "lambdaRole"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logRetention")
    def log_retention(self) -> aws_cdk.aws_logs.RetentionDays:
        return typing.cast(aws_cdk.aws_logs.RetentionDays, jsii.get(self, "logRetention"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the signal catalog.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))


class SignalCatalogNode(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.SignalCatalogNode",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toObject", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="node")
    def _node(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.get(self, "node"))

    @_node.setter
    def _node(self, value: typing.Mapping[typing.Any, typing.Any]) -> None:
        jsii.set(self, "node", value)


@jsii.data_type(
    jsii_type="cdk-aws-iotfleetwise.SignalCatalogProps",
    jsii_struct_bases=[],
    name_mapping={
        "database": "database",
        "nodes": "nodes",
        "role": "role",
        "table": "table",
        "description": "description",
        "name": "name",
    },
)
class SignalCatalogProps:
    def __init__(
        self,
        *,
        database: aws_cdk.aws_timestream.CfnDatabase,
        nodes: typing.Sequence[SignalCatalogNode],
        role: aws_cdk.aws_iam.Role,
        table: aws_cdk.aws_timestream.CfnTable,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database: 
        :param nodes: 
        :param role: 
        :param table: 
        :param description: 
        :param name: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "database": database,
            "nodes": nodes,
            "role": role,
            "table": table,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def database(self) -> aws_cdk.aws_timestream.CfnDatabase:
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(aws_cdk.aws_timestream.CfnDatabase, result)

    @builtins.property
    def nodes(self) -> typing.List[SignalCatalogNode]:
        result = self._values.get("nodes")
        assert result is not None, "Required property 'nodes' is missing"
        return typing.cast(typing.List[SignalCatalogNode], result)

    @builtins.property
    def role(self) -> aws_cdk.aws_iam.Role:
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(aws_cdk.aws_iam.Role, result)

    @builtins.property
    def table(self) -> aws_cdk.aws_timestream.CfnTable:
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast(aws_cdk.aws_timestream.CfnTable, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SignalCatalogProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SignalCatalogSensor(
    SignalCatalogNode,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.SignalCatalogSensor",
):
    def __init__(
        self,
        name: builtins.str,
        fully_qualified_name: builtins.str,
        data_type: builtins.str,
        unit: typing.Optional[builtins.str] = None,
        min: typing.Optional[jsii.Number] = None,
        max: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: -
        :param fully_qualified_name: -
        :param data_type: -
        :param unit: -
        :param min: -
        :param max: -
        :param description: -
        '''
        jsii.create(self.__class__, self, [name, fully_qualified_name, data_type, unit, min, max, description])


class TimeBasedCollectionScheme(
    CollectionScheme,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.TimeBasedCollectionScheme",
):
    def __init__(self, period: aws_cdk.Duration) -> None:
        '''
        :param period: -
        '''
        jsii.create(self.__class__, self, [period])


class Vehicle(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.Vehicle",
):
    '''The vehicle of a specific type from which IoT FleetWise collect signals.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        create_iot_thing: builtins.bool,
        vehicle_id: builtins.str,
        vehicle_model: "VehicleModel",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param create_iot_thing: 
        :param vehicle_id: 
        :param vehicle_model: 
        '''
        props = VehicleProps(
            create_iot_thing=create_iot_thing,
            vehicle_id=vehicle_id,
            vehicle_model=vehicle_model,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vehicleId")
    def vehicle_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vehicleId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vehicleModel")
    def vehicle_model(self) -> "VehicleModel":
        return typing.cast("VehicleModel", jsii.get(self, "vehicleModel"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="certificateId")
    def certificate_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="certificatePem")
    def certificate_pem(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificatePem"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpointAddress")
    def endpoint_address(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointAddress"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKey"))


class VehicleInterface(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.VehicleInterface",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toObject", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="intf")
    def _intf(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.get(self, "intf"))

    @_intf.setter
    def _intf(self, value: typing.Mapping[typing.Any, typing.Any]) -> None:
        jsii.set(self, "intf", value)


class VehicleModel(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.VehicleModel",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        network_interfaces: typing.Sequence[VehicleInterface],
        signal_catalog: SignalCatalog,
        description: typing.Optional[builtins.str] = None,
        network_file_definitions: typing.Optional[typing.Sequence[NetworkFileDefinition]] = None,
        signals: typing.Optional[typing.Sequence["VehicleSignal"]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: 
        :param network_interfaces: 
        :param signal_catalog: 
        :param description: 
        :param network_file_definitions: 
        :param signals: 
        '''
        props = VehicleModelProps(
            name=name,
            network_interfaces=network_interfaces,
            signal_catalog=signal_catalog,
            description=description,
            network_file_definitions=network_file_definitions,
            signals=signals,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="signalCatalog")
    def signal_catalog(self) -> SignalCatalog:
        return typing.cast(SignalCatalog, jsii.get(self, "signalCatalog"))


@jsii.data_type(
    jsii_type="cdk-aws-iotfleetwise.VehicleModelProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "network_interfaces": "networkInterfaces",
        "signal_catalog": "signalCatalog",
        "description": "description",
        "network_file_definitions": "networkFileDefinitions",
        "signals": "signals",
    },
)
class VehicleModelProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        network_interfaces: typing.Sequence[VehicleInterface],
        signal_catalog: SignalCatalog,
        description: typing.Optional[builtins.str] = None,
        network_file_definitions: typing.Optional[typing.Sequence[NetworkFileDefinition]] = None,
        signals: typing.Optional[typing.Sequence["VehicleSignal"]] = None,
    ) -> None:
        '''
        :param name: 
        :param network_interfaces: 
        :param signal_catalog: 
        :param description: 
        :param network_file_definitions: 
        :param signals: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "network_interfaces": network_interfaces,
            "signal_catalog": signal_catalog,
        }
        if description is not None:
            self._values["description"] = description
        if network_file_definitions is not None:
            self._values["network_file_definitions"] = network_file_definitions
        if signals is not None:
            self._values["signals"] = signals

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_interfaces(self) -> typing.List[VehicleInterface]:
        result = self._values.get("network_interfaces")
        assert result is not None, "Required property 'network_interfaces' is missing"
        return typing.cast(typing.List[VehicleInterface], result)

    @builtins.property
    def signal_catalog(self) -> SignalCatalog:
        result = self._values.get("signal_catalog")
        assert result is not None, "Required property 'signal_catalog' is missing"
        return typing.cast(SignalCatalog, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_file_definitions(
        self,
    ) -> typing.Optional[typing.List[NetworkFileDefinition]]:
        result = self._values.get("network_file_definitions")
        return typing.cast(typing.Optional[typing.List[NetworkFileDefinition]], result)

    @builtins.property
    def signals(self) -> typing.Optional[typing.List["VehicleSignal"]]:
        result = self._values.get("signals")
        return typing.cast(typing.Optional[typing.List["VehicleSignal"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VehicleModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-aws-iotfleetwise.VehicleProps",
    jsii_struct_bases=[],
    name_mapping={
        "create_iot_thing": "createIotThing",
        "vehicle_id": "vehicleId",
        "vehicle_model": "vehicleModel",
    },
)
class VehicleProps:
    def __init__(
        self,
        *,
        create_iot_thing: builtins.bool,
        vehicle_id: builtins.str,
        vehicle_model: VehicleModel,
    ) -> None:
        '''Interface.

        :param create_iot_thing: 
        :param vehicle_id: 
        :param vehicle_model: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "create_iot_thing": create_iot_thing,
            "vehicle_id": vehicle_id,
            "vehicle_model": vehicle_model,
        }

    @builtins.property
    def create_iot_thing(self) -> builtins.bool:
        result = self._values.get("create_iot_thing")
        assert result is not None, "Required property 'create_iot_thing' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def vehicle_id(self) -> builtins.str:
        result = self._values.get("vehicle_id")
        assert result is not None, "Required property 'vehicle_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vehicle_model(self) -> VehicleModel:
        result = self._values.get("vehicle_model")
        assert result is not None, "Required property 'vehicle_model' is missing"
        return typing.cast(VehicleModel, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VehicleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VehicleSignal(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.VehicleSignal",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toObject", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="signal")
    def _signal(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.get(self, "signal"))

    @_signal.setter
    def _signal(self, value: typing.Mapping[typing.Any, typing.Any]) -> None:
        jsii.set(self, "signal", value)


class CanDefinition(
    NetworkFileDefinition,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.CanDefinition",
):
    def __init__(
        self,
        network_interface: builtins.str,
        signals_map: typing.Mapping[builtins.str, builtins.str],
        can_dbc_files: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param network_interface: -
        :param signals_map: -
        :param can_dbc_files: -
        '''
        jsii.create(self.__class__, self, [network_interface, signals_map, can_dbc_files])


class CanVehicleInterface(
    VehicleInterface,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.CanVehicleInterface",
):
    def __init__(self, interface_id: builtins.str, name: builtins.str) -> None:
        '''
        :param interface_id: -
        :param name: -
        '''
        jsii.create(self.__class__, self, [interface_id, name])


class CanVehicleSignal(
    VehicleSignal,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.CanVehicleSignal",
):
    def __init__(
        self,
        name: builtins.str,
        fully_qualified_name: builtins.str,
        interface_id: builtins.str,
        message_id: jsii.Number,
        factor: jsii.Number,
        is_big_endian: builtins.bool,
        is_signed: builtins.bool,
        length: jsii.Number,
        offset: jsii.Number,
        start_bit: jsii.Number,
    ) -> None:
        '''
        :param name: -
        :param fully_qualified_name: -
        :param interface_id: -
        :param message_id: -
        :param factor: -
        :param is_big_endian: -
        :param is_signed: -
        :param length: -
        :param offset: -
        :param start_bit: -
        '''
        jsii.create(self.__class__, self, [name, fully_qualified_name, interface_id, message_id, factor, is_big_endian, is_signed, length, offset, start_bit])


class SignalCatalogBranch(
    SignalCatalogNode,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.SignalCatalogBranch",
):
    def __init__(
        self,
        name: builtins.str,
        fully_qualified_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: -
        :param fully_qualified_name: -
        :param description: -
        '''
        jsii.create(self.__class__, self, [name, fully_qualified_name, description])


__all__ = [
    "Campaign",
    "CampaignProps",
    "CampaignSignal",
    "CanDefinition",
    "CanVehicleInterface",
    "CanVehicleSignal",
    "CollectionScheme",
    "Fleet",
    "FleetProps",
    "NetworkFileDefinition",
    "SignalCatalog",
    "SignalCatalogBranch",
    "SignalCatalogNode",
    "SignalCatalogProps",
    "SignalCatalogSensor",
    "TimeBasedCollectionScheme",
    "Vehicle",
    "VehicleInterface",
    "VehicleModel",
    "VehicleModelProps",
    "VehicleProps",
    "VehicleSignal",
]

publication.publish()

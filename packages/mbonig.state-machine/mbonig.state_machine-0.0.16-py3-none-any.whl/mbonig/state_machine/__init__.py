'''
# Workflow Studio compatible State Machine

[![View on Construct Hub](https://constructs.dev/badge?package=%40matthewbonig%2Fstate-machine)](https://constructs.dev/packages/@matthewbonig/state-machine)

This is a Workflow Studio compatible AWS Step Function state machine construct.

The goal of this construct is to make it easy to build and maintain your state machines using the Workflow Studio but still
leverage the AWS CDK as the source of truth for the state machine.

Read more about it [here](https://matthewbonig.com/2022/02/19/step-functions-and-the-cdk/).

## How to Use This Construct

Start by designing your initial state machine using the Workflow Studio.
When done with your first draft, copy and paste the ASL definition to a local file.

Create a new instance of this construct, handing it a fully parsed version of the ASL.
Then add overridden values.
The fields in the `overrides` field should match the `States` field of the ASL.

### Examples

```python
const secret = new Secret(stack, 'Secret', {});
new StateMachine(stack, 'Test', {
  stateMachineName: 'A nice state machine',
  definition: JSON.parse(fs.readFileSync(path.join(__dirname, 'sample.json'), 'utf8').toString()),
  overrides: {
    'Read database credentials secret': {
      Parameters: {
        SecretId: secret.secretArn,
      },
    },
  },
});
```

You can also override nested states in arrays, for example:

```python
new StateMachine(stack, 'Test', {
    stateMachineName: 'A-nice-state-machine',
    overrides: {
      Branches: [{
        // pass an empty object too offset overrides
      }, {
        StartAt: 'StartInstances',
        States: {
          StartInstances: {
            Parameters: {
              InstanceIds: ['INSTANCE_ID'],
            },
          },
        },
      }],
    },
    stateMachineType: StateMachineType.STANDARD,
    definition: {
      States: {
        Branches: [
          {
            StartAt: 'ResumeCluster',
            States: {
              'Redshift Pass': {
                Type: 'Pass',
                End: true,
              },
            },
          },
          {
            StartAt: 'StartInstances',
            States: {
              'StartInstances': {
                Type: 'Task',
                Parameters: {
                  InstanceIds: [
                    'MyData',
                  ],
                },
                Resource: 'arn:aws:states:::aws-sdk:ec2:startInstances',
                Next: 'DescribeInstanceStatus',
              },
              'DescribeInstanceStatus': {
                Type: 'Task',
                Next: 'EC2 Pass',
                Parameters: {
                  InstanceIds: [
                    'MyData',
                  ],
                },
                Resource: 'arn:aws:states:::aws-sdk:ec2:describeInstanceStatus',
              },
              'EC2 Pass': {
                Type: 'Pass',
                End: true,
              },
            },
          },
        ],
      },
    },
  });
```

For Python, be sure to use a context manager when opening your JSON file.

* You do not need to `str()` the dictionary object you supply as your `definition` prop.
* Elements of your override path **do** need to be strings.

```python
secret = Secret(stack, 'Secret')

with open('sample.json', 'r+', encoding='utf-8') as sample:
    sample_dict = json.load(sample)

state_machine = StateMachine(
    self,
    'Test',
    definition = sample_dict,
    overrides = {
    "Read database credentials secret": {
      "Parameters": {
        "SecretId": secret.secret_arn,
      },
    },
  })
```

In this example, the ASL has a state called 'Read database credentials secret' and the SecretId parameter is overridden with a
CDK generated value.
Future changes can be done by editing, debugging, and testing the state machine directly in the Workflow Studio.
Once everything is working properly, copy and paste the ASL back to your local file.

## Issues

Please open any issues you have on [Github](https://github.com/mbonig/state-machine/issues).

## Contributing

Please submit PRs from forked repositories if you'd like to contribute.
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
import aws_cdk.aws_stepfunctions
import constructs


class StateMachine(
    aws_cdk.aws_stepfunctions.StateMachine,
    metaclass=jsii.JSIIMeta,
    jsii_type="@matthewbonig/state-machine.StateMachine",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        definition: typing.Any,
        logs: typing.Optional[aws_cdk.aws_stepfunctions.LogOptions] = None,
        overrides: typing.Any = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        state_machine_name: typing.Optional[builtins.str] = None,
        state_machine_type: typing.Optional[aws_cdk.aws_stepfunctions.StateMachineType] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
        tracing_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param definition: An object that can be serialized into an ASL.
        :param logs: Defines what execution history events are logged and where they are logged. Default: No logging
        :param overrides: An object that matches the schema/shape of the ASL .States map with overridden values.
        :param role: The execution role for the state machine service. Default: A role is automatically created
        :param state_machine_name: A name for the state machine. Default: A name is automatically generated
        :param state_machine_type: Type of the state machine. Default: StateMachineType.STANDARD
        :param timeout: Maximum run time for this state machine. Default: No timeout
        :param tracing_enabled: Specifies whether Amazon X-Ray tracing is enabled for this state machine. Default: false
        '''
        props = StateMachineProps(
            definition=definition,
            logs=logs,
            overrides=overrides,
            role=role,
            state_machine_name=state_machine_name,
            state_machine_type=state_machine_type,
            timeout=timeout,
            tracing_enabled=tracing_enabled,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@matthewbonig/state-machine.StateMachineProps",
    jsii_struct_bases=[],
    name_mapping={
        "definition": "definition",
        "logs": "logs",
        "overrides": "overrides",
        "role": "role",
        "state_machine_name": "stateMachineName",
        "state_machine_type": "stateMachineType",
        "timeout": "timeout",
        "tracing_enabled": "tracingEnabled",
    },
)
class StateMachineProps:
    def __init__(
        self,
        *,
        definition: typing.Any,
        logs: typing.Optional[aws_cdk.aws_stepfunctions.LogOptions] = None,
        overrides: typing.Any = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        state_machine_name: typing.Optional[builtins.str] = None,
        state_machine_type: typing.Optional[aws_cdk.aws_stepfunctions.StateMachineType] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
        tracing_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param definition: An object that can be serialized into an ASL.
        :param logs: Defines what execution history events are logged and where they are logged. Default: No logging
        :param overrides: An object that matches the schema/shape of the ASL .States map with overridden values.
        :param role: The execution role for the state machine service. Default: A role is automatically created
        :param state_machine_name: A name for the state machine. Default: A name is automatically generated
        :param state_machine_type: Type of the state machine. Default: StateMachineType.STANDARD
        :param timeout: Maximum run time for this state machine. Default: No timeout
        :param tracing_enabled: Specifies whether Amazon X-Ray tracing is enabled for this state machine. Default: false
        '''
        if isinstance(logs, dict):
            logs = aws_cdk.aws_stepfunctions.LogOptions(**logs)
        self._values: typing.Dict[str, typing.Any] = {
            "definition": definition,
        }
        if logs is not None:
            self._values["logs"] = logs
        if overrides is not None:
            self._values["overrides"] = overrides
        if role is not None:
            self._values["role"] = role
        if state_machine_name is not None:
            self._values["state_machine_name"] = state_machine_name
        if state_machine_type is not None:
            self._values["state_machine_type"] = state_machine_type
        if timeout is not None:
            self._values["timeout"] = timeout
        if tracing_enabled is not None:
            self._values["tracing_enabled"] = tracing_enabled

    @builtins.property
    def definition(self) -> typing.Any:
        '''An object that can be serialized into an ASL.'''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def logs(self) -> typing.Optional[aws_cdk.aws_stepfunctions.LogOptions]:
        '''Defines what execution history events are logged and where they are logged.

        :default: No logging
        '''
        result = self._values.get("logs")
        return typing.cast(typing.Optional[aws_cdk.aws_stepfunctions.LogOptions], result)

    @builtins.property
    def overrides(self) -> typing.Any:
        '''An object that matches the schema/shape of the ASL .States map with overridden values.

        Example::

            {'My First State': { Parameters: { FunctionName: 'aLambdaFunctionArn' } } }
        '''
        result = self._values.get("overrides")
        return typing.cast(typing.Any, result)

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''The execution role for the state machine service.

        :default: A role is automatically created
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def state_machine_name(self) -> typing.Optional[builtins.str]:
        '''A name for the state machine.

        :default: A name is automatically generated
        '''
        result = self._values.get("state_machine_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state_machine_type(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.StateMachineType]:
        '''Type of the state machine.

        :default: StateMachineType.STANDARD
        '''
        result = self._values.get("state_machine_type")
        return typing.cast(typing.Optional[aws_cdk.aws_stepfunctions.StateMachineType], result)

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.Duration]:
        '''Maximum run time for this state machine.

        :default: No timeout
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def tracing_enabled(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether Amazon X-Ray tracing is enabled for this state machine.

        :default: false
        '''
        result = self._values.get("tracing_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StateMachineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "StateMachine",
    "StateMachineProps",
]

publication.publish()

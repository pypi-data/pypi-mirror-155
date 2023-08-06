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

import aws_cdk.aws_stepfunctions
import constructs


class TextractAsyncToJSON(
    aws_cdk.aws_stepfunctions.StateMachineFragment,
    metaclass=jsii.JSIIMeta,
    jsii_type="schadem-cdk-construct-sfn-textract-output-config-to-json.TextractAsyncToJSON",
):
    def __init__(
        self,
        parent: constructs.Construct,
        id: builtins.str,
        *,
        s3_output_bucket: builtins.str,
        s3_output_prefix: builtins.str,
        lambda_log_level: typing.Optional[builtins.str] = None,
        lambda_memory_mb: typing.Optional[jsii.Number] = None,
        lambda_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param parent: -
        :param id: -
        :param s3_output_bucket: 
        :param s3_output_prefix: The prefix to use for the output files.
        :param lambda_log_level: 
        :param lambda_memory_mb: memory of Lambda function (may need to increase for larger documents).
        :param lambda_timeout: 
        '''
        props = TextractAsyncToJSONProps(
            s3_output_bucket=s3_output_bucket,
            s3_output_prefix=s3_output_prefix,
            lambda_log_level=lambda_log_level,
            lambda_memory_mb=lambda_memory_mb,
            lambda_timeout=lambda_timeout,
        )

        jsii.create(self.__class__, self, [parent, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[aws_cdk.aws_stepfunctions.INextable]:
        '''The states to chain onto if this fragment is used.'''
        return typing.cast(typing.List[aws_cdk.aws_stepfunctions.INextable], jsii.get(self, "endStates"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="startState")
    def start_state(self) -> aws_cdk.aws_stepfunctions.State:
        '''The start state of this state machine fragment.'''
        return typing.cast(aws_cdk.aws_stepfunctions.State, jsii.get(self, "startState"))


@jsii.data_type(
    jsii_type="schadem-cdk-construct-sfn-textract-output-config-to-json.TextractAsyncToJSONProps",
    jsii_struct_bases=[],
    name_mapping={
        "s3_output_bucket": "s3OutputBucket",
        "s3_output_prefix": "s3OutputPrefix",
        "lambda_log_level": "lambdaLogLevel",
        "lambda_memory_mb": "lambdaMemoryMB",
        "lambda_timeout": "lambdaTimeout",
    },
)
class TextractAsyncToJSONProps:
    def __init__(
        self,
        *,
        s3_output_bucket: builtins.str,
        s3_output_prefix: builtins.str,
        lambda_log_level: typing.Optional[builtins.str] = None,
        lambda_memory_mb: typing.Optional[jsii.Number] = None,
        lambda_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param s3_output_bucket: 
        :param s3_output_prefix: The prefix to use for the output files.
        :param lambda_log_level: 
        :param lambda_memory_mb: memory of Lambda function (may need to increase for larger documents).
        :param lambda_timeout: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "s3_output_bucket": s3_output_bucket,
            "s3_output_prefix": s3_output_prefix,
        }
        if lambda_log_level is not None:
            self._values["lambda_log_level"] = lambda_log_level
        if lambda_memory_mb is not None:
            self._values["lambda_memory_mb"] = lambda_memory_mb
        if lambda_timeout is not None:
            self._values["lambda_timeout"] = lambda_timeout

    @builtins.property
    def s3_output_bucket(self) -> builtins.str:
        result = self._values.get("s3_output_bucket")
        assert result is not None, "Required property 's3_output_bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_output_prefix(self) -> builtins.str:
        '''The prefix to use for the output files.'''
        result = self._values.get("s3_output_prefix")
        assert result is not None, "Required property 's3_output_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lambda_log_level(self) -> typing.Optional[builtins.str]:
        result = self._values.get("lambda_log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_memory_mb(self) -> typing.Optional[jsii.Number]:
        '''memory of Lambda function (may need to increase for larger documents).'''
        result = self._values.get("lambda_memory_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lambda_timeout(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("lambda_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TextractAsyncToJSONProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "TextractAsyncToJSON",
    "TextractAsyncToJSONProps",
]

publication.publish()

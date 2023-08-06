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

import aws_cdk
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_logs
import aws_cdk.aws_sqs
import aws_cdk.aws_stepfunctions
import aws_cdk.aws_stepfunctions_tasks
import constructs


class TextractGenericSyncSfnTask(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="schadem-cdk-construct-textract-generic-sync.TextractGenericSyncSfnTask",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        s3_output_bucket: builtins.str,
        s3_output_prefix: builtins.str,
        associate_with_parent: typing.Optional[builtins.bool] = None,
        custom_function: typing.Optional[aws_cdk.aws_stepfunctions_tasks.LambdaInvoke] = None,
        enable_dashboard: typing.Optional[builtins.bool] = None,
        enable_monitoring: typing.Optional[builtins.bool] = None,
        input: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        lambda_log_level: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        s3_input_bucket: typing.Optional[builtins.str] = None,
        s3_input_prefix: typing.Optional[builtins.str] = None,
        textract_state_machine_timeout_minutes: typing.Optional[jsii.Number] = None,
        workflow_tracing_enabled: typing.Optional[builtins.bool] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        result_selector: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param s3_output_bucket: 
        :param s3_output_prefix: The prefix to use for the output files.
        :param associate_with_parent: Pass the execution ID from the context object to the execution input. This allows the Step Functions UI to link child executions from parent executions, making it easier to trace execution flow across state machines. If you set this property to ``true``, the ``input`` property must be an object (provided by ``sfn.TaskInput.fromObject``) or omitted entirely. Default: - false
        :param custom_function: not implemented yet.
        :param enable_dashboard: not implemented yet.
        :param enable_monitoring: not implemented yet.
        :param input: The JSON input for the execution, same as that of StartExecution. Default: - The state input (JSON path '$')
        :param lambda_log_level: The prefix to use for the output files.
        :param name: The name of the execution, same as that of StartExecution. Default: - None
        :param s3_input_bucket: location of input S3 objects - if left empty will generate rule for s3 access to all [*].
        :param s3_input_prefix: prefix for input S3 objects - if left empty will generate rule for s3 access to all [*].
        :param textract_state_machine_timeout_minutes: how long can we wait for the process (default is 48 hours (60*48=2880)).
        :param workflow_tracing_enabled: 
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: - ``IntegrationPattern.REQUEST_RESPONSE`` for most tasks. ``IntegrationPattern.RUN_JOB`` for the following exceptions: ``BatchSubmitJob``, ``EmrAddStep``, ``EmrCreateCluster``, ``EmrTerminationCluster``, and ``EmrContainersStartJobRun``.
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param result_selector: The JSON that will replace the state's raw result and become the effective result before ResultPath is applied. You can use ResultSelector to create a payload with values that are static or selected from the state's raw result. Default: - None
        :param timeout: Timeout for the state machine. Default: - None
        '''
        props = TextractGenericSyncSfnTaskProps(
            s3_output_bucket=s3_output_bucket,
            s3_output_prefix=s3_output_prefix,
            associate_with_parent=associate_with_parent,
            custom_function=custom_function,
            enable_dashboard=enable_dashboard,
            enable_monitoring=enable_monitoring,
            input=input,
            lambda_log_level=lambda_log_level,
            name=name,
            s3_input_bucket=s3_input_bucket,
            s3_input_prefix=s3_input_prefix,
            textract_state_machine_timeout_minutes=textract_state_machine_timeout_minutes,
            workflow_tracing_enabled=workflow_tracing_enabled,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            result_selector=result_selector,
            timeout=timeout,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        return typing.cast(typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig], jsii.get(self, "taskMetrics"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]], jsii.get(self, "taskPolicies"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dashboardName")
    def dashboard_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dashboardName"))

    @dashboard_name.setter
    def dashboard_name(self, value: builtins.str) -> None:
        jsii.set(self, "dashboardName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="putOnSQSLambdaLogGroup")
    def put_on_sqs_lambda_log_group(self) -> aws_cdk.aws_logs.ILogGroup:
        return typing.cast(aws_cdk.aws_logs.ILogGroup, jsii.get(self, "putOnSQSLambdaLogGroup"))

    @put_on_sqs_lambda_log_group.setter
    def put_on_sqs_lambda_log_group(self, value: aws_cdk.aws_logs.ILogGroup) -> None:
        jsii.set(self, "putOnSQSLambdaLogGroup", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stateMachine")
    def state_machine(self) -> aws_cdk.aws_stepfunctions.IStateMachine:
        return typing.cast(aws_cdk.aws_stepfunctions.IStateMachine, jsii.get(self, "stateMachine"))

    @state_machine.setter
    def state_machine(self, value: aws_cdk.aws_stepfunctions.IStateMachine) -> None:
        jsii.set(self, "stateMachine", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="textractPutOnSQSFunction")
    def textract_put_on_sqs_function(self) -> aws_cdk.aws_lambda.IFunction:
        return typing.cast(aws_cdk.aws_lambda.IFunction, jsii.get(self, "textractPutOnSQSFunction"))

    @textract_put_on_sqs_function.setter
    def textract_put_on_sqs_function(self, value: aws_cdk.aws_lambda.IFunction) -> None:
        jsii.set(self, "textractPutOnSQSFunction", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="textractSyncCallFunction")
    def textract_sync_call_function(self) -> aws_cdk.aws_lambda.IFunction:
        return typing.cast(aws_cdk.aws_lambda.IFunction, jsii.get(self, "textractSyncCallFunction"))

    @textract_sync_call_function.setter
    def textract_sync_call_function(self, value: aws_cdk.aws_lambda.IFunction) -> None:
        jsii.set(self, "textractSyncCallFunction", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="textractSyncLambdaLogGroup")
    def textract_sync_lambda_log_group(self) -> aws_cdk.aws_logs.ILogGroup:
        return typing.cast(aws_cdk.aws_logs.ILogGroup, jsii.get(self, "textractSyncLambdaLogGroup"))

    @textract_sync_lambda_log_group.setter
    def textract_sync_lambda_log_group(self, value: aws_cdk.aws_logs.ILogGroup) -> None:
        jsii.set(self, "textractSyncLambdaLogGroup", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="textractSyncSQS")
    def textract_sync_sqs(self) -> aws_cdk.aws_sqs.IQueue:
        return typing.cast(aws_cdk.aws_sqs.IQueue, jsii.get(self, "textractSyncSQS"))

    @textract_sync_sqs.setter
    def textract_sync_sqs(self, value: aws_cdk.aws_sqs.IQueue) -> None:
        jsii.set(self, "textractSyncSQS", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        jsii.set(self, "version", value)


@jsii.data_type(
    jsii_type="schadem-cdk-construct-textract-generic-sync.TextractGenericSyncSfnTaskProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "result_selector": "resultSelector",
        "timeout": "timeout",
        "s3_output_bucket": "s3OutputBucket",
        "s3_output_prefix": "s3OutputPrefix",
        "associate_with_parent": "associateWithParent",
        "custom_function": "customFunction",
        "enable_dashboard": "enableDashboard",
        "enable_monitoring": "enableMonitoring",
        "input": "input",
        "lambda_log_level": "lambdaLogLevel",
        "name": "name",
        "s3_input_bucket": "s3InputBucket",
        "s3_input_prefix": "s3InputPrefix",
        "textract_state_machine_timeout_minutes": "textractStateMachineTimeoutMinutes",
        "workflow_tracing_enabled": "workflowTracingEnabled",
    },
)
class TextractGenericSyncSfnTaskProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        result_selector: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
        s3_output_bucket: builtins.str,
        s3_output_prefix: builtins.str,
        associate_with_parent: typing.Optional[builtins.bool] = None,
        custom_function: typing.Optional[aws_cdk.aws_stepfunctions_tasks.LambdaInvoke] = None,
        enable_dashboard: typing.Optional[builtins.bool] = None,
        enable_monitoring: typing.Optional[builtins.bool] = None,
        input: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        lambda_log_level: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        s3_input_bucket: typing.Optional[builtins.str] = None,
        s3_input_prefix: typing.Optional[builtins.str] = None,
        textract_state_machine_timeout_minutes: typing.Optional[jsii.Number] = None,
        workflow_tracing_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: - ``IntegrationPattern.REQUEST_RESPONSE`` for most tasks. ``IntegrationPattern.RUN_JOB`` for the following exceptions: ``BatchSubmitJob``, ``EmrAddStep``, ``EmrCreateCluster``, ``EmrTerminationCluster``, and ``EmrContainersStartJobRun``.
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param result_selector: The JSON that will replace the state's raw result and become the effective result before ResultPath is applied. You can use ResultSelector to create a payload with values that are static or selected from the state's raw result. Default: - None
        :param timeout: Timeout for the state machine. Default: - None
        :param s3_output_bucket: 
        :param s3_output_prefix: The prefix to use for the output files.
        :param associate_with_parent: Pass the execution ID from the context object to the execution input. This allows the Step Functions UI to link child executions from parent executions, making it easier to trace execution flow across state machines. If you set this property to ``true``, the ``input`` property must be an object (provided by ``sfn.TaskInput.fromObject``) or omitted entirely. Default: - false
        :param custom_function: not implemented yet.
        :param enable_dashboard: not implemented yet.
        :param enable_monitoring: not implemented yet.
        :param input: The JSON input for the execution, same as that of StartExecution. Default: - The state input (JSON path '$')
        :param lambda_log_level: The prefix to use for the output files.
        :param name: The name of the execution, same as that of StartExecution. Default: - None
        :param s3_input_bucket: location of input S3 objects - if left empty will generate rule for s3 access to all [*].
        :param s3_input_prefix: prefix for input S3 objects - if left empty will generate rule for s3 access to all [*].
        :param textract_state_machine_timeout_minutes: how long can we wait for the process (default is 48 hours (60*48=2880)).
        :param workflow_tracing_enabled: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "s3_output_bucket": s3_output_bucket,
            "s3_output_prefix": s3_output_prefix,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if result_selector is not None:
            self._values["result_selector"] = result_selector
        if timeout is not None:
            self._values["timeout"] = timeout
        if associate_with_parent is not None:
            self._values["associate_with_parent"] = associate_with_parent
        if custom_function is not None:
            self._values["custom_function"] = custom_function
        if enable_dashboard is not None:
            self._values["enable_dashboard"] = enable_dashboard
        if enable_monitoring is not None:
            self._values["enable_monitoring"] = enable_monitoring
        if input is not None:
            self._values["input"] = input
        if lambda_log_level is not None:
            self._values["lambda_log_level"] = lambda_log_level
        if name is not None:
            self._values["name"] = name
        if s3_input_bucket is not None:
            self._values["s3_input_bucket"] = s3_input_bucket
        if s3_input_prefix is not None:
            self._values["s3_input_prefix"] = s3_input_prefix
        if textract_state_machine_timeout_minutes is not None:
            self._values["textract_state_machine_timeout_minutes"] = textract_state_machine_timeout_minutes
        if workflow_tracing_enabled is not None:
            self._values["workflow_tracing_enabled"] = workflow_tracing_enabled

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''An optional description for this state.

        :default: - No comment
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.Duration]:
        '''Timeout for the heartbeat.

        :default: - None
        '''
        result = self._values.get("heartbeat")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        '''JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        '''
        result = self._values.get("input_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        '''AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default:

        - ``IntegrationPattern.REQUEST_RESPONSE`` for most tasks.
        ``IntegrationPattern.RUN_JOB`` for the following exceptions:
        ``BatchSubmitJob``, ``EmrAddStep``, ``EmrCreateCluster``, ``EmrTerminationCluster``, and ``EmrContainersStartJobRun``.

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        '''
        result = self._values.get("integration_pattern")
        return typing.cast(typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern], result)

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        '''JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        '''
        result = self._values.get("output_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        '''JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        '''
        result = self._values.get("result_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def result_selector(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''The JSON that will replace the state's raw result and become the effective result before ResultPath is applied.

        You can use ResultSelector to create a payload with values that are static
        or selected from the state's raw result.

        :default: - None

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/input-output-inputpath-params.html#input-output-resultselector
        '''
        result = self._values.get("result_selector")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.Duration]:
        '''Timeout for the state machine.

        :default: - None
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

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
    def associate_with_parent(self) -> typing.Optional[builtins.bool]:
        '''Pass the execution ID from the context object to the execution input.

        This allows the Step Functions UI to link child executions from parent executions, making it easier to trace execution flow across state machines.

        If you set this property to ``true``, the ``input`` property must be an object (provided by ``sfn.TaskInput.fromObject``) or omitted entirely.

        :default: - false

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/concepts-nested-workflows.html#nested-execution-startid
        '''
        result = self._values.get("associate_with_parent")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def custom_function(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions_tasks.LambdaInvoke]:
        '''not implemented yet.'''
        result = self._values.get("custom_function")
        return typing.cast(typing.Optional[aws_cdk.aws_stepfunctions_tasks.LambdaInvoke], result)

    @builtins.property
    def enable_dashboard(self) -> typing.Optional[builtins.bool]:
        '''not implemented yet.'''
        result = self._values.get("enable_dashboard")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_monitoring(self) -> typing.Optional[builtins.bool]:
        '''not implemented yet.'''
        result = self._values.get("enable_monitoring")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def input(self) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]:
        '''The JSON input for the execution, same as that of StartExecution.

        :default: - The state input (JSON path '$')

        :see: https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[aws_cdk.aws_stepfunctions.TaskInput], result)

    @builtins.property
    def lambda_log_level(self) -> typing.Optional[builtins.str]:
        '''The prefix to use for the output files.'''
        result = self._values.get("lambda_log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the execution, same as that of StartExecution.

        :default: - None

        :see: https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_input_bucket(self) -> typing.Optional[builtins.str]:
        '''location of input S3 objects - if left empty will generate rule for s3 access to all [*].'''
        result = self._values.get("s3_input_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_input_prefix(self) -> typing.Optional[builtins.str]:
        '''prefix for input S3 objects - if left empty will generate rule for s3 access to all [*].'''
        result = self._values.get("s3_input_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def textract_state_machine_timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''how long can we wait for the process (default is 48 hours (60*48=2880)).'''
        result = self._values.get("textract_state_machine_timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def workflow_tracing_enabled(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("workflow_tracing_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TextractGenericSyncSfnTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "TextractGenericSyncSfnTask",
    "TextractGenericSyncSfnTaskProps",
]

publication.publish()

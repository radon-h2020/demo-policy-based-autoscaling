# demo-policy-based-autoscaling
Auto-Scaling of VM instances with and without CSAR using Prometheus and Orchestrator

# autoscaling-with-csar
This folder containts source codes of auto-scaling of VM instances with CSAR using Prometheus and xOpera Orchestrator. The orchestrator is used to deploy an application on the run-time environment by enforcing the state described by the application blueprint (CSAR) onto the target cloud provider. The Prometheus server fetches the run-time metrics from the running cloud instances to measure their current states and the Alertmanager generates an alert to the auto-scaler agent endpoint based on the rules defined in the Prometheus server. The auto-scaler agent receives the notifications from the Alertmanager, takes a scaling-up/scaling-down decision and deploy/undeploy an instance in the cloud infrastructure using the help of the orchestrator.


# autoscaling-without-csar
This folder containts source codes of auto-scaling of VM instances without CSAR using Prometheus and xOpera Orchestrator. This policy automatically scale the services by modifying their TOSCA service template with an autoscaler agent, which utilizes RADON monitoring tool (Prometheus and Alertmanager) to receive scaling related events, modifies the service template to scale it up or down as required.

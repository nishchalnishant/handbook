# 4-Year DevOps, MLOps, and Cloud Interview Glossary

This glossary focuses on terms that are realistic for a 4-year DevOps, Cloud, Kubernetes, Terraform, and MLOps interview. The goal is not to memorize every tool name, but to explain important concepts with production context, common mistakes, and interview-ready talking points.

## How to Use This File

For each term, be able to answer:

- What problem does it solve?
- Where have you seen or used it in a real system?
- What can go wrong with it?
- How would you troubleshoot it?

## DevOps and CI/CD

### CI/CD Pipeline

A CI/CD pipeline is an automated workflow that takes code from commit to build, test, scan, package, deploy, and verification. In interviews, explain that CI validates code quality early, while CD makes releases predictable and repeatable.

For 4 years of experience, you should know typical stages: checkout, dependency install, unit tests, static analysis, container build, image scan, artifact push, deployment, smoke test, and rollback. A strong answer mentions that pipelines should produce immutable artifacts and promote the same artifact across environments instead of rebuilding separately for dev, staging, and production.

Common failure points include flaky tests, slow builds, missing secrets, environment drift, bad deployment permissions, and lack of rollback strategy.

### Artifact

An artifact is the output of a build process. It can be a Docker image, JAR, binary, Helm chart, Terraform plan, Python wheel, or ML model file. In good delivery systems, artifacts are versioned, traceable to a commit, scanned, and stored in an artifact repository.

Interviewers often check whether you understand that production should deploy a known artifact, not rebuild source code directly on the server. This improves reproducibility and makes rollback easier.

### Immutable Deployment

Immutable deployment means you do not patch running servers or containers manually. Instead, every change creates a new versioned artifact or infrastructure instance. If something fails, you replace it with a known-good version.

This is important in cloud and Kubernetes because containers are expected to be disposable. A common anti-pattern is SSHing into a pod or VM to fix production manually without capturing the change in code.

### Blue-Green Deployment

Blue-green deployment uses two production-like environments. One environment serves live traffic, while the other receives the new version. After validation, traffic is switched to the new environment.

The benefit is fast rollback: switch traffic back to the previous environment. The tradeoff is cost and complexity because two environments or two sets of workloads may need to run at the same time.

### Canary Deployment

Canary deployment gradually sends a small percentage of traffic to a new version before a full rollout. For example, 5%, then 25%, then 50%, then 100%, while monitoring error rate, latency, and business metrics.

A good interview answer mentions automated analysis using metrics from Prometheus, Datadog, CloudWatch, or Azure Monitor. Canary is safer than a big-bang deployment, but it requires good observability and traffic splitting.

### Rollback vs Roll Forward

Rollback means returning to a previous known-good version. Roll forward means deploying a new fix that corrects the issue. In Kubernetes, rollback can be done with Deployment revision history, Helm rollback, or GitOps reverting to a previous Git commit.

In interviews, do not say rollback is always the answer. If a database migration is involved, rollback may be risky. In such cases, backward-compatible changes and roll-forward fixes are often safer.

### Feature Flag

A feature flag allows functionality to be turned on or off without deploying new code. It separates deployment from release. Teams can deploy code safely and enable features only for specific users, regions, or percentages of traffic.

The risk is flag debt. Old flags must be removed, or the codebase becomes complex. Interviewers may ask how feature flags help canary releases, A/B testing, and emergency kill switches.

### DORA Metrics

DORA metrics measure software delivery performance:

- Deployment frequency
- Lead time for changes
- Change failure rate
- Mean time to recovery

For a 4-year engineer, the key is knowing how these metrics reflect engineering health. High deployment frequency is not useful if change failure rate is also high. MTTR improves when teams have good observability, rollback, ownership, and incident response.

### Idempotency

Idempotency means running the same operation multiple times produces the same final result. This matters in automation, Terraform, Ansible, CI/CD, APIs, and retry logic.

Example: creating a user should not create duplicate users if the same request is retried. In infrastructure, applying the same Terraform configuration repeatedly should not keep changing resources.

### Environment Drift

Environment drift happens when actual infrastructure or configuration differs from what is declared in code. This can happen when someone changes cloud resources manually, patches servers directly, or modifies Kubernetes objects outside GitOps.

Drift causes "works in staging but fails in production" problems. Terraform plan, Argo CD OutOfSync status, and configuration audits help detect drift.

## Git and Source Control

### Branching Strategy

A branching strategy defines how teams organize code changes. Common models include trunk-based development, GitFlow, and release branches.

At 4 years of experience, you should explain tradeoffs. Trunk-based development supports frequent integration and faster CI/CD, but needs strong automated tests and feature flags. GitFlow can work for scheduled releases but may create long-lived branches and painful merges.

### Pull Request

A pull request is a review and collaboration mechanism before merging code. It usually triggers CI checks, code review, security scanning, and policy validation.

A good interview answer mentions branch protection rules, required approvals, status checks, CODEOWNERS, and small PRs. Large PRs increase review risk and delay feedback.

### Git Rebase vs Merge

Merge preserves branch history and creates a merge commit. Rebase rewrites commits on top of another branch to create a linear history.

In interviews, mention that rebase is useful for cleaning local feature branch history, but should be used carefully on shared branches because it rewrites history. Merge is safer for preserving collaboration history.

### Semantic Versioning

Semantic versioning uses `MAJOR.MINOR.PATCH`. Major means breaking change, minor means backward-compatible feature, patch means backward-compatible bug fix.

This matters for APIs, Helm charts, Terraform modules, libraries, and container releases. Interviewers may expect you to connect versioning with rollback, compatibility, and release notes.

## Docker and Containers

### Container

A container is an isolated process with its own filesystem, dependencies, environment, and runtime configuration. Containers use Linux kernel features such as namespaces and cgroups.

Containers are not lightweight virtual machines. They share the host kernel. This matters for security, resource isolation, and debugging.

### Docker Image

A Docker image is a layered, read-only package used to start containers. It contains application code, dependencies, runtime, and metadata.

In interviews, mention image tags versus image digests. Tags like `latest` are mutable and risky. Digests are immutable and better for reproducible deployments.

### Multi-Stage Docker Build

Multi-stage builds separate build-time dependencies from runtime images. For example, compile code in one stage and copy only the final binary into a small runtime image.

Benefits include smaller images, faster pulls, reduced attack surface, and fewer vulnerabilities. This is a very common practical interview topic.

### Dockerfile Best Practices

Important practices include using small base images, pinning versions, avoiding secrets in image layers, using `.dockerignore`, running as non-root, reducing layers where useful, and using multi-stage builds.

A strong answer also mentions caching. Put rarely changing dependency installation steps before frequently changing application code to speed up builds.

### Container Runtime

A container runtime starts and manages containers. Examples include containerd and CRI-O. Docker uses containerd underneath, while Kubernetes talks to runtimes through the Container Runtime Interface.

Interviewers may ask this to check whether you understand that Kubernetes does not need Docker specifically to run containers.

### Image Vulnerability Scanning

Image scanning checks container images for known CVEs, vulnerable packages, secrets, and misconfigurations. Tools include Trivy, Grype, Snyk, Prisma, and cloud-native scanners.

Scanning should happen in CI before deployment, but runtime patching still matters because new CVEs are discovered after images are built.

## Kubernetes

### Pod

A pod is the smallest deployable unit in Kubernetes. It can contain one or more containers sharing the same network namespace, IP address, and volumes.

Most application pods have one main container. Sidecars are used for helpers like proxies, log shippers, or service mesh containers. Interviewers often ask why Kubernetes uses pods instead of directly scheduling containers: the pod provides a shared execution context.

### Deployment

A Deployment manages stateless applications using ReplicaSets. It handles rolling updates, rollbacks, and desired replica count.

For interviews, know how rolling update works with `maxSurge` and `maxUnavailable`. Also know that Deployments are not ideal for workloads needing stable network identity or persistent ordered startup; StatefulSets are better there.

### StatefulSet

A StatefulSet manages stateful workloads that need stable pod names, stable network identity, and persistent storage. Examples include databases, Kafka, and ZooKeeper-like systems.

Unlike Deployments, StatefulSet pods have predictable names like `mysql-0`, `mysql-1`. Scaling and rollout happen in ordered fashion by default.

### DaemonSet

A DaemonSet ensures one pod runs on every matching node. Common examples are log collectors, monitoring agents, CNI agents, security agents, and storage daemons.

If a new node joins the cluster, the DaemonSet automatically schedules a pod there. This is commonly asked in operations interviews.

### Service

A Kubernetes Service provides a stable virtual endpoint for a set of pods. Since pods are ephemeral and IPs change, Services allow clients to reach pods through a stable name and IP.

Important types are ClusterIP, NodePort, LoadBalancer, and Headless. You should know that Services select pods using labels.

### Ingress

Ingress exposes HTTP/HTTPS routes from outside the cluster to internal Services. It usually handles host-based and path-based routing.

Ingress requires an Ingress Controller such as NGINX, Kong, ALB Controller, Traefik, or HAProxy. Creating an Ingress object alone does nothing unless a controller is installed.

### Gateway API

Gateway API is a newer Kubernetes networking API designed to be more expressive than Ingress. It separates infrastructure ownership from application routing using resources like Gateway, GatewayClass, and HTTPRoute.

For interviews, it is enough to say Gateway API is useful for advanced routing, multi-team ownership, and more consistent traffic management across implementations.

### ConfigMap and Secret

ConfigMaps store non-sensitive configuration. Secrets store sensitive values such as passwords, tokens, and certificates.

Important interview point: Kubernetes Secrets are base64-encoded, not automatically secure encryption by themselves. In production, use encryption at rest, RBAC, external secret stores, and avoid exposing secrets through logs or environment dumps.

### Readiness, Liveness, and Startup Probes

Readiness probe decides whether a pod should receive traffic. Liveness probe decides whether a container should be restarted. Startup probe gives slow-starting applications extra time before liveness checks begin.

A common mistake is using liveness probes too aggressively, causing healthy but slow services to restart repeatedly. Readiness should fail when the app cannot safely serve traffic, such as missing DB connectivity or incomplete warmup.

### Requests and Limits

Requests define guaranteed CPU and memory used by the scheduler. Limits define the maximum resources a container can consume.

If memory exceeds the limit, the container can be OOMKilled. CPU limits throttle usage. A strong answer mentions that incorrect requests cause poor scheduling, while incorrect limits can create performance issues.

### HPA

Horizontal Pod Autoscaler scales pod replicas based on metrics such as CPU, memory, or custom metrics. HPA needs metrics-server for CPU/memory and adapters for custom metrics.

Interviewers may ask why HPA is not scaling. Possible causes: missing metrics-server, wrong resource requests, bad metric target, pending pods due to cluster capacity, or cooldown behavior.

### Cluster Autoscaler

Cluster Autoscaler adds or removes nodes based on pending pods and underutilized nodes. It works at the node level, while HPA works at the pod level.

A good answer explains the relationship: HPA may create more pods, then Cluster Autoscaler adds nodes if those pods cannot be scheduled.

### RBAC

RBAC controls who can perform actions on Kubernetes resources. It uses Roles, ClusterRoles, RoleBindings, and ClusterRoleBindings.

For interviews, know the difference between namespace-scoped Role and cluster-scoped ClusterRole. Also mention least privilege and avoiding broad permissions like `cluster-admin`.

### ServiceAccount

A ServiceAccount is the identity used by pods to interact with the Kubernetes API or cloud services through workload identity mechanisms.

In cloud Kubernetes, ServiceAccounts often integrate with IAM, such as IRSA on EKS or Workload Identity on GKE/AKS. This avoids storing cloud access keys inside pods.

### NetworkPolicy

NetworkPolicy controls pod-to-pod and pod-to-external traffic. It is used to enforce least-privilege networking inside the cluster.

A key interview detail: NetworkPolicy only works if the CNI plugin supports it. Also, once a pod is selected by an ingress policy, only allowed ingress traffic is permitted. Default-deny policies are common in production.

### CNI

CNI is the plugin standard for Kubernetes networking. It gives pods IP addresses and connects them to the cluster network.

Examples include Calico, Cilium, Flannel, Weave, and cloud-provider CNIs. CNI choice affects network policy, performance, observability, and IP address management.

### CSI

CSI is the plugin standard for Kubernetes storage. It lets Kubernetes consume storage systems such as EBS, Azure Disk, GCE Persistent Disk, EFS, and Ceph.

Interviewers may expect you to know PersistentVolume, PersistentVolumeClaim, StorageClass, reclaim policy, and dynamic provisioning.

### CrashLoopBackOff

CrashLoopBackOff means a container repeatedly starts, crashes, and Kubernetes backs off before restarting it again.

Troubleshooting steps: check pod events, container logs, previous logs, command/entrypoint, environment variables, mounted secrets/config, resource limits, health probes, and dependency connectivity.

### ImagePullBackOff

ImagePullBackOff means Kubernetes cannot pull the container image. Causes include wrong image name/tag, missing registry credentials, network issue, private registry auth failure, or image not existing.

Troubleshooting includes `kubectl describe pod`, checking imagePullSecrets, registry permissions, and whether nodes can reach the registry.

### Helm Chart

A Helm chart is a package of Kubernetes templates and default values. It helps install and manage complex Kubernetes applications.

For interviews, know chart, release, values.yaml, templates, dependencies, and rollback. Also mention that Helm can create hard-to-debug templates if values are not managed carefully.

## Terraform and Infrastructure as Code

### Infrastructure as Code

Infrastructure as Code means managing infrastructure using versioned code instead of manual console changes. It improves repeatability, reviewability, and disaster recovery.

Tools include Terraform, CloudFormation, Bicep, Pulumi, and Crossplane. The key idea is declarative desired state and automation.

### Terraform State

Terraform state maps your configuration to real infrastructure resources. Without state, Terraform cannot know what it manages.

This is one of the most important Terraform interview topics. State should be stored remotely for teams, protected, encrypted, backed up, and locked during operations. Never casually edit state manually.

### Terraform Backend

A backend defines where Terraform stores state. Examples include S3 with DynamoDB locking, Azure Storage, GCS, and Terraform Cloud.

For team environments, local state is risky because others cannot safely collaborate and state may be lost.

### Terraform Plan

Terraform plan shows the changes Terraform intends to make before applying them. It is used for review and safety.

In CI/CD, pull requests often run `terraform plan` and post output for review. Production applies should usually be controlled, approved, and use the reviewed plan where possible.

### Terraform Module

A module is reusable Terraform configuration. Teams use modules to standardize VPCs, Kubernetes clusters, IAM roles, databases, and monitoring.

Good modules expose useful variables, sensible defaults, outputs, and versioning. Bad modules expose too many internals or hide critical behavior.

### Terraform Drift

Terraform drift happens when real infrastructure changes outside Terraform. Example: someone modifies a security group rule manually in the cloud console.

Drift is detected through `terraform plan`, scheduled drift checks, or platform tools. Mature teams avoid manual changes except emergencies and backport emergency fixes into code.

### Terraform Workspaces

Terraform workspaces allow multiple state files for the same configuration. They are sometimes used for environments such as dev and prod.

Interview nuance: workspaces are not always the best environment strategy. Separate directories, separate backends, or Terragrunt may be clearer for production-grade separation.

### Ansible

Ansible is agentless automation used for configuration management, provisioning, patching, and orchestration. It connects over SSH or WinRM and applies tasks from playbooks.

Compared with Terraform, Ansible is often better for configuring operating systems and applications, while Terraform is better for provisioning infrastructure. In practice, teams may use both.

## Cloud Engineering

### VPC / VNet

A VPC or VNet is an isolated cloud network where you define subnets, route tables, gateways, firewall rules, and connectivity.

For interviews, be ready to design public and private subnets, NAT, load balancers, database isolation, peering, VPN, and private endpoints.

### Public and Private Subnets

A public subnet has a route to the internet gateway and can host internet-facing load balancers or bastion hosts. A private subnet does not allow direct inbound internet access and is used for application servers, databases, and internal services.

Private resources often use NAT Gateway for outbound internet access, such as pulling patches or container images.

### Security Group

A security group is a stateful virtual firewall attached to cloud resources. In AWS, if inbound traffic is allowed, return traffic is automatically allowed.

A common interview scenario is debugging connectivity by checking route tables, security groups, NACLs, DNS, service listening port, and application health.

### IAM

IAM manages identities and permissions. It includes users, groups, roles, policies, service principals, and workload identities depending on cloud provider.

Strong answers mention least privilege, role-based access, short-lived credentials, MFA for humans, no hardcoded keys, and audit logs.

### Managed Kubernetes

Managed Kubernetes services such as EKS, AKS, and GKE provide a cloud-managed control plane while users manage worker nodes, workloads, networking, security, and add-ons.

Do not say managed Kubernetes means no operations. Teams still handle upgrades, node pools, autoscaling, ingress, observability, security, cost, and workload reliability.

### Load Balancer

A load balancer distributes traffic across multiple backends. Cloud load balancers can operate at Layer 4 or Layer 7.

In Kubernetes, a Service of type LoadBalancer can provision a cloud load balancer. Ingress controllers often use load balancers as their external entry point.

### Object Storage

Object storage such as S3, Azure Blob, or GCS stores files as objects in buckets or containers. It is used for backups, logs, artifacts, data lakes, Terraform state, and ML datasets.

Important points include versioning, lifecycle rules, encryption, access policies, public access blocking, and replication.

### KMS

KMS manages encryption keys for cloud resources. It is commonly used for encrypting disks, object storage, databases, secrets, and Terraform state.

Interviewers may check whether you understand envelope encryption, key rotation, IAM access to keys, and auditability.

### Multi-Cloud

Multi-cloud means using more than one cloud provider, such as AWS and Azure. It can reduce vendor lock-in or satisfy business requirements, but it increases operational complexity.

A practical answer should mention identity differences, networking complexity, monitoring fragmentation, cost management, and the need for common IaC and platform standards.

## Observability and SRE

### Observability

Observability is the ability to understand system behavior from outputs such as metrics, logs, and traces. Monitoring tells you when something known is wrong; observability helps investigate unknown failures.

For interviews, connect observability to faster incident response, better deployments, SLOs, and capacity planning.

### Metrics, Logs, and Traces

Metrics are numeric time-series data, logs are event records, and traces show request flow across services.

Good troubleshooting uses all three. Metrics show the symptom, logs provide context, and traces reveal where latency or errors occur across distributed services.

### Prometheus

Prometheus collects metrics by scraping endpoints and stores time-series data. It uses PromQL for querying and Alertmanager for alert routing.

Interview topics include exporters, scrape targets, labels, recording rules, alert rules, high-cardinality problems, and retention.

### Grafana

Grafana visualizes metrics, logs, and traces through dashboards. It commonly integrates with Prometheus, Loki, Elasticsearch/OpenSearch, Tempo, CloudWatch, and Azure Monitor.

Interviewers may ask what makes a good dashboard. A useful dashboard shows service health, latency, traffic, errors, saturation, dependencies, and deployment markers.

### SLI, SLO, and SLA

An SLI is a measured reliability indicator, such as request success rate or latency. An SLO is the target for that indicator, such as 99.9% success. An SLA is a contractual promise, often with penalties.

A strong answer includes error budgets. If the service is burning error budget too fast, teams should reduce risky releases and focus on reliability.

### Alert Fatigue

Alert fatigue happens when teams receive too many noisy or low-value alerts. This causes real incidents to be missed.

Good alerts should be actionable, user-impacting, routed to the right team, and tied to SLOs where possible. Avoid alerting on every low-level metric without context.

### Incident Management

Incident management is the process for detecting, responding to, communicating, mitigating, and learning from production incidents.

At this experience level, know roles like incident commander, communications owner, and subject matter experts. Also know the value of blameless postmortems and action items.

### Postmortem

A postmortem is a structured review after an incident. It explains timeline, impact, root cause, contributing factors, detection gaps, and prevention actions.

A good postmortem is blameless. The purpose is improving systems, not blaming people.

## DevSecOps

### SAST

Static Application Security Testing scans source code or compiled code without running the application. It finds issues such as injection risk, insecure APIs, hardcoded secrets, and unsafe patterns.

SAST is useful early in CI, but it can produce false positives. Teams should tune rules and focus on meaningful findings.

### DAST

Dynamic Application Security Testing scans a running application from the outside. It can find runtime issues such as authentication flaws, insecure headers, injection, and exposed endpoints.

DAST usually runs later than SAST because it needs a deployed environment. It complements but does not replace code scanning.

### SBOM

An SBOM lists the software components inside an application or image. It helps teams understand dependency risk when new vulnerabilities are disclosed.

SBOMs are increasingly important in supply chain security. They should be generated during builds and associated with artifacts.

### Secret Management

Secret management is the secure storage, access, rotation, and auditing of credentials such as passwords, tokens, certificates, and API keys.

Tools include HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager, External Secrets Operator, and Sealed Secrets. Avoid storing secrets in Git, images, plain environment dumps, or CI logs.

### Policy as Code

Policy as Code means defining security and compliance rules in code and enforcing them automatically. Examples include OPA, Kyverno, Sentinel, and cloud policy tools.

Common policies include blocking privileged containers, requiring labels, enforcing image registries, requiring encryption, and preventing public storage buckets.

## API Gateway and Kong

### API Gateway

An API gateway is a controlled entry point for APIs. It handles routing, authentication, rate limiting, TLS, request transformation, logging, and traffic policies.

In interviews, explain the difference between an API gateway and a load balancer. A load balancer distributes traffic, while an API gateway understands API-level concerns like paths, consumers, tokens, quotas, and transformations.

### Kong Gateway

Kong Gateway is an API gateway built on NGINX/OpenResty with a plugin architecture. It can run in traditional, DB-less, or hybrid mode.

For a Kong-related interview, know Services, Routes, Consumers, Plugins, Upstreams, Targets, Admin API, `deck`, and Kong Ingress Controller.

### Kong Route and Service

In Kong, a Service represents the upstream backend API. A Route defines how client requests match and get forwarded to that Service.

Example: requests to `/payments` on `api.example.com` match a Route, then Kong forwards them to the payment Service upstream.

### Kong Plugin

A Kong plugin adds behavior during the request or response lifecycle. Examples include JWT auth, key auth, rate limiting, request transformation, CORS, logging, and Prometheus metrics.

Interviewers may ask where plugins run. Many important checks happen in the access phase before the request reaches the upstream.

### Rate Limiting

Rate limiting restricts request volume by consumer, IP, route, or service. It protects backends from abuse, cost spikes, and accidental overload.

In distributed systems, local in-memory counters may be inaccurate across multiple gateway nodes. Redis-backed or centralized counters give better consistency but add dependency and latency.

### mTLS

mTLS means both client and server authenticate each other using certificates. It is used for service-to-service security, gateway-to-upstream security, and zero-trust architectures.

Common troubleshooting areas include expired certificates, wrong CA trust chain, incorrect SAN, SNI mismatch, and clock skew.

## GitOps and Platform Engineering

### GitOps

GitOps uses Git as the source of truth for infrastructure and application desired state. A controller such as Argo CD continuously reconciles cluster state with Git.

Benefits include auditability, pull-request review, drift detection, and easy rollback by reverting commits. Risks include poor secret handling, unclear repo structure, and uncontrolled auto-sync.

### Argo CD

Argo CD is a Kubernetes GitOps controller. It watches Git repositories and applies manifests, Helm charts, or Kustomize overlays to clusters.

Important terms include Application, sync, health, OutOfSync, prune, self-heal, project, and App of Apps.

### Internal Developer Platform

An Internal Developer Platform gives teams self-service workflows for creating services, deploying apps, viewing ownership, managing environments, and following golden paths.

At 4 years, you should understand that platform engineering is not just tooling. It is about reducing cognitive load for developers while keeping security, reliability, and compliance built in.

### Backstage

Backstage is a developer portal framework. It is commonly used for service catalogs, documentation, templates, ownership, scorecards, and golden paths.

Interviewers may ask how it helps operations. It improves discoverability: who owns a service, where its repo is, what dashboards exist, what APIs it exposes, and how healthy it is.

## MLOps

### MLOps

MLOps applies DevOps practices to machine learning systems, but with extra concerns around data, models, experiments, drift, and governance.

Unlike normal software, ML behavior depends heavily on data quality and model performance. A model can degrade even if the code and infrastructure do not change.

### ML Pipeline

An ML pipeline automates steps such as data extraction, validation, feature engineering, training, evaluation, registration, deployment, and monitoring.

For interviews, explain the difference between CI/CD and CT. Continuous training retrains models when code, data, schedule, or performance triggers require it.

### Feature Store

A feature store is a central system for managing reusable ML features. It helps ensure training and serving use consistent feature definitions.

Feature stores usually have offline storage for training and online storage for low-latency inference. They reduce training-serving skew.

### Experiment Tracking

Experiment tracking records model runs, parameters, metrics, code versions, datasets, and artifacts. Tools include MLflow, Weights & Biases, Neptune, and SageMaker Experiments.

This matters because ML work involves many trials. Without tracking, teams cannot reproduce why one model performed better than another.

### Model Registry

A model registry stores versioned models and metadata. It tracks lifecycle stages such as staging, production, archived, or rejected.

In interviews, connect registry to approval workflows, reproducibility, rollback, and governance.

### Model Serving

Model serving exposes trained models for inference. This can be real-time API serving, batch inference, streaming inference, or embedded inference.

Important production concerns include latency, throughput, scaling, model loading time, GPU usage, request validation, and fallback behavior.

### Data Drift

Data drift means production input data distribution changes compared to training data. Example: customer behavior changes, new region traffic appears, or upstream data format changes.

Data drift does not always mean the model is wrong, but it is a warning sign. It should trigger investigation, monitoring, and possibly retraining.

### Concept Drift

Concept drift means the relationship between inputs and outputs changes. For example, fraud patterns change, so old features no longer predict fraud accurately.

Concept drift is harder than data drift because labels may arrive late. Monitoring business outcomes and delayed ground truth is important.

### Training-Serving Skew

Training-serving skew happens when features are calculated differently during training and production inference. This causes models to perform well offline but poorly in production.

Feature stores, shared transformation code, data validation, and shadow testing help reduce skew.

### Model Monitoring

Model monitoring tracks both service health and model quality. Service metrics include latency, error rate, saturation, and throughput. Model metrics include prediction distribution, drift, accuracy, precision, recall, and business KPIs.

A strong answer mentions that labels may not be immediately available, so proxy metrics and delayed evaluation are often needed.

### LLMOps

LLMOps is the operational practice for LLM applications. It includes prompt/version management, evaluation, retrieval quality, cost monitoring, latency, safety checks, guardrails, and feedback loops.

Interviewers may ask about RAG, hallucination, vector databases, prompt injection, and monitoring token cost.

### RAG

Retrieval-Augmented Generation combines search/retrieval with LLM generation. The system retrieves relevant documents, adds them to the prompt, and asks the model to answer using that context.

Important concerns include chunking, embeddings, vector search quality, stale documents, access control, hallucination, citations, and evaluation.

## Scenario Terms Interviewers Often Use

### High CPU in Kubernetes

High CPU can come from traffic spikes, inefficient code, tight loops, bad queries, retries, or insufficient limits/requests. Troubleshooting includes checking HPA, pod metrics, node metrics, recent deployments, logs, traces, and dependency latency.

Do not only say "increase CPU." First identify whether the load is expected, whether autoscaling works, and whether the application is behaving correctly.

### Pod Pending

Pod Pending means Kubernetes cannot schedule the pod. Causes include insufficient CPU/memory, node selectors, taints without tolerations, affinity rules, missing PVCs, or cluster autoscaler issues.

Troubleshooting starts with `kubectl describe pod` and scheduler events.

### 5xx Spike

A 5xx spike means server-side errors increased. It may be caused by a bad deployment, dependency outage, DB connection exhaustion, timeout mismatch, resource saturation, or upstream failure.

Good investigation checks deployment timeline, error rate by endpoint, logs, traces, upstream health, load balancer status, and recent config changes.

### Slow API Latency

Slow latency can come from application code, database queries, network issues, DNS, downstream services, cold starts, CPU throttling, or overloaded pods.

Use RED metrics: rate, errors, and duration. Distributed tracing helps identify which dependency or span is slow.

### Terraform Apply Failure

Terraform apply can fail due to permissions, quota limits, state lock, provider errors, invalid dependencies, naming conflicts, or resources changed outside Terraform.

A good response is to inspect the error, avoid manual partial fixes when possible, check state, confirm cloud-side resource status, and rerun plan after correction.

### Failed Deployment

A failed deployment may be due to bad image, missing config, failed probes, insufficient resources, migration failure, or dependency issue.

For Kubernetes, check rollout status, ReplicaSet, pod events, logs, probes, config, image pull status, and recent changes. Then decide rollback or roll forward.

## Final Revision Checklist

- Explain CI/CD with artifact immutability and rollback.
- Explain Kubernetes workload, networking, storage, and security basics.
- Explain Terraform state, backend, plan, apply, modules, and drift.
- Explain cloud networking with VPC/VNet, subnets, routing, security groups, and IAM.
- Explain observability using metrics, logs, traces, SLOs, and alerts.
- Explain DevSecOps using SAST, DAST, SBOM, secrets, and policy.
- Explain MLOps using data, features, training, registry, serving, drift, and monitoring.
- For every scenario, start with symptoms, impact, recent changes, data collection, mitigation, root cause, and prevention.

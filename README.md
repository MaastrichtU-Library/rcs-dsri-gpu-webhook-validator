# RCS GPU Webhook Validator

## Build and push Docker image to registry

```bash
docker build --platform linux/amd64 . --tag gpu-webhook-validator:1.0.0

docker tag gpu-webhook-validator:1.0.0 ghcr.io/maastrichtu-library/gpu-webhook-validator:1.0.0

docker login ghcr.io -u <USERNAME>

docker push ghcr.io/maastrichtu-library/gpu-webhook-validator:1.0.0
```

## Deploy on OpenShift

First deploy the Service. The service will trigger OpenShift to automatically create self-signed certs, and store them in the 'gpu-webhook-validator-certs' secret.

```
metadata:
  annotations:
    service.beta.openshift.io/serving-cert-secret-name: gpu-webhook-validator-certs
```

Apply the YAML file to the correct namespace.

```
oc apply -f gpu_webhook_validator_service.yml -n <NAMESPACE>
```

Next, we will need to fill in the 'ValidatingWebhokConfiguration_example.yml' accordingly to create our own ValidatingWebhokConfiguration.yml file

First, We need to have a specific route URL. So, in your namespace in OpenShift create a route, note that you need to set TLS termination to 'reencrypt'! Paste it in your file. 

Now, we need to retrieve the base64 format of the OpenShift CA bundle. Paste the output in your file. 

```
oc get configmap -n <namespace> <configMap> -o jsonpath='{.data.service-ca\.crt}' | base64 -w0
```

Deploy the Flask app in the namespace. Use the deployment_example.yml file as a template for your deployment.yml.

Note that the list of allowed namespaces is an environment variable 'ALLOWED_NAMESPACES' which is passed via the 'deployment.yml' file. Pass these variables accordingly.

```
oc apply -f deployment.yml -n <NAMESPACE>
```

If you have filled in the ValidatingWebhookConfiguration.yml correctly, starting the webhook is as simple as just applying the YAML file to the namespace.

```
oc apply -f ValidatingWebhookConfiguration.yml -n <NAMESPACE>
```

And stopping the webhook is as simple as deleting the configuration.

```
oc delete validatingwebhookconfiguration gpu-webhook-validator
```

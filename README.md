# RCS GPU Webhook Validator

## Build and push Docker image to registry

```bash
docker build --platform linux/amd64 . --tag gpu-webhook-validator:1.0.0

docker tag gpu-webhook-validator:1.0.0 ghcr.io/maastrichtu-library/gpu-webhook-validator:1.0.0

docker login ghcr.io -u <USERNAME>

docker push ghcr.io/maastrichtu-library/gpu-webhook-validator:1.0.0
```

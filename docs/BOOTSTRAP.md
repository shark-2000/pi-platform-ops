# Pi 500+ GitOps bootstrap

Target: existing single-node K3s on Raspberry Pi 500+ (ARM64).

This repository is currently public. Never commit credentials, tunnel tokens, kubeconfigs, or plaintext Kubernetes Secrets.

## Bootstrap (one-time, on the Pi)

Argo CD must already be running in namespace `argocd`.

```bash
sudo k3s kubectl apply -f https://raw.githubusercontent.com/shark-2000/pi-platform-ops/main/bootstrap/hello-pi-application.yaml
sudo k3s kubectl get applications -n argocd
sudo k3s kubectl get pods -n apps-dev
```

Alternatively, use the Argo CD GUI: New App, name `hello-pi`, project `default`, Git URL `https://github.com/shark-2000/pi-platform-ops.git`, revision `main`, path `apps/hello-pi`, destination cluster `https://kubernetes.default.svc`, namespace `apps-dev`; enable auto sync, self heal, and create namespace; leave prune disabled.

Verify change propagation by editing `spec.replicas` in `apps/hello-pi/deployment.yaml` and committing to `main`. Argo CD will reconcile the cluster. Revert back to one replica afterward.

## Next phases

- CI image builds to GHCR from application source repositories
- digest-based promotion PRs into GitOps
- Cloudflare Tunnel + Access (token in encrypted secret, never Git plaintext)
- RBAC, policy validation, monitoring, external backups and restore drills

Do not expose the Kubernetes API to the internet. The existing CKA namespace is not managed by this repository.

# Demo API: from source to an ARM64 image

1. Open **Actions > Demo API - ARM64 CI > Run workflow**. This runs unit tests, builds a linux/arm64 Docker image, and publishes to GHCR.
2. Find the package at https://github.com/users/shark-2000/packages/container/package/pi-demo-api. For the first demo, make the package **public** in package settings or configure Kubernetes imagePullSecrets (do not commit tokens).
3. For safe promotion, use the **immutable image digest** from GHCR, not a mutable tag, and create a separate GitOps deployment under `apps/demo-api`. First build must finish before its digest can be known.
4. Add an Argo CD Application for this deployment only after the image exists; do not disrupt `hello-pi`.
5. Verify `/healthz` using local Kubernetes port forwarding and check Argo CD Healthy/Synced.

This starter workflow still needs pinned Actions SHAs, supply-chain vulnerability scanning, branch protection, and automated promotion PRs before it meets a production security baseline.

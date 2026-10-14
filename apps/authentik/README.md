# Authentik private-first rollout

Requires existing namespace `authentik` and Secret `authentik-secrets` with keys `AUTHENTIK_SECRET_KEY` and `AUTHENTIK_POSTGRESQL__PASSWORD`. Neither secret is committed to Git.

This deploys one Authentik server, one worker, one independent PostgreSQL StatefulSet, and two local-path PVCs. ClusterIP only. No public ingress or Cloudflare route.

Prerequisites before merge:
- Verify linux/arm64 support for `ghcr.io/goauthentik/server:2026.5.0` and `postgres:17.6-alpine`.
- Verify health endpoint and process args match the pinned Authentik version.
- Make off-node backups of secret values and PostgreSQL/media data; local-path StorageClass uses Delete reclaim policy and has no volume expansion.

After merge, register: `sudo k3s kubectl apply -f https://raw.githubusercontent.com/shark-2000/pi-platform-ops/main/bootstrap/authentik-application.yaml`.

Check: `sudo k3s kubectl -n authentik get pods,pvc,svc`.

Private tunnel from Mac (using existing `pi` shell shortcut): `pi -L 19000:127.0.0.1:19000 "sudo k3s kubectl -n authentik port-forward svc/authentik-server 19000:9000"`.

Initial setup: http://localhost:19000/if/flow/initial-setup/

Only after restoring backup and verifying an administrator login: Cloudflare tunnel route auth.aquavault.ai -> http://authentik-server.authentik.svc.cluster.local:9000, then create Authentik OIDC provider for Cloudflare Access, keep independent Access recovery method. Do NOT protect auth.aquavault.ai with a self-referential Authentik Access policy.

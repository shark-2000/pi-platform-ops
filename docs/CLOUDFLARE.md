# Cloudflare Tunnel for aquavault.ai

## Secure deployment order

1. In Cloudflare Zero Trust create **self-hosted Access applications** for `argo.aquavault.ai` and `api.aquavault.ai`, with only explicitly approved identities; use MFA for administrators. Never expose Argo CD before a working Access policy. Also enable **Protect with Access** on tunnel routes where supported.
2. Create a **remotely managed** tunnel named `pi500-k3s` in Cloudflare > Networking > Tunnels, selecting Docker as the connector type. Copy the token privately; do NOT put it in GitHub, logs, chat, or shell history.
3. On the Pi, create the secret using a non-echoing prompt:

```bash
sudo k3s kubectl create namespace cloudflare --dry-run=client -o yaml | sudo k3s kubectl apply -f -
read -rsp "Cloudflare tunnel token: " CF_TUNNEL_TOKEN; echo
printf '%s' "$CF_TUNNEL_TOKEN" | sudo k3s kubectl -n cloudflare create secret generic cloudflare-tunnel-token --from-file=token=/dev/stdin
unset CF_TUNNEL_TOKEN
```

4. Bootstrap Argo CD via `sudo k3s kubectl apply -f https://raw.githubusercontent.com/shark-2000/pi-platform-ops/main/bootstrap/cloudflared-application.yaml`.
5. Inspect `sudo k3s kubectl -n cloudflare get pods` and `sudo k3s kubectl -n cloudflare logs deployment/cloudflared --tail=40`.
6. Only AFTER Access policies are tested, configure tunnel routes:
   - `argo.aquavault.ai` -> `https://argocd-server.argocd.svc.cluster.local:443`. Argo CD's default certificate is self-signed. Configure proper origin certificate trust before publishing this route rather than disabling TLS validation.
7. Keep port 6443 (Kubernetes API), SSH and your router unexposed. No incoming port forwarding is needed.

Tunnel token is deliberately **not** included in GitOps. For later fully declarative bootstrapping, use SOPS/age or external-secret management, with recovery keys stored outside the Pi.

The existing CKA lab and hello-pi application remain untouched until the Cloudflare Argo CD Application is bootstrapped.

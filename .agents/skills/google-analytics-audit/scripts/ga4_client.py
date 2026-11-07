#!/usr/bin/env python3
"""
Cliente GA4 (Google Analytics 4) Data API para Lastras de Cuéllar.
Permite autenticarse mediante Service Account y consultar métricas web,
páginas más vistas, canales de tráfico y audiencias.

Soporta dos motores de ejecución:
1. SDK Oficial: `google.analytics.data` / `google.auth` (si están instalados).
2. Fallback Autónomo: Intercambio OAuth2 de JWT firmado con OpenSSL + REST API v1beta
   sin dependencias externas pesadas.
"""

import os
import sys
import json
import time
import base64
import tempfile
import subprocess
import urllib.request
import urllib.error

DEFAULT_CREDENTIALS_PATHS = [
    os.path.join(os.getcwd(), ".agents", "ga4_credentials.json"),
    os.path.join(os.path.dirname(__file__), "..", "..", "..", ".agents", "ga4_credentials.json"),
    os.path.expanduser("~/.agents/ga4_credentials.json"),
]

GA4_SCOPE = "https://www.googleapis.com/auth/analytics.readonly"
OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"
API_BASE_URL = "https://analyticsdata.googleapis.com/v1beta"


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


class GA4Client:
    def __init__(self, credentials_path: str = None, property_id: str = None):
        self.credentials_path = credentials_path or os.environ.get("GA4_CREDENTIALS_JSON") or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not self.credentials_path:
            for p in DEFAULT_CREDENTIALS_PATHS:
                norm_p = os.path.abspath(p)
                if os.path.exists(norm_p):
                    self.credentials_path = norm_p
                    break

        self.property_id = property_id or os.environ.get("GA4_PROPERTY_ID")
        self.creds_data = None
        self._cached_token = None
        self._token_expiry = 0

        self._load_credentials()

    def _load_credentials(self):
        if not self.credentials_path:
            return

        if os.path.exists(self.credentials_path):
            try:
                with open(self.credentials_path, "r", encoding="utf-8") as f:
                    self.creds_data = json.load(f)
                    if not self.property_id and "property_id" in self.creds_data:
                        self.property_id = str(self.creds_data["property_id"]).strip()
            except Exception as e:
                raise ValueError(f"Error al leer credenciales desde {self.credentials_path}: {e}")
        else:
            # Podría venir como string JSON directo en la variable de entorno
            try:
                self.creds_data = json.loads(self.credentials_path)
                if not self.property_id and "property_id" in self.creds_data:
                    self.property_id = str(self.creds_data["property_id"]).strip()
            except Exception:
                raise FileNotFoundError(f"Archivo de credenciales GA4 no encontrado: {self.credentials_path}")

    def is_configured(self) -> bool:
        return bool(self.creds_data and self.property_id)

    def get_access_token(self) -> str:
        """Obtiene un Bearer access token válido para Google Analytics Data API."""
        now = time.time()
        if self._cached_token and now < (self._token_expiry - 60):
            return self._cached_token

        # 1. Intentar con google-auth si está disponible
        try:
            from google.oauth2 import service_account
            import google.auth.transport.requests

            if isinstance(self.creds_data, dict):
                credentials = service_account.Credentials.from_service_account_info(
                    self.creds_data, scopes=[GA4_SCOPE]
                )
            else:
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path, scopes=[GA4_SCOPE]
                )

            request = google.auth.transport.requests.Request()
            credentials.refresh(request)
            self._cached_token = credentials.token
            self._token_expiry = now + 3500
            return self._cached_token
        except ImportError:
            pass  # Fallback a OpenSSL JWT autónomo

        # 2. Fallback autónomo mediante firma RSA con OpenSSL
        if not self.creds_data:
            raise RuntimeError("Credenciales de Service Account no disponibles para generar token.")

        client_email = self.creds_data.get("client_email")
        private_key = self.creds_data.get("private_key")
        token_uri = self.creds_data.get("token_uri", OAUTH_TOKEN_URL)

        if not client_email or not private_key:
            raise ValueError("El archivo JSON de Service Account no contiene 'client_email' o 'private_key'.")

        issued_at = int(now)
        expires_at = issued_at + 3600

        jwt_header = {"alg": "RS256", "typ": "JWT"}
        jwt_claim_set = {
            "iss": client_email,
            "scope": GA4_SCOPE,
            "aud": token_uri,
            "exp": expires_at,
            "iat": issued_at,
        }

        encoded_header = b64url_encode(json.dumps(jwt_header).encode("utf-8"))
        encoded_claims = b64url_encode(json.dumps(jwt_claim_set).encode("utf-8"))
        signing_input = f"{encoded_header}.{encoded_claims}".encode("utf-8")

        # Firmar con openssl dgst -sha256 -sign
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".pem") as key_file:
            key_file.write(private_key)
            key_file_path = key_file.name

        try:
            proc = subprocess.Popen(
                ["openssl", "dgst", "-sha256", "-sign", key_file_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            signature, stderr_err = proc.communicate(input=signing_input)
            if proc.returncode != 0:
                raise RuntimeError(f"Error al firmar JWT con OpenSSL: {stderr_err.decode('utf-8')}")
        finally:
            if os.path.exists(key_file_path):
                os.remove(key_file_path)

        assertion = f"{encoded_header}.{encoded_claims}.{b64url_encode(signature)}"

        # Intercambiar assertion por access token
        post_data = urllib.parse.urlencode({
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": assertion,
        }).encode("utf-8")

        req = urllib.request.Request(
            token_uri,
            data=post_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                resp_json = json.loads(resp.read().decode("utf-8"))
                token = resp_json.get("access_token")
                expires_in = resp_json.get("expires_in", 3600)
                self._cached_token = token
                self._token_expiry = now + expires_in
                return token
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Fallo en intercambio de token OAuth2 de Google ({e.code}): {error_body}")

    def execute_raw_report(self, payload: dict) -> dict:
        """Llama a properties/{property_id}:runReport de Google Analytics Data API."""
        if not self.property_id:
            raise ValueError("Property ID de GA4 no especificado. Configura 'property_id' en credentials o variable GA4_PROPERTY_ID.")

        token = self.get_access_token()
        url = f"{API_BASE_URL}/properties/{self.property_id}:runReport"

        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=req_data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Error en Google Analytics Data API ({e.code}): {error_body}")

    def execute_realtime_report(self, payload: dict) -> dict:
        """Llama a properties/{property_id}:runRealtimeReport."""
        if not self.property_id:
            raise ValueError("Property ID de GA4 no especificado.")

        token = self.get_access_token()
        url = f"{API_BASE_URL}/properties/{self.property_id}:runRealtimeReport"

        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=req_data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Error en GA4 Realtime API ({e.code}): {error_body}")

    @staticmethod
    def parse_report_response(resp: dict) -> list:
        """Convierte la respuesta cruda de runReport en una lista de dicts limpia."""
        dimension_headers = [h.get("name") for h in resp.get("dimensionHeaders", [])]
        metric_headers = [h.get("name") for h in resp.get("metricHeaders", [])]

        results = []
        rows = resp.get("rows", [])
        for r in rows:
            row_dict = {}
            dim_values = [d.get("value") for d in r.get("dimensionValues", [])]
            metric_values = [m.get("value") for m in r.get("metricValues", [])]

            for h, v in zip(dimension_headers, dim_values):
                row_dict[h] = v
            for h, v in zip(metric_headers, metric_values):
                # Intentar castear numérico
                try:
                    if "." in v:
                        row_dict[h] = float(v)
                    else:
                        row_dict[h] = int(v)
                except ValueError:
                    row_dict[h] = v

            results.append(row_dict)
        return results

    # ==========================================
    # Consultas de alto nivel predefinidas
    # ==========================================

    def get_overview(self, days: int = 30) -> dict:
        """Obtiene KPIs globales del portal en los últimos N días."""
        payload = {
            "dateRanges": [{"startDate": f"{days}daysAgo", "endDate": "yesterday"}],
            "metrics": [
                {"name": "totalUsers"},
                {"name": "activeUsers"},
                {"name": "newUsers"},
                {"name": "sessions"},
                {"name": "screenPageViews"},
                {"name": "averageSessionDuration"},
                {"name": "bounceRate"},
                {"name": "engagementRate"},
                {"name": "userEngagementDuration"},
            ],
        }
        raw = self.execute_raw_report(payload)
        parsed = self.parse_report_response(raw)
        return parsed[0] if parsed else {}

    def get_top_pages(self, days: int = 30, limit: int = 20) -> list:
        """Obtiene las páginas y artículos más visitados."""
        payload = {
            "dateRanges": [{"startDate": f"{days}daysAgo", "endDate": "yesterday"}],
            "dimensions": [
                {"name": "pagePath"},
                {"name": "pageTitle"},
            ],
            "metrics": [
                {"name": "screenPageViews"},
                {"name": "activeUsers"},
                {"name": "averageSessionDuration"},
                {"name": "bounceRate"},
                {"name": "engagementRate"},
            ],
            "orderBys": [
                {"metric": {"metricName": "screenPageViews"}, "desc": True}
            ],
            "limit": str(limit),
        }
        raw = self.execute_raw_report(payload)
        return self.parse_report_response(raw)

    def get_traffic_channels(self, days: int = 30) -> list:
        """Obtiene distribución por canal de adquisición (Orgánico, Directo, Social, etc.)."""
        payload = {
            "dateRanges": [{"startDate": f"{days}daysAgo", "endDate": "yesterday"}],
            "dimensions": [
                {"name": "sessionDefaultChannelGroup"},
            ],
            "metrics": [
                {"name": "sessions"},
                {"name": "activeUsers"},
                {"name": "engagementRate"},
            ],
            "orderBys": [
                {"metric": {"metricName": "sessions"}, "desc": True}
            ],
        }
        raw = self.execute_raw_report(payload)
        return self.parse_report_response(raw)

    def get_devices_and_geo(self, days: int = 30) -> dict:
        """Obtiene desglose de dispositivos (mobile vs desktop) y principales ciudades."""
        payload_devices = {
            "dateRanges": [{"startDate": f"{days}daysAgo", "endDate": "yesterday"}],
            "dimensions": [{"name": "deviceCategory"}],
            "metrics": [{"name": "sessions"}, {"name": "activeUsers"}],
            "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
        }
        raw_dev = self.execute_raw_report(payload_devices)
        devices = self.parse_report_response(raw_dev)

        payload_geo = {
            "dateRanges": [{"startDate": f"{days}daysAgo", "endDate": "yesterday"}],
            "dimensions": [{"name": "city"}, {"name": "region"}],
            "metrics": [{"name": "sessions"}, {"name": "activeUsers"}],
            "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
            "limit": "15",
        }
        raw_geo = self.execute_raw_report(payload_geo)
        geo = self.parse_report_response(raw_geo)

        return {"devices": devices, "geo": geo}

    def get_realtime(self) -> dict:
        """Consulta usuarios activos en tiempo real (últimos 30 min)."""
        payload = {
            "metrics": [{"name": "activeUsers"}],
            "dimensions": [{"name": "unifiedScreenName"}],
            "limit": "10",
        }
        raw = self.execute_realtime_report(payload)
        parsed = self.parse_report_response(raw)
        total_active = sum(row.get("activeUsers", 0) for row in parsed)
        return {"totalActiveUsers": total_active, "screens": parsed}

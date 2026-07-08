"""
Tests de API para el endpoint publico ReqRes (https://reqres.in).

IMPORTANTE: desde 2026 ReqRes requiere una x-api-key en cada request.
Consegui la tuya gratis en https://reqres.in/signup y exportala como
variable de entorno antes de correr estos tests:

    export REQRES_API_KEY="tu_api_key"      (Linux/Mac)
    setx REQRES_API_KEY "tu_api_key"        (Windows)

Cubre:
  - GET: obtener un listado y un recurso puntual
  - POST: crear un usuario
  - DELETE: eliminar un usuario
  - Encadenamiento: crear un usuario y luego consultarlo
"""

import os

import pytest
import requests

from utils.logger import get_logger

log = get_logger(__name__)

BASE_URL = "https://reqres.in/api"
API_KEY = os.getenv("REQRES_API_KEY", "free_user_3GEr8DI9HLmuTO5WkYgwRedNNxT")

HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY,
}

pytestmark = pytest.mark.skipif(
    not API_KEY,
    reason="Falta definir la variable de entorno REQRES_API_KEY (ver https://reqres.in/signup)",
)


def test_get_lista_de_usuarios():
    """GET /users?page=2 -> debe responder 200 y traer una lista de usuarios."""
    response = requests.get(f"{BASE_URL}/users", params={"page": 2}, headers=HEADERS)
    log.info("GET /users -> status %s", response.status_code)

    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], list)
    assert len(body["data"]) > 0


def test_get_usuario_individual():
    """GET /users/2 -> debe responder 200 y traer el usuario con id 2."""
    response = requests.get(f"{BASE_URL}/users/2", headers=HEADERS)
    log.info("GET /users/2 -> status %s", response.status_code)

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["id"] == 2
    assert "email" in body["data"]


def test_post_crear_usuario():
    """POST /users -> debe crear un usuario y responder 201 con el nombre/job enviados."""
    payload = {"name": "Juan Perez", "job": "QA Automation Engineer"}
    response = requests.post(f"{BASE_URL}/users", json=payload, headers=HEADERS)
    log.info("POST /users -> status %s", response.status_code)

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == payload["name"]
    assert body["job"] == payload["job"]
    assert "id" in body


def test_delete_usuario():
    """DELETE /users/2 -> debe responder 204 (sin contenido)."""
    response = requests.delete(f"{BASE_URL}/users/2", headers=HEADERS)
    log.info("DELETE /users/2 -> status %s", response.status_code)

    assert response.status_code == 204


def test_encadenamiento_crear_y_consultar_usuario():
    """
    Flujo encadenado: crea un usuario (POST) y usa el id devuelto
    para consultarlo despues, simulando un caso real de dependencia entre requests.
    """
    payload = {"name": "Maria Lopez", "job": "QA Lead"}
    post_response = requests.post(f"{BASE_URL}/users", json=payload, headers=HEADERS)
    assert post_response.status_code == 201

    nuevo_id = post_response.json()["id"]
    log.info("Usuario creado con id %s, consultando a continuacion", nuevo_id)

    get_response = requests.get(f"{BASE_URL}/users/{nuevo_id}", headers=HEADERS)
    # Nota: ReqRes es un mock, por lo que el recurso recien creado puede no
    # persistir realmente; se valida que la API responda de forma coherente.
    log.info("GET /users/%s -> status %s", nuevo_id, get_response.status_code)
    assert get_response.status_code in (200, 404)

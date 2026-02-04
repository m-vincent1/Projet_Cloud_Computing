"""
Service de lecture des données depuis Azure Blob Storage ou fichiers locaux
Implémente un cache mémoire avec TTL de 60 secondes
"""
import os
import json
import yaml
import logging
from typing import Any, Optional
from cachetools import TTLCache
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError

logger = logging.getLogger(__name__)


class ContentService:
    """
    Service pour lire le contenu depuis Azure Blob Storage ou fichiers locaux.
    Utilise un cache mémoire avec TTL pour optimiser les performances.
    """

    def __init__(self, config):
        """
        Initialise le service avec la configuration donnée.

        Args:
            config: Objet de configuration contenant les paramètres Azure et cache
        """
        self.config = config
        self.cache_ttl = getattr(config, 'CACHE_TTL', 60)

        # Cache mémoire avec TTL (max 100 entrées, expire après CACHE_TTL secondes)
        self._cache = TTLCache(maxsize=100, ttl=self.cache_ttl)

        # Client Azure Blob (initialisé si connection string disponible)
        self._blob_service_client = None
        self._container_client = None
        self._init_blob_client()

    def _init_blob_client(self):
        """Initialise le client Azure Blob Storage si configuré"""
        connection_string = getattr(self.config, 'AZURE_STORAGE_CONNECTION_STRING', '')

        if connection_string and not getattr(self.config, 'USE_LOCAL_FILES', False):
            try:
                self._blob_service_client = BlobServiceClient.from_connection_string(
                    connection_string
                )
                container_name = getattr(self.config, 'BLOB_CONTAINER_NAME', 'content')
                self._container_client = self._blob_service_client.get_container_client(
                    container_name
                )
                logger.info(f"Azure Blob Storage client initialized for container: {container_name}")
            except AzureError as e:
                logger.error(f"Failed to initialize Azure Blob client: {e}")
                self._blob_service_client = None

    def _read_from_blob(self, filename: str) -> Optional[dict]:
        """
        Lit un fichier depuis Azure Blob Storage.

        Args:
            filename: Nom du fichier à lire

        Returns:
            Contenu du fichier parsé en dict, ou None si erreur
        """
        if not self._container_client:
            logger.warning("Azure Blob client not available")
            return None

        try:
            blob_client = self._container_client.get_blob_client(filename)
            content = blob_client.download_blob().readall().decode('utf-8')
            return self._parse_content(content, filename)
        except AzureError as e:
            logger.error(f"Error reading blob {filename}: {e}")
            return None

    def _read_from_local(self, filename: str) -> Optional[dict]:
        """
        Lit un fichier depuis le système de fichiers local.

        Args:
            filename: Nom du fichier à lire

        Returns:
            Contenu du fichier parsé en dict, ou None si erreur
        """
        local_path = getattr(self.config, 'LOCAL_DATA_PATH', 'data')
        filepath = os.path.join(local_path, filename)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return self._parse_content(content, filename)
        except FileNotFoundError:
            logger.error(f"Local file not found: {filepath}")
            return None
        except IOError as e:
            logger.error(f"Error reading local file {filepath}: {e}")
            return None

    def _parse_content(self, content: str, filename: str) -> Optional[dict]:
        """
        Parse le contenu selon l'extension du fichier (JSON ou YAML).

        Args:
            content: Contenu brut du fichier
            filename: Nom du fichier pour déterminer le format

        Returns:
            Contenu parsé en dict
        """
        try:
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                return yaml.safe_load(content)
            else:
                return json.loads(content)
        except (json.JSONDecodeError, yaml.YAMLError) as e:
            logger.error(f"Error parsing {filename}: {e}")
            return None

    def get_content(self, filename: str) -> dict:
        """
        Récupère le contenu d'un fichier avec mise en cache.

        Args:
            filename: Nom du fichier à récupérer

        Returns:
            Contenu du fichier ou dict vide avec erreur
        """
        # Vérifier le cache
        if filename in self._cache:
            logger.debug(f"Cache hit for {filename}")
            return self._cache[filename]

        logger.debug(f"Cache miss for {filename}, fetching...")

        # Lire depuis Blob ou fichiers locaux
        use_local = getattr(self.config, 'USE_LOCAL_FILES', False)

        if use_local:
            data = self._read_from_local(filename)
        else:
            data = self._read_from_blob(filename)

        if data is None:
            return {"items": [], "error": f"Unable to load {filename}"}

        # Mettre en cache
        self._cache[filename] = data
        return data

    def get_events(self) -> dict:
        """Récupère les événements"""
        filename = getattr(self.config, 'EVENTS_FILE', 'events.json')
        return self.get_content(filename)

    def get_news(self) -> dict:
        """Récupère les actualités"""
        filename = getattr(self.config, 'NEWS_FILE', 'news.json')
        return self.get_content(filename)

    def get_faq(self) -> dict:
        """Récupère la FAQ"""
        filename = getattr(self.config, 'FAQ_FILE', 'faq.json')
        return self.get_content(filename)

    def clear_cache(self):
        """Vide le cache (utile pour les tests)"""
        self._cache.clear()
        logger.info("Cache cleared")

    def is_blob_available(self) -> bool:
        """Vérifie si le client Azure Blob est disponible et fonctionnel"""
        if not self._container_client:
            return False
        try:
            # Tenter de lister les blobs pour vérifier la connexion
            list(self._container_client.list_blobs(max_results=1))
            return True
        except AzureError:
            return False

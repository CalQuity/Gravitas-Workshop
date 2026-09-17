"""
Custom Agno VectorDb adapter for a Pinecone "integrated embedding" index.

Background
------------------------
Agno (the RAG framework) expects any vector database it works with to expose
a specific set of methods: insert, upsert, search, delete, exists, etc.
This file is called an "adapter" (or sometimes a "wrapper") because it
translates between two different "languages":

    Agno's world  <-->  PineconeHostedDb (this file)  <-->  Pinecone's world

Every method below follows the same basic shape:
    1. Accept an Agno-style input (e.g. a list of Document objects).
    2. Convert it into whatever shape Pinecone's API expects.
    3. Call Pinecone.
    4. Convert Pinecone's response back into something Agno understands
       (usually Document objects, or a simple bool/None).

A special detail about THIS particular adapter: it uses Pinecone's
"integrated embedding" feature, which means we never compute embeddings
ourselves in Python. We just send plain text to Pinecone, and Pinecone's
hosted model (here, "llama-text-embed-v2") turns that text into vectors
for us automatically -- both when we store data and when we search.
"""

from agno.knowledge.document import Document
from agno.vectordb.base import VectorDb
from agno.vectordb.search import SearchType

from pinecone import Pinecone
import asyncio
import hashlib
from typing import Any


class PineconeHostedDb(VectorDb):
    """A small Agno adapter for a Pinecone integrated-embedding index.

    The adapter sends plain text to Pinecone. Pinecone's index embeds both
    stored passages and search queries with ``llama-text-embed-v2``.

    This class inherits from Agno's ``VectorDb`` base class, which means
    Agno expects it to provide a standard set of methods (insert, search,
    delete, etc.). Every method here is a Pinecone-specific implementation
    of one of those expected methods.
    """

    def __init__(
        self,
        *,
        api_key: str,
        index_name: str,
        namespace: str,
        embed_model: str,
        text_field: str,
    ) -> None:
        """Set up the adapter and connect to an existing Pinecone index.

        The ``*`` before the parameters forces every argument to be passed
        by keyword (e.g. ``PineconeHostedDb(api_key=..., index_name=...)``),
        which avoids mixing up these several similar-looking string values.

        Args:
            api_key: Pinecone API key used to authenticate the client.
            index_name: Name of the existing Pinecone index to connect to.
                This index is assumed to already exist (this adapter does
                not create new indexes -- see ``create()`` below).
            namespace: A named "section" within the shared index where this
                project's records live, keeping them separate from other
                projects using the same index.
            embed_model: The embedding model this index is expected to use
                (e.g. "llama-text-embed-v2"). Used only to validate the
                index configuration in ``create()``.
            text_field: The metadata field name that Pinecone treats as the
                "text to embed" for this index (Pinecone's integrated
                embedding needs to know which field holds the raw text).
        """
        # Let the parent VectorDb class store the standard name/description.
        super().__init__(name=index_name, description="Pinecone hosted embeddings")

        # Save configuration as instance attributes -- each PineconeHostedDb
        # object remembers its own namespace, model, and text field.
        self.namespace = namespace
        self.embed_model = embed_model
        self.text_field = text_field

        # Create the actual connection to Pinecone and grab a handle to the
        # specific index (similar to connecting to a specific table/database).
        self.client = Pinecone(api_key=api_key)
        self.index = self.client.index(index_name)

    def create(self) -> None:
        """Validate the existing hosted-model index instead of creating another one.

        Normally a VectorDb's ``create()`` method would create a brand new
        index. Here, the Pinecone index is shared infrastructure that
        already exists, so instead of creating anything, this method just
        double-checks that the index is configured the way this project
        expects (same embedding model, same text field name). If something
        doesn't match, it raises an error early -- much easier to debug
        than a confusing failure later during search or upsert.
        """
        try:
            details = self.client.describe_index(self.name)
        except Exception as error:
            # Wrap whatever Pinecone's error was into a clearer message,
            # while keeping the original error attached via "from error".
            raise ValueError(f"Pinecone index '{self.name}' does not exist or is unavailable") from error

        # Safely dig into the response object without crashing if some
        # field happens to be missing (getattr with a default of None).
        embed = getattr(details, "embed", None)
        actual_model = getattr(embed, "model", None)
        field_map = getattr(embed, "field_map", None) or {}
        actual_text_field = field_map.get("text")

        # Confirm the index's configured embedding model matches what
        # this project expects.
        if actual_model != self.embed_model:
            raise ValueError(
                f"Pinecone index '{self.name}' uses {actual_model!r}, "
                f"but this project expects {self.embed_model!r}"
            )
        # Confirm the index's "which field holds the text" setting matches
        # what this project expects.
        if actual_text_field != self.text_field:
            raise ValueError(
                f"Pinecone index '{self.name}' maps text to {actual_text_field!r}, "
                f"but this project expects {self.text_field!r}"
            )

    async def async_create(self) -> None:
        """Async version of create(). Runs the same check in a background thread."""
        # asyncio.to_thread lets a normal (blocking) function run inside an
        # async application without freezing everything else while it runs.
        await asyncio.to_thread(self.create)

    def exists(self) -> bool:
        """Check whether this adapter's configured index currently exists in Pinecone."""
        try:
            self.client.describe_index(self.name)
            return True
        except Exception:
            # Any error here (e.g. "not found") is treated as "doesn't exist".
            return False

    async def async_exists(self) -> bool:
        """Async version of exists()."""
        return await asyncio.to_thread(self.exists)

    def name_exists(self, name: str) -> bool:
        """Check whether ANY index with the given name exists (not just this one)."""
        try:
            self.client.describe_index(name)
            return True
        except Exception:
            return False

    async def async_name_exists(self, name: str) -> bool:
        """Async version of name_exists()."""
        return await asyncio.to_thread(self.name_exists, name)

    def id_exists(self, id: str) -> bool:
        """Check whether a record with this exact ID is already stored in Pinecone."""
        response = self.index.fetch(ids=[id], namespace=self.namespace)
        # getattr(..., {}) or {} = "use response.vectors if present, otherwise
        # treat it as an empty dict" -- avoids crashing on an unexpected response shape.
        vectors = getattr(response, "vectors", {}) or {}
        return id in vectors

    def content_hash_exists(self, content_hash: str, user_id: str | None = None) -> bool:
        """Check whether a piece of content (identified by its hash) was already stored.

        A "content hash" is a short fingerprint computed from a document's
        text. Identical text always produces the same hash, so comparing
        hashes is a fast way to detect duplicate content without comparing
        full text bodies.

        Args:
            content_hash: The fingerprint of the content to look for.
            user_id: Optional -- if given, only match records belonging to
                this specific user.
        """
        selected_filter: dict[str, Any] = {"content_hash": {"$eq": content_hash}}
        if user_id:
            selected_filter["user_id"] = {"$eq": user_id}

        # We don't actually care about relevance here, just "does anything match?",
        # so we ask for only the single closest hit (top_k=1).
        response = self.index.search(
            namespace=self.namespace,
            top_k=1,
            inputs={"text": content_hash},
            filter=selected_filter,
            fields=[self.text_field],
        )
        return bool(response.result.hits)

    def _records(
        self,
        content_hash: str,
        documents: list[Document],
        filters: dict[str, Any] | None,
        user_id: str | None,
    ) -> list[dict[str, Any]]:
        """Internal helper: convert Agno Documents into Pinecone record dicts.

        The leading underscore in the method name is a Python convention
        signaling "this is a private helper, not meant to be called from
        outside this class." It's used internally by upsert().

        Each Document becomes one Pinecone "record" -- a dictionary with a
        unique ID, the text to embed, and assorted metadata.
        """
        records = []
        # enumerate(..., start=1) loops through documents while also giving
        # a counter (position) starting at 1, so we know each chunk's order.
        for position, document in enumerate(documents, start=1):
            # Build a unique, reproducible ID for this specific chunk by
            # hashing a combination of content_hash + position + the actual
            # text. sha256(...).hexdigest() turns that into a fixed-length
            # fingerprint string.
            record_id = hashlib.sha256(
                f"{content_hash}:{position}:{document.content}".encode("utf-8")
            ).hexdigest()

            # Merge the document's own metadata with any extra filters passed in.
            # The `or {}` guards handle the case where either might be None.
            metadata = {**(document.meta_data or {}), **(filters or {})}

            # Add/override a few standard fields on top of the merged metadata.
            metadata.update(
                {
                    "name": document.name or "Workshop document",
                    "content_hash": content_hash,
                    "content_id": document.content_id or content_hash,
                    "chunk": position,
                }
            )
            if user_id:
                metadata["user_id"] = user_id

            # Build the final record in the exact shape Pinecone expects:
            # an "_id", the text under whichever field Pinecone embeds,
            # plus all the metadata spread in.
            records.append({"_id": record_id, self.text_field: document.content, **metadata})
        return records

    def upsert(
        self,
        content_hash: str,
        documents: list[Document],
        filters: dict[str, Any] | None = None,
        user_id: str | None = None,
    ) -> None:
        """Insert new records or update existing ones with the same ID ("upsert").

        This is the method that actually sends data to Pinecone. It builds
        the record dictionaries via _records(), then calls Pinecone's
        upsert_records API.
        """
        if not documents:
            # Nothing to do -- avoid making a pointless API call.
            return
        records = self._records(content_hash, documents, filters, user_id)
        self.index.upsert_records(namespace=self.namespace, records=records)

    async def async_upsert(
        self,
        content_hash: str,
        documents: list[Document],
        filters: dict[str, Any] | None = None,
        user_id: str | None = None,
        **_: Any,
    ) -> None:
        """Async version of upsert()."""
        await asyncio.to_thread(self.upsert, content_hash, documents, filters, user_id)

    def insert(
        self,
        content_hash: str,
        documents: list[Document],
        filters: dict[str, Any] | None = None,
        user_id: str | None = None,
    ) -> None:
        """Insert documents.

        Agno's VectorDb interface expects both an `insert` and an `upsert`
        method to exist. Since Pinecone's hosted-embedding API already
        treats "insert" and "update" the same way, this simply delegates
        to upsert() rather than duplicating logic.
        """
        self.upsert(content_hash, documents, filters, user_id)

    async def async_insert(
        self,
        content_hash: str,
        documents: list[Document],
        filters: dict[str, Any] | None = None,
        user_id: str | None = None,
    ) -> None:
        """Async version of insert()."""
        await self.async_upsert(content_hash, documents, filters, user_id)

    def search(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, Any] | None = None,
        user_id: str | None = None,
    ) -> list[Document]:
        """Run a semantic search against Pinecone and return Agno Documents.

        Because this index uses Pinecone's integrated embedding, we send
        the raw query text and Pinecone handles turning it into a vector
        and finding the closest matches -- we never compute embeddings
        ourselves.

        Args:
            query: The search text.
            limit: Maximum number of results to return (Pinecone's top_k).
            filters: Optional metadata filters to narrow the search.
            user_id: Optional -- if given, only search this user's records.
        """
        selected_filters = dict(filters or {})
        if user_id:
            selected_filters["user_id"] = {"$eq": user_id}

        response = self.index.search(
            namespace=self.namespace,
            top_k=limit,
            inputs={"text": query},
            filter=selected_filters or None,
        )

        documents = []
        for hit in response.result.hits:
            # Some Pinecone response objects support .to_dict(), others don't --
            # handle both cases safely rather than assuming one shape.
            fields = hit.fields.to_dict() if hasattr(hit.fields, "to_dict") else dict(hit.fields or {})

            # Pull the actual text content out of the metadata dict (so it isn't
            # duplicated inside meta_data), defaulting to "" if missing.
            content = fields.pop(self.text_field, "")

            # Record how relevant this result was, so callers can see the score.
            fields["score"] = hit.score

            # Rebuild this as a standard Agno Document, so from Agno's point of
            # view, search results look identical regardless of which vector
            # database is actually being used behind the scenes.
            documents.append(
                Document(
                    id=hit.id,
                    name=fields.get("name"),
                    content=content,
                    meta_data=fields,
                )
            )
        return documents

    async def async_search(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, Any] | None = None,
        user_id: str | None = None,
    ) -> list[Document]:
        """Async version of search()."""
        return await asyncio.to_thread(self.search, query, limit, filters, user_id)

    def delete_by_id(self, id: str) -> bool:
        """Delete a single record by its exact ID."""
        self.index.delete(ids=[id], namespace=self.namespace)
        return True

    def delete_by_name(self, name: str) -> bool:
        """Delete all records whose metadata "name" field matches exactly."""
        self.index.delete(filter={"name": {"$eq": name}}, namespace=self.namespace)
        return True

    def delete_by_metadata(self, metadata: dict[str, Any]) -> bool:
        """Delete all records matching an arbitrary set of metadata key/value pairs.

        Uses a dict comprehension to turn e.g. {"source_file": "a.pdf"} into
        Pinecone's filter syntax: {"source_file": {"$eq": "a.pdf"}}.
        """
        selected_filter = {key: {"$eq": value} for key, value in metadata.items()}
        self.index.delete(filter=selected_filter, namespace=self.namespace)
        return True

    def delete_by_content_id(self, content_id: str, user_id: str | None = None) -> bool:
        """Delete all records belonging to a specific content_id (optionally per-user)."""
        selected_filter: dict[str, Any] = {"content_id": {"$eq": content_id}}
        if user_id:
            selected_filter["user_id"] = {"$eq": user_id}
        self.index.delete(filter=selected_filter, namespace=self.namespace)
        return True

    def delete(self) -> bool:
        """Delete this project's records while keeping the shared index.

        Wipes every record in this adapter's namespace, but leaves the
        Pinecone index itself (and other projects' namespaces) untouched.
        """
        self.index.delete(delete_all=True, namespace=self.namespace)
        return True

    def drop(self) -> None:
        """Intentionally disabled: never delete the shared Pinecone index.

        Because this index is shared infrastructure across a workshop
        (not owned exclusively by one project), dropping it would be
        destructive to everyone else using it. This method exists only to
        satisfy Agno's VectorDb interface, and always raises an error
        instead of doing anything.
        """
        raise RuntimeError("This workshop adapter never deletes the shared Pinecone index")

    async def async_drop(self) -> None:
        """Async version of drop() -- still always raises, on purpose."""
        self.drop()

    def get_supported_search_types(self) -> list[str]:
        """Declare which search modes this adapter supports.

        This adapter only supports pure vector (semantic/embedding-based)
        search -- not keyword or hybrid search.
        """
        return [SearchType.vector]

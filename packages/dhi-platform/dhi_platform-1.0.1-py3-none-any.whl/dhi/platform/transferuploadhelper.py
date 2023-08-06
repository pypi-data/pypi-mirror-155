from azure.storage.blob import BlobClient
from .metadata import MetadataClientV2

class TransferUploadHelper:
    def __init__(self, metadataclient2:MetadataClientV2) -> None:
        self._metadata2 = metadataclient2

    def stage_file(self, file_path:str, max_parallelism=2, block_size=20*1024*1024) -> str:
        """
        Prepare a file for import into the platform by uploading it into a staging area.

        :param file_path: Input file
        :param max_parallelism: maximum concurrency to use when files are over 64 MB
        :param block_size: max_block_size - The maximum chunk size for uploading a block blob in chunks.
        :return: Url with the staged file (the url can be used as an input for transfer operations)
        :rtype: str
        """
        blob_url = ""
        with open(file_path, "rb") as data:
            blob_url = self.stage_stream(data, max_parallelism=max_parallelism, block_size=block_size)
        return blob_url
    
    def stage_stream(self, stream, max_parallelism:int=2, block_size:int=20*1024*1024) -> str:
        """
        Prepare a stream for import into the platform by uploading it into a staging area.

        :param stream: Input stream
        :param max_parallelism: maximum concurrency to use when files are over 64 MB
        :param block_size: max_block_size - The maximum chunk size for uploading a block blob in chunks.
        :return: Url with the staged stream (the url can be used as an input for transfer operations)
        :rtype: str
        """
        # TODO: there is room for improvement for parallizing block uploads as in .net SDK
        blob_url = self._metadata2.GetUploadUrlV2().Body["data"]
        blob = BlobClient.from_blob_url(blob_url, max_block_size=block_size)
        blob.upload_blob(stream, max_concurrency=max_parallelism)
        return blob_url
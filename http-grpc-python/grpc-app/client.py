
import grpc
# import file_service_pb2
import file_pb2 as file_service_pb2
# import file_service_pb2_grpc
import file_pb2_grpc as file_service_pb2_grpc
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

CHUNK_SIZE = 1024 * 1024  # 1MB chunks


def upload_file(filename):
    channel = grpc.insecure_channel('10.0.0.10:31429')
    stub = file_service_pb2_grpc.FileServiceStub(channel)

    def get_file_chunks():
        with open(filename, 'rb') as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                yield file_service_pb2.FileUploadRequest(
                    chunk=chunk,
                    filename=os.path.basename(filename)
                )

    try:
        file_size = os.path.getsize(filename)
        logger.info(f"Starting upload of {filename} ({file_size/1024/1024:.2f} MB)")

        response = stub.UploadFile(get_file_chunks())
        logger.info(f"Upload status: {response.success}")
        logger.info(f"Server message: {response.message}")

        if response.success:
            logger.info(f"Successfully uploaded {filename}")
        else:
            logger.error(f"Failed to upload {filename}")

    except grpc.RpcError as e:
        logger.error(f"gRPC error while uploading file: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"Unexpected error while uploading file: {e}", exc_info=True)


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        logger.error("Usage: python client.py <filename>")
        sys.exit(1)

    upload_file(sys.argv[1])

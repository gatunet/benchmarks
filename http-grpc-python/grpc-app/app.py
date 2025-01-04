import grpc
import logging
from concurrent import futures

import file_pb2
import file_pb2_grpc

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class Servicer(file_pb2_grpc.FileServiceServicer):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def UploadFile(self, request_iterator, context):
        self.logger.info("Starting request")
        file_data = []

        for request in request_iterator:
            file_data.append(request.chunk)

        self.logger.info("Finished request")
        return file_pb2.FileUploadResponse(
            success=True,
            message=f"{len(file_data)}"
        )


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    file_pb2_grpc.add_FileServiceServicer_to_server(
        Servicer(),
        server
    )

    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info("Server UP")
    server.wait_for_termination()

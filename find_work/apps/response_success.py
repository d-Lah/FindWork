from abc import (
    ABC,
    abstractmethod
)
from rest_framework import status
from rest_framework.response import Response


class ResponseSuccess(ABC):
    @classmethod
    @abstractmethod
    def get_response(self):
        pass

    @classmethod
    @abstractmethod
    def add_data_for_response_data(self, key, value):
        pass


class ResponseCreate(ResponseSuccess):
    response_data = {
        "status": "Create"
    }

    def get_response(self):
        return Response(
            self.response_data,
            status=status.HTTP_201_CREATED,
        )

    def add_data_for_response_data(self, key, value):
        self.response_data[key] = value


class ResponseUpdate(ResponseSuccess):
    response_data = {
        "status": "Update"
    }

    def get_response(self):
        return Response(
            self.response_data,
            status=status.HTTP_200_OK
        )

    def add_data_for_response_data(self, key, value):
        self.response_data[key] = value


class ResponseValid(ResponseSuccess):
    response_data = {
        "status": "Valid"
    }

    def get_response(self):
        return Response(
            self.response_data,
            status=status.HTTP_200_OK
        )

    def add_data_for_response_data(self, key, value):
        self.response_data[key] = value


class ResponseGet(ResponseSuccess):
    response_data = {
        "status": "Get"
    }

    def get_response(self):
        return Response(
            self.response_data,
            status=status.HTTP_200_OK
        )

    def add_data_for_response_data(self, key, value):
        self.response_data[key] = value

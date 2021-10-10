import traceback
from collections import OrderedDict

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from rest_framework import status
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination

from users.models import DUser
from .constants import MAX_PAGE_SIZE, PAGE_QUERY_PARAM, PAGE_SIZE
from .serializers import DUserSerializer


def index(request):
    return HttpResponseRedirect(redirect_to='list')


@api_view(['PUT', 'POST'])
def add_edit(request):

    user_id = int(request.GET.get("user_id")) \
        if (request.GET.get("user_id") is not None
            and int(request.GET.get("user_id")) > 0) \
        else None

    # Add new user
    if user_id is None and request.method == 'POST':
        user_serializer = DUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        # Edit existing user by user_id
        try:
            user = DUser.objects.get(id=user_id)
        except DUser.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND)

        user_serializer = DUserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete(request):

    user_id = int(request.GET.get("user_id")) \
        if (request.GET.get("user_id") is not None
            and int(request.GET.get("user_id")) > 0) \
        else None

    # Delete all users
    if user_id is None and request.method == 'DELETE':
        count = DUser.objects.all().delete()
        return JsonResponse({'message': '{} user(s) were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)
    else:
        # Delete user by user_id
        try:
            user = DUser.objects.get(id=user_id)
        except DUser.DoesNotExist:
            return JsonResponse({'message': 'No user found of id {}'.format(user_id)}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return JsonResponse({'message': 'User was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def list(request, user_id=0):

    if request.method == 'GET':

        if user_id == 0:
            try:
                page_size = int(request.GET.get(PAGE_SIZE)) \
                    if (request.GET.get(PAGE_SIZE) is not None
                        and int(request.GET.get(PAGE_SIZE)) > 0) \
                    else MAX_PAGE_SIZE

                pagination = PageNumberPagination()
                pagination.page_size = page_size
                pagination.max_page_size = MAX_PAGE_SIZE
                pagination.page_size_query_param = PAGE_SIZE
                pagination.page_query_param = PAGE_QUERY_PARAM

                users = DUser.objects.all()

                result = pagination.paginate_queryset(users, request)

                serializer = DUserSerializer(result, many=True)
                return pagination.get_paginated_response(serializer.data)
            except NotFound as e:
                return JsonResponse(
                    OrderedDict([
                        ('count', None),
                        ('next', None),
                        ('previous', None),
                        ('results', [])
                    ])
                )
        else:
            try:
                user = DUser.objects.get(id=user_id)
            except DUser.DoesNotExist:
                return JsonResponse(status=status.HTTP_404_NOT_FOUND)
            serializer = DUserSerializer(user, data=request.data)
            if serializer.is_valid():
                return JsonResponse(serializer.data)
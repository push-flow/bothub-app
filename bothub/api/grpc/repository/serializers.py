from django_grpc_framework import proto_serializers
from rest_framework import serializers

from bothub.api.v2.repository.serializers import RepositoryCategorySerializer
from bothub.common.models import Repository
from bothub.protos import repository_pb2


class RepositoryProtoSerializer(proto_serializers.ModelProtoSerializer):
    owner__nickname = serializers.SerializerMethodField()
    intents = serializers.SerializerMethodField()
    available_languages = serializers.SerializerMethodField()
    categories_list = serializers.SerializerMethodField()

    class Meta:
        model = Repository
        proto_class = repository_pb2.Repository
        fields = [
            "uuid",
            "name",
            "slug",
            "description",
            "is_private",
            "created_at",
            "language",
            "owner",
            "algorithm",
            "use_competing_intents",
            "use_name_entities",
            "use_analyze_char",
            "owner__nickname",
            "intents",
            "categories",
            "available_languages",
            "categories_list",
        ]

    def get_owner__nickname(self, repository: Repository):
        return repository.owner.nickname

    def get_intents(self, repository: Repository):
        return repository.get_formatted_intents()

    def get_available_languages(self, repository: Repository):
        return repository.available_languages()

    def get_categories_list(self, repository: Repository):
        return RepositoryCategorySerializer(repository.categories, many=True).data
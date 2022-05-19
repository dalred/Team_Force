from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import Skills

User = get_user_model()


class UserCurrentSerializer(serializers.ModelSerializer):
    """
        Uses extra user model's fields in GET AND POST, PATCH /me/ endpoint.
    """
    skills = serializers.SlugRelatedField(many=True,
                                          required=False,
                                          slug_field='name',
                                          queryset=Skills.objects.all()
                                          )

    class Meta:
        model = User
        exclude = ["role", "email", "is_active", "last_login", "password"]


class UserSerializer(serializers.ModelSerializer):
    """
            Uses extra user model's fields in get /users/ endpoint.
    """
    # tags = TagListSerializerField()

    skills = serializers.SlugRelatedField(many=True,
                                          required=False,
                                          slug_field='name',
                                          queryset=Skills.objects.all()
                                          )

    class Meta:
        model = User
        exclude = ["role", "password", "is_active"]

    def is_valid(self, raise_exception=False):
        # Словарь который передает пользователь
        self._tags = self.initial_data.pop('skills')
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()
        # Допустим что мы обновляем поле Skills у кандидата, если обновляем полностью, то это clear
        # Если цель добавить туда навыки, то затереть #clear
        user.skills.clear()
        for skill_name in self._tags:
            # Извлечь если навык существует, создать если нет.
            skill, _ = Skills.objects.get_or_create(name=skill_name)
            user.skills.add(skill)
        return user


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Uses extra user model's fields in POST /users/ endpoint.
    """
    skills = serializers.SlugRelatedField(many=True,
                                          required=False,
                                          slug_field='name',
                                          queryset=Skills.objects.all()
                                          )

    class Meta:
        model = User
        exclude = ["password", "role", "is_active", "last_login"]

    def is_valid(self, raise_exception=False):
        # Словарь который передает пользователь
        self._tags = self.initial_data.get('skills', [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        for skill_name in self._tags:
            skill, _ = Skills.objects.get_or_create(name=skill_name)
            user.skills.add(skill)

        user.set_password(validated_data["password"])
        user.save()
        return user

# Не нравится taggit, возможно кому-то зашел, предпочитаю по старинке.
# C фиксутрами возникут проблемы итак далее. В целом я и с taggit оттестировал проект

# class UserCreateSerializer(TaggitSerializer, serializers.ModelSerializer):
#     """
#                 Uses extra user model's fields in POST /users/ endpoint.
#     """
#     # tags = TagListSerializerField()
#
#     class Meta:
#         model = User
#         exclude = ["role", "is_active", "last_login"]

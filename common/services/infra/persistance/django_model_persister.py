from __future__ import annotations
from dataclasses import dataclass
from typing import *

from django.db import models
from django.db.models import QuerySet


class ModelPersister(Protocol):
    """
    汎用DjangoMODEL永続化の契約を示すクラス
    """
    def exists_by_lookup(self, model_class: Type[models.Model], lookup: Dict[str, Any]) -> bool:
        """
        指定のTABLE、検索条件でレコードが存在するかを判定し返す
        
        :param model_class: 検索先MODEL名
        :param lookup: 検索条件 Dict[カラム名, 条件値]
        :return: true=存在する / false=存在しない
        """
        ...

    def create(self, model_class: Type[models.Model], data: Dict[str, Any]) -> models.Model:
        """
        指定のTABLE、データ内容で永続化を行う。
        
        :param model_class: 永続化先MODEL名
        :param lookup: 登録データ Dict[カラム名, 値]
        :return: 永続化したModelインスタンス
        :raises: ValidationError, DatabaseError
        """
        ...
        
    def lookup_first(self, model_class: Type[models.Model], lookup: Dict[str, Any]) -> models.Model | None:
        """
        指定のTABLE、検索条件で検索して1番目のレコードを返す
        
        :param model_class: 検索先MODEL名
        :param lookup: 検索条件 Dict[カラム名, 条件値]
        :return: Model: 検索結果のModel
        """
        ...
        
    def get(self, model_class: Type[models.Model], **lookup) -> models.Model:
        """
        指定のTABLE、検索条件で検索しレコードを1件返す。（1件しか当てたくない場合に使用）
        
        :param model_class: 検索先MODEL名
        :param lookup: 検索条件 Dict[カラム名, 条件値]
        :return: Model: 検索結果のModel
        :raises: ObjectDoesNotExist, MultipleObjectsReturned
        """
        ...


@dataclass(frozen=True)
class DjangoModelPersister(ModelPersister):
    """
    Django ORM を使った永続化（I/O）。
    domain/processor から ORM を隔離する。
    """

    def exists_by_lookup(
        self,
        model_class: Type[models.Model],
        lookup: Dict[str, Any]
    ) -> bool:

        return model_class.objects.filter(**lookup).exists()

    def create(
        self, 
        model_class: Type[models.Model], 
        data: Dict[str, Any]
    ) -> models.Model:
        
        obj: models.Model = model_class(**data)
        obj.full_clean()
        obj.save()
        
        return obj
    
    def lookup_first(self, model_class: Type[models.Model], lookup: Dict[str, Any]) -> models.Model | None:
        
        return model_class.objects.filter(**lookup).first()
    
    def get(self, model_class: Type[models.Model], **lookup) -> models.Model:
        
        return model_class.objects.get(**lookup)
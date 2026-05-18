import importlib


class ImportUtils:

    @staticmethod
    def import_class(full_path: str):
        """"""

        """
        引数のパスに対応するクラス型を返す。
        
        :param full_path: クラスの絶対パス
        :return klass: クラス型
        :raise ValueError: 該当クラスなし
        """

        module_path, class_name = full_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        klass = getattr(module, class_name)
        return klass

from typing import NamedTuple

from db import db

class Category(NamedTuple):
    codename: str
    name: str
    is_base_expense: bool
    aliases: list[str]


class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self) -> list[Category]:
        '''Загружает категории из БД и заполняет алиасы'''
        categories = db.fetchall("category", "codename name is_base_expense aliases".split())
        result = self._fill_aliases(categories)
        return result

    def _fill_aliases(self, categories: list[dict]) -> list[Category]:
        """Заполняет по каждой категории aliases, то есть возможные
                названия этой категории, которые можем писать в тексте сообщения.
                Например, категория 'кафе' может быть написана как cafe,
                ресторан и тд."""
        categories_result = []
        for index, category in enumerate(categories):
            aliases = category["aliases"].split()
            aliases = list(filter(None, aliases))
            aliases.append(category["codename"])
            aliases.append(category["name"])
            categories_result.append(Category(
                codename=category["codename"],
                name=category["name"],
                is_base_expense=category['is_base_expense'],
                aliases=aliases))
        return categories_result

    def get_all_categories(self) -> list[Category]:
        return self._categories

    def get_category(self, category_name: str) -> Category:
        """Возвращает категорию по одному из её алиасов."""
        found = None
        other_category = None
        for category in self._categories:
            if category.codename == "other":
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    found = category
        if not found:
            found = other_category
        return found



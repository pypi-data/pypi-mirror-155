# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['danio']

package_data = \
{'': ['*']}

install_requires = \
['cached-property>=1.5.2,<2.0.0', 'databases>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'danio',
    'version': '0.4.5.0',
    'description': 'ORM for asyncio world by dataclass',
    'long_description': '# Danio\n\n<p>\n<a href="https://github.com/strongbugman/danio/actions">\n    <img src="https://github.com/strongbugman/danio/workflows/UnitTest/badge.svg" alt="UnitTest">\n</a>\n<a href="https://pypi.org/project/danio/">\n    <img src="https://badge.fury.io/py/danio.svg" alt="Package version">\n</a>\n<a href="https://codecov.io/gh/strongbugman/danio">\n    <img src="https://codecov.io/gh/strongbugman/danio/branch/main/graph/badge.svg" alt="Code coverage">\n</a>\n</p>\n\n\nDanio is a ORM for python asyncio world.It is designed to make getting easy and clearly.It builds on python\'s dataclass and encode\'s [databases](https://github.com/encode/databases)\n\n## Features\n\n* keep OOM in mind, custom your Field and Model behavior easily\n* type hints any where, no more need to memorize words your field names any more\n* base CRUD operation, transactions, lock and so on\n* signals like before save, after save and so on\n* complex operation like bulk create, upsert, create or update and so on\n* assist model schema migration\n* support MySQL/PostgreSQL/SQLite\n\n## install\n\n`pip install danio`\n\n## Documents\n\n[Danio Document](https://strongbugman.github.io/danio/)\n\n## Glance\n\n```python\ndb = danio.Database(\n    "mysql://root:letmein@server:3306/test",\n    maxsize=3,\n    charset="utf8mb4",\n    use_unicode=True,\n    connect_timeout=60,\n)\n\n@dataclasses.dataclass\nclass User(danio.Model):\n    class Gender(enum.Enum):\n        MALE = 0\n        FEMALE = 1\n        OTHER = 2\n\n    name: str = danio.field(\n        danio.CharField,\n        comment="User name",\n        default=danio.CharField.NoDefault,\n    )\n    age: int = danio.field(danio.IntField)\n    created_at: datetime.datetime = danio.field(\n        danio.DateTimeField,\n        comment="when created",\n    )\n    updated_at: datetime.datetime = danio.field(\n        danio.DateTimeField,\n        comment="when created",\n    )\n    gender: Gender = danio.field(danio.IntField, enum=Gender, default=Gender.FEMALE)\n\n    async def before_create(self, **kwargs):\n        # user_count += 1\n        await super().before_create(**kwargs)\n\n    async def before_update(self, **kwargs):\n        self.updated_at = datetime.datetime.now()\n\n    async def validate(self):\n        await super().validate()\n        if not self.name:\n            raise danio.ValidateException("Empty name!")\n\n    @classmethod\n    def get_database(\n        cls, operation: danio.Operation, table: str, *args, **kwargs\n    ) -> danio.Database:\n        return db\n\n# base CRUD\nuser = await User(name="batman").save()\nuser = await User.where(User.name == "batman").fetch_one()\nuser.gender = User.Gender.MALE\nawait user.save()\nawait user.delete()\n# sql chain\nawait User.where(User.name != "").limit(10).fetch_all()\n# multi where condition\nawait User.where(User.id != 1, User.name != "").fetch_all()\nawait User.where(User.id != 1).where(User.name != "").fetch_all()\nawait User.where(User.id <= 10, User.id >= 20, is_and=False).fetch_all()\n# complicated expression\nawait User.where(User.id == 1).update(age=(User.age + 1) / (User.age / 12) - 2)\nawait User.where((User.age + 1) == 3).fetch_all()\n# complicated sql operation\nawait User.where(User.id == u.id).update(\n    age=User.age.case(User.age > 10, 1, default=18).case(User.age <= 0, 10)\n)\ncreated, updated = await UserProfile.upsert(\n    [\n        dict(id=1, name="upsert"),\n    ],\n    update_fields=["name"],\n)\n# bulk operation\nawait User.bulk_create([User(name=f"user_{i}") for i in range(10)])\nawait User.bulk_update(await User.fetch_all())\nawait User.bulk_delete(await User.fetch_all())\n# shortcut\nuser, created = await User(id=1, name="created?").get_or_create(\n    key_fields=(User.id,)\n)\nuser, created, updated = await User(id=2, name="updated?").create_or_update(\n    key_fields=(User.id,)\n)\n```',
    'author': 'strongbugman',
    'author_email': 'strongbugman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

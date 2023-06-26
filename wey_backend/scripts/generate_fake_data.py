import os
import pathlib
import random
import sys
from datetime import timedelta

import django
from django.apps import apps
from django.utils import timezone

import faker

# 将项目根目录添加到 Python 的模块搜索路径中
back = os.path.dirname
BASE_DIR = back(back(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == "__main__":
    # 启动 django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wey_backend.settings")
    django.setup()

    from post.models import Post, Comment
    from account.models import User

    # 取消实时索引生成，因为本地运行 fake 脚本时可能并未启动 Elasticsearch 服务。
    # apps.get_app_config("haystack").signal_processor.teardown()

    print("clean database")
    Post.objects.all().delete()
    Comment.objects.all().delete()
    User.objects.all().delete()

    print("create a blog user")
    user = User.objects.create_superuser("admin", "admin@123.com", "admin")
    commenter = User.objects.create_superuser("commenter", "commenter@123.com", "commenter")

    a_year_ago = timezone.now() - timedelta(days=365)

    # print("create a markdown sample post")
    # Post.objects.create(
    #     title="Markdown 与代码高亮测试",
    #     body=pathlib.Path(BASE_DIR)
    #     .joinpath("scripts", "md.sample")
    #     .read_text(encoding="utf-8"),
    #     category=Category.objects.create(name="Markdown测试"),
    #     author=user,
    # )

    print("create some faked posts published within the past year")
    fake = faker.Faker()  # English
    for _ in range(100):
        created_time = fake.date_time_between(
            start_date="-1y", end_date="now", tzinfo=timezone.get_current_timezone()
        )
        # created_time = fake.iso8601()
        # print(created_time)
        post = Post.objects.create(
            body="\n\n".join(fake.paragraphs(10)),
            created_at=created_time,
            created_by=user,
        )
        post.save()

    fake = faker.Faker("zh_CN")
    for _ in range(100):  # Chinese
        created_time = fake.date_time_between(
            start_date="-1y", end_date="now", tzinfo=timezone.get_current_timezone()
        )
        post = Post.objects.create(
            body="\n\n".join(fake.paragraphs(10)),
            created_at=created_time,
            created_by=user,
        )
        post.save()

    print("create some comments")
    for post in Post.objects.all()[:20]:
        post_created_time = post.created_at
        delta_in_days = "-" + str((timezone.now() - post_created_time).days) + "d"
        for _ in range(random.randrange(3, 15)):
            comment = Comment.objects.create(
                body=fake.paragraph(),
                created_by=commenter,
            )
            post.comments.add(comment)
            post.comments_count += 1
        post.save()

    print("done!")
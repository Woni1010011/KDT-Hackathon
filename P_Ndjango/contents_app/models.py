from django.db import models

# Create your models here.


class Ingredients(models.Model):
    igrd_no = models.BigAutoField(primary_key=True)  # 주 키로 설정된 bigserial 필드
    igrd_name = models.CharField(max_length=255, null=False)  # varchar(255) 필드
    igrd_content = models.TextField(null=True)  # text 필드 (NULL 허용)
    # 소비기한 삭제

    def __str__(self):
        return self.igrd_name


class Board(models.Model):
    post_no = models.BigAutoField(primary_key=True)  # 주 키로 설정된 bigserial 필드
    board_no = models.IntegerField(null=False)  # int 필드
    post_title = models.CharField(max_length=255, null=False)  # varchar(255) 필드
    post_content = models.TextField(null=True)  # text 필드 (NULL 허용)
    user_nick = models.CharField(max_length=50, null=False)  # varchar(50) 필드
    post_time = models.DateTimeField(auto_now_add=True)  # timestamp 필드
    post_like = models.IntegerField(default=0, null=False)  # int 필드
    post_hit = models.IntegerField(default=0, null=False)


class Comment(models.Model):
    post_no = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name="comments"
    )  # board 테이블 참조
    comment_content = models.TextField(null=False)  # text 필드
    comment_time = models.DateTimeField(null=False)  # timestamp 필드

    def __str__(self):
        return self.comment_content[:20] + "..."


class Recipe(models.Model):
    recipe_no = models.BigAutoField(primary_key=True)
    recipe_title = models.CharField(max_length=255, null=False)
    recipe_level = models.CharField(max_length=100, null=True)
    cook_time = models.CharField(max_length=100, null=True)
    serving = models.CharField(max_length=100, null=True)
    ingredients = models.TextField(null=False)
    direction = models.TextField(null=False)
    recipe_img = models.TextField(null=True)
    cooking_tips = models.TextField(null=True)
    recipe_url = models.CharField(max_length=255, null=True)
    importance = models.FloatField(null=True)

    def __str__(self):
        return self.recipe_title

    class Meta:
        db_table = "contents_app_recipe"


class Recipes(models.Model):
    recipe_no = models.BigAutoField(primary_key=True)
    recipe_title = models.CharField(max_length=255, null=False)
    recipe_level = models.CharField(max_length=100, null=True)
    cook_time = models.CharField(max_length=100, null=True)
    serving = models.CharField(max_length=100, null=True)
    ingredients = models.TextField(null=False)
    direction = models.TextField(null=False)
    recipe_img = models.TextField(null=True)
    cooking_tips = models.TextField(null=True)
    recipe_url = models.CharField(max_length=255, null=True)
    importance = models.FloatField(null=True)

    def __str__(self):
        return self.recipe_title

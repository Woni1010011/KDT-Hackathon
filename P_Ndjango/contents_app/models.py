from django.db import models

# Create your models here.

class Ingredients(models.Model):
    igrd_no = models.BigAutoField(primary_key=True)  # 주 키로 설정된 bigserial 필드
    igrd_name = models.CharField(max_length=255, null=False)  # varchar(255) 필드
    igrd_content = models.TextField(null=True)  # text 필드 (NULL 허용)
    exp_date = models.DateField(null=False)  # date 필드

    def __str__(self):
        return self.igrd_name
    
class Board(models.Model):
    board_no = models.BigAutoField(primary_key=True)  # 주 키로 설정된 bigserial 필드
    post_no = models.IntegerField(null=False)  # int 필드
    post_title = models.CharField(max_length=255, null=False)  # varchar(255) 필드
    post_content = models.TextField(null=True)  # text 필드 (NULL 허용)
    user_nick = models.CharField(max_length=50, null=False)  # varchar(50) 필드
    post_time = models.DateTimeField(null=False)  # timestamp 필드
    post_like = models.IntegerField(default=0, null=False)  # int 필드

    def __str__(self):
        return self.post_title

class Comment(models.Model):
    post_no = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="comments")  # board 테이블 참조
    comment_content = models.TextField(null=False)  # text 필드
    comment_time = models.DateTimeField(null=False)  # timestamp 필드

    def __str__(self):
        return self.comment_content[:20] + "..."






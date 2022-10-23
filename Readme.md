## 목표

페어 프로그래밍을 통한 영화 리뷰 커뮤니티 서비스를 개발합니다. 아래 조건을 만족해야합니다.

- **CRUD** 구현

- **Staticfiles** 활용 정적 파일(이미지, CSS, JS) 다루기

- Django **Auth** 활용 회원 관리 구현

- Media 활용 동적 파일 다루기

- 모델간 

  1 : N 관계

   매핑 코드 작성 및 활용

  - 유저 - 리뷰
  - 리뷰 - 댓글
  - 유저 - 댓글

## 토픽

### 깃 저장소 생성

branch master

1. 원격 저장소 생성

2. 콜라보레이터 초대

3. 로컬 저장소 깃 초기화

4. 로컬 저장소 .gitignore 생성 & 작성

   [gitignore.io](https://www.toptal.com/developers/gitignore/)

------

### 개발환경 설정

branch setup-env

1. Django 프로젝트 생성

2. 가상환경 생성 & 실행

3. 필요한 패키지 설치

4. 패키지 목록 저장

   ```bash
   pip freeze > requirements.txt
   ```

5. Django 프로젝트 생성

   ```bash
   django-admin startproject config .
   ```

------

### 회원 가입

branch account/signup

앱 App 생성

- 앱 이름 : accounts

모델 Model 작성

- 모델 이름 : User
- Django AbstractUser 모델 상속

폼 Form 작성

- Django 내장폼 UserCreationForm을 상속받은 CustomUserCreationForm 작성

기능 View

- `POST` accounts/signup/
- CustomUserCreationForm 활용

화면 Template

- `GET` accounts/signup/
- 회원가입 폼
- ![image-20221023151141995](Readme.assets/image-20221023151141995.png)

------

### 로그인

branch accounts/login

기능 View

- `POST` accounts/signup/
- 내장 폼 AuthenticationForm 활용

화면 Template

- `GET` accounts/signup/
- 로그인 폼
- 회원가입 페이지 이동 버튼
- ![image-20221023151159080](Readme.assets/image-20221023151159080.png)

------

### 로그아웃

branch accounts/logout

기능 View

- `POST` account/logout
- ![image-20221023151232240](Readme.assets/image-20221023151232240.png)

------

### 리뷰 작성

branch reviews/create

앱 App 생성

앱 이름 : reviews

모델 Model 생성

모델 이름 : Review

- 모델 필드

  | 이름       | 역할          | 필드                | 속성              |
  | ---------- | ------------- | ------------------- | ----------------- |
  | user       | 리뷰 작성자   | FK                  |                   |
  | title      | 리뷰 제목     | CharField           |                   |
  | content    | 리뷰 내용     | TextField           |                   |
  | movie_name | 영화 이름     | CharField           |                   |
  | grade      | 영화 평점     | FloatField          |                   |
  | created_at | 리뷰 생성시간 | DateTime            | auto_now_add=True |
  | updated_at | 리뷰 수정시간 | DateTime            | auto_now = True   |
  | image      | 영화 포스터   | ProcessedImageField |                   |

기능 View

- `POST` reviews/create/

화면 Template

- `GET` reviews/create/
- 리뷰 작성 폼

```py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your views here.
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    movie_name = models.CharField(max_length=50)
    grade = models.FloatField(validators=[MinValueValidator(0.0),MaxValueValidator(5.0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(upload_to='images/', blank=True,
                                processors=[ResizeToFill(1200, 960)],
                                format='JPEG',              
                                options={'quality': 80})

```



------

### 리뷰 목록 조회

branch reviews/index

**기능 View**

- `GET` reviews/

**화면 Template**

- `GET` reviews/
- ![image-20221023151547035](Readme.assets/image-20221023151547035.png)

------

### 리뷰 정보 조회

branch reviews/detail

**기능 View**

- `GET` reviews/[int:review_pk](int:review_pk)/

**화면 Template**

- `GET` reviews/[int:review_pk](int:review_pk)/
- 리뷰 수정 / 삭제 버튼
  - 수정 / 삭제 버튼은 해당 리뷰 작성자에게만 출력합니다.
- 댓글 작성 폼
  - 댓글 작성 폼은 로그인 사용자에게만 출력합니다.
- 댓글 목록
- ![image-20221023151608928](Readme.assets/image-20221023151608928.png)

------

### 리뷰 정보 수정

branch reviews/update

**기능 View**

- `POST` reviews/[int:review_pk](int:review_pk)/update/
- 데이터를 생성한 사용자만 수정할 수 있습니다.

**화면 Template**

- `GET` reviews/[int:review_pk](int:review_pk)/update/
- 리뷰 수정 폼
- ![image-20221023151951881](Readme.assets/image-20221023151951881.png)

------

### 리뷰 삭제

branch reviews/delete

**기능 View**

- `POST` http://127.0.0.1:8000/reviews/[int:review_pk](int:review_pk)/delete/
- 데이터를 생성한 사용자만 삭제할 수 있습니다.
- ```py
  def delete(request, pk):
      review = Review.objects.get(pk=pk)
      review.delete()
  
      return redirect('reviews:index')
  ```
- 

------

### 댓글 작성

branch comments/create

reviews 앱에 구현

모델 Model 생성

모델 이름 : Comment

- 모델 필드

  | 이름    | 역할        | 필드      | 속성 |
  | ------- | ----------- | --------- | ---- |
  | review  | 참조 리뷰   | TextField |      |
  | user    | 댓글 작성자 | FK        |      |
  | content | 댓글 내용   | FK        |      |

기능 View

- `POST` reviews/[int:review_pk](int:review_pk)/comments/
- 로그인한 사용자만 댓글을 생성할 수 있습니다.

화면 Template

- `GET` reviews/[int:review_pk](int:review_pk)/
- 리뷰 정보 조회 페이지 하단에 댓글 작성 폼 출력

```py	
    
class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    
```



### 댓글 목록 조회

branch comments/index

기능 View

- `GET` reviwes/[int:review_pk](int:review_pk)/

화면 Template

- `GET` reviews/[int:review_pk](int:review_pk)/
- 리뷰 정보 조회 페이지 하단에 댓글 목록 출력
- ![image-20221023153034664](Readme.assets/image-20221023153034664.png)

------

### 댓글 삭제

branch comments/delete

기능 View

- `POST` reviews/[int:review_pk](int:review_pk)/comments/[int:comment_pk](int:comment_pk)/delete/
- 데이터를 생성한 사용자만 삭제할 수 있습니다.

화면 Template

- `GET` reviews/[int:review_pk](int:review_pk)/
- 각 댓글에 리뷰 삭제 버튼 추가
  - 삭제 버튼은 해당 댓글 작성자에게만 출력합니다.

![image-20221023153100915](Readme.assets/image-20221023153100915.png)

작성자만 삭제 가능, 로그인 시 댓글 작성 가능 (template에서 처리함)


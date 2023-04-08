# CEOS 17기 백엔드 스터디

### 에브리타임 서비스 설명 w/ ERD
* 데이터 모델링 분류를 크게 **account**, **board**, **timetable** 세가지로 나누었다.
* account 기능: User, School
    * 사용자는 가입할 때, 학교를 선택하여야 한다.
    * 이후 사용자는 개인 정보(아이디, 비밀번호, 이메일, 닉네임, 입학연도 등)를 입력하여 에브리타임에 가입한다. 
* board 기능(커뮤니티 기능): Board, Post, Message, My_board, Post_media, Comment, Scrap
    * 사용자는 게시판을 즐겨찾기를 통해 고정할 수 있다.
    * 사용자는 게시물을 작성할 수 있으며, 게시물을 스크랩, 공감할 수 있고, 댓글과 대댓글을 작성할 수 있다.
    * 사용자는 스크랩한 게시물을 따로 모아서 볼 수 있다. 
    * 사용자는 게시글을 쓴 사람 혹은 댓글을 단 사람과 쪽지를 주고 받을 수 있다.
* timetable 기능: Friend, Timetable, Lecture, My_lecture, Review
    * 사용자는 강의를 선택하여 시간표에 넣을 수 있다.
    * 사용자는 선택한 강의에 대해 강의평을 작성할 수 있다. 
    * 사용자는 친구맺기 기능을 통해 친구와 시간표를 공유할 수 있다.
![img_6.png](img_6.png)

### ORM 이용해보기
* ForeignKey 필드를 포함하는 모델로 **Board**을 선택하였다. 
1. 데이터베이스에 해당 모델 객체 3개 이상 넣기
```angular2html
from account.models import School
school1 = School(school_name = '홍익대학교')
school1 = School(school_name = '이화여자대학교')
school1 = School(school_name = '서강대학교')
school1 = School(school_name = '연세대학교')
```
![img.png](img.png)
```angular2html
from board.models import Board
board1 = Board(category = '학과', name = '홍익대컴퓨터공학과', school_id_id = 1)
board1 = Board(category = '학과', name = '컴퓨터공학과', school_id_id = 1)
board2 = Board(category = '진로', name = '진로게시판', school_id_id = 2)
board3 = Board(category = '홍보', name = '홍보게시판', school_id_id = 3)
board4 = Board(category = '단체', name = '총학생회', school_id_id = 4)
```
![img_1.png](img_1.png)
2. 삽입한 객체들을 쿼리셋으로 조회해보기
```angular2html
Board.objects.all()
```
![img_2.png](img_2.png)
3. filter 함수 사용해보기
```angular2html
Board.objects.filter(category= '단체')
```
![img_3.png](img_3.png)

### 겪은 오류와 해결 과정
* 메세지에서 두 속성이 같은 유저를 참고할 때 related_name을 설정하라는 오류가 발생했다.
* User 입장에서는 Message에서 두개의 필드가 참조를 하고 있기 때문에 역참조하는 입장에서 생각해봤을 때 이를 구분해달라는 오류인 것 같다고 생각했다.
```angular2html
user = models.ForeignKey(User, on_delete=models.PROTECT)
sender = models.ForeignKey(User, related_name='sender',on_delete=models.PROTECT)
```
related_name 역할?
* User 인스턴스와 연결되어 있는 Message를 거꾸로 불러올 때, related_name='sender' 라는 이름으로 부르겠다고 지정해 준 것이다.
* ralated_name이 필수는 아니지만 위 경우처럼 한 테이블에서 서로 다른 두 속성이 같은 테이블을 참조할  때는 필수로 지정해주어야 한다.

### 새롭게 알게 된점
1. 커스텀 User 모델
* 커스텀 User 모델을 작성하는 세 가지 방법
  *  표준 User 모델과 1대 1 관계를 가지는 모델을 만드는 방법
  * AbstractUser을 상속받는 모델을 만드는 방법
  * AbstractBaseUser을 상속받는 모델을 만드는 방법
* 세가지 중, AbstractBaseUser을 상속받아 구현하였다.
* 커스터마이즈 유연성이 세가지 중 가장 높다.(=최소한의 필드만 제공)
2. 생성시각, 수정시각
```angular2html
class TimestampedModel(models.Model):
    # 생성된 날짜를 기록
    created_at = models.DateTimeField(auto_now_add=True)
    # 수정된 날짜를 기록
    updated_at = models.DateTimeField(auto_now=True)
```
언제 만들어졌고 수정되었는지는 향후 유지보수에 있어서 굉장히 중요한 정보이기 때문에 TimestampedModel 클래스를 따로 만들어 모든 클래스가 이를 상속받도록 하였다.
3. UUID
* 중복되지 않는 ID를 만드는 표준 규약
* 계속해서 생성하여도 중복될 확률이 0에 가깝다고 한다.
* 사용자의 기본키를 UUIDField로 지정하였다.
* 기본키가 연속성의 규칙을 가지면 보안상의 문제도 무시할 수 없을 것이다. 
```angular2html
user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```
4. 대댓글 자기 참조
* 대댓글도 본질은 댓글이기 때문에 따로 테이블을 만들지 않고 'self'로 자기 참조를 통해 구현하였다.
* 이 필드에 값이 있으면 대댓글, 없으면 댓글이다.
```angular2html
parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
```

### 회고
작년에 데이터베이스 강의를 들었을 때 교수님께서 현실에 있는 데이터를 추상화하는 과정(모델링)이 데이터베이스를 다룰 때 가장 중요한 부분이라고 강조하셨던 기억이 있어서 이번 과제를 하는데 있어서 ERD를 짜는 데 가장 많은 시간을 할애하였다.
과제를 하면서 가장 헷갈렸던 부분 중 하나가 테이블을 어디까지 세세하게 나누어야하고, 어떤 정보를 담아야할지였는데 내가 에브리타임을 사용하는 사람일 경우를 기준으로 생각해보니 필요한 정보만을 추출하여 ERD를 짤 수 있었다.
그리고 우리가 실제로 자주 사용하는 어플을 가지고 데이터 모델링을 해볼 수 있어서 재미있었고, Django와 조금은(?) 더 친해진 느낌이다.....ㅎ


# CEOS 17기 백엔드 3주차 스터디

## 2주차 데이터 모델링 피드백 반영

### CharField를 TextField로 수정
```python
content = models.TextField(blank=False)
```
- MySQL에서 char type의 최댓값은 255이기 때문에, 이보다 더 큰 값을 넣어줘야 하는 필드는 TextField로 바꿔주었다.

### class naming 규칙 반영
- My_board 를 MyBoard 로 변경하였다.
- My_Lecture 를 MyLecture 로 변경하였다.

## 3주차 미션: DRF1 - Serializer, API View & Filter

### Serializer

- Serializer는 Django가 다룰 수 있는 객체를 외부에서 받는 JSON 등의 데이터 형태로 변환한다는 것을 의미한다. 
- Deserialize는 Serializer와 반대되는 개념이다.
- 요청 JSON 데이터를 Deserialize 하여 Django 객체에 저장하고, 
- Django 객체를 Serializer 하여 응답 JSON 데이터로 바꿔주는 것이다.

### Nested Serializer

- 두 테이블 간의 관계를 표현하기 위해서 Nested Serializer 를 사용하였다.
```python
class BoardSerializer(serializers.ModelSerializer):
    school_id = SchoolSerializer

    class Meta:
        model = Board  # models.py의 board 사용
        fields = '__all__'  # 모든 필드 포함
```

- School 과 Board 는 1:N 의 관계를 가지므로, Board 에 관련된 School 의 정보를 함께 가져오기 위해 Nested Serializer 를 사용하였다.

### 의문점

- 저번 과제에서 models.py를 구현할 때, 대댓글 테이블을 따로 만들지 않고 댓글 테이블을 자기 참조하여 만들었는데 이를 Serializer로 구현하려니 코드가 이상해졌다.
```python
parent_comment = CommentSerializer()
```
- 위 코드를 CommentSerializer 에 넣으니 에러가 나는 것을 보고, Serializer 는 자기 참조가 안 되는 듯 보였다.
- 그래서 아래와 같이 코드를 InCommentSerializer 를 따로 만들어 코드를 리팩토링 해보았다.
```python
class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer
    user = UserSerializer

    # parent_comment = CommentSerializer()

    class Meta:
        model = Comment  
        fields = '__all__'  # 모든 필드 포함


class InCommentSerializer(serializers.ModelSerializer):
    parent_comment = CommentSerializer

    class Meta:
        model = Comment
        fields = '__all__'  # 모든 필드 포함
```
- InCommentSerializer 는 Comment 클래스에 있는 모드 필드를 포함하되, **parent_comment = CommentSerializer** 를 설정하여 CommentSerializer 와 관계를 맺도록 하였다.
- 이와 관련해서 구글링을 해보았지만 참고할 만 한 레퍼런스가 딱히 없어서 이렇게 구현을 했는데 이런 방법이 맞는 것인지 궁금합니다..

###  CBV (Class-Based View)

```python
class BoardList(APIView):

    def get(self, request, format=None):  
        try:
            board_list = Board.objects.all()
            serializer = BoardSerializer(board_list, many=True)
            return Response(serializer.data)
        except AttributeError as e:
            print(e)
            return Response("message: error")

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class BoardDetail(APIView):
    def get(self, request, pk):
        try:
            board = Board.objects.get(id=pk)
            serializer = BoardSerializer(board)
            return Response(serializer.data, status=201)
        except ObjectDoesNotExist as e:
            print(e)
            return Response({"message: error"})

    def delete(self, request, pk):
        try:
            board = Board.objects.get(id=pk)
            board.delete()
            return Response(status=200)
        except ObjectDoesNotExist as e:
            print(e)
            return Response({"message: not exist"})
```
- BoardList 는 APIView 를 상속받고 있다.
- APIView는 클래스로 정의된다.
- APIView를 상속받은 클래스 안에 request method에 맞는 함수들을 정의해주면 각각의 요청은 request method 이름에 맞게 구분되어 그에 맞는 결과를 반환하게 된다. 
 
### ViewSet 으로 리팩토링

- 여러가지 API 기능을 통합해서 하나의 API set 으로 제공하는 것이다.
- CBV 로 작성한 코드를 보면 BoardList, BoardDetail 각각의 api 가 중복되는 경우가 있다. 
- 이럴때 ViewSet 을 쓰게 되면 중복되는 로직의 코드를 줄일 수 있어 코드의 효율성을 높일 수 있다.
- ViewSet은 .get(), .post() 대신 .list(), .create() 같은 액션을 제공한다. 
```python
class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BoardFilter
```

### URL 매핑 with Router
```python
router = routers.DefaultRouter()
router.register('board', BoardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```
- viewset들의 view를 명시적으로 등록하는 것보다 router 클래스를 사용해 viewset을 등록하였다. 

### Filtering 기능 구현하기
```python
class BoardFilter(FilterSet):
    name = filters.CharFilter(field_name='name')
    school_id = filters.NumberFilter(method='filter_school_id')

    def filter_school_id(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })

    class Meta:
        model = Board
        fields = ['name', 'school_id']
```
- Board 클래스 내의 name, school_id_id 에 필터를 걸어 줄 BoardFilter 클래스를 FilterSet 을 상속해 선언해주었다.

### 모든 데이터를 가져오는 API 만들기

- Board의 모든 list를 가져오는 API 요청 결과

  - url : board/ 
  - method: GET
```
{
        "id": 3,
        "created_at": "2023-04-01T01:33:26.211450+09:00",
        "updated_at": "2023-04-01T01:33:26.211450+09:00",
        "category": "진로",
        "name": "진로게시판",
        "is_deleted": false,
        "school_id": 2
    },
    {
        "id": 2,
        "created_at": "2023-04-01T01:33:18.361955+09:00",
        "updated_at": "2023-04-01T01:33:18.362962+09:00",
        "category": "학과",
        "name": "컴퓨터공학과",
        "is_deleted": false,
        "school_id": 1
    },
    {
        "id": 1,
        "created_at": "2023-04-01T01:25:16.489555+09:00",
        "updated_at": "2023-04-01T01:25:16.489555+09:00",
        "category": "학과",
        "name": "홍익대컴퓨터공학과",
        "is_deleted": false,
        "school_id": 1
    }
```
![BoardList](https://user-images.githubusercontent.com/81136546/230720061-8c31293c-e3b4-410c-abb9-4613d71344dc.png)

### 특정 데이터를 가져오는 API 만들기

- 3번째 Board를 가져오는 API 요청 결과 
  - url: board/3/
  - method: GET
```
{
    "id": 3,
    "created_at": "2023-04-01T01:33:26.211450+09:00",
    "updated_at": "2023-04-01T01:33:26.211450+09:00",
    "category": "진로",
    "name": "진로게시판",
    "is_deleted": false,
    "school_id": 2
}
```
![BoardDetail](https://user-images.githubusercontent.com/81136546/230720765-d1c30990-8926-4100-9cfc-8d054253fd66.png)

### 새로운 데이터를 create하도록 요청하는 API 만들기

- Board를 추가하는 API 요청 결과
  - url: board/
  - method: POST

![POST](https://user-images.githubusercontent.com/81136546/230721062-e08f08f2-f2f3-401c-8a67-6a562794989f.png)

![POST1](https://user-images.githubusercontent.com/81136546/230721095-7a5f4b35-57eb-403b-bd38-e9ee5c2903c5.png)

### 특정 데이터를 삭제 또는 업데이트하는 API

- 특정 Board 를 삭제하는 API 요청 결과
  - url: board/4/
  - method: DELETE
- id가 4인 board 를 삭제한 후 다시 /board/4 로 GET 요청을 하면 아래와 같이 뜬다.
```python
{
    "detail": "찾을 수 없습니다."
}
```

### 겪은 오류와 해결 과정
1. many = True 추가
```python
class BoardList(APIView):

    def get(self, request, format=None):  
        try:
            board_list = Board.objects.all()
            serializer = BoardSerializer(board_list, many = True)
            return Response(serializer.data)
        except AttributeError as e:
            print(e)
            return Response("message: error")
```
- Serializer 에 해당 필드가 있는데 자꾸 없다는 오류가 떴다. 
- serializer로 보내주는 데이터가 여러 개의 object인 queryset 인 경우,
- queryset을 넘겨주기 위해서는 **many=True** 를 추가로 작성해줘야 한다고 한다.
- 나와 같은 오류를 해결한 블로그를 첨부하겠다. 
  [many=True](https://dongza.tistory.com/20)

2. Nested Serializer

- Nested Serializer 를 사용하는 이유는 두 테이블 간의 관계를 연결시켜, 외래키가 포함된 테이블의 정보까지 함께 보기 위함이다.
- 하지만 외래키인 school_id_id 필드를 넣어줬음에도 'school_id_id cannot be null' 이라는 에러가 뜨며 api가 돌아가지 않았다.
- 그래서 아래와 같이 SchoolSerializer 뒤에 괄호를 없앴더니 정상적으로 돌아가긴 했다.
- 결과적으로는 돌아가지만 내가 구현한 것은 사실 Nested Serializer 는 아닌 것이다..
- 이 부분은 추후에 수정해야겠다고 생각했다..!
```python
class BoardSerializer(serializers.ModelSerializer):
    school_id = SchoolSerializer

    class Meta:
        model = Board  # models.py의 board 사용
        fields = '__all__'  # 모든 필드 포함
```

### 회고

- ViewSet 을 사용하니 확실히 따로 api 를 구현할 때 보다 코드 길이가 줄어드는게 너무 신기했고 개발자 입장에서 너무 편리하다고 생각이 들었다.
- 직접 API 를 만들고 값을 넣어가며 눈으로 보이는 코딩을 할 수 있어서 확실히 지난 과제보다 재미있었다ㅎㅎㅎ!!
- nested serializer에서 미흡한 점이 있었지만 이번 과제를 함으로써 django 에서 쓰이는 다양한 기능을 써볼 수 있어서 정말 유익했다!!
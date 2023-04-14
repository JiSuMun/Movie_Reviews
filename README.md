# 영화 후기 공유 서비스 프로젝트
### 서현석, 문지수, 최충현

## 기능 구현

1. accounts
    - 회원가입, 로그인, 로그아웃, 회원정보수정, 비밀번호 수정
    - 프로필 페이지
      - 각 사용자가 작성한 리뷰 확인 가능

2. reviews
    - 리뷰 조회, 생성, 수정, 삭제
      - 비로그인 사용자: 조회만 가능
    - 댓글 조회, 생성, 삭제
      - 댓글을 중간에서 삭제해도 앞의 숫자를 채워 자연스럽게 댓글 번호 생성


## 문제점 - 해결

1. 이미지 사이즈
    - detail 페이지에서 원본 이미지만큼 이미지 출력되는 현상
    - imageKit 활용
      - quality를 설정하지 않았음에도 이미지가 계속해서 깨짐
        - 이미지의 비율이 일치하지 않을 경우 깨지는 현상이 발생 가능
    - Image, BytesIO import 하여 해결
        - reviews.views.py - def create(request) 참고
2. profile에서 detail 페이지 이동 안됨
    - 홑따옴표 실수
3. profile에서 후기번호 구현
    - {{ forloop.counter }} 이용
4. 이미지 사이즈 수정 후 'NoneType' object has no attribute 'read' 에러 발생
    - 업로드된 파일이 없는 경우 cleaned_data에 'image'가 없기 때문에, image 변수에 None 값이 할당되어 NoneType 객체가 되고, 이후 .read() 메소드를 호출할 때 'NoneType' object has no attribute 'read' 에러가 발생
    - form.is_valid 전 cleaned_data에서 'image'가 있는지 검사
    - if 'image' in request.FILES: 추가하여 해결
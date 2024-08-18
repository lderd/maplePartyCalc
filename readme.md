

## 배포

배포는 aws ec2에 깃을 연결하여 docker build 후 docker 실행하는 방식으로 되어있음.

실행할 때, 깃 내부의 `Dockerfile`의 위치에서 다음 실행

```bash
docker build -t myimage .
docker run -d --name mycontainer -p 80:80 myimage
```

정지할 때, 컨테이너는 고유해야 하기에 사용한 컨테이너를 삭제한다.

```bash
docker stop mycontainer
docker rm mycontainer
```

## DNS

dnsexit에서 무료 dns 사용. 2025-08-17에 expiration됨. 30일 전부터 renew 가능. 1년단위로 계속 renew 할 시 무료.

## 아래를 app파일 내부에 .env 환경변수 파일에 저장하여 사용할것

APILAYER_KEY="이미지 to 텍스트 사이트 api 키"  
AWS_ACCESS_KEY="aws 엑세스 키"  
AWS_SECRET_ACCESS_KEY="aws 비밀 엑세스 키"  
AWS_BUCKET_NAME="이미지 업로드 될 s3 버킷 이름"

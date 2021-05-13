# 이 프로그램은?
> 크로마키 편집기

크로마키 배경에서 객체를 추출하여 다른 배경화면에 삽입할 수 있는 편집기 입니다.
배경에 해당하는 부분을 클릭하고 상단의 H,S,V를 조절하여 배경을 제거하고, 객체를 드래그하여 선택한 후 다른 배경화면에 드래그해서 선택한 객체를 삽입할 수 있습니다.

## 개발 환경
- Windows 10
- Python 3.7.4

## Requirement
```sh
pip install -r requirements.txt
```

## 시작하기
- 1.파이썬 IDE로 실행하기(ex 파이참)

- 2.명령어로 실행하기
    ```sh
    python chromakey_editor.py
    ```

## 조작 키
- `마우스 좌클릭` : 배경 픽셀 선택
- `클릭 후 드래그` : 객체 선택 or 객체 삽입
- `B` : 배경화면 윈도우 창 열기
- `C` : 배경화면 윈도우 창 초기화
- `S` : 배경화면 윈도우 창 이미지 저장
- `ESC` : 프로그램 종료


## 미리보기
![1](https://user-images.githubusercontent.com/59381113/118110024-de80d080-b41c-11eb-88c9-4c6062755c3f.gif)
---
![2](https://user-images.githubusercontent.com/59381113/118110030-e04a9400-b41c-11eb-8ba1-45673f8accb6.gif)

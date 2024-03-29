# 크로마키 편집기
import cv2 as cv
import numpy as np
import imutils


# 트랙바 콜백 함수
def nothing(x):
    pass


# A 윈도우 마우스 콜백 함수
def mouse_callback(event, x, y, flags, param):
    global image_copy, mouse_pressed
    global s_x, s_y, e_x, e_y
    global colorHSV

    # 마우스 클릭 시
    if event == cv.EVENT_LBUTTONDOWN:
        mouse_pressed = True

        # 파란색 사각형 초기화(클릭하면)
        image_copy = np.copy(originImg)

        # 선택 시작 좌표 기록
        s_x, s_y = x, y

        # 배경 화소 샘플 채취
        # 선택한 픽셀의 BGR값
        colorBGR = image_copy[s_y, s_x]
        # 선택한 픽셀의 HSV값
        colorHSV = cv.cvtColor(image_copy, cv.COLOR_BGR2HSV)[s_y, s_x]

        # 좌표,RGB,HSV 터미널 창에 출력
        print("=============================================================================")
        print(f"좌표(x, y) : ({s_x}, {s_y})")
        print(f"RGB : {colorBGR[::-1]}")    # 출력할때는 BGR->RGB로 변경
        print(f"HSV : {colorHSV}")


    # 마우스 클릭 하고 이동시
    elif event == cv.EVENT_MOUSEMOVE:
        if mouse_pressed:
            # 중복되는 파란색 사각형 제거
            image_copy = np.copy(originImg)

            # 파란색 사각형으로 선택 영역 보이기
            cv.rectangle(image_copy, (s_x, s_y),
                         (x, y), (0, 255, 0), 1)

    elif event == cv.EVENT_LBUTTONUP:
        mouse_pressed = False
        # 선택 종료 좌표 기록
        e_x, e_y = x, y

        # y축상의 시작점과 끝점이 바뀌었으면 두 좌표를 바꾼다.
        if s_y > e_y:
            s_y, e_y = e_y, s_y

        # x축상의 시작점과 끝점이 바뀌었으면 두 좌표를 바꾼다.
        if s_x > e_x:
            s_x, e_x = e_x, s_x

        if e_y - s_y > 1 and e_x - s_x > 0:
            # 요구사항(4) : Croping동작(오려내기)
            # s_y, s_x에 각각 +1해서 선택박스(파란선)가 보이지 않도록 수정하고, 선택한 지점의 픽셀 추출
            cropImg = resultImg[s_y + 1:e_y, s_x + 1:e_x]
            # Crop 이미지 저장
            cv.imwrite('crop.jpg', cropImg)


# B 윈도우 마우스 콜백 함수
def br_mouse_callback(event, x, y, flags, param):
    global background_copy, mouse_pressed, edit_enable
    global br_s_x, br_s_y, br_e_x, br_e_y  # B 윈도우 전용 x,y 시작 끝점 변수 선언

    # 한번 편집을 하면 편집못하게 (c를 누르면 다시 편집가능)
    if edit_enable == False:
        return

    # 마우스 클릭 시
    if event == cv.EVENT_LBUTTONDOWN:
        mouse_pressed = True

        # 선택 시작 좌표 기록
        br_s_x, br_s_y = x, y

    # 마우스 클릭 후 이동하면
    elif event == cv.EVENT_MOUSEMOVE: 
        if mouse_pressed:

            # 중복되는 파란색 사각형 제거
            background_copy = np.copy(brgImg)

            # 파란색 사각형으로 선택 영역 보이기
            cv.rectangle(background_copy, (br_s_x, br_s_y),
                         (x, y), (255, 0, 0), 1)

    elif event == cv.EVENT_LBUTTONUP:
        # 저장된 Crop이미지 로드
        cropImg = cv.imread('crop.jpg')
        mouse_pressed = False

        # 선택 종료 좌표 기록
        br_e_x, br_e_y = x, y

        # 이미지 넣을 때 파란색 사각형 제거
        background_copy = np.copy(brgImg)

        # y축상의 시작점과 끝점이 바뀌었으면 두 좌표를 바꿈.
        if br_s_y > br_e_y:
            br_s_y, br_e_y = br_e_y, br_s_y
        # x축상의 시작점과 끝점이 바뀌었으면 두 좌표를 바꿈.
        if br_s_x > br_e_x:
            br_s_x, br_e_x = br_e_x, br_s_x

        if br_e_y - br_s_y > 1 and br_e_x - br_s_x > 0:
            # 검은배경 제거하고 crop영상의 객체가 덮어 씌워짐
            # 너비: e_x - s_x
            width = br_e_x - br_s_x
            # 높이: e_y - s_y
            height = br_e_y - br_s_y

            # 너비, 높이만큼 Crop이미지 사이즈변경 즉, 선택한 영역만큼 사이즈 변경
            resize_cropImg = cv.resize(cropImg, (width, height), interpolation=cv.INTER_AREA)

            # 삽입하고자 하는 배경 위치를 Crop이미지 크기만큼 컷팅
            background_cut = background_copy[br_s_y:br_e_y, br_s_x:br_e_x]

            # Crop 이미지를 GRAYSCALE로 변환
            cropGray = cv.cvtColor(resize_cropImg, cv.COLOR_BGR2GRAY)

            # 픽셀값이 10이상이면 흰색, 10미만이면 검정색으로 표시(마스크 추출)
            _, mask = cv.threshold(cropGray, 10, 255, cv.THRESH_BINARY)
            # 마스크 반전
            mask_inv = ~mask

            # 배경 이미지에서 Crop이미지 크기만큼의 영역에 Crop이미지의 모양만 0값이 부여(검정색으로)
            crop_black = cv.bitwise_and(background_cut, background_cut, mask=mask_inv)

            # Crop이미지 크기만큼의 영역의 이미지에 Crop이미지를 add
            result_cropImg = cv.add(crop_black, resize_cropImg)

            # 배경화면의 특정픽셀을 result_cropImg 이미지로 변경(선택영역 만큼)
            background_copy[br_s_y:br_e_y, br_s_x:br_e_x] = result_cropImg

            # 편집 못하게 False로 설정(c를 누르면 다시 편집가능)
            edit_enable = False


if __name__ == '__main__':
    Path = 'data/'

    # 영상 파일 변수명 ch_key
    ch_key = 'image.png'
    # ch_key = 'chro2.jpg'
    back_gr = 'background.jpg'
    Image_FullName = Path + ch_key
    Background_FullName = Path + back_gr

    s_x = s_y = e_x = e_y = -1
    br_s_x = br_s_y = br_e_x = br_e_y = -1

    colorHSV = 0

    # 이미지 로드
    originImg = cv.imread(Image_FullName)
    originImg = imutils.resize(originImg, width=500)        # 이미지 크기 고정
    image_copy = np.copy(originImg)

    brgImg = cv.imread(Background_FullName)
    background_copy = np.copy(brgImg)

    # A 윈도우 및 트랙바 설치
    cv.namedWindow('A')
    cv.createTrackbar("H", "A", 0, 50, nothing)
    cv.createTrackbar("S", "A", 0, 50, nothing)
    cv.createTrackbar("V", "A", 0, 50, nothing)

    # A 윈도우의 마우스 콜백 함수 호출
    cv.setMouseCallback('A', mouse_callback)

    # 체크 변수 선언
    mouse_pressed = False
    background_on = False
    edit_enable = True

    while True:
        # A 윈도우에 이미지 출력
        cv.imshow('A', image_copy)
        image_copy_HSV = cv.cvtColor(image_copy, cv.COLOR_BGR2HSV)

        # H,S,V값 트랙바로 조절
        # 트랙바 값(H,S,V), 1칸당 1/50값으로 50까지 올리면 최종 0 ~ 2범위로 설정(+-100% 범위)
        h = cv.getTrackbarPos("H", "A") / 50
        v = cv.getTrackbarPos("V", "A") / 50
        s = cv.getTrackbarPos("S", "A") / 50

        # 초기값 colorHSV가 int타입 이라서 colorHSV[0]의 오류 해결
        if type(colorHSV) != int:

            # 트랙바 변동에 따른 low 범위
            low_h = colorHSV[0] * (1 - h)
            if low_h < 0:
                low_h = low_h + 360
            low_s = colorHSV[1] * (1 - s)
            if low_s < 0:
                low_s = 0
            low_v = colorHSV[2] * (1 - v)
            if low_v < 0:
                low_v = 0

            lowRange = (low_h, low_s, low_v)

            # 트랙바 변동에 따른 high 범위
            high_h = colorHSV[0] * (1 + h)
            if high_h > 360:
                high_h = high_h - 360
            high_s = colorHSV[1] * (1 + s)
            if high_s > 255:
                high_s = 255
            high_v = colorHSV[2] * (1 + v)
            if high_v > 255:
                high_v = 255

            highRange = (high_h, high_s, high_v)

            # 위에서 설정한 low, high 범위안에 있으면 흰색, 나머지는 검정으로 설정(마스크 추출)
            mask = cv.inRange(image_copy_HSV, lowRange, highRange)
            # 마스크 반전(클릭한 배경화소를 하얀색-> 검은색으로 변경, 그래야 bitwise_and 로 배경만 제거 가능)
            mask_inv = ~mask

            # 마스크의 하얀색 부분(배경 제외)만 image_copy에서 보이게 설정
            resultImg = cv.bitwise_and(image_copy, image_copy, mask=mask_inv)
            cv.imshow('A', resultImg)

        k = cv.waitKey(100)

        # b 클릭 시 윈도우 B 열기
        if k == ord('b') or k == ord('B') or background_on:
            background_on = True  # 한번만 b키를 누르면 계속 if문 반복 실행되게 설정

            # B 윈도우 및 마우스 콜백함수
            cv.namedWindow('B')
            cv.setMouseCallback('B', br_mouse_callback)
            cv.imshow('B', background_copy)

        # s 클릭 시 최종 결과를 image.jpg파일로 저장 및 ESC 종료(맨 아래코드)
        # s 클릭 시 저장(B 윈도우를 띄워야만 저장가능)
        if (k == ord('s') or k == ord('S')) and background_on:
            cv.imwrite('image.jpg', background_copy)

        # c 클릭 시 편집 취소(다시 편집가능)
        elif k == ord('c') or k == ord('C'):
            background_copy = np.copy(brgImg)   # 편집 이미지 리셋
            edit_enable = True

        # ESC 클릭 시 종료
        elif k == 27:
            break





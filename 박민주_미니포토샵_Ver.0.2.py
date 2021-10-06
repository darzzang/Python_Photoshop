# 미니 포토샵 프로젝트
# 포토샵과 같은 소프트웨어를 '영상처리(Image Processing) 프로그램'이라 함
# 원칙적으로 영상처리에 대한 이론과 알고리즘을 익힌 후 미니 포토샵 프로그램을 작성하면 좋음
# 현실적으로 이론은 배제하고 화면에 구현되는 것 위주로 진행

# 주의 사항1.이미지 파일명이나 저장된 경로에 한글이 들어가면 안됨
# 주의 사항2. 이미지 크기는 가로와 세로가 동일해야 함
# 주의 사항3. 처리하는 속도가 다소 오래 걸림

# 사용할 라이브러리 또는 모듈을 임포트
# 윈도우 프로그래밍을 하기 위한 모듈
from tkinter import *
# 파일 입출력을 위한 모듈
from tkinter.filedialog import *
# 숫자나 문자를 입력 받기 위한 모듈
from tkinter.simpledialog import *
# 설치한 이미지 처리 기능을 제공하는 이미지 매직의 라이브러리 임포트
# GIF,PNG 뿐 아니라 JPG 같은 이미지를 모두 처리하기 위해 외부 라이브러리 이미지 매직 사용
from wand.image import *


# 모든 함수들이  공통적으로 사용할 전역 변수 선언부
window,canvas, paper=None, None, None
photo, photo2=None, None #photo는 처음 불러들인 원본 이미지, photo2는 처리 결과를 저장할 변수
oriX,oriY= 0,0 # 원본 이미지의 폭과 높이를 저장하는 변수


# 함수 정의 부분
# 이미지를 화면상에 출력하는 사용자 정의 함수 선언
def displayImage(img, width, height) :
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY
    # 이전 캔버스가 존재한다면 이전 캔버스를 삭제하여 기존에 이미지가 출력된 캔버스를 깨끗하게 처리
    if canvas != None :
        canvas.destroy()
    # 새 캔버스 생성, 처리된 이미지의 가로 세로 사이즈대로 생성
    canvas = Canvas(window, width=width, height=height)    # Canvas 는 클래스  # 뒤의 값은 넘겨받은 photo2의 가로세로 값
    # 새 캔버스에 붙일 종이(paper) 생성, 처리된 이미지의 가로 세로 사이즈대로 생성
    # 실질적으로 뿌려짐
    paper=PhotoImage(width=width, height=height)
    # 새 캔버스에 종이(paper)를 붙임 ( 차후 그 종이 위에 처리된 이미지를 출력)
    # 생성될 위치는 가로 세로의 사이즈의 중간 위치
    canvas.create_image( (width/2, height/2), image=paper, state="normal")

    # 기존 이미지의 값을 불러오는 부분 
    blob = img.make_blob(format='RGB')   #이미지를 바이너리 코드로 변환해주는 함수, 배열의 형태로 저장
    # 뿌려주는 부분
    for i in range(0,width) :
        for k in range(0, height) :
            r = blob[(i*3*width)+(k*3) + 0]   # blob[0],blob[3],blob[6],blob[9]...의 값을 r에 저장
            g = blob[(i*3*width)+(k*3) + 1]  # blob[1],blob[4],blob[7],blob[10], 의 값을 g에 저장
            b = blob[(i*3*width)+(k*3) + 2]  # blob[2],blob[5],blob[8],blob[11]의 값을 g에 저장
            # paper에 칼라로 점을 찍어줌, 세로로 높이만큼 찍고 가로를 너비만큼 반복
            paper.put("#%02x%02x%02x" % (r,g,b) , (k,i)) # r,g,b값 을 (02x)에 의해 각각 두자리 16진수로 변환하여 rgb 값으로 결합한 후 (k,i)에 찍어줌
            #print(r,g,b)  # r,g,b값 출력 테스트
            #print("#%02x%02x%02x, (%d, %d)" % (r,g,b, k,i)) # r,g,b값 을 16진수로 변환 결과 출력 테스트
    # 처리된 결과 이미지의 픽셀을 찍어둔 종이paper가 붙여있는 캔버스를 화면에 출력
    #canvas.pack()
    canvas.place(x=(670-width)/2, y=(520-height)/2)
    

# 파일 열기
def func_open():
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY   # newX, newY 는 바뀐 이미지를 저장하는 지역변수
    # askopenfilename() 함수로 파일 열기 대화상자를 나타내어 그림 파일 선택
    readFp = askopenfilename(parent=window, filetypes=(("모든 그림 파일", "*.jpg;*.jpeg;*.bmp;*.png;*.tif;*.gif"),  ("모든 파일", "*.*") ))

    # 이미지는 GIF, JPG, PNG를 불러와 모두 처리하기 위해 PhotoImage() 가 아닌 Wand 라이브러리에서 제공하는 Image()를 사용
    # 이미지를 준비하는 단계
    # photo는 처음 불러들인 원본 이미지
    photo = Image(filename=readFp)
    oriX = photo.width  # 원본 이미지의 가로 사이즈를 oriX에 저장
    oriY = photo.height # 원본 이미지의 세로 사이즈를 oriX에 저장

    # 화면에 파일 이름 출력하기
    photo_Label=Label(window, text=readFp, fg="white",bg='#4f4f4f')
    photo_Label.place(x=47, y=20)

    #photo2는 처리 결과를 저장할 변수
    photo2 = photo.clone()  # 원본 이미지인 photo를 복제하여 photo2 덮어쓰기
    newX = photo2.width
    newY = photo2.height
    
    # 복제된 photo2를 캔버스의 페이퍼에 디스플레이하는 사용자 정의 함수 실행
    displayImage(photo2, newX, newY)


# 파일 저장
def func_save():
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언

    # photo2는 func_open() 함수를 실행하면 생성됨
    # 파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None :
        return
    # 대화 상자로부터 넘겨받은 파일의 정보를 saveFp에 저장
    saveFp = asksaveasfile(parent=window, mode="w", defaultextension=".jpg", filetypes=(("JPG 파일", "*.jpg;*.jpeg"), ("모든 파일", "*.*") )) 
    savePhoto = photo2.convert("jpg")   # 결과 이미지인 photo2의 파일 형식을  jpg로 변환
    savePhoto.save(filename=saveFp.name)    # 파일 저장 대화창에서 입력받은 파일 이름으로 저장

def func_exit():
    window.quit()   # 윈도우창 닫기
    window.destroy()    # 윈도우창 파괴


# "View"  > 확대 및 축소
# Wand 라이브러리에서 제공하는 resize(가로,세로)함수를 사용
def func_zoomin() :
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
    # 파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None :
        return
    # askinteger() 함수를 실행해 대화 상자로 확대할 배수 입력받음
    scale = askinteger("확대배수", "확대할 배수를 입력하세요(2~4)",minvalue=2, maxvalue=4)
    photo2.resize( int(newX * scale), int(newY * scale))  # 원본 이미지의 가로 세로 사이즈에 배수를 곱하여 크기 변경
    newX = photo2.width # 변경된 이미지의 가로 사이즈 newX에 저장
    newY = photo2.height  # 변경된 이미지의 세로 사이즈 newY에 저장
    # 처리된 이미지의 이미지, 가로,세로 정보를 displayImage() 함수에 넘겨줌
    displayImage(photo2, newX, newY)
    
def func_zoomout() :
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
    # 파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None :
        return
    # askinteger() 함수를 실행해 대화 상자로 축소할 배수 입력받음
    scale = askinteger("축소배수", "축소할 배수를 입력하세요(2~4)",minvalue=2, maxvalue=4)
    photo2.resize( int(newX / scale), int(newY / scale))  # 원본 이미지의 가로 세로 사이즈에 배수를 곱하여 크기 변경
    photo2.convert(channelr(threshold="50%"))
    newX = photo2.width # 변경된 이미지의 가로 사이즈 newX에 저장
    newY = photo2.height  # 변경된 이미지의 세로 사이즈 newY에 저장
    # 처리된 이미지의 이미지, 가로,세로 정보를 displayImage() 함수에 넘겨줌
    displayImage(photo2, newX, newY)

# 상하 반전, flip() 함수 사용
def func_mirror1() :
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
    # 파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None :
        return
    photo2.flip()
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

# 좌우 반전, flop() 함수 사용
def func_mirror2() :
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
    # 파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None :
        return
    photo2.flop()
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)


# "View" > 회전
# Wand 라이브러리에서 제공하는 rotate(각도)함수를 사용
def func_rotate() :
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
    # 파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None :
        return
    degree = askinteger("회전", "회전할 각도를 입력하세요(0~360)", minvalue=0, maxvalue=360) 
    photo2.rotate(degree)   # 회전할 각도를 받음
    newX = photo2.width 
    newY = photo2.height
    displayImage(photo2, newX, newY)


# "Image" > 밝게 / 어둡게
# Wand 라이브러리에서 제공하는 modulate(명도값, 채도값, 색상값)함수를 사용
# 명도는 modulate(명도값, 100,100)함수를 사용
# 원본의 명도값이 100이므로 100 이상은 '밝게', 100 이하는 '어둡게' 처리
# 밝게, modulate(밝기값, 100,100)함수에 100~200 값 입력
def func_bright() :
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
    # 파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None :
        return
    value = askinteger("밝게", "값을 입력하세요(100~200)", minvalue=100, maxvalue=200)
    photo2.modulate(value, 100, 100)
    newX = photo2.width 
    newY = photo2.height
    displayImage(photo2, newX, newY)   

# 어둡게, modulate(밝기값, 100,100)함수에 0~100 값 입력
def func_dark() :
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
    # 파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None :
        return
    value = askinteger("어둡게", "값을 입력하세요(0~100)", minvalue=0, maxvalue=100)
    photo2.modulate(value, 100, 100)
    newX = photo2.width 
    newY = photo2.height
    displayImage(photo2, newX, newY)

# "Image" > 선명하게/탁하게
# Wand 라이브러리에서 제공하는 modulate(100,채도값,100)함수를 사용
# 원본의 채도값이 100이므로 100 이상은 '선명하게', 100 이하는 '탁하게' 처리    

# 선명하게, modulate(100,채도값,100)함수에 100~200 값 입력
def func_clear() :
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
    # 파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None :
        return
    value = askinteger("선명하게", "값을 입력하세요(100~200)", minvalue=100, maxvalue=200)
    photo2.modulate(100, value, 100)
    newX = photo2.width 
    newY = photo2.height
    displayImage(photo2, newX, newY)
    
def func_unclear() :
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
    # 파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None :
        return
    value = askinteger("탁하게", "값을 입력하세요(0~100)", minvalue=0, maxvalue=100)
    photo2.modulate(100, value, 100)
    newX = photo2.width 
    newY = photo2.height
    displayImage(photo2, newX, newY)

# "Image" > 흑백이미지
# 이미지의 type 값을 "grayscale"로 설정   
def func_bw() :
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
    # 파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None :
        return
    photo2.type="grayscale"
    newX = photo2.width 
    newY = photo2.height
    displayImage(photo2, newX, newY)

# "Image" > 가장자리 만들기
# 그림의 가장자리의 선만 따서 그려짐
def func_edge():
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
    # 파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None :
        return
    photo2.edge(radius = 1)
    newX = photo2.width 
    newY = photo2.height
    displayImage(photo2, newX, newY)

# "Image" > 스케치 효과
def func_sketch():
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
    # 파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None :
        return
    photo2.sketch(0.5, 0.0, 98.0)
    newX = photo2.width 
    newY = photo2.height
    displayImage(photo2, newX, newY)

# "Edit" > 삽화처럼 둥글게 자르기
def func_vignette():
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
    # 파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None :
        return
    photo2.vignette(10,10)
    newX = photo2.width 
    newY = photo2.height
    displayImage(photo2, newX, newY)



# 되돌리기 
def func_revert() :
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
    # 파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None :
        return
    photo2 = photo.clone()  # 원본 이미지인 photo를 복제하여 photo2 덮어쓰기
    newX = photo2.width 
    newY = photo2.height
    displayImage(photo2, newX, newY)    


# 메인 코드부
window = Tk()
window.geometry("800x534")
window.title("미니 포토샵(Ver 0.1)")
window.configure(bg="darkgrey")

# 배경 이미지 출력
'''
# 빈 이미지 출력
photo = PhotoImage()
'''
bg_photo = PhotoImage(file="ptsbg.png")
pLabel = Label(window,image=bg_photo)
#pLabel.pack(expand=1,anchor=CENTER)
pLabel.place(x=-2, y=-2)


# 메뉴 생성

# 1. 메뉴 자체 생성
# 메뉴 자체 = Menu(부모 윈도우)
# 부모 윈도우.config(menu=메뉴자체) : 윈도우창에 메뉴 등록
mainMenu = Menu(window, fg="white",bg='#4f4f4f')
window.config(menu=mainMenu)

# 2. 상위 메뉴 생성
# 상위 메뉴 = Menu(메뉴자체)
# 메뉴자체.add_cascade(label="상위 메뉴 텍스트", menu=상위메뉴)
# add_cascade() 메소드는 상위 메뉴와 하위 메뉴 연결
fileMenu = Menu(mainMenu, tearoff=0, fg="white",bg='#4f4f4f')    # tearoff=0 => 구분선 없앰 
mainMenu.add_cascade(label="File",menu=fileMenu)

# 3. 하위 메뉴 생성
# 상위메뉴.add_command(label="하위 메뉴1", command=함수1)
# add_command() 메소드는 기본 메뉴 항목 생성
fileMenu.add_command(label="Open", command=func_open)
fileMenu.add_command(label="Save", command=func_save)
fileMenu.add_separator()    # 구분선 삽입
fileMenu.add_command(label="Revert", command=func_revert)
fileMenu.add_separator() # 구분선 삽입
fileMenu.add_command(label="Exit", command=func_exit)

# 2. 두번째 상위 메뉴(이미지 처리1) 생성
viewMenu = Menu(mainMenu, tearoff=0, fg="white",bg='#4f4f4f')
mainMenu.add_cascade(label="View",menu=viewMenu)

# 3. 두번째 하위 메뉴 생성
viewMenu.add_command(label="Zoom in", command=func_zoomin)
viewMenu.add_command(label="Zoom out", command=func_zoomout)
viewMenu.add_separator() # 구분선 삽입
viewMenu.add_command(label="Flip", command=func_mirror1)
viewMenu.add_command(label="Flop", command=func_mirror2)
viewMenu.add_command(label="Rotate", command=func_rotate)

# 2. 상위 메뉴 추가, 세번째 상위 메뉴 생성
imageMenu = Menu(mainMenu, tearoff=0, fg="white",bg='#4f4f4f')
mainMenu.add_cascade(label="Image",menu=imageMenu)

# 3. 세번째 하위 메뉴 생성
imageMenu.add_command(label="Bright up", command=func_bright)
imageMenu.add_command(label="Bright down", command=func_dark)
imageMenu.add_separator()
imageMenu.add_command(label="Clear", command=func_clear)
imageMenu.add_command(label="Unclear", command=func_unclear)
imageMenu.add_separator()
imageMenu.add_command(label="Edge", command=func_edge)
imageMenu.add_command(label="Sketch", command=func_sketch)
imageMenu.add_separator()
imageMenu.add_command(label="Black & White", command=func_bw)


# 2. 네번째 상위 메뉴 생성
editMenu = Menu(mainMenu, tearoff=0, fg="white",bg='#4f4f4f')
mainMenu.add_cascade(label="Edit",menu=editMenu)

# 3. 네번째 하위 메뉴 생성
editMenu.add_command(label="Vignette", command=func_vignette)


window.mainloop()


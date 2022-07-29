# ▶ 1. ZipFile 환경 설정
import os
import io
import zipfile
from zipfile import ZipFile
import pandas as pd
import requests
import tensorflow as tf

#
# ## 현재 폴더 내 압축폴더 유무 확인
# # zipfiles = [file for file in os.listdir() if file.endswith('zip')]
# # print(zipfiles) #['TL3.zip', 'TL4.zip']
#
#
# # ▶ 1.1 한글 파일명을 포함한 ZIP 파일 압축 해제
# #  모듈을 통해 압축을 해제하는 순서는 다음과 같다.
# # 1.ZipFile 클래스에 압축을 해제할 파일과 읽기 전용 모드를 제공해 ZipFile 객체를 with 문을 사용해 생성한다.
# # 2.ZipFile 객체의 infolist 메서드를 사용해 ZIP 파일에 압축되어 있는 파일 목록(디렉터리도 파일로 취급)을 가져온다(변수명 예, zipInfo)
# # 3.for 문을 사용해 zipInfo 변수를 순회한다.
# # 4.zipInfo 변수안에 있는 개별의 객체는 ZIpInfo 객체로 이 안에서 filename 속성의 값을 euc-kr로 해석한후 utf-8로 다시 인코딩한 값으로 덮어쓴다.5.
# # 5.ZipFile 객체의 extract 메서드에 ZipInfo 객체(for 문 안에선 member 변수)를 인자로 제공한다.
#

file_path = 'D:\work\python\Final_project_Speech_synthesis.git'

with zipfile.ZipFile("C:/Users/ASIA-19/Desktop/언정.zip", "r") as zf: # "r" , zip 파일 수정
    zipInfo = zf.infolist()
    for member in zipInfo:
        member.filename = member.filename.encode('cp437').decode("euc-kr", 'ignore')
        zf.extract(member, file_path)


# ▶ 2. 폴더 안의 모든 하위 파일 복사 하나의 폴더로 합치기
import os
import shutil
import time

#폴더 안에 있는 모든 하위 파일(서브폴더의 파일 포함)을 읽어 리스트로 반환.
#반복문과 재귀 함수를 이용해서 하위 폴더의 파일까지 모두 접근
def read_all_file(path):
    output = os.listdir(path)
    file_list = []

    for i in output:
        if os.path.isdir(path+"/"+i):
            file_list.extend(read_all_file(path+"/"+i))
        elif os.path.isfile(path+"/"+i):
            file_list.append(path+"/"+i)

    return file_list

#폴더 내의 모든 하위 파일들을 새로운 경로로 복사

def copy_all_file(file_list, new_path):
    for src_path in file_list:
        file = src_path.split("/")[-1]
        shutil.copyfile(src_path, new_path+"/"+file)
        print("파일 {} 작업 완료".format(file)) # 작업한 파일명 출력

# 폴더 안의 모든 하위 파일들(서브 폴더의 파일 포함)을 복사해서 또다른 하나의 폴더로 합친다.
# src_path에는 기존 폴더의 경로를 적어주고, new_path에는 파일들을 옮길 새로운 폴더 경로를 적어준다.

start_time = time.time() # 작업 시작 시간

src_path = 'D:\work\python\Final_project_Speech_synthesis.git\언정' # 기존 폴더 경로
new_path = "D:\work\python\Final_project_Speech_synthesis.git\lej" # 옮길 폴더 경로, 미리 "./lej/wav" 폴더 만들어두기

file_list = read_all_file(src_path)
copy_all_file(file_list, new_path)

print("=" * 40)
print("러닝 타임 : {}".format(time.time() - start_time)) # 총 소요시간 계산


# ▶ 2.1 특정 폴더(디렉토리) 파일 리스트 가져오기
import os
import shutil
file_list = os.listdir('./lej/')
file_list_wav = [file for file in file_list if file.endswith(".wav")]
for path in file_list_wav:
    shutil.move("./lej/"+path, "./lej/wav")
    print('copied ', path)

if os.path.exists("./lej/wav/0033_G2A3E2S0C3_KMA_000001.wav"):
    print("exists")

# ▶ 3 json 처리
# 3-1. 경로 지정
import json

path = './lej/'
file_list = os.listdir(path)


# 2-2.  json파일만 리스트에 넣기
file_list_py = [file for file in file_list if file.endswith('.json')]


# 2-3. 데이터프레임으로 변환
dict_list = []
for i in file_list_py:
    for line in open((path+i),"r", encoding='utf-8'):
      try:
        dict_list.append(json.loads(line))
      except:
        pass
df = pd.DataFrame(dict_list)


# 2-4. 파일정보, 전사정보만 추출
# df1 = df[['파일정보', '전사정보']]
df1 = df[['파일정보', '전사정보']]
# print(df1)
# exit()

files = []
for i in range(len(df1['파일정보'])):
  file = list(df['파일정보'][i].values())[1]
  files.append(file)


texts = []
for i in range(len(df1['전사정보'])):
  text = list(df['전사정보'][i].values())[1]
  texts.append(text)


df2 = pd.DataFrame({'file':files, 'text':texts})
print(df2)
# exit()

# 2-5. 저장
df2.to_csv('./lej/{}.csv'.format(path.split('/')[-2]))

# 4. txt파일로 만들기
df = pd.read_csv('./lej/lej.csv')
# print(len(df))
# exit()


# 4-1. 리스트로 만들기
script_list = df['text'].values.tolist()
# print(script_list)
# exit()


# 4-2. text 속 특수문자 제거
import string

script_only = []
for i in script_list:
  input_string = i
  output_string = input_string.translate(str.maketrans('', '', string.punctuation))
  script_only.append(output_string)
# print(script_only)


# 4-3. text컬럼 값 수정
df['text'] = pd.DataFrame(script_only)


# 4-4. length 컬럼 추가
length = []
df1 = df['text']
for i in df1:
  length.append(len(i)+1)

df['len'] = pd.DataFrame(length)


# 4-5. 타입 변환
df['len'] = df['len'].astype('str')
df['file'] = df['file'].astype('str')


# 4-6. 텍스트 파일 쓰기  mimic-recording-studio 설치 된 곳에 저장
f = open('C:/Users/ASIA-19/Desktop/mimic-recording-studio/audio_files/lej-metadata.txt', 'w', encoding='utf-8')
for i in range(len(df)):
  f.write(df['file'][i] + '|' + df['text'][i] + '.' + '|' + df['len'][i] +'\n')
f.close()


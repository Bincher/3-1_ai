import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Flatten
import time

class MyCallback(tf.keras.callbacks.Callback):
    def __init__(self):
        super().__init__()
        self.start_time = time.time()

    def on_epoch_end(self, epoch, logs=None):
        if time.time() - self.start_time > 300:
            self.model.stop_training = True

mnist = tf.keras.datasets.mnist
(x_train, y_train_origin), (x_test, y_test_origin) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0           # 이미지 데이터를 0과 1 사이의 값으로 정규화

nb_classes = 10
y_train = keras.utils.to_categorical(y_train_origin, num_classes=nb_classes)       # 레이블 데이터를 one-hot 인코딩
y_test = keras.utils.to_categorical(y_test_origin, num_classes=nb_classes)       # 레이블 데이터를 one-hot 인코딩

model = keras.Sequential()             # 순차 모델 생성
model.add(Flatten(input_shape=(28, 28)))       # 28x28 이미지를 1차원으로 평탄화
model.add(Dense(128, activation='relu'))     # 128개의 뉴런을 가진 은닉층 추가, 활성화 함수는 relu
model.add(Dense(10, activation='softmax'))     # 10개의 뉴런을 가진 출력층 추가, 활성화 함수는 소프트맥스

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.01), loss='mse', metrics=['categorical_accuracy'])
# model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.01), loss='categorical_crossentropy', metrics=['categorical_accuracy'])
# 모델의 컴파일 설정. 옵티마이저로 SGD 사용, 학습률은 0.01. 손실 함수는 평균 제곱 오차, 평가 지표로 정확도를 사용

hist = model.fit(x_train, y_train, epochs=300, batch_size=100, validation_data=(x_test, y_test), callbacks=[MyCallback()])
# 모델을 훈련 데이터로 학습시킴. 에포크 수는 300, 배치 크기는 100. 검증 데이터를 사용하여 모델의 성능을 평가. MyCallback 클래스를 콜백으로 사용하여 학습 시간 제한 설정

model.evaluate(x_test, y_test)       # 모델을 테스트 데이터로 평가

y_new = model.predict(x_test)       # 모델을 사용하여 테스트 데이터에 대한 예측 수행
print(y_new)       # 예측 결과 출력
y_label = tf.argmax(y_new, axis=1)     # 예측된 결과에서 가장 높은 확률을 가진 클래스의 인덱스 추출
print(y_label.numpy())       # 추출된 인덱스 출력

# 검증
total_count = len(y_label)       # 전체 개수 계산
correct_count = 0       # 맞춘 개수 초기화
for i in range(len(y_label)):
    if y_label[i] == y_test_origin[i]:     # 예측한 클래스와 실제 클래스 비교
        correct_count += 1       # 일치하는 경우 정답 개수 증가
print("총 개수:", total_count, "맞춘 개수:", correct_count, "정확도:", correct_count / total_count)
# 전체 개수, 맞춘 개수, 정확도 출력

print(hist.history["val_categorical_accuracy"])       # 검증 데이터에 대한 정확도 기록 출력
print(">>> 최대값:", max(hist.history["val_categorical_accuracy"]))       # 검증 데이터의 정확도 중 최대값 출력

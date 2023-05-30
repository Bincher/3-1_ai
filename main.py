import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
import time

class MyCallback(tf.keras.callbacks.Callback):
    def __init__(self):
        super().__init__()
        self.start_time = time.time()

    def on_epoch_end(self, epoch, logs=None):
        if time.time() - self.start_time > 300:
            self.model.stop_training = True

mnist = tf.keras.datasets.mnist
# MNIST 데이터셋 로드
(x_train, y_train_origin), (x_test, y_test_origin) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0  # 0과 1 사이의 값으로 변환
x_train = x_train.reshape((-1, 28, 28, 1))
x_test = x_test.reshape((-1, 28, 28, 1))

nb_classes = 10
y_train = keras.utils.to_categorical(y_train_origin, num_classes=nb_classes)  # one-hot encoding
y_test = keras.utils.to_categorical(y_test_origin, num_classes=nb_classes)    # one-hot encoding

print(x_train.shape)  # 훈련 데이터의 입력 형상 출력
print(y_train.shape)  # 훈련 데이터의 출력 형상 출력
print(y_test_origin)  # 테스트 데이터의 실제 출력 값 출력
print(y_test)  # 테스트 데이터의 one-hot 인코딩된 출력 값 출력

model = keras.Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
# 32개의 필터를 가진 3x3 컨볼루션 레이어 추가, 활성화 함수는 ReLU
model.add(MaxPooling2D(pool_size=(2, 2)))
# 2x2 크기의 맥스 풀링 레이어 추가
model.add(Conv2D(32, (3, 3), activation='relu'))
# 32개의 필터를 가진 3x3 컨볼루션 레이어 추가, 활성화 함수는 ReLU
model.add(MaxPooling2D(pool_size=(2, 2)))
# 2x2 크기의 맥스 풀링 레이어 추가
model.add(Flatten())
# 다차원 입력을 1차원으로 평탄화
model.add(Dense(128, activation='sigmoid'))
# 128개의 뉴런을 가진 은닉층 추가, 활성화 함수는 ReLU
model.add(Dense(10, activation='softmax'))
# 10개의 뉴런을 가진 출력층 추가, 활성화 함수는 소프트맥스

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.1), loss='mse', metrics=['categorical_accuracy'])
# 모델의 컴파일 설정. 옵티마이저로 SGD 사용, 학습률은 0.1. 손실 함수는 평균 제곱 오차, 평가 지표로 정확도를 사용

callback = MyCallback()  # 시간 제한 콜백 객체 생성
model.fit(x_train, y_train, epochs=30, batch_size=100, validation_data=(x_test, y_test), callbacks=[callback])
# 모델을 훈련 데이터로 학습시킴. 에포크 수는 30, 배치 크기는 100. 검증 데이터를 사용하여 모델의 성능을 평가. 시간 제한 콜백 사용

model.evaluate(x_test, y_test)  # 모델을 테스트 데이터로 평가

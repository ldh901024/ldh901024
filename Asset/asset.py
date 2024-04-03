# 필요한 라이브러리 임포트
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

# 데이터 수집 및 전처리 (여기서는 예제 데이터를 사용합니다)
# 실제로는 키움증권 API를 통해 얻은 데이터를 사용해야 합니다.
data = pd.read_csv('example_stock_data.csv')
X = data.drop('Target', axis=1)  # 특성 데이터
y = data['Target']  # 타겟 데이터

# 데이터를 학습용과 테스트용으로 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 여러 개의 기본 모델 정의
model_rf = RandomForestClassifier(n_estimators=100, random_state=42)
model_gb = GradientBoostingClassifier(n_estimators=100, random_state=42)

# 앙상블 모델 (투표 기반)
ensemble_model = VotingClassifier(estimators=[('rf', model_rf), ('gb', model_gb)], voting='hard')

# 모델 학습
ensemble_model.fit(X_train, y_train)

# 모델 성능 평가
y_pred = ensemble_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')
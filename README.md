# Dia4AutoKey

Diablo IV 전용 매크로 프로그램입니다. PyQt5 GUI와 `pyautogui`, `pynput`을 사용하여 키보드와 마우스 동작을 자동화합니다.

## 설치
```bash
pip install -r requirements.txt
```

## 실행
```bash
python main.py
```

## 개발
- `models.py` : pydantic 데이터 모델 정의
- `macro_engine.py` : 매크로 실행 로직
- `controller.py` : GUI와 엔진 연결
- `ui_main.py` : Qt Designer 기반 UI 코드
- `tests/` : pytest 단위 테스트

## 테스트
```bash
pytest
```

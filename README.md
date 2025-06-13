# Dia4AutoKey

Diablo IV 전용 매크로 프로그램입니다. PyQt5 GUI와 `pyautogui`, `pynput`을 사용하여 키보드와 마우스 동작을 자동화합니다.

## 설치
```bash
pip install -r requirements.txt
```

### Windows 설치
Windows에서도 동일한 명령으로 설치할 수 있습니다. 다만 Linux 전용 패키지는 자동으로 제외되므로 별도 설정 없이 사용 가능합니다.

### EXE 생성
PyInstaller가 설치되어 있다면 다음 명령으로 실행 파일을 만들 수 있습니다.
```bash
pyinstaller --noconsole --onefile main.py --name Dia4AutoKey
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

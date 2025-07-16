import sys
from pathlib import Path
 
# 상위 디렉토리를 Python path에 추가 (한 번만 실행)
root_dir = Path(__file__).parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir)) 
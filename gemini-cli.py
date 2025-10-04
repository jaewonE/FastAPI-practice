import subprocess
import shutil
from pathlib import Path

# 설정
PROMPT_FILE = Path("summarized_prompt.txt")
PAPERS_DIR = Path("papers")
RESULTS_DIR = Path("results")
MODEL_NAME = "gemini-2.5-flash"
PROJECT_TMP_DIR = Path(".gemini/tmp")


def main():
    # 사전 점검
    if shutil.which("gemini") is None:
        raise RuntimeError(
            "gemini CLI를 찾을 수 없습니다. `npm i -g @google/gemini-cli` 등으로 설치 후 PATH를 확인하세요.")
    if not PROMPT_FILE.exists():
        raise FileNotFoundError(f"프롬프트 파일이 없습니다: {PROMPT_FILE}")
    if not PAPERS_DIR.exists():
        raise FileNotFoundError(f"논문 폴더가 없습니다: {PAPERS_DIR}")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    PROJECT_TMP_DIR.mkdir(parents=True, exist_ok=True)

    # papers 폴더의 .md 파일을 이름순으로 순차 처리
    paper_files = sorted(PAPERS_DIR.glob("**/*.md"))
    if not paper_files:
        print("papers 폴더에 .md 파일이 없습니다.")
        return

    for paper in paper_files:
        # 결과 파일 경로
        out_path = RESULTS_DIR / f"{paper.stem}.summary.md"

        # 프롬프트 구성:
        # 1) summarized_prompt.txt 내용을 먼저 읽음
        # 2) 이어서 해당 논문(md)의 내용을 붙여 임시 프롬프트 파일을 생성
        prompt_text = PROMPT_FILE.read_text(encoding="utf-8")
        paper_text = paper.read_text(encoding="utf-8")
        combined_text = f"{prompt_text}\n{paper_text}"

        # 대용량/특수문자 경로 문제를 피하기 위해 프로젝트 내부 임시 파일을 사용
        tmp_path = PROJECT_TMP_DIR / f"{paper.stem}.prompt.txt"
        try:
            tmp_path.write_text(combined_text, encoding="utf-8")

            # gemini CLI 호출
            cmd = [
                "gemini",
                "-m", MODEL_NAME,
                "-p", f"@{{{tmp_path.resolve().as_posix()}}}",
            ]

            print(f"[RUN] {paper} → {out_path.name}")
            proc = subprocess.run(cmd, capture_output=True, text=True)

            if proc.returncode != 0:
                # 실패 시 stderr를 결과 파일에 남겨 추후 디버깅
                err_txt = (
                    f"[ERROR] gemini CLI failed for {paper.name}\n\n"
                    f"STDERR:\n{proc.stderr}"
                )
                out_path.write_text(err_txt, encoding="utf-8")
                print(f"  ↳ 실패(로그 저장): {out_path}")
                continue

            # 성공: stdout을 결과 파일로 저장
            output_text = proc.stdout.strip()
            print(output_text)
            out_path.write_text(output_text, encoding="utf-8")
            print(f"  ↳ 완료: {out_path}")
        finally:
            try:
                tmp_path.unlink(missing_ok=True)
            except Exception:
                pass


if __name__ == "__main__":
    main()

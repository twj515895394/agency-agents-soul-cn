import os
import re

CN_REPO_DIR = "/Users/tangwujun/Documents/trae_projects/agency-agents-soul-cn"

def scan_files(directory):
    soul_files = []
    for root, dirs, files in os.walk(directory):
        if ".git" in root or ".scratch" in root or ".handoff" in root:
            continue
        for file in files:
            if file.endswith("-soul.md") or file == "soul.md":
                soul_files.append(os.path.join(root, file))
    return soul_files

def main():
    files = scan_files(CN_REPO_DIR)
    print(f"Total soul files in CN repo: {len(files)}")
    
    headers = []
    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Find first H1 header
        h1_match = re.search(r"^#\s*(.*?)$", content, re.MULTILINE)
        if h1_match:
            headers.append((os.path.relpath(fpath, CN_REPO_DIR), h1_match.group(1).strip()))
        else:
            headers.append((os.path.relpath(fpath, CN_REPO_DIR), "NO H1 HEADER"))
            
    # Print the first 30 and group by pattern
    has_caps_soul = 0
    has_title_soul = 0
    other = 0
    for rel_path, h1 in sorted(headers):
        if "(SOUL)" in h1:
            has_caps_soul += 1
        elif "Soul" in h1:
            has_title_soul += 1
        else:
            other += 1
            
    print(f"\nPattern statistics:")
    print(f"Contains (SOUL): {has_caps_soul}")
    print(f"Contains 'Soul': {has_title_soul}")
    print(f"Other patterns: {other}")
    
    print("\nSample headers:")
    for rel_path, h1 in sorted(headers)[:40]:
        print(f"  {rel_path} ===> {h1}")

if __name__ == "__main__":
    main()

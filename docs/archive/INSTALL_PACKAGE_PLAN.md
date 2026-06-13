# NSIS 安装包方案

> 目标: 个人数字资产管家_Setup.exe | 无需用户安装Python

## 方案A: NSIS + 嵌入式Python (推荐)

| 指标 | 值 |
|------|-----|
| 包大小 | ~45MB |
| 开发时间 | 2-3天 |

### NSIS 脚本

```nsis
OutFile "个人数字资产管家_Setup.exe"
InstallDir "$PROGRAMFILES\个人数字资产管家"
Section "Install"
  SetOutPath $INSTDIR
  File /r "build\*"
  CreateShortcut "$DESKTOP\个人数字资产管家.lnk" "$INSTDIR\python\python.exe" "dashboard.py"
SectionEnd
```

## 方案B: PyInstaller

| 指标 | 值 |
|------|-----|
| 包大小 | ~55MB |
| 开发时间 | 1-2天 |
| 注意 | 需额外配置streamlit |

## 推荐

**短期**: 便携版(已完成) -> **中期**: NSIS安装包 -> **长期**: PyInstaller单文件+自动更新

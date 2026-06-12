# Git Network Fix Report

> 日期: 2026-06-12 | Issue: git push to GitHub failed

## 根因

**GFW 深度包检测（DPI）阻断 git/libcurl 的 TLS SNI 握手**

### 证据链

| 测试 | 结果 | 说明 |
|------|------|------|
| `Test-NetConnection github.com:443` | ✅ / ⚠️ 间歇 | TCP 层有时可达 |
| `curl.exe https://github.com` | ❌ 000 | libcurl 的 TLS SNI 被阻断 |
| `Python urllib https://github.com` | ✅ OK | Python 的 ssl 库正常 |
| `npm ping` | ✅ OK | npm 的 TLS 实现不同 |
| `git ls-remote origin` | ❌ 卡死 | git 使用 libcurl |
| `git push` | ❌ 卡死 | 同上 |

结论：git 使用的 libcurl 库在 TLS SNI 阶段被 GFW 阻断，而 Python/npm 使用不同的 SSL 实现，未被拦截。

## 修复内容

### 1. 配置 git 全局代理

```bash
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
```

代理服务 `127.0.0.1:7890` 为本机已运行的代理（如 Clash/V2Ray）。

### 2. 移除 node_modules 以缩小 push 体积

```bash
git rm -r --cached node_modules
git commit -m "Remove node_modules from git tracking"
```

`node_modules` 已通过 `.gitignore` 排除。

### 3. 修复 Remote URL

```bash
git remote set-url origin https://github.com/graceliu710605/GraceOS.git
# 原 URL: GraceOS-.git (多了 '-')
```

## 验证结果

| 测试 | 结果 |
|------|------|
| `git ls-remote origin` | ✅ 成功 |
| `git push -u origin main` | ✅ `* [new branch] main -> main` |

## 注意事项

- 代理必须保持运行才能持续 push/pull
- 如果代理不可用，git push 会再次失败
- Python HTTPS 可直达 GitHub，但 git 本身的 libcurl 无法绕过 GFW

# SDK开启调试模式

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100091](https://developer.work.weixin.qq.com/document/path/100091)
- **文档 ID**: `100091`
- **API 名称**: `spec_open_debug_mode`
- **请求方法**: `N/A`
- **接口地址**: `N/A`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

SDK开启调试模式

## 其他说明

### Python

```
from wwspecapisdk import spec_open_debug_mode

spec_open_debug_mode(debug_token, access_token)
```

### C++

```
#include "cpp_sdk.h"

bool is_succ = Tencent::WxWork::SpecOpenDebugMode(debug_token, access_token);
```

### Java

```
import com.tencent.wework.SpecUtil;

boolean isSuccess = SpecUtil.OpenDebugMode(debugToken, accessToken);
```

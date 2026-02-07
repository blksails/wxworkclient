# SDK开启调试模式

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100083](https://developer.work.weixin.qq.com/document/path/100083)
- **文档 ID**: `100083`
- **API 名称**: `spec_open_debug_mode`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

依赖的参数：
- access_token：应用的access_token，注意必须确保在有效时间内，一般是2小时
- debug_token：程序的调试凭证

## 请求信息

### 请求示例

#### 示例 1: Python

```text
from wwspecapisdk import spec_open_debug_mode

spec_open_debug_mode(debug_token, access_token)
```

#### 示例 2: C++

```text
#include "cpp_sdk.h"

bool is_succ = Tencent::WxWork::SpecOpenDebugMode(debug_token, access_token);
```

#### 示例 3: Java

```text
import com.tencent.wework.SpecUtil;

boolean isSuccess = SpecUtil.OpenDebugMode(debugToken, accessToken);
```

# AccessToken 自动处理

## 概述

代码生成器现在会自动从请求结构体中提取 `AccessToken` 相关字段，并将其添加到 URL 的 query 参数中。

## 支持的字段

以下字段名称会被自动识别并提取：

- `AccessToken`
- `ProviderAccessToken`
- `SuiteAccessToken`
- `CorpAccessToken`

## 工作原理

生成的客户端方法会使用反射（reflection）来检查请求结构体中是否包含上述字段。如果找到这些字段且值不为空，会自动将其添加到 HTTP 请求的 query 参数中。

### 示例

#### Request 定义

```go
type GetAccountBalanceRequest struct {
    ProviderAccessToken string `json:"provider_access_token"` // 应用服务商的接口调用凭证
}
```

#### 生成的方法

```go
func (c *client) GetAccountBalance(req *GetAccountBalanceRequest) (*GetAccountBalanceResponse, error) {
    query := url.Values{}
    
    // 自动从 req 中提取 AccessToken 相关字段添加到 query
    if req != nil {
        v := reflect.ValueOf(req).Elem()
        t := v.Type()
        for i := 0; i < v.NumField(); i++ {
            field := t.Field(i)
            fieldName := field.Name
            
            // 检查是否是 AccessToken 相关字段
            if fieldName == "AccessToken" || fieldName == "ProviderAccessToken" || 
               fieldName == "SuiteAccessToken" || fieldName == "CorpAccessToken" {
                jsonTag := field.Tag.Get("json")
                if jsonTag != "" && jsonTag != "-" {
                    // 移除 omitempty 等选项
                    if idx := strings.Index(jsonTag, ","); idx > 0 {
                        jsonTag = jsonTag[:idx]
                    }
                    fieldValue := v.Field(i)
                    if fieldValue.Kind() == reflect.String && fieldValue.String() != "" {
                        query.Set(jsonTag, fieldValue.String())
                    }
                }
            }
        }
    }
    
    return c.impGen.GetAccountBalance.Do("GET", "/cgi-bin/service/get_account_balance", req, query)
}
```

#### 使用示例

```go
// 创建客户端
client := wxwork.New(wxwork.Config{
    SuiteId:     "your_suite_id",
    SuiteSecret: "your_suite_secret",
})

// 调用 API
resp, err := client.GetAccountBalance(&wxwork.GetAccountBalanceRequest{
    ProviderAccessToken: "your_provider_access_token_here",
})
if err != nil {
    log.Fatal(err)
}

// ProviderAccessToken 会自动被添加到 URL query 参数中
// 实际请求: GET /cgi-bin/service/get_account_balance?provider_access_token=your_provider_access_token_here
```

## 优点

1. **自动化处理**：无需手动构建 query 参数
2. **类型安全**：AccessToken 作为结构体字段，享有类型检查
3. **一致性**：所有 API 都使用相同的模式
4. **灵活性**：支持多种 token 类型（provider、suite、corp 等）

## 注意事项

1. **字段必须为 string 类型**：只有 string 类型的字段会被提取
2. **字段不能为空**：空字符串不会被添加到 query 中
3. **JSON tag 必须存在**：字段必须有 `json:"..."` tag，且不能为 `"-"`
4. **性能考虑**：使用反射会有轻微的性能开销，但对于网络请求来说可以忽略不计

## 重新生成代码

如果修改了 API 定义或需要重新生成代码：

```bash
# 使用 LLM JSON 文件生成
./gencode --use-llm --llm-dir=docs/api_docs --output=. --package=wxwork

# 清理并重新生成
./gencode --use-llm --llm-dir=docs/api_docs --output=. --package=wxwork --clean
```

package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/url"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"text/template"
)

// LLMAPISpec represents the structure from *_llm.json files
type LLMAPISpec struct {
	PageTitle string       `json:"page_title"`
	APIs      []LLMAPIItem `json:"apis"`
}

type LLMAPIItem struct {
	GroupTitle       string    `json:"group_title"`
	APIName          string    `json:"api_name"`
	Method           string    `json:"method"`
	APIURL           string    `json:"api_url"`
	Description      string    `json:"description"`
	QueryParams      []Param   `json:"query_params"`
	BodyParams       []Param   `json:"body_params"`
	ResponseParams   []Param   `json:"response_params"`
	RequestExamples  []Example `json:"request_examples"`
	ResponseExamples []Example `json:"response_examples"`
	Sections         []Section `json:"sections"`
}

// APIItem represents a parsed API item (converted from LLMAPIItem)
type APIItem struct {
	Title            string    `json:"title"`
	Method           string    `json:"method"`
	APIURL           string    `json:"api_url"`
	APIName          string    `json:"api_name"`
	Description      string    `json:"description"`
	RequestParams    []Param   `json:"request_params"`
	ResponseParams   []Param   `json:"response_params"`
	RequestExamples  []Example `json:"request_examples"`
	ResponseExamples []Example `json:"response_examples"`
	Sections         []Section `json:"sections"`
	SourceFile       string    `json:"source_file"`
}

type Param struct {
	Name        string `json:"name"`
	Type        string `json:"type"`
	Required    *bool  `json:"required"`
	RequiredRaw string `json:"required_raw"`
	Description string `json:"description"`
	IsQuery     bool   // 标记是否为 query 参数
}

type Example struct {
	Language string `json:"language"`
	Code     string `json:"code"`
}

type Section struct {
	Title   string `json:"title"`
	Content string `json:"content"`
}

// GoType represents a generated Go type
type GoType struct {
	Name       string
	Comment    string
	Fields     []GoField
	IsRequest  bool
	IsResponse bool
}

type GoField struct {
	Name     string
	Type     string
	JSONTag  string
	Comment  string
	Required bool
	IsQuery  bool // 是否为 query 参数
}

// GoMethod represents a client method
type GoMethod struct {
	Name            string
	Comment         string
	RequestType     string
	ResponseType    string
	HTTPMethod      string
	APIPath         string
	HasRequestBody  bool
	HasResponseBody bool
	QueryParams     []string // query 参数名列表
}

var (
	inputDir    = flag.String("input", "docs/api_docs", "Directory containing *_llm.json files")
	outputDir   = flag.String("output", "generated", "Output directory for generated files")
	packageName = flag.String("package", "wxwork", "Package name for generated code")
	limit       = flag.Int("limit", 0, "Limit number of APIs to generate (0 = all)")
	cleanFirst  = flag.Bool("clean", true, "Clean generated files before generating new ones")
)

// skipAPIs 跳过生成的 API 列表（api_name）
var skipAPIs = map[string]bool{
	"chatdata/export/get_job_status": true,
	// 可以添加更多需要跳过的 API
}

// cleanGeneratedFiles 清理之前生成的文件
func cleanGeneratedFiles(outputDir string) error {
	generatedFiles := []string{
		"types_generated.go",
		"client_generated.go",
		"impls_generated.go",
	}

	var errors []string
	for _, filename := range generatedFiles {
		filePath := filepath.Join(outputDir, filename)
		if _, err := os.Stat(filePath); err == nil {
			// 文件存在，删除它
			if err := os.Remove(filePath); err != nil {
				errors = append(errors, fmt.Sprintf("%s: %v", filename, err))
			} else {
				log.Printf("Cleaned: %s", filePath)
			}
		}
	}

	if len(errors) > 0 {
		return fmt.Errorf("failed to clean some files: %s", strings.Join(errors, "; "))
	}

	return nil
}

// scanExistingTypes 扫描 types.go 和 types_placeholder.go 中已存在的类型
func scanExistingTypes(projectRoot string) map[string]bool {
	existingTypes := make(map[string]bool)

	// 扫描 types.go 和 types_placeholder.go
	filesToScan := []string{"types.go", "types_placeholder.go"}

	for _, filename := range filesToScan {
		typesFile := filepath.Join(projectRoot, filename)
		if _, err := os.Stat(typesFile); os.IsNotExist(err) {
			continue
		}

		content, err := os.ReadFile(typesFile)
		if err != nil {
			log.Printf("WARN: Cannot read %s: %v", filename, err)
			continue
		}

		// 匹配 type XXXRequest struct 和 type XXXResponse struct
		typePattern := regexp.MustCompile(`type\s+(\w+(?:Request|Response))\s+struct`)
		matches := typePattern.FindAllSubmatch(content, -1)

		for _, match := range matches {
			if len(match) > 1 {
				typeName := string(match[1])
				existingTypes[typeName] = true
			}
		}
	}

	log.Printf("INFO: Found %d existing types", len(existingTypes))
	return existingTypes
}

// loadLLMFiles 扫描并加载所有 *_llm.json 文件
func loadLLMFiles(llmDir string) ([]APIItem, error) {
	// 查找所有 *_llm.json 文件
	pattern := filepath.Join(llmDir, "*_llm.json")
	files, err := filepath.Glob(pattern)
	if err != nil {
		return nil, fmt.Errorf("glob pattern failed: %w", err)
	}

	log.Printf("Found %d *_llm.json files in %s", len(files), llmDir)

	allAPIs := []APIItem{}
	errorCount := 0

	for i, file := range files {
		if i%100 == 0 {
			log.Printf("Processing file %d/%d...", i, len(files))
		}

		apis, err := loadLLMFile(file)
		if err != nil {
			log.Printf("WARN: Failed to load %s: %v", filepath.Base(file), err)
			errorCount++
			continue
		}

		allAPIs = append(allAPIs, apis...)
	}

	log.Printf("Loaded %d APIs from %d files (%d errors)", len(allAPIs), len(files), errorCount)
	return allAPIs, nil
}

// loadLLMFile 加载单个 *_llm.json 文件
func loadLLMFile(filePath string) ([]APIItem, error) {
	data, err := os.ReadFile(filePath)
	if err != nil {
		return nil, err
	}

	var spec LLMAPISpec
	if err := json.Unmarshal(data, &spec); err != nil {
		return nil, err
	}

	// 转换为 APIItem 格式
	items := make([]APIItem, 0, len(spec.APIs))
	for _, llmAPI := range spec.APIs {
		item := convertLLMToAPIItem(llmAPI, spec.PageTitle, filePath)
		items = append(items, item)
	}

	return items, nil
}

// convertLLMToAPIItem 将 LLMAPIItem 转换为 APIItem
func convertLLMToAPIItem(llm LLMAPIItem, pageTitle, sourceFile string) APIItem {
	// 合并 query_params 和 body_params 为 request_params
	// 标记 query_params 为查询参数
	requestParams := make([]Param, 0, len(llm.QueryParams)+len(llm.BodyParams))

	// 添加所有 query 参数（包括 access_token）
	for _, param := range llm.QueryParams {
		param.IsQuery = true
		requestParams = append(requestParams, param)
	}

	// 添加 body 参数
	requestParams = append(requestParams, llm.BodyParams...)

	return APIItem{
		Title:            llm.GroupTitle,
		Method:           llm.Method,
		APIURL:           llm.APIURL,
		APIName:          llm.APIName,
		Description:      llm.Description,
		RequestParams:    requestParams,
		ResponseParams:   llm.ResponseParams,
		RequestExamples:  llm.RequestExamples,
		ResponseExamples: llm.ResponseExamples,
		Sections:         llm.Sections,
		SourceFile:       filepath.Base(sourceFile),
	}
}

func main() {
	flag.Parse()

	if err := run(); err != nil {
		log.Fatal(err)
	}
}

func run() error {
	// Determine project root
	var projectRoot string
	if filepath.IsAbs(*outputDir) {
		projectRoot = filepath.Dir(*outputDir)
	} else {
		// If relative path, use current working directory
		cwd, _ := os.Getwd()
		projectRoot = cwd
	}

	// Clean generated files if requested
	if *cleanFirst {
		log.Printf("Cleaning previously generated files...")
		if err := cleanGeneratedFiles(*outputDir); err != nil {
			log.Printf("WARN: Failed to clean some files: %v", err)
		}
	}

	// Scan existing types
	existingTypes := scanExistingTypes(projectRoot)

	// Load APIs from *_llm.json files
	log.Printf("Loading APIs from *_llm.json files in %s", *inputDir)
	allAPIs, err := loadLLMFiles(*inputDir)
	if err != nil {
		return fmt.Errorf("load LLM files: %w", err)
	}

	// Filter APIs with valid api_name
	validAPIs := []APIItem{}
	skippedCount := 0
	for _, api := range allAPIs {
		// 跳过在跳过列表中的 API
		if skipAPIs[api.APIName] {
			log.Printf("INFO: Skipping API: %s (in skip list)", api.APIName)
			skippedCount++
			continue
		}

		if api.APIName != "" && api.Method != "" {
			validAPIs = append(validAPIs, api)
		}
	}

	log.Printf("Found %d APIs with valid api_name and method (skipped %d)", len(validAPIs), skippedCount)

	if *limit > 0 && *limit < len(validAPIs) {
		validAPIs = validAPIs[:*limit]
		log.Printf("Limited to %d APIs", *limit)
	}

	// Generate types and methods
	types := []GoType{}
	methods := []GoMethod{}
	implFieldsMap := make(map[string]bool) // For deduplication
	implFields := []string{}               // For impls struct fields

	for _, api := range validAPIs {
		methodName := generateMethodNameFromURL(api.APIURL, api.APIName)
		apiPath, queryParams := extractAPIPathAndQuery(api.APIURL)

		// Skip if invalid method name or path
		if methodName == "" || apiPath == "" {
			log.Printf("WARN: Skipping invalid API: name=%s url=%s", api.APIName, api.APIURL)
			continue
		}

		// Skip duplicates
		if implFieldsMap[methodName] {
			log.Printf("WARN: Skipping duplicate API: %s (%s)", methodName, api.APIURL)
			continue
		}

		// Check if types already exist in types.go
		reqTypeName := methodName + "Request"
		respTypeName := methodName + "Response"

		typeExists := existingTypes[reqTypeName] || existingTypes[respTypeName]
		if typeExists {
			log.Printf("INFO: Type %s already exists in types.go, skipping generation", methodName)
			continue
		}

		implFieldsMap[methodName] = true

		// Generate request type with nested types (always generate even if no request params)
		reqType := generateRequestType(api)
		types = append(types, reqType)

		// 收集嵌套类型
		if len(api.RequestParams) > 0 {
			nestedRoot := buildNestedStructure(api.RequestParams, api.APIName)
			_, subTypes := flattenNestedFields(nestedRoot, reqType.Name)
			types = append(types, subTypes...)
		}

		// Generate response type with nested types (always generate even if no response params)
		respType := generateResponseType(api)
		types = append(types, respType)

		// 收集嵌套类型（过滤掉 errcode 和 errmsg）
		if len(api.ResponseParams) > 0 {
			filteredParams := []Param{}
			for _, param := range api.ResponseParams {
				if param.Name != "errcode" && param.Name != "errmsg" {
					filteredParams = append(filteredParams, param)
				}
			}
			nestedRoot := buildNestedStructure(filteredParams, api.APIName)
			_, subTypes := flattenNestedFields(nestedRoot, respType.Name)
			types = append(types, subTypes...)
		}

		// Generate client method
		method := generateMethod(api)
		method.QueryParams = queryParams
		methods = append(methods, method)

		// Add to impls field
		implFields = append(implFields, methodName)
	}

	// Create output directory
	if err := os.MkdirAll(*outputDir, 0755); err != nil {
		return fmt.Errorf("create output dir: %w", err)
	}

	// Generate types file
	if err := generateTypesFile(types); err != nil {
		return fmt.Errorf("generate types: %w", err)
	}

	// Generate impls struct file
	if err := generateImplsFile(implFields); err != nil {
		return fmt.Errorf("generate impls: %w", err)
	}

	// Generate client methods file
	if err := generateClientFile(methods); err != nil {
		return fmt.Errorf("generate client: %w", err)
	}

	log.Printf("✅ Generated %d types and %d methods", len(types), len(methods))
	log.Printf("📁 Output directory: %s", *outputDir)

	return nil
}

// NestedField 表示嵌套的字段结构
type NestedField struct {
	Name     string
	Type     string
	JSONTag  string
	Comment  string
	Required bool
	IsQuery  bool // 是否为 query 参数
	IsArray  bool // 是否为数组类型
	Children map[string]*NestedField
}

// buildNestedStructure 构建嵌套结构
func buildNestedStructure(params []Param, apiName string) map[string]*NestedField {
	root := make(map[string]*NestedField)

	// 第一遍：标记哪些字段有嵌套子字段（在所有层级），以及哪些是数组
	hasNestedFields := make(map[string]bool)
	isArrayField := make(map[string]bool) // 标记数组字段
	for _, param := range params {
		if strings.Contains(param.Name, ".") {
			parts := strings.Split(param.Name, ".")
			// 为所有中间路径标记
			path := ""
			for i := 0; i < len(parts)-1; i++ {
				if i > 0 {
					path += "."
				}
				// 检查是否包含 [] 后缀
				if strings.HasSuffix(parts[i], "[]") {
					cleanPart := strings.TrimSuffix(parts[i], "[]")
					path += cleanPart
					isArrayField[path] = true // 标记为数组
					hasNestedFields[path] = true
				} else {
					path += parts[i]
					hasNestedFields[path] = true
				}
			}
		} else {
			// 顶层字段，检查类型是否为数组
			cleanName := strings.TrimSuffix(param.Name, "[]")
			if strings.Contains(strings.ToLower(param.Type), "[]") || 
			   strings.Contains(strings.ToLower(param.Type), "array") {
				isArrayField[cleanName] = true
			}
		}
	}

	// 第二遍：构建结构
	for _, param := range params {
		// Skip Chinese-only field names or application type fields
		if isChinese(param.Name) || isApplicationType(param.Name) {
			continue
		}

		// Skip problematic field names
		if !isValidFieldName(param.Name) {
			log.Printf("WARN: Skipping invalid field name: %s in %s", param.Name, apiName)
			continue
		}

		// 检查是否是嵌套字段
		if strings.Contains(param.Name, ".") {
			parts := strings.Split(param.Name, ".")
			current := root
			currentPath := ""

			for i, part := range parts {
				if i > 0 {
					currentPath += "."
				}
				cleanPart := strings.TrimSuffix(part, "[]")
				currentPath += cleanPart

				isLeaf := i == len(parts)-1
				fieldName := toGoFieldName(cleanPart)

				if isLeaf {
					// 叶子节点
					if _, exists := current[cleanPart]; !exists {
						current[cleanPart] = &NestedField{
							Name:     fieldName,
							Type:     inferGoType(param.Type, param.Name),
							JSONTag:  toJSONTag(cleanPart),
							Comment:  cleanComment(param.Description),
							Required: param.Required != nil && *param.Required,
							IsQuery:  param.IsQuery,
							Children: nil,
						}
					}
				} else {
					// 中间节点
					if _, exists := current[cleanPart]; !exists {
						current[cleanPart] = &NestedField{
							Name:     fieldName,
							Type:     "",
							JSONTag:  toJSONTag(cleanPart),
							Comment:  "",
							Required: false,
							IsQuery:  param.IsQuery,
							IsArray:  isArrayField[currentPath], // 设置数组标记
							Children: make(map[string]*NestedField),
						}
					} else if current[cleanPart].Children == nil {
						// 如果节点已存在但 Children 为 nil（之前可能被当作叶子节点），初始化它
						current[cleanPart].Children = make(map[string]*NestedField)
						// 清空 Type，因为它现在是一个嵌套对象
						current[cleanPart].Type = ""
						// 设置数组标记
						current[cleanPart].IsArray = isArrayField[currentPath]
					}
					current = current[cleanPart].Children
				}
			}
		} else {
			// 普通字段
			// 移除 [] 后缀以获取实际字段名
			cleanName := strings.TrimSuffix(param.Name, "[]")
			
			// 如果该字段（清理后的名字）有嵌套子字段，跳过它
			if hasNestedFields[cleanName] {
				// 这个字段有嵌套子字段，不要创建简单类型
				continue
			}

			fieldName := toGoFieldName(cleanName)
			if _, exists := root[cleanName]; !exists {
				root[cleanName] = &NestedField{
					Name:     fieldName,
					Type:     inferGoType(param.Type, param.Name),
					JSONTag:  toJSONTag(cleanName),
					Comment:  cleanComment(param.Description),
					Required: param.Required != nil && *param.Required,
					IsQuery:  param.IsQuery,
					Children: nil,
				}
			}
		}
	}

	return root
}

// flattenNestedFields 将嵌套结构展平成 GoField 列表和子类型列表
func flattenNestedFields(root map[string]*NestedField, parentTypeName string) ([]GoField, []GoType) {
	fields := []GoField{}
	subTypes := []GoType{}

	for _, nf := range root {
		if nf.Children != nil && len(nf.Children) > 0 {
			// 这是一个嵌套对象，生成子类型
			subTypeName := parentTypeName + nf.Name
			subFields, subSubTypes := flattenNestedFields(nf.Children, subTypeName)

			subType := GoType{
				Name:    subTypeName,
				Comment: fmt.Sprintf("%s - 嵌套类型", subTypeName),
				Fields:  subFields,
			}
			subTypes = append(subTypes, subType)
			subTypes = append(subTypes, subSubTypes...)

			// 根据是否为数组生成不同的类型
			fieldType := "*" + subTypeName
			if nf.IsArray {
				fieldType = "[]" + subTypeName // 数组类型，不使用指针
			}

			// 添加指向子类型的字段
			fields = append(fields, GoField{
				Name:     nf.Name,
				Type:     fieldType,
				JSONTag:  nf.JSONTag,
				Comment:  nf.Comment,
				Required: nf.Required,
				IsQuery:  nf.IsQuery,
			})
		} else {
			// 普通字段
			fields = append(fields, GoField{
				Name:     nf.Name,
				Type:     nf.Type,
				JSONTag:  nf.JSONTag,
				Comment:  nf.Comment,
				Required: nf.Required,
				IsQuery:  nf.IsQuery,
			})
		}
	}

	return fields, subTypes
}

func generateRequestType(api APIItem) GoType {
	name := generateMethodNameFromURL(api.APIURL, api.APIName) + "Request"

	// 构建嵌套结构
	nestedRoot := buildNestedStructure(api.RequestParams, api.APIName)

	// 展平为字段和子类型
	fields, _ := flattenNestedFields(nestedRoot, name)

	return GoType{
		Name:      name,
		Comment:   fmt.Sprintf("%s - %s", name, cleanTitle(api.Title)),
		Fields:    fields,
		IsRequest: true,
	}
}

func generateResponseType(api APIItem) GoType {
	name := generateMethodNameFromURL(api.APIURL, api.APIName) + "Response"

	// 过滤掉 errcode 和 errmsg
	filteredParams := []Param{}
	for _, param := range api.ResponseParams {
		if param.Name != "errcode" && param.Name != "errmsg" {
			filteredParams = append(filteredParams, param)
		}
	}

	// 构建嵌套结构
	nestedRoot := buildNestedStructure(filteredParams, api.APIName)

	// 展平为字段和子类型
	fields, _ := flattenNestedFields(nestedRoot, name)

	// 在最前面添加 CommonResponse
	allFields := []GoField{
		{
			Name:    "CommonResponse",
			Type:    "CommonResponse",
			JSONTag: "",
			Comment: "",
		},
	}
	allFields = append(allFields, fields...)

	return GoType{
		Name:       name,
		Comment:    fmt.Sprintf("%s - %s", name, cleanTitle(api.Title)),
		Fields:     allFields,
		IsResponse: true,
	}
}

func generateMethod(api APIItem) GoMethod {
	methodName := generateMethodNameFromURL(api.APIURL, api.APIName)
	reqType := methodName + "Request"
	respType := methodName + "Response"

	// Extract path from URL
	apiPath := extractAPIPath(api.APIURL)

	return GoMethod{
		Name:            methodName,
		Comment:         fmt.Sprintf("%s - %s", methodName, cleanTitle(api.Title)),
		RequestType:     reqType,
		ResponseType:    respType,
		HTTPMethod:      api.Method,
		APIPath:         apiPath,
		HasRequestBody:  len(api.RequestParams) > 0,
		HasResponseBody: len(api.ResponseParams) > 0,
	}
}

func toGoTypeName(apiName string) string {
	// Convert api_name like "user/create" to "UserCreate"
	// Skip if it looks like a full URL
	if strings.HasPrefix(apiName, "http://") || strings.HasPrefix(apiName, "https://") {
		return ""
	}

	parts := strings.Split(apiName, "/")
	result := ""
	for _, part := range parts {
		result += toPascalCase(part)
	}

	// If the result is empty or starts with a number, prefix with "API"
	if result == "" || (len(result) > 0 && result[0] >= '0' && result[0] <= '9') {
		result = "API" + result
	}

	return result
}

func toGoFieldName(name string) string {
	// Remove dots, brackets and other special chars
	name = strings.ReplaceAll(name, ".", "_")
	name = strings.ReplaceAll(name, "[", "_")
	name = strings.ReplaceAll(name, "]", "_")
	name = strings.ReplaceAll(name, "(", "_")
	name = strings.ReplaceAll(name, ")", "_")
	name = strings.Trim(name, "-_")

	// If starts with a number or special char, prefix with "Code"
	if len(name) > 0 && (name[0] >= '0' && name[0] <= '9' || !isValidIdentifierStart(name[0])) {
		name = "Code" + name
	}

	// If empty or only special chars, use generic name
	cleaned := toPascalCase(name)
	if cleaned == "" {
		return "Field"
	}

	return cleaned
}

func isValidFieldName(name string) bool {
	if name == "" {
		return false
	}

	// Check for problematic characters
	problematicChars := []string{
		"\n", "\t", "\r",
		"└", "├", "─", // Tree/box drawing characters
		" ",            // Space
		":", "/", "\\", // Slashes and colons
		"<", ">", "|", "?", "*", // Other special chars
	}

	for _, char := range problematicChars {
		if strings.Contains(name, char) {
			return false
		}
	}

	// Check for quotes (already removed in toJSONTag but double check)
	if strings.Contains(name, `"`) || strings.Contains(name, `'`) {
		return false
	}

	return true
}

func isValidIdentifierStart(c byte) bool {
	return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_'
}

func toPascalCase(s string) string {
	// Remove all non-ASCII characters first
	s = regexp.MustCompile(`[^\x00-\x7F]+`).ReplaceAllString(s, "")

	// Handle snake_case
	s = strings.ReplaceAll(s, "-", "_")
	parts := strings.Split(s, "_")
	result := ""
	for _, part := range parts {
		if part == "" {
			continue
		}
		result += strings.ToUpper(part[:1]) + strings.ToLower(part[1:])
	}

	// Handle common abbreviations
	result = strings.ReplaceAll(result, "Id", "ID")
	result = strings.ReplaceAll(result, "Url", "URL")
	result = strings.ReplaceAll(result, "Api", "API")
	result = strings.ReplaceAll(result, "Jsapi", "JSAPI")
	result = strings.ReplaceAll(result, "Kf", "KF")

	return result
}

func toJSONTag(name string) string {
	// Clean up problematic characters for JSON tags
	name = strings.ReplaceAll(name, `"`, "")
	name = strings.ReplaceAll(name, `'`, "")
	name = strings.ReplaceAll(name, "\n", "")
	name = strings.ReplaceAll(name, "\t", "")
	return strings.ToLower(name)
}

func inferGoType(typeName, fieldName string) string {
	// 只使用字段名的最后一部分（去掉路径和数组标记）
	// 例如：userlist[].userid -> userid
	lastPart := fieldName
	if strings.Contains(fieldName, ".") {
		parts := strings.Split(fieldName, ".")
		lastPart = parts[len(parts)-1]
	}
	// 移除 [] 标记
	lastPart = strings.TrimSuffix(lastPart, "[]")
	
	fieldLower := strings.ToLower(lastPart)
	typeLower := strings.ToLower(typeName)

	// 处理数组类型（如 string[], uint32[], int32[]）
	if strings.Contains(typeLower, "[]") {
		// 提取基础类型
		baseType := strings.TrimSuffix(typeName, "[]")
		baseType = strings.TrimSpace(baseType)
		baseLower := strings.ToLower(baseType)
		
		// 根据基础类型返回对应的数组类型
		switch {
		case baseLower == "string":
			return "[]string"
		case baseLower == "int32":
			return "[]int32"
		case baseLower == "uint32":
			return "[]uint32"
		case baseLower == "int64":
			return "[]int64"
		case baseLower == "uint64":
			return "[]uint64"
		case baseLower == "int":
			return "[]int"
		case baseLower == "bool":
			return "[]bool"
		case baseLower == "float32":
			return "[]float32"
		case baseLower == "float64":
			return "[]float64"
		case strings.Contains(baseLower, "object"):
			return "[]interface{}" // object[] 会在嵌套结构中处理
		default:
			return "[]interface{}"
		}
	}

	// 优先根据明确的类型名称判断（来自 JSON 定义）
	if strings.Contains(typeLower, "uint32") {
		return "uint32"
	}
	if strings.Contains(typeLower, "int32") {
		return "int32"
	}
	if strings.Contains(typeLower, "uint64") {
		return "uint64"
	}
	if strings.Contains(typeLower, "int64") {
		return "int64"
	}
	if strings.Contains(typeLower, "bool") {
		return "bool"
	}
	if strings.Contains(typeLower, "float32") {
		return "float32"
	}
	if strings.Contains(typeLower, "float64") || strings.Contains(typeLower, "float") {
		return "float64"
	}
	if strings.Contains(typeLower, "int") {
		return "int"
	}
	if strings.Contains(typeLower, "array") {
		return "[]interface{}"
	}
	if strings.Contains(typeLower, "object") {
		return "map[string]interface{}"
	}

	// 基于字段名的通用模式推断（在类型名不明确时使用）
	if strings.Contains(fieldLower, "list") || strings.Contains(fieldLower, "ids") {
		return "[]string"
	}

	if strings.Contains(fieldLower, "time") || strings.Contains(fieldLower, "timestamp") {
		return "int64"
	}

	if strings.Contains(fieldLower, "count") || strings.Contains(fieldLower, "num") {
		return "int"
	}

	// 最后才基于字段名后缀推断（优先级最低）
	if strings.HasSuffix(fieldLower, "id") || strings.HasSuffix(fieldLower, "code") {
		return "string"
	}

	// Default to string
	return "string"
}

func cleanComment(s string) string {
	s = strings.TrimSpace(s)
	s = strings.ReplaceAll(s, "\n", " ")
	s = regexp.MustCompile(`\s+`).ReplaceAllString(s, " ")

	// Replace Chinese punctuation with ASCII equivalents
	s = strings.ReplaceAll(s, "：", ":")
	s = strings.ReplaceAll(s, "，", ",")
	s = strings.ReplaceAll(s, "。", ".")
	s = strings.ReplaceAll(s, "（", "(")
	s = strings.ReplaceAll(s, "）", ")")
	s = strings.ReplaceAll(s, "、", ",")
	s = strings.ReplaceAll(s, "；", ";")

	return s
}

func isChinese(s string) bool {
	// Check if string contains only Chinese characters
	for _, r := range s {
		if r >= 0x4e00 && r <= 0x9fff {
			return true
		}
	}
	return false
}

func isApplicationType(s string) bool {
	// Filter out application type descriptors
	appTypes := []string{"自建应用", "代开发应用", "第三方应用", "服务商应用"}
	for _, t := range appTypes {
		if s == t {
			return true
		}
	}
	return false
}

func cleanTitle(s string) string {
	s = strings.TrimSpace(s)
	// Remove " - 文档 - 企业微信开发者中心"
	s = regexp.MustCompile(`\s*-\s*文档\s*-\s*企业微信开发者中心\s*$`).ReplaceAllString(s, "")
	return s
}

func extractAPIPath(apiURL string) string {
	path, _ := extractAPIPathAndQuery(apiURL)
	return path
}

// extractServiceNameFromURL 从 API URL 中提取服务名
// 例如: https://qyapi.weixin.qq.com/cgi-bin/user/create -> "user"
// 例如: https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get -> "externalcontact"
func extractServiceNameFromURL(apiURL string) string {
	if apiURL == "" {
		return ""
	}

	// 移除 query string
	idx := strings.Index(apiURL, "?")
	if idx > 0 {
		apiURL = apiURL[:idx]
	}

	// 解析 URL 获取 path
	u, err := url.Parse(apiURL)
	if err != nil {
		return ""
	}

	path := u.Path
	// 移除 /cgi-bin/ 前缀
	path = strings.TrimPrefix(path, "/cgi-bin/")
	
	// 分割路径，获取服务名
	parts := strings.Split(path, "/")
	if len(parts) < 2 {
		return ""
	}

	// 返回服务名（第一段）
	return parts[0]
}

// generateMethodNameFromURL 从 API URL 和 api_name 生成完整的方法名
// 例如: url="https://qyapi.weixin.qq.com/cgi-bin/user/create", api_name="create" -> "UserCreate"
func generateMethodNameFromURL(apiURL, apiName string) string {
	serviceName := extractServiceNameFromURL(apiURL)
	
	if serviceName == "" {
		// 如果无法从 URL 提取服务名，使用原来的逻辑
		return toGoTypeName(apiName)
	}

	// 检查 apiName 是否已经包含服务名（避免重复）
	// 例如 api_name="user/create" 已经包含 "user"
	if strings.Contains(apiName, "/") {
		return toGoTypeName(apiName)
	}

	// 组合服务名和操作名
	fullName := serviceName + "/" + apiName
	return toGoTypeName(fullName)
}

func extractAPIPathAndQuery(apiURL string) (string, []string) {
	if apiURL == "" {
		return "", nil
	}

	queryParams := []string{}

	// Extract query string
	idx := strings.Index(apiURL, "?")
	if idx > 0 {
		queryString := apiURL[idx+1:]
		apiURL = apiURL[:idx]

		// Parse query parameters
		parts := strings.Split(queryString, "&")
		for _, part := range parts {
			kv := strings.Split(part, "=")
			if len(kv) > 0 {
				paramName := kv[0]
				// 排除占位符参数（大写字母开头的）
				if paramName != "" && !isPlaceholder(paramName) {
					queryParams = append(queryParams, paramName)
				}
			}
		}
	}

	// Get path after domain
	idx = strings.Index(apiURL, "/cgi-bin/")
	if idx >= 0 {
		return apiURL[idx:], queryParams
	}

	// If no /cgi-bin/, return empty (invalid)
	return "", queryParams
}

func isPlaceholder(s string) bool {
	// 检查是否是占位符（如 ACCESS_TOKEN, SUITE_ACCESS_TOKEN）
	if len(s) == 0 {
		return false
	}
	// 全大写或包含大写字母且以大写开头
	return strings.ToUpper(s) == s && s[0] >= 'A' && s[0] <= 'Z'
}

func generateTypesFile(types []GoType) error {
	tmpl := `// Code generated by gencode. DO NOT EDIT.
package {{ .PackageName }}

{{ range .Types }}
// {{ .Comment }}
type {{ .Name }} struct {
{{- range .Fields }}
{{- if .IsQuery }}
{{- if .Comment }}
	{{ .Name }} {{ .Type }} ` + "`json:\"{{ .JSONTag }}\" query:\"{{ .JSONTag }}\"`" + ` // {{ .Comment }}
{{- else }}
	{{ .Name }} {{ .Type }} ` + "`json:\"{{ .JSONTag }}\" query:\"{{ .JSONTag }}\"`" + `
{{- end }}
{{- else if .Comment }}
	{{ .Name }} {{ .Type }} ` + "`json:\"{{ .JSONTag }}\"`" + ` // {{ .Comment }}
{{- else if .JSONTag }}
	{{ .Name }} {{ .Type }} ` + "`json:\"{{ .JSONTag }}\"`" + `
{{- else }}
	{{ .Name }}
{{- end }}
{{- end }}
}

{{ end }}
`

	t, err := template.New("types").Parse(tmpl)
	if err != nil {
		return err
	}

	outFile := filepath.Join(*outputDir, "types_generated.go")
	f, err := os.Create(outFile)
	if err != nil {
		return err
	}
	defer f.Close()

	data := map[string]interface{}{
		"PackageName": *packageName,
		"Types":       types,
	}

	return t.Execute(f, data)
}

func generateImplsFile(implFields []string) error {
	tmpl := `// Code generated by gencode. DO NOT EDIT.
package {{ .PackageName }}

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strings"
)

// impl 是 API 调用的泛型实现
type impl[Req any, Resp any] struct {
	c *client
}

// install 安装客户端实例
func (i *impl[Req, Resp]) install(c *client) {
	i.c = c
}

// Do 执行 API 调用
func (i *impl[Req, Resp]) Do(method, path string, req *Req, query url.Values) (*Resp, error) {
	// 构建完整 URL
	fullURL := i.c.getUrl(path)
	if len(query) > 0 {
		fullURL = fullURL + "?" + query.Encode()
	}

	var bodyReader io.Reader
	if req != nil && (method == "POST" || method == "PUT" || method == "PATCH") {
		jsonData, err := json.Marshal(req)
		if err != nil {
			return nil, fmt.Errorf("marshal request: %w", err)
		}
		bodyReader = strings.NewReader(string(jsonData))
	}

	httpReq, err := http.NewRequest(method, fullURL, bodyReader)
	if err != nil {
		return nil, fmt.Errorf("create request: %w", err)
	}

	if bodyReader != nil {
		httpReq.Header.Set("Content-Type", "application/json")
	}

	httpResp, err := i.c.httpClient.Do(httpReq)
	if err != nil {
		return nil, fmt.Errorf("do request: %w", err)
	}
	defer httpResp.Body.Close()

	respBody, err := io.ReadAll(httpResp.Body)
	if err != nil {
		return nil, fmt.Errorf("read response: %w", err)
	}

	// 先检查是否有错误
	var commonResp CommonResponse
	if err := json.Unmarshal(respBody, &commonResp); err == nil {
		if commonResp.Errcode != 0 {
			return nil, &RespError{
				Errcode: commonResp.Errcode,
				Errmsg:  commonResp.Errmsg,
			}
		}
	}

	var resp Resp
	if err := json.Unmarshal(respBody, &resp); err != nil {
		return nil, fmt.Errorf("unmarshal response: %w", err)
	}

	return &resp, nil
}

// implsGenerated contains all generated API implementations
type implsGenerated struct {
	inited bool
{{- range .ImplFields }}
	{{ . }} impl[{{ . }}Request, {{ . }}Response]
{{- end }}
}

// installAll installs all generated implementations
func (imp *implsGenerated) installAll(c *client) {
	if imp.inited {
		return
	}
	
{{- range .ImplFields }}
	imp.{{ . }}.install(c)
{{- end }}
	
	imp.inited = true
}
`

	t, err := template.New("impls").Parse(tmpl)
	if err != nil {
		return err
	}

	outFile := filepath.Join(*outputDir, "impls_generated.go")
	f, err := os.Create(outFile)
	if err != nil {
		return err
	}
	defer f.Close()

	data := map[string]interface{}{
		"PackageName": *packageName,
		"ImplFields":  implFields,
	}

	return t.Execute(f, data)
}

func generateClientFile(methods []GoMethod) error {
	// Generate methods file
	methodsTmpl := `// Code generated by gencode. DO NOT EDIT.
package {{ .PackageName }}

import (
	"fmt"
	"net/http"
	"net/url"
	"reflect"
	"strings"
)

// DefaultHost 默认的企业微信 API 地址
var DefaultHost = "https://qyapi.weixin.qq.com"

// CommonResponse 通用响应结构
type CommonResponse struct {
	Errcode int    ` + "`json:\"errcode\"`" + `
	Errmsg  string ` + "`json:\"errmsg\"`" + `
}

// RespError API 错误响应
type RespError struct {
	Errcode int
	Errmsg  string
}

func (e *RespError) Error() string {
	return fmt.Sprintf("wxwork api error: code=%d, msg=%s", e.Errcode, e.Errmsg)
}

// Config 客户端配置
type Config struct {
	Host        string // API 地址，默认 https://qyapi.weixin.qq.com
	SuiteId     string
	SuiteSecret string
	Debug       bool
}

// Client 企业微信客户端接口
type Client interface {
{{- range .Methods }}
	{{ .Name }}(req *{{ .RequestType }}) (*{{ .ResponseType }}, error)
{{- end }}
}

// client 客户端实现
type client struct {
	Host        string
	SuiteId     string
	SuiteSecret string
	Debug       bool

	httpClient   *http.Client
	impGen       implsGenerated
	expireHandle func(corpId string) string
}

// New 创建企业微信客户端
func New(cfg Config) Client {
	host := cfg.Host
	if host == "" {
		host = DefaultHost
	}
	
	c := &client{
		Host:        host,
		SuiteId:     cfg.SuiteId,
		SuiteSecret: cfg.SuiteSecret,
		Debug:       cfg.Debug,
		httpClient:  &http.Client{},
	}

	c.init()
	return c
}

// init 初始化客户端
func (c *client) init() {
	c.impGen.installAll(c)
}

// getUrl 获取完整的 API URL
func (c *client) getUrl(path string) string {
	p, err := url.JoinPath(c.Host, path)
	if err != nil {
		panic(err)
	}
	return p
}

// HandleTokenExpired 设置 token 过期处理函数
func (c *client) HandleTokenExpired(fn func(corpId string) string) {
	c.expireHandle = fn
}

// extractQueryParams 从请求结构体中提取带有 query tag 的字段到 URL 查询参数
func extractQueryParams(req interface{}, query url.Values) {
	if req == nil {
		return
	}
	
	v := reflect.ValueOf(req)
	if v.Kind() == reflect.Ptr {
		v = v.Elem()
	}
	if v.Kind() != reflect.Struct {
		return
	}
	
	t := v.Type()
	for i := 0; i < v.NumField(); i++ {
		field := t.Field(i)
		queryTag := field.Tag.Get("query")
		if queryTag == "" || queryTag == "-" {
			continue
		}
		
		// 移除 omitempty 等选项
		if idx := strings.Index(queryTag, ","); idx > 0 {
			queryTag = queryTag[:idx]
		}
		
		fieldValue := v.Field(i)
		// 根据字段类型转换值
		switch fieldValue.Kind() {
		case reflect.String:
			if s := fieldValue.String(); s != "" {
				query.Set(queryTag, s)
			}
		case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
			if n := fieldValue.Int(); n != 0 {
				query.Set(queryTag, fmt.Sprintf("%d", n))
			}
		case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64:
			if n := fieldValue.Uint(); n != 0 {
				query.Set(queryTag, fmt.Sprintf("%d", n))
			}
		case reflect.Bool:
			if fieldValue.Bool() {
				query.Set(queryTag, "true")
			}
		}
	}
}

// 确保 client 实现了 Client 接口
var _ Client = (*client)(nil)

{{ range .Methods }}
// {{ .Comment }}
func (c *client) {{ .Name }}(req *{{ .RequestType }}) (*{{ .ResponseType }}, error) {
	query := url.Values{}
	
	// 自动从 req 中提取带有 query tag 的字段到 URL 查询参数
	extractQueryParams(req, query)
	
	return c.impGen.{{ .Name }}.Do("{{ .HTTPMethod }}", "{{ .APIPath }}", req, query)
}

{{ end }}
`

	t, err := template.New("client").Parse(methodsTmpl)
	if err != nil {
		return err
	}

	outFile := filepath.Join(*outputDir, "client_generated.go")
	f, err := os.Create(outFile)
	if err != nil {
		return err
	}
	defer f.Close()

	data := map[string]interface{}{
		"PackageName": *packageName,
		"Methods":     methods,
	}

	return t.Execute(f, data)
}

package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"text/template"
)

// APISpec represents the structure from apis.json
type APISpec struct {
	GeneratedAt string    `json:"generated_at"`
	SourceDir   string    `json:"source_dir"`
	Count       int       `json:"count"`
	ErrorCount  int       `json:"error_count"`
	Errors      []any     `json:"errors"`
	APIs        []APIItem `json:"apis"`
}

type APIItem struct {
	ID               string           `json:"id"`
	Score            int              `json:"score"`
	Title            string           `json:"title"`
	DocURL           string           `json:"doc_url"`
	Method           string           `json:"method"`
	APIURL           string           `json:"api_url"`
	APIName          string           `json:"api_name"`
	Description      string           `json:"description"`
	RequestParams    []Param          `json:"request_params"`
	ResponseParams   []Param          `json:"response_params"`
	RequestExamples  []Example        `json:"request_examples"`
	ResponseExamples []Example        `json:"response_examples"`
	Sections         []Section        `json:"sections"`
	SourceFile       string           `json:"source_file"`
}

type Param struct {
	Name        string `json:"name"`
	Type        string `json:"type"`
	Required    *bool  `json:"required"`
	RequiredRaw string `json:"required_raw"`
	Description string `json:"description"`
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
}

var (
	inputFile  = flag.String("input", "docs/apis/apis.json", "Input APIs JSON file")
	outputDir  = flag.String("output", "generated", "Output directory for generated files")
	packageName = flag.String("package", "wxwork", "Package name for generated code")
	limit      = flag.Int("limit", 0, "Limit number of APIs to generate (0 = all)")
)

func main() {
	flag.Parse()

	if err := run(); err != nil {
		log.Fatal(err)
	}
}

func run() error {
	// Read APIs JSON
	data, err := os.ReadFile(*inputFile)
	if err != nil {
		return fmt.Errorf("read input file: %w", err)
	}

	var spec APISpec
	if err := json.Unmarshal(data, &spec); err != nil {
		return fmt.Errorf("parse JSON: %w", err)
	}

	log.Printf("Loaded %d APIs from %s", spec.Count, *inputFile)

	// Filter APIs with valid api_name
	validAPIs := []APIItem{}
	for _, api := range spec.APIs {
		if api.APIName != "" && api.Method != "" {
			validAPIs = append(validAPIs, api)
		}
	}

	log.Printf("Found %d APIs with valid api_name and method", len(validAPIs))

	if *limit > 0 && *limit < len(validAPIs) {
		validAPIs = validAPIs[:*limit]
		log.Printf("Limited to %d APIs", *limit)
	}

	// Generate types and methods
	types := []GoType{}
	methods := []GoMethod{}
	implFieldsMap := make(map[string]bool) // For deduplication
	implFields := []string{}                // For impls struct fields

	for _, api := range validAPIs {
		methodName := toGoTypeName(api.APIName)
		apiPath := extractAPIPath(api.APIURL)
		
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
		implFieldsMap[methodName] = true
		
		// Generate request type
		if len(api.RequestParams) > 0 {
			reqType := generateRequestType(api)
			types = append(types, reqType)
		}

		// Generate response type
		if len(api.ResponseParams) > 0 {
			respType := generateResponseType(api)
			types = append(types, respType)
		}

		// Generate client method
		method := generateMethod(api)
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

func generateRequestType(api APIItem) GoType {
	name := toGoTypeName(api.APIName) + "Request"
	fields := []GoField{}

	for _, param := range api.RequestParams {
		// Skip Chinese-only field names or application type fields
		if isChinese(param.Name) || isApplicationType(param.Name) {
			continue
		}
		
		// Skip problematic field names
		if !isValidFieldName(param.Name) {
			log.Printf("WARN: Skipping invalid field name: %s in %s", param.Name, api.APIName)
			continue
		}
		
		field := GoField{
			Name:     toGoFieldName(param.Name),
			Type:     inferGoType(param.Type, param.Name),
			JSONTag:  toJSONTag(param.Name),
			Comment:  cleanComment(param.Description),
			Required: param.Required != nil && *param.Required,
		}
		fields = append(fields, field)
	}

	return GoType{
		Name:      name,
		Comment:   fmt.Sprintf("%s - %s", name, cleanTitle(api.Title)),
		Fields:    fields,
		IsRequest: true,
	}
}

func generateResponseType(api APIItem) GoType {
	name := toGoTypeName(api.APIName) + "Response"
	fields := []GoField{}

	// Add embedded CommonResponse
	fields = append(fields, GoField{
		Name:    "CommonResponse",
		Type:    "CommonResponse",
		JSONTag: "",
		Comment: "",
	})

	for _, param := range api.ResponseParams {
		// Skip errcode and errmsg as they're in CommonResponse
		if param.Name == "errcode" || param.Name == "errmsg" {
			continue
		}
		
		// Skip problematic field names
		if !isValidFieldName(param.Name) {
			log.Printf("WARN: Skipping invalid field name: %s in %s", param.Name, api.APIName)
			continue
		}

		field := GoField{
			Name:    toGoFieldName(param.Name),
			Type:    inferGoType(param.Type, param.Name),
			JSONTag: toJSONTag(param.Name),
			Comment: cleanComment(param.Description),
		}
		fields = append(fields, field)
	}

	return GoType{
		Name:       name,
		Comment:    fmt.Sprintf("%s - %s", name, cleanTitle(api.Title)),
		Fields:     fields,
		IsResponse: true,
	}
}

func generateMethod(api APIItem) GoMethod {
	methodName := toGoTypeName(api.APIName)
	reqType := methodName + "Request"
	respType := methodName + "Response"

	// Extract path from URL
	apiPath := extractAPIPath(api.APIURL)

	return GoMethod{
		Name:            methodName,
		Comment:         fmt.Sprintf("%s - %s\n// Doc: %s", methodName, cleanTitle(api.Title), api.DocURL),
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
		" ",  // Space
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
	fieldLower := strings.ToLower(fieldName)
	
	// Common patterns
	if strings.Contains(fieldLower, "list") || strings.Contains(fieldLower, "ids") {
		return "[]string"
	}
	
	if strings.HasSuffix(fieldLower, "id") || strings.HasSuffix(fieldLower, "code") {
		return "string"
	}
	
	if strings.Contains(fieldLower, "time") || strings.Contains(fieldLower, "timestamp") {
		return "int64"
	}
	
	if strings.Contains(fieldLower, "count") || strings.Contains(fieldLower, "num") {
		return "int"
	}
	
	// Based on type name
	typeLower := strings.ToLower(typeName)
	if strings.Contains(typeLower, "int") {
		return "int"
	}
	if strings.Contains(typeLower, "bool") {
		return "bool"
	}
	if strings.Contains(typeLower, "array") || strings.Contains(typeLower, "[]") {
		return "[]interface{}"
	}
	if strings.Contains(typeLower, "object") {
		return "map[string]interface{}"
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
	if apiURL == "" {
		return ""
	}
	
	// Extract path from URL, remove query string
	idx := strings.Index(apiURL, "?")
	if idx > 0 {
		apiURL = apiURL[:idx]
	}
	
	// Get path after domain
	idx = strings.Index(apiURL, "/cgi-bin/")
	if idx >= 0 {
		return apiURL[idx:]
	}
	
	// If no /cgi-bin/, return empty (invalid)
	return ""
}

func generateTypesFile(types []GoType) error {
	tmpl := `// Code generated by gencode. DO NOT EDIT.
package {{ .PackageName }}

{{ range .Types }}
// {{ .Comment }}
type {{ .Name }} struct {
{{- range .Fields }}
{{- if .Comment }}
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
	"net/url"
)

{{ range .Methods }}
// {{ .Comment }}
func (c *client) {{ .Name }}(req *{{ .RequestType }}) (*{{ .ResponseType }}, error) {
	var query url.Values
	query = url.Values{}
	
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

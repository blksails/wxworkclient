package main

import (
	"fmt"
	"log"
	"os"

	wxwork "pkg.blksails.net/wxworkclient"
)

func main() {
	// 创建企业微信 Client
	client := wxwork.New(wxwork.Config{
		SuiteId:     os.Getenv("WXWORK_SUITE_ID"),
		SuiteSecret: os.Getenv("WXWORK_SUITE_SECRET"),
		SuiteToken:  os.Getenv("WXWORK_SUITE_TOKEN"),
		SuiteAesKey: os.Getenv("WXWORK_SUITE_AES_KEY"),
		Debug:       true,
	})

	// 从环境变量获取 access_token
	// 注意：实际使用时，应该通过企业微信 API 获取 access_token
	accessToken := os.Getenv("WXWORK_ACCESS_TOKEN")
	if accessToken == "" {
		log.Fatal("请设置 WXWORK_ACCESS_TOKEN 环境变量")
	}

	// 示例 1: 获取用户信息
	getUserInfo(client, accessToken)

	// 示例 2: 创建用户
	createUser(client, accessToken)

	// 示例 3: 发送应用消息
	sendMessage(client, accessToken)
}

func getUserInfo(client wxwork.Client, accessToken string) {
	// 使用生成的类型和方法
	req := &wxwork.UserGetRequest{
		AccessToken: accessToken,
		Userid:      "zhangsan",
	}

	resp, err := client.UserGet(req)
	if err != nil {
		log.Printf("获取用户信息失败: %v", err)
		return
	}

	fmt.Printf("用户信息: %+v\n", resp)
}

func createUser(client wxwork.Client, accessToken string) {
	req := &wxwork.UserCreateRequest{
		AccessToken: accessToken,
		Userid:      "lisi",
		Name:        "李四",
		Department:  "1",
		Mobile:      "13800138000",
	}

	resp, err := client.UserCreate(req)
	if err != nil {
		log.Printf("创建用户失败: %v", err)
		return
	}

	fmt.Printf("创建用户成功: %+v\n", resp)
}

func sendMessage(client wxwork.Client, accessToken string) {
	req := &wxwork.MessageSendRequest{
		AccessToken: accessToken,
		Touser:      "zhangsan|lisi",
		Msgtype:     "text",
		Agentid:     "1000001",
		Content:     "你好，这是一条测试消息",
	}

	resp, err := client.MessageSend(req)
	if err != nil {
		log.Printf("发送消息失败: %v", err)
		return
	}

	fmt.Printf("发送消息成功: %+v\n", resp)
}

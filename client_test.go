package wxwork

import (
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

func Test_client_SuiteAccessToken(t *testing.T) {
	var c = New(Config{
		SuiteId:     os.Getenv("WXWORK_SUITE_ID"),
		SuiteSecret: os.Getenv("WXWORK_SUITE_SECRET"),
	})

	got, got1, err := c.SuiteAccessToken(os.Getenv("WXWORK_SUITE_TICKET"))
	assert.NoError(t, err)
	assert.NotEmpty(t, got)
	assert.NotEmpty(t, got1)
	t.Logf("SuiteAccessToken: %s, %d", got, got1)
}

func Test_client_GetAuthInfo(t *testing.T) {
	var c = &client{
		Host:        DefaultHost,
		SuiteId:     os.Getenv("WXWORK_SUITE_ID"),
		SuiteSecret: os.Getenv("WXWORK_SUITE_SECRET"),
	}

	got, err := c.GetAuthInfo(os.Getenv("WXWORK_SUITE_ACCESS_TOKEN"), os.Getenv("WXWORK_CORP_ID"), os.Getenv("WXWORK_PERMANENT_CODE"))
	assert.NoError(t, err)
	assert.NotEmpty(t, got)
	t.Logf("GetAuthInfo: %+v", got)
}

func Test_client_GetPermanentCode(t *testing.T) {
	var c = &client{
		Host:        DefaultHost,
		SuiteId:     os.Getenv("WXWORK_SUITE_ID"),
		SuiteSecret: os.Getenv("WXWORK_SUITE_SECRET"),
	}

	got, err := c.GetPermanentCode(os.Getenv("WXWORK_SUITE_ACCESS_TOKEN"), os.Getenv("WXWORK_AUTH_CODE"))
	assert.NoError(t, err)
	assert.NotEmpty(t, got)
	t.Logf("GetPermanentCode: %+v", got)
}

func Test_client_ListKFAccounts(t *testing.T) {
	var c = &client{
		Host:        DefaultHost,
		SuiteId:     os.Getenv("WXWORK_SUITE_ID"),
		SuiteSecret: os.Getenv("WXWORK_SUITE_SECRET"),
	}

	got, err := c.ListKFAccounts(os.Getenv("WXWORK_ACCESS_TOKEN"), 0, 100)
	assert.NoError(t, err)
	assert.NotEmpty(t, got)
	t.Logf("ListKFAccounts: %+v", got)
}

func Test_client_GetAccessToken(t *testing.T) {
	var c = &client{
		Host:        DefaultHost,
		SuiteId:     os.Getenv("WXWORK_SUITE_ID"),
		SuiteSecret: os.Getenv("WXWORK_SUITE_SECRET"),
	}

	got, _, err := c.GetAccessToken(os.Getenv("WXWORK_CORP_ID"), os.Getenv("WXWORK_CORP_SECRET"))
	assert.NoError(t, err)
	assert.NotEmpty(t, got)
	t.Logf("GetAccessToken: %+v", got)
}

func Test_client_AddContactWay(t *testing.T) {
	var c = &client{
		Host:        DefaultHost,
		SuiteId:     os.Getenv("WXWORK_SUITE_ID"),
		SuiteSecret: os.Getenv("WXWORK_SUITE_SECRET"),
	}

	got, err := c.AddContactWay(os.Getenv("WXWORK_ACCESS_TOKEN"), os.Getenv("WXWORK_OPEN_KFID"), os.Getenv("WXWORK_SCENE"))
	assert.NoError(t, err)
	assert.NotEmpty(t, got)
	t.Logf("AddContactWay: %+v", got)
}

func Test_client_AddKfAccount(t *testing.T) {
	var c = &client{
		Host:        DefaultHost,
		SuiteId:     os.Getenv("WXWORK_SUITE_ID"),
		SuiteSecret: os.Getenv("WXWORK_SUITE_SECRET"),
	}

	got, err := c.AddKfAccount(os.Getenv("WXWORK_ACCESS_TOKEN"), "测试客服", os.Getenv("WXWORK_MEDIA_ID"))
	assert.NoError(t, err)
	assert.NotEmpty(t, got)
	t.Logf("AddContactWay: %+v", got)
}

// Test_client_MediaUpload
func Test_client_MediaUpload(t *testing.T) {
	var c = &client{
		Host:        DefaultHost,
		SuiteId:     os.Getenv("WXWORK_SUITE_ID"),
		SuiteSecret: os.Getenv("WXWORK_SUITE_SECRET"),
	}

	got, err := c.UploadMedia(os.Getenv("WXWORK_ACCESS_TOKEN"), "image",
		"../../media/test.png")
	assert.NoError(t, err)
	assert.NotEmpty(t, got)
	t.Logf("MediaID: %+v", got)
}

// Test_client_ListCustomerAcquisition
func Test_client_ListCustomerAcquisition(t *testing.T) {
	var c = &client{
		Host:        DefaultHost,
		SuiteId:     os.Getenv("WXWORK_SUITE_ID"),
		SuiteSecret: os.Getenv("WXWORK_SUITE_SECRET"),
	}

	got, next, err := c.ListCustomerAcquisition(os.Getenv("WXWORK_ACCESS_TOKEN"), "", 100)

	assert.NotEmpty(t, next)
	assert.NoError(t, err)
	assert.NotEmpty(t, got)
	t.Logf("CustomerAcquisition: %+v", got)
}

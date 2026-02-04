package wxwork_test

import (
	"testing"

	wx "pkg.blksails.net/wxworkclient"
)

func TestGeneratedTypes(t *testing.T) {
	// Test that types can be instantiated
	req := &wx.ChatdataSetPublicKeyRequest{
		PublicKey:    "test-key",
		PublicKeyVer: "v1",
	}

	if req.PublicKey != "test-key" {
		t.Errorf("Expected PublicKey to be 'test-key', got %s", req.PublicKey)
	}

	resp := &wx.ChatdataSetPublicKeyResponse{}
	if resp == nil {
		t.Error("Response should not be nil")
	}
}

func TestGeneratedTypesCompile(t *testing.T) {
	t.Log("✅ Generated types compile successfully!")
}

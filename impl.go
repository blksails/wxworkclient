package wxwork

import (
	"bytes"
	"encoding/json"
	"io/ioutil"
	"log"
	"mime/multipart"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
	"reflect"
)

type installable interface {
	install(c *client)
}

type impls struct {
	inited                       bool
	SuiteAccessToken             impl[SuiteRequest, SuiteResponse]
	GetPermanentCode             impl[GetPermanentRequest, AuthCorpResponse]
	GetPreAuthCode               impl[GetPreAuthCodeRequest, GetPreAuthCodeResponse]
	GetAuthInfo                  impl[GetAuthInfoRequest, AuthCorpResponse]
	GetUserInfo                  impl[GetUserInfoRequest, GetUserInfoResponse]
	GetJSAPITicket               impl[GetJSAPITicketRequest, GetJSAPITicketResponse]
	GetUser                      impl[GetUserRequest, GetUserResponse]
	GetUserDetail                impl[GetUserDetailRequest, GetUserDetailResponse]
	GetCorpToken                 impl[GetCorpTokenRequest, GetCorpTokenResponse]
	UploadMedia                  implUpload[UploadMediaRequest, UploadMediaResponse]
	AddKfAccount                 impl[AddKfAccountRequest, AddKfAccountResponse]
	ListKFAccounts               impl[ListKFRequest, ListKFResponse]
	UpdateKfAccount              impl[UpdateKfAccountRequest, UpdateKfAccountResponse]
	DeleteKfAccount              impl[DeleteKfAccountRequest, DeleteKfAccountResponse]
	GetAccessToken               impl[GetAccessTokenRequest, GetAccessTokenResponse]
	AddContactWay                impl[KfContactWayRequest, KfContactWayResponse]
	KfServiceState               impl[KfServiceStateRequest, KfServiceStateResponse]
	KfSyncMsg                    impl[KfSyncMsgRequest, KfSyncMsgResponse]
	KfSendMsg                    impl[KfSendMsgRequest, KfSendMsgResponse]
	KfSendOnEvent                impl[KfSendOnEventRequest, KfSendOnEventResponse]
	ListCustomerAcquisition      impl[ListCustomerAcquisitionRequest, ListCustomerAcquisitionResponse]
	ListCustomerAcquisitionLinks impl[ListCustomerAcquisitionRequest, ListCustomerAcquisitionLinksResponse]
	CreateCustomerAcquisition    impl[CreateCustomerAcquisitionRequest, CreateCustomerAcquisitionResponse]
	DeleteCustomerAcquisition    impl[DeleteCustomerAcquisitionRequest, DeleteCustomerAcquisitionResponse]
	UpdateCustomerAcquisition    impl[UpdateCustomerAcquisitionRequest, UpdateCustomerAcquisitionResponse]
	FollowUsers                  impl[FollowUsersRequest, FollowUsersResponse]
	DepartmentList               impl[DepartmentListRequest, DepartmentListResponse]
	DepartmentUserList           impl[DepartmentUserListRequest, DepartmentUserListResponse]
	AddCustomers                 impl[AddCustomersRequest, AddCustomersResponse]
	GetUserIds                   impl[GetUserIdsRequest, GetUserIdsResponse]
	SendAppMessage               impl[AppMessage, AppMessageResponse]
	GetCustomerInfo              impl[GetCustomerInfoRequest, GetCustomerInfoResponse]
	UnionidToExternalUserid      impl[UnionidToExternalUseridRequest, UnionidToExternalUseridResponse]
	GetNewExternalUserid         impl[GetNewExternalUseridRequest, GetNewExternalUseridResponse]
}

var installType = reflect.TypeOf((*installable)(nil)).Elem()

// installAll
func (imp *impls) installAll(c *client) {
	if imp.inited {
		return
	}

	var v = reflect.ValueOf(imp)
	v = reflect.Indirect(v)
	for i := 0; i < v.NumField(); i++ {
		var (
			f = v.Field(i)
			t = f.Type()
		)

		// if f impl installable then call install
		if t.Implements(installType) {
			f.Interface().(installable).install(c)
		}

		if f.Addr().Type().Implements(installType) {
			f.Addr().Interface().(installable).install(c)
		}
	}

	imp.inited = true
}

type handleError func(error) (any, error)

type impl[R any, Q Response] struct {
	client *client
}

// Do 执行请求
func (impl *impl[R, Q]) Do(method string, uri string, body *R, query ...url.Values) (resp *Q, err error) {
	var (
		urlpath    = impl.client.getUrl(uri)
		httpClient http.Client
		b          bytes.Buffer
		enc        = json.NewEncoder(&b)
		req        *http.Request
		q          url.Values
	)

	if err = enc.Encode(body); err != nil {
		return
	}

	if len(query) > 0 {
		q = query[0]
	}

	if impl.client.Debug {
		q.Set("debug", "1")
	}

	urlpath = impl.addQuery(urlpath, q)

	log.Printf("wxwork api request %s: %s", http.MethodPost, urlpath)
	req, err = http.NewRequest(http.MethodPost, urlpath, &b)
	if err != nil {
		return
	}

	req.Header.Set("Content-Type", "application/json")
	resp1, err := httpClient.Do(req)
	if err != nil {
		return
	}
	bb, err := httputil.DumpResponse(resp1, true)
	if err != nil {
		return nil, err
	}
	log.Printf("wxwork api response %s", string(bb))
	resp = new(Q)
	if err = json.NewDecoder(resp1.Body).Decode(resp); err != nil {
		return
	}

	if err = (*resp).Err(); err != nil {
		return nil, err
	}

	return
}

// concatQuery
func (impl *impl[R, Q]) addQuery(urlpath string, query url.Values) string {
	u, err := url.Parse(urlpath)
	if err != nil {
		panic(err)
	}
	u.RawQuery = query.Encode()
	return u.String()
}

// install
func (impl *impl[R, Q]) install(c *client) {
	impl.client = c
}

type implUpload[R any, Q Response] struct {
	client *client
}

// Do 执行请求
func (impl *implUpload[R, Q]) Do(uri string, params map[string]string, paramName, path string, query ...url.Values) (resp *Q, err error) {
	var (
		urlpath    = impl.client.getUrl(uri)
		httpClient http.Client
		req        *http.Request
	)

	if len(query) > 0 {
		urlpath = impl.addQuery(urlpath, query[0])
	}

	req, err = newfileUploadRequest(urlpath, params, paramName, path)
	if err != nil {
		return
	}

	req.Header.Set("Content-Type", "multipart/form-data")

	resp1, err := httpClient.Do(req)
	if err != nil {
		return
	}

	resp = new(Q)
	if err = json.NewDecoder(resp1.Body).Decode(resp); err != nil {
		return
	}

	if err = (*resp).Err(); err != nil {
		return nil, err
	}

	return
}

// concatQuery
func (impl *implUpload[R, Q]) addQuery(urlpath string, query url.Values) string {
	u, err := url.Parse(urlpath)
	if err != nil {
		panic(err)
	}
	u.RawQuery = query.Encode()
	return u.String()
}

// install
func (impl *implUpload[R, Q]) install(c *client) {
	impl.client = c
}

func newfileUploadRequest(uri string, params map[string]string, paramName, path string) (*http.Request, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	fileContents, err := ioutil.ReadAll(file)
	if err != nil {
		return nil, err
	}
	fi, err := file.Stat()
	if err != nil {
		return nil, err
	}
	file.Close()

	body := new(bytes.Buffer)
	writer := multipart.NewWriter(body)
	part, err := writer.CreateFormFile(paramName, fi.Name())
	if err != nil {
		return nil, err
	}
	part.Write(fileContents)

	for key, val := range params {
		_ = writer.WriteField(key, val)
	}
	err = writer.Close()
	if err != nil {
		return nil, err
	}

	return http.NewRequest("POST", uri, body)
}

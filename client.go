package wxwork

import (
	"errors"
	"net/url"
	"os"
	"strconv"
	"time"

	"github.com/akrennmair/slice"
	"github.com/spf13/viper"
	"go.uber.org/multierr"
	"pkg.blksails.net/kf/utils"
)

var DefaultHost = "https://qyapi.weixin.qq.com"

type Client interface {
	SuiteAccessToken(ticket string) (string, int64, error)
	GetPermanentCode(suiteAccessToken string, authCode string) (*AuthCorpResponse, error)
	GetAuthInfo(suiteAccessToken string, authCorpId string, permanent_code string) (*AuthCorpResponse, error)
	GetPreAuthCode(suiteAccessToken string) (string, int64, error)
	GetCorpToken(suiteAccessToken string, authCorpId string, permanentCode string) (string, int64, error)
	GetUserInfo(accessToken string, code string) (*UserInfo, *ExtUserInfo, error)
	GetUserDetail(accessToken string, userTicket string) (*GetUserDetailResponse, error)
	GetUser(accessToken string, userid string) (*GetUserResponse, error)
	GetAccessToken(corpid string, corpSecret string) (string, int64, error)
	UploadMedia(accessToken string, mediaType string, filename string) (*UploadMediaResponse, error)
	AddKfAccount(accessToken string, name string, media_id string) (string, error)
	ListKFAccounts(accessToken string, offset int64, limit int64) ([]AccountList, error)
	UpdateKfAccount(accessToken string, openKfid string, name string, media_id string) error
	DeteteKfAccount(accessToken string, openKfid string) error
	AddContactWay(accessToken string, kdif string, scene string) (string, error)
	KfSyncMsg(accessToken string, openKfid string, token string, cursor string, limit int64) (*MessagesResponse, error)
	KfSendMsg(accessToken string, openKfid string, externalUserId string, msgType string, payload MsgPayload) (string, error)
	KfSendMsgText(accessToken string, openKfid string, externalUserId string, text string) (string, error)
	KfSendMsgCaLink(accessToken string, openKfid string, externalUserId string, linkURL string) (string, error)
	KfSendOnEventText(accessToken string, code string, msgId string, text string) (string, error)
	KfSendOnEventMenu(accessToken string, code string, msgId string, menu *Msgmenu) (string, error)
	ListCustomerAcquisition(accessToken string, cursor string, limit int64) ([]string, string, error)
	ListCustomerAcquisitionLinks(accessToken string, limit int64, cursor string) (*ListCustomerAcquisitionLinksResponse, error)
	CreateCustomerAcquisition(accessToken string, linkName string, userIds []string, departs []int64) (AcquisitionLink, error)
	UpdateCustomerAcquisition(accessToken string, linkId string, linkName string, userIds []string, departs []int64) error
	FollowUsers(accessToken string) ([]string, error)
	DepartmentList(accessToken string, departmentId int64) ([]Department, error)
	DepartmentUserList(accessToken string, departmentId int64, cursor string) ([]User, error)
	AddCustomersList(accessToken string, linkId string, limit int64, cursor string) ([]Customer, string, error)
	GetUserIds(accessToken string, cursor string) ([]DeptUser, string, error)
	SendAppMessage(accessToken string, payload *AppMessage) (*AppMessageResponse, error)
	GetJSTicket(accessToken string) (string, int64, error)
	GetCustomerInfo(accessToken string, externalUserIds []string) (*GetCustomerInfoResponse, error)
	UnionidToExternalUserid(accessToken string, unionid string, openid string) (*UnionidToExternalUseridResponse, error)
	GetNewExternalUserid(accessToken string, externalUseridList []string) (*GetNewExternalUseridResponse, error)
}

type Config struct {
	// CorpId         string
	// ProviderSecret string
	SuiteId     string
	SuiteSecret string
	SuiteToken  string
	SuiteAesKey string
	Debug       bool
}

type client struct {
	Host        string
	SuiteId     string
	SuiteSecret string
	Debug       bool

	imp          impls
	expireHandle func(corpId string) string
}

// New 创建客户端
func New(cfg Config) Client {
	c := &client{
		Host:        utils.Default(viper.GetString("wxwork.host"), os.Getenv("WXWORK_HOST"), DefaultHost),
		SuiteId:     cfg.SuiteId,
		SuiteSecret: cfg.SuiteSecret,
		Debug:       cfg.Debug,
	}

	c.init()
	return c
}

type MsgPayload interface {
	isMsgPayload()
}

// init
func (c *client) init() *client {
	c.imp.installAll(c)
	return c
}

func (c *client) GetAuthInfo(suiteAccessToken string, authCorpId string, permanentCode string) (*AuthCorpResponse, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("suite_access_token", suiteAccessToken)

	return c.imp.GetAuthInfo.Do("POST", "/cgi-bin/service/get_auth_info", &GetAuthInfoRequest{
		AuthCorpid:    authCorpId,
		PermanentCode: permanentCode,
	}, query)
}

func (c *client) GetPermanentCode(suiteAccessToken string, authCode string) (*AuthCorpResponse, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("suite_access_token", suiteAccessToken)
	return c.imp.GetPermanentCode.Do("POST", "/cgi-bin/service/get_permanent_code", &GetPermanentRequest{
		AuthCode: authCode,
	}, query)
}

// GetPreAuthCode 获取预授权码
func (c *client) GetPreAuthCode(suiteAccessToken string) (string, int64, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("suite_access_token", suiteAccessToken)

	resp, err := c.imp.GetPreAuthCode.Do("GET", "/cgi-bin/service/get_pre_auth_code", &GetPreAuthCodeRequest{}, query)
	if err != nil {
		return "", 0, err
	}

	return resp.PreAuthCode, resp.ExpiresIn, nil
}

// GetUserInfo
func (c *client) GetUserInfo(accessToken string, code string) (*UserInfo, *ExtUserInfo, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)
	query.Add("code", code)

	resp, err := c.imp.GetUserInfo.Do("GET", "/cgi-bin/auth/getuserinfo", &GetUserInfoRequest{}, query)
	if err != nil {
		return nil, nil, err
	}

	if resp.Userid != "" {
		var userDetail GetUserDetailResponse
		user, err := c.GetUser(accessToken, resp.Userid)
		if err != nil {
			return nil, nil, err
		}

		if resp.UserTicket != "" {
			_userDetail, err := c.GetUserDetail(accessToken, resp.UserTicket)
			if err != nil {
				return nil, nil, err
			}
			userDetail = *_userDetail
		}

		return &UserInfo{
			Userid:           resp.Userid,
			UserTicket:       resp.UserTicket,
			Name:             user.Name,
			Department:       user.Department,
			Order:            user.Order,
			Position:         user.Position,
			Mobile:           utils.Default(user.Mobile, userDetail.Mobile),
			Gender:           utils.Default(user.Gender, userDetail.Gender),
			Email:            utils.Default(user.Email, userDetail.Email),
			BizMail:          utils.Default(user.BizMail, userDetail.BizMail),
			IsLeaderInDept:   user.IsLeaderInDept,
			DirectLeader:     user.DirectLeader,
			Avatar:           utils.Default(user.Avatar, userDetail.Avatar),
			ThumbAvatar:      user.ThumbAvatar,
			Telephone:        user.Telephone,
			Alias:            user.Alias,
			Address:          utils.Default(user.Address, userDetail.Address),
			OpenUserid:       user.OpenUserid,
			MainDepartment:   user.MainDepartment,
			Extattr:          user.Extattr,
			Status:           user.Status,
			QrCode:           utils.Default(user.QrCode, userDetail.QrCode),
			ExternalPosition: user.ExternalPosition,
			ExternalProfile:  user.ExternalProfile,
		}, nil, nil
	} else if resp.Openid != "" {
		return nil, &ExtUserInfo{
			Openid:         resp.Openid,
			ExternalUserid: resp.ExternalUserid,
		}, nil
	} else {
		return nil, nil, errors.New("invalid response")
	}
}

// GetUser
func (c *client) GetUser(accessToken string, userid string) (*GetUserResponse, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)
	query.Add("userid", userid)

	return c.imp.GetUser.Do("GET", "/cgi-bin/user/get", &GetUserRequest{}, query)
}

// GetUserDetail
func (c *client) GetUserDetail(accessToken string, userTicket string) (*GetUserDetailResponse, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)

	return c.imp.GetUserDetail.Do("POST", "/cgi-bin/auth/getuserdetail", &GetUserDetailRequest{
		UserTicket: userTicket,
	}, query)
}

// GetCorpToken 获取企业微信access_token
func (c *client) GetCorpToken(suiteAccessToken string, authCorpId string, permanentCode string) (string, int64, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("suite_access_token", suiteAccessToken)

	resp, err := c.imp.GetCorpToken.Do("POST", "/cgi-bin/service/get_corp_token", &GetCorpTokenRequest{
		AuthCorpid:    authCorpId,
		PermanentCode: permanentCode,
	}, query)
	if err != nil {
		return "", 0, err
	}

	return resp.AccessToken, resp.ExpiresIn, nil
}

func (c *client) SuiteAccessToken(ticket string) (string, int64, error) {
	c.imp.installAll(c)

	resp, err := c.imp.SuiteAccessToken.Do("POST", "/cgi-bin/service/get_suite_token", &SuiteRequest{
		SuiteID:     c.SuiteId,
		SuiteSecret: c.SuiteSecret,
		SuiteTicket: ticket,
	})

	if err != nil {
		return "", 0, err
	}

	return resp.SuiteAccessToken, int64(resp.ExpiresIn), nil
}

// GetAccessToken 获取企业微信access_token
func (c *client) GetAccessToken(corpid string, corpSecret string) (string, int64, error) {
	c.imp.installAll(c)
	query := url.Values{}
	query.Add("corpid", corpid)
	query.Add("corpsecret", corpSecret)

	resp, err := c.imp.GetAccessToken.Do("GET", "/cgi-bin/gettoken", &GetAccessTokenRequest{}, query)
	if err != nil {
		return "", 0, err
	}

	return resp.AccessToken, resp.ExpiresIn, nil
}

// ListKFAccounts 获取客服列表
func (c *client) ListKFAccounts(accessToken string, offset int64, limit int64) ([]AccountList, error) {
	c.imp.installAll(c)
	query := url.Values{}
	query.Add("access_token", accessToken)
	resp, err := c.imp.ListKFAccounts.Do("POST", "/cgi-bin/kf/account/list", &ListKFRequest{
		Offset: offset,
		Limit:  limit,
	}, query)

	if err != nil {
		return nil, err
	}

	return resp.AccountList, nil
}

// AddContactWay 添加企业微信客服联系方式
func (c *client) AddContactWay(accessToken string, kdif string, scene string) (string, error) {
	c.imp.installAll(c)
	query := url.Values{}

	query.Add("access_token", accessToken)
	resp, err := c.imp.AddContactWay.Do("POST", "/cgi-bin/kf/add_contact_way", &KfContactWayRequest{
		OpenKfid: kdif,
		Scene:    scene,
	}, query)
	if err != nil {
		return "", err
	}

	return resp.URL, nil
}

// KfServiceState 获取企业微信客服状态
func (c *client) KfServiceState(accessToken string, openKfid string, externalUserId string) (*KfServiceStateResponse, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)
	return c.imp.KfServiceState.Do("POST", "/cgi-bin/kf/service_state/get", &KfServiceStateRequest{
		OpenKfid:       openKfid,
		ExternalUserid: externalUserId,
	}, query)
}

// AddKfAccount 添加企业微信客服账号
func (c *client) AddKfAccount(accessToken string, name string, media_id string) (string, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)
	resp, err := c.imp.AddKfAccount.Do("POST", "/cgi-bin/kf/account/add", &AddKfAccountRequest{
		Name:    name,
		MediaID: media_id,
	}, query)
	if err != nil {
		return "", err
	}
	return resp.OpenKfid, nil
}

// KfSyncMsg 同步企业微信客服消息
func (c *client) KfSyncMsg(accessToken string, openKfid string, token string, cursor string, limit int64) (*MessagesResponse, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)
	resp, err := c.imp.KfSyncMsg.Do("POST", "/cgi-bin/kf/sync_msg", &KfSyncMsgRequest{
		Cursor:      cursor,
		Token:       token,
		Limit:       limit,
		VoiceFormat: 0,
		OpenKfid:    openKfid,
	}, query)

	if err != nil {
		return nil, err
	}

	return &MessagesResponse{
		CommonResponse: resp.CommonResponse,
		NextCursor:     resp.NextCursor,
		HasMore:        resp.HasMore,
		MsgList:        resp.MsgList,
	}, nil
}

// KfSendMsg 发送企业微信客服消息
func (c *client) KfSendMsg(accessToken string, openKfid string, externalUserId string, msgType string, payload MsgPayload) (string, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)
	req := &KfSendMsgRequest{
		Touser:   externalUserId,
		OpenKfid: openKfid,
		Msgtype:  msgType,
	}

	req.SetPayload(msgType, payload)

	resp, err := c.imp.KfSendMsg.Do("POST", "/cgi-bin/kf/send_msg", req, query)
	if err != nil {
		return "", err
	}

	return resp.Msgid, nil
}

// KfSendMsgText 发送文本消息
func (c *client) KfSendMsgText(accessToken string, openKfid string, externalUserId string, text string) (string, error) {
	return c.KfSendMsg(accessToken, openKfid, externalUserId, "text", &Text{
		Content: text,
	})
}

// KfSendMsgCaLink 发送获客链接消息
func (c *client) KfSendMsgCaLink(accessToken string, openKfid string, externalUserId string, linkURL string) (string, error) {
	return c.KfSendMsg(accessToken, openKfid, externalUserId, "ca_link", &CaLink{
		LinkURL: linkURL,
	})
}

// ListCustomerAcquisitionLinks 获取获客链接列表
func (c *client) ListCustomerAcquisitionLinks(accessToken string, limit int64, cursor string) (*ListCustomerAcquisitionLinksResponse, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)

	req := &ListCustomerAcquisitionRequest{
		Limit:  limit,
		Cursor: cursor,
	}

	resp, err := c.imp.ListCustomerAcquisitionLinks.Do("POST", "/cgi-bin/externalcontact/customer_acquisition/list", req, query)
	if err != nil {
		return nil, err
	}

	return resp, nil
}

// KfSendOnEvent 发送事件消息
func (c *client) KfSendOnEventText(accessToken string, code string, msgId string, text string) (string, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)
	req := &KfSendOnEventRequest{
		Code:    code,
		Msgid:   msgId,
		Msgtype: "text",
		Text: &Text{
			Content: text,
		},
	}

	resp, err := c.imp.KfSendOnEvent.Do("POST", "/cgi-bin/kf/send_msg_on_event", req, query)
	if err != nil {
		return "", err
	}

	return resp.Msgid, nil
}

// KfSendOnEventMenu
func (c *client) KfSendOnEventMenu(accessToken string, code string, msgId string, menu *Msgmenu) (string, error) {
	c.imp.installAll(c)
	query := url.Values{}
	query.Add("access_token", accessToken)
	req := &KfSendOnEventRequest{
		Code:    code,
		Msgid:   msgId,
		Msgtype: "msgmenu",
		Msgmenu: menu,
	}

	resp, err := c.imp.KfSendOnEvent.Do("POST", "/cgi-bin/kf/send_msg_on_event", req, query)
	if err != nil {
		return "", err
	}

	return resp.Msgid, nil
}

// UploadMedia 上传临时素材
func (c *client) UploadMedia(accessToken string, mediaType string, filename string) (*UploadMediaResponse, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)
	query.Add("type", mediaType)

	resp, err := c.imp.UploadMedia.Do("/cgi-bin/media/upload", map[string]string{}, "media", filename, query)
	if err != nil {
		return nil, err
	}

	if err != nil {
		return nil, err
	}

	return &UploadMediaResponse{
		CommonResponse: resp.CommonResponse,
		MediaID:        resp.MediaID,
		CreatedAt:      resp.CreatedAt,
	}, nil

}

// UpdateKfAccount 更新客服账号
func (c *client) UpdateKfAccount(accessToken string, openKfid string, name string, media_id string) error {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)
	_, err := c.imp.UpdateKfAccount.Do("POST", "/cgi-bin/kf/account/update", &UpdateKfAccountRequest{
		OpenKfid: openKfid,
		Name:     name,
		MediaID:  media_id,
	}, query)
	if err != nil {
		return err
	}
	return nil
}

// DeteteKfAccount 删除客服账号
func (c *client) DeteteKfAccount(accessToken string, openKfid string) error {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)

	_, err := c.imp.DeleteKfAccount.Do("POST", "/cgi-bin/kf/account/del", &DeleteKfAccountRequest{
		OpenKfid: openKfid,
	}, query)
	return err
}

// ListCustomerAcquisition 获取客户列表
func (c *client) ListCustomerAcquisition(accessToken string, cursor string, limit int64) ([]string, string, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)

	resp, err := c.imp.ListCustomerAcquisition.Do("POST",
		"/cgi-bin/externalcontact/customer_acquisition/list_link",
		&ListCustomerAcquisitionRequest{
			Cursor: cursor,
			Limit:  limit,
		}, query)
	if err != nil {
		return nil, "", err
	}

	return resp.LinkIDList, resp.NextCursor, nil
}

// CreateCustomerAcquisition 创建客户
func (c *client) CreateCustomerAcquisition(accessToken string, linkName string, userIds []string, departs []int64) (AcquisitionLink, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)

	resp, err := c.imp.CreateCustomerAcquisition.Do("POST",
		"/cgi-bin/externalcontact/customer_acquisition/create_link",
		&CreateCustomerAcquisitionRequest{
			LinkName: linkName,
			Range: Range{
				UserList:       userIds,
				DepartmentList: departs,
			},
			SkipVerify: true,
		}, query)
	if err != nil {
		return AcquisitionLink{}, err
	}

	return AcquisitionLink{
		LinkID:     resp.Link.LinkID,
		LinkName:   resp.Link.LinkName,
		URL:        resp.Link.URL,
		CreateTime: resp.Link.CreateTime,
	}, nil
}

// UpdateCustomerAcquisition 更新客户
func (c *client) UpdateCustomerAcquisition(accessToken string, linkId string, linkName string, userIds []string, departs []int64) error {
	c.imp.installAll(c)
	query := url.Values{}
	query.Add("access_token", accessToken)

	_, err := c.imp.UpdateCustomerAcquisition.Do("POST",
		"/cgi-bin/externalcontact/customer_acquisition/update_link",
		&UpdateCustomerAcquisitionRequest{
			LinkID:   linkId,
			LinkName: linkName,
			Range: Range{
				UserList:       userIds,
				DepartmentList: departs,
			},
		}, query)
	if err != nil {
		return err
	}

	return nil
}

// FollowUsers
func (c *client) FollowUsers(accessToken string) ([]string, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)

	resp, err := c.imp.FollowUsers.Do("GET",
		"/cgi-bin/externalcontact/get_follow_user_list",
		&FollowUsersRequest{}, query)
	if err != nil {
		return nil, err
	}

	return resp.FollowUser, nil
}

// DepartmentList 获取部门列表
func (c *client) DepartmentList(accessToken string, departmentId int64) ([]Department, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)
	if departmentId > 0 {
		query.Add("id", strconv.FormatInt(departmentId, 10))
	}

	resp, err := c.imp.DepartmentList.Do("GET",
		"/cgi-bin/department/list",
		&DepartmentListRequest{}, query)
	if err != nil {
		return nil, err
	}

	departs := slice.Map(resp.Department, func(dep Department) Department {
		return Department{
			ID:               dep.ID,
			Name:             dep.Name,
			NameEn:           dep.NameEn,
			DepartmentLeader: dep.DepartmentLeader,
			Parentid:         dep.Parentid,
			Order:            dep.Order,
		}
	})

	return departs, nil
}

// DepartmentUserList 获取部门用户列表
func (c *client) DepartmentUserList(accessToken string, departmentId int64, cursor string) ([]User, error) {
	c.imp.installAll(c)

	departs, err := c.DepartmentList(accessToken, departmentId)
	if err != nil {
		return nil, err
	}

	query := url.Values{}
	query.Add("access_token", accessToken)

	var (
		users []User
		errs  error
	)
	for _, dep := range departs {
		query.Set("department_id", strconv.FormatInt(dep.ID, 10))

		resp, err := c.imp.DepartmentUserList.Do("GET",
			"/cgi-bin/user/simplelist",
			&DepartmentUserListRequest{},
			query)
		if err != nil {
			return nil, err
		}

		for _, user := range resp.UserList {
			userResp, err := c.GetUser(accessToken, user.Userid)
			if err != nil {
				errs = multierr.Append(errs, err)
				continue
			}
			users = append(users, User{
				Userid:           user.Userid,
				Name:             user.Name,
				Department:       userResp.Department,
				Order:            userResp.Order,
				Position:         userResp.Position,
				Mobile:           userResp.Mobile,
				Gender:           userResp.Gender,
				Email:            userResp.Email,
				BizMail:          userResp.BizMail,
				IsLeaderInDept:   userResp.IsLeaderInDept,
				DirectLeader:     userResp.DirectLeader,
				Avatar:           userResp.Avatar,
				ThumbAvatar:      userResp.ThumbAvatar,
				Telephone:        userResp.Telephone,
				Alias:            userResp.Alias,
				Address:          userResp.Address,
				OpenUserid:       userResp.OpenUserid,
				MainDepartment:   userResp.MainDepartment,
				Extattr:          userResp.Extattr,
				Status:           userResp.Status,
				QrCode:           userResp.QrCode,
				ExternalPosition: userResp.ExternalPosition,
				ExternalProfile:  userResp.ExternalProfile,
			})
		}
	}

	return users, nil
}

// AddCustomersList 添加客户
func (c *client) AddCustomersList(accessToken string, linkId string, limit int64, cursor string) ([]Customer, string, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)

	resp, err := c.imp.AddCustomers.Do("POST",
		"/cgi-bin/externalcontact/customer_acquisition/customer",
		&AddCustomersRequest{
			LinkID: linkId,
			Limit:  limit,
			Cursor: cursor,
		}, query)
	if err != nil {
		return nil, "", err
	}

	customers := slice.Map(resp.CustomerList, func(cust CustomerList) Customer {
		return Customer{
			ExternalUserid: cust.ExternalUserid,
			Userid:         cust.Userid,
			ChatStatus:     cust.ChatStatus,
			State:          cust.State,
		}
	})
	return customers, resp.NextCursor, nil
}

// GetUserIds
func (c *client) GetUserIds(accessToken string, cursor string) ([]DeptUser, string, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)

	resp, err := c.imp.GetUserIds.Do("POST",
		"/cgi-bin/user/list_id",
		&GetUserIdsRequest{
			Cursor: cursor,
		}, query)
	if err != nil {
		return nil, "", err
	}

	return resp.DeptUser, resp.NextCursor, nil
}

// SendAppMessage 发送应用消息
func (c *client) SendAppMessage(accessToken string, payload *AppMessage) (*AppMessageResponse, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)

	resp, err := c.imp.SendAppMessage.Do("POST",
		"/cgi-bin/message/send",
		payload, query)
	if err != nil {
		return nil, err
	}

	return resp, nil
}

// GetJSTicket 获取jsapi_ticket
func (c *client) GetJSTicket(accessToken string) (string, int64, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)
	resp, err := c.imp.GetJSAPITicket.Do("GET", "/cgi-bin/get_jsapi_ticket", &GetJSAPITicketRequest{}, query)
	if err != nil {
		return "", 0, err
	}

	return resp.Ticket, resp.ExpiresIn, nil
}

// GetCustomerInfo 获取客户基础信息
func (c *client) GetCustomerInfo(accessToken string, externalUserIds []string) (*GetCustomerInfoResponse, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)

	resp, err := c.imp.GetCustomerInfo.Do("POST", "/cgi-bin/kf/customer/batchget", &GetCustomerInfoRequest{
		ExternalUseridList: externalUserIds,
	}, query)
	if err != nil {
		return nil, err
	}

	return resp, nil
}

// UnionidToExternalUserid 将unionid转换为服务商主体下的external_userid
func (c *client) UnionidToExternalUserid(accessToken string, unionid string, openid string) (*UnionidToExternalUseridResponse, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)

	resp, err := c.imp.UnionidToExternalUserid.Do("POST", "/cgi-bin/idconvert/unionid_to_external_userid", &UnionidToExternalUseridRequest{
		Unionid:     unionid,
		Openid:      openid,
		SubjectType: 1, // 1表示服务商主体
	}, query)
	if err != nil {
		return nil, err
	}

	return resp, nil
}

// GetNewExternalUserid 将旧的external_userid转换为新的external_userid（批量）
func (c *client) GetNewExternalUserid(accessToken string, externalUseridList []string) (*GetNewExternalUseridResponse, error) {
	c.imp.installAll(c)

	query := url.Values{}
	query.Add("access_token", accessToken)

	resp, err := c.imp.GetNewExternalUserid.Do("POST", "/cgi-bin/externalcontact/get_new_external_userid", &GetNewExternalUseridRequest{
		ExternalUseridList: externalUseridList,
	}, query)
	if err != nil {
		return nil, err
	}

	return resp, nil
}

// getUrl 获取请求地址
func (c *client) getUrl(path string) string {
	p, err := url.JoinPath(c.Host, path)
	if err != nil {
		panic(err)
	}

	return p
}

// HandleTokenExpired 处理token过期
func (c *client) HandleTokenExpired(fn func(corpId string) string) {
	c.expireHandle = fn
}

// HandleTokenExpired 处理token过期
func (c *client) handleTokenExpired(corpId string) string {
	if c.expireHandle != nil {
		return c.expireHandle(corpId)
	}

	return ""
}

func parseDuration(expireIn int) time.Duration {
	return time.Duration(expireIn) * time.Second
}

const MAX_RETRY = 3

func retryAccessToken[Resp any](c *client, corpId string, fn func(accessToken string) (Resp, error)) func(string) (Resp, error) {
	return func(accessToken string) (q Resp, e error) {
		for i := 0; i < MAX_RETRY; i++ {
			resp, err := fn(accessToken)
			if err != nil {
				if errs, ok := err.(*RespError); ok && errs.Errcode == 42001 {
					accessToken = c.handleTokenExpired(corpId)
					continue
				}
			}
			return resp, nil
		}

		e = errors.New("out of max retry")
		return
	}
}

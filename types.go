package wxwork

type Response interface {
	Err() error
}

type CommonResponse struct {
	Errcode int    `json:"errcode"`
	Errmsg  string `json:"errmsg"`
}

type RespError struct {
	Errcode int    `json:"errcode"`
	Errmsg  string `json:"errmsg"`
}

type AuthCorpResponse struct {
	CommonResponse
	AccessToken    string `json:"access_token"`
	ExpiresIn      int64  `json:"expires_in"`
	PermanentCode  string `json:"permanent_code"`
	DealerCorpInfo struct {
		Corpid   string `json:"corpid"`
		CorpName string `json:"corp_name"`
	} `json:"dealer_corp_info"`
	AuthCorpInfo struct {
		Corpid            string `json:"corpid"`
		CorpName          string `json:"corp_name"`
		CorpType          string `json:"corp_type"`
		CorpSquareLogoURL string `json:"corp_square_logo_url"`
		CorpRoundLogoURL  string `json:"corp_round_logo_url"`
		CorpUserMax       int    `json:"corp_user_max"`
		CorpFullName      string `json:"corp_full_name"`
		VerifiedEndTime   int    `json:"verified_end_time"`
		SubjectType       int    `json:"subject_type"`
		CorpWxqrcode      string `json:"corp_wxqrcode"`
		CorpScale         string `json:"corp_scale"`
		CorpIndustry      string `json:"corp_industry"`
		CorpSubIndustry   string `json:"corp_sub_industry"`
		Location          string `json:"location"`
	} `json:"auth_corp_info"`
	AuthInfo struct {
		Agent []AuthAgent `json:"agent"`
	} `json:"auth_info"`
	AuthUserInfo struct {
		Userid     string `json:"userid"`
		OpenUserid string `json:"open_userid"`
		Name       string `json:"name"`
		Avatar     string `json:"avatar"`
	} `json:"auth_user_info"`
	State string `json:"state"`
}

type AuthAgent struct {
	Agentid          int    `json:"agentid"`
	Name             string `json:"name"`
	RoundLogoURL     string `json:"round_logo_url"`
	SquareLogoURL    string `json:"square_logo_url"`
	AuthMode         int    `json:"auth_mode"`
	IsCustomizedApp  bool   `json:"is_customized_app"`
	AuthFromThirdapp bool   `json:"auth_from_thirdapp"`
	Privilege        struct {
		Level      int      `json:"level"`
		AllowParty []int    `json:"allow_party"`
		AllowUser  []string `json:"allow_user"`
		AllowTag   []int    `json:"allow_tag"`
	} `json:"privilege"`
	SharedFrom struct {
		Corpid    string `json:"corpid"`
		ShareType int    `json:"share_type"`
	} `json:"shared_from"`
}

type TextOrMenuPayload interface {
	TextPayload
}

type MenuPayload interface {
	isMenu()
}

type TextPayload interface {
	isText()
}

type MessagesResponse struct {
	CommonResponse

	NextCursor string    `json:"next_cursor"`
	HasMore    int64     `json:"has_more"`
	MsgList    []MsgList `json:"msg_list"`
}

// Err implement error interface
func (r CommonResponse) Err() error {
	if r.Errcode == 0 {
		return nil
	}

	return &RespError{
		Errcode: r.Errcode,
		Errmsg:  r.Errmsg,
	}
}

// Error
func (r *RespError) Error() string {
	return r.Errmsg
}

type MsgList struct {
	Msgid          string        `json:"msgid"`
	OpenKfid       string        `json:"open_kfid"`
	ExternalUserid string        `json:"external_userid"`
	SendTime       int64         `json:"send_time"`
	Origin         int64         `json:"origin"`
	Msgtype        string        `json:"msgtype"`
	Text           *Text         `json:"text,omitempty"`
	Image          *Image        `json:"image,omitempty"`
	Link           *Link         `json:"link,omitempty"`
	Voice          *Voice        `json:"voice,omitempty"`
	Video          *Video        `json:"video,omitempty"`
	File           *File         `json:"file,omitempty"`
	Msgmenu        *Msgmenu      `json:"msgmenu,omitempty"`
	BusinessCard   *BusinessCard `json:"business_card,omitempty"`
	CaLink         *CaLink       `json:"ca_link,omitempty"`
	Event          *Event        `json:"event,omitempty"`
}

type Event struct {
	EventType      string         `json:"event_type"`
	OpenKfid       string         `json:"open_kfid"`
	ExternalUserid string         `json:"external_userid"`
	Scene          string         `json:"scene"`
	SceneParam     string         `json:"scene_param"`
	WelcomeCode    string         `json:"welcome_code"`
	WechatChannels WechatChannels `json:"wechat_channels"`
}

type WechatChannels struct {
	Nickname string `json:"nickname"`
	Scene    int64  `json:"scene"`
}

type Text struct {
	Content   string `json:"content"`
	NoNewline int64  `json:"no_newline"`
	MenuId    string `json:"menu_id"`
}

// isMsgPayload
func (t *Text) isMsgPayload() {}
func (t *Text) isText()       {}

type Image struct {
	MediaID string `json:"media_id"`
}

// isMsgPayload
func (t *Image) isMsgPayload() {}

type Voice struct {
	MediaID string `json:"media_id"`
}

// isMsgPayload
func (t *Voice) isMsgPayload() {}

type Video struct {
	MediaID string `json:"media_id"`
}

// isMsgPayload
func (t *Video) isMsgPayload() {}

type File struct {
	MediaID string `json:"media_id"`
}

// isMsgPayload
func (t *File) isMsgPayload() {}

// type Link struct {
// 	Title        string `json:"title"`
// 	Desc         string `json:"desc"`
// 	URL          string `json:"url"`
// 	ThumbMediaID string `json:"thumb_media_id"`
// }

// isMsgPayload
func (t *Link) isMsgPayload() {}

type Miniprogram struct {
	Appid        string `json:"appid"`
	Title        string `json:"title"`
	ThumbMediaID string `json:"thumb_media_id"`
	Pagepath     string `json:"pagepath"`
	Content      string `json:"content"`
}

// isMsgPayload
func (t *Miniprogram) isMsgPayload() {}

type Msgmenu struct {
	HeadContent string `json:"head_content"`
	List        []List `json:"list"`
	TailContent string `json:"tail_content"`
}

// isMsgPayload
func (t *Msgmenu) isMsgPayload() {}

type List struct {
	Type        string       `json:"type"`
	Click       *Click       `json:"click,omitempty"`
	View        *View        `json:"view,omitempty"`
	Miniprogram *Miniprogram `json:"miniprogram,omitempty"`
	Text        *Text        `json:"text,omitempty"`
}

type Click struct {
	ID      string `json:"id"`
	Content string `json:"content"`
}

type View struct {
	URL     string `json:"url"`
	Content string `json:"content"`
}

type BusinessCard struct {
	Userid string `json:"userid"`
}

// isMsgPayload
func (t *BusinessCard) isMsgPayload() {}

type AccountList struct {
	OpenKfid        string `json:"open_kfid"`
	Name            string `json:"name"`
	Avatar          string `json:"avatar"`
	ManagePrivilege bool   `json:"manage_privilege"`
}

// type UploadMediaResponse struct {
// 	CommonResponse

// 	MediaID   string `json:"media_id"`
// 	CreatedAt int64  `json:"created_at"`
// }

type AcquisitionLink struct {
	LinkID     string `json:"link_id"`
	LinkName   string `json:"link_name"`
	URL        string `json:"url"`
	CreateTime int64  `json:"create_time"`
}

// type Department struct {
// 	ID               int64    `json:"id"`
// 	Name             string   `json:"name"`
// 	NameEn           string   `json:"name_en"`
// 	DepartmentLeader []string `json:"department_leader"`
// 	Parentid         int64    `json:"parentid"`
// 	Order            int64    `json:"order"`
// }

type Customer struct {
	ExternalUserid string `json:"external_userid"`
	Userid         string `json:"userid"`
	ChatStatus     int64  `json:"chat_status"`
	State          string `json:"state"`
}

type SuiteRequest struct {
	SuiteID     string `json:"suite_id"`
	SuiteSecret string `json:"suite_secret"`
	SuiteTicket string `json:"suite_ticket"`
}

type SuiteResponse struct {
	CommonResponse

	SuiteAccessToken string `json:"suite_access_token"`
	ExpiresIn        int    `json:"expires_in"`
}

type GetPermanentRequest struct {
	AuthCode string `json:"auth_code"`
}

type GetPreAuthCodeRequest struct {
}

// Generated by https://quicktype.io

type GetPreAuthCodeResponse struct {
	CommonResponse

	PreAuthCode string `json:"pre_auth_code"`
	ExpiresIn   int64  `json:"expires_in"`
}

type GetAuthInfoRequest struct {
	AuthCorpid    string `json:"auth_corpid"`
	PermanentCode string `json:"permanent_code"`
}

// Generated by https://quicktype.io

type ListKFRequest struct {
	Offset int64 `json:"offset"`
	Limit  int64 `json:"limit"`
}

// Generated by https://quicktype.io

type ListKFResponse struct {
	CommonResponse

	AccountList []AccountList `json:"account_list"`
}

type GetAccessTokenRequest struct {
}

// Generated by https://quicktype.io

type GetAccessTokenResponse struct {
	CommonResponse

	AccessToken string `json:"access_token"`
	ExpiresIn   int64  `json:"expires_in"`
}

// Generated by https://quicktype.io

type KfContactWayRequest struct {
	OpenKfid string `json:"open_kfid"`
	Scene    string `json:"scene,omitempty"`
}

// Generated by https://quicktype.io

type KfContactWayResponse struct {
	CommonResponse

	URL string `json:"url"`
}

// Generated by https://quicktype.io

type KfServiceStateRequest struct {
	OpenKfid       string `json:"open_kfid"`
	ExternalUserid string `json:"external_userid"`
}

// Generated by https://quicktype.io

type KfServiceStateResponse struct {
	CommonResponse

	ServiceState   int64  `json:"service_state"`
	ServicerUserid string `json:"servicer_userid"`
}

// Generated by https://quicktype.io

type AddKfAccountRequest struct {
	Name    string `json:"name"`
	MediaID string `json:"media_id"`
}

// Generated by https://quicktype.io

type AddKfAccountResponse struct {
	CommonResponse

	OpenKfid string `json:"open_kfid"`
}

type KfSyncMsgRequest struct {
	Cursor      string `json:"cursor"`
	Token       string `json:"token"`
	Limit       int64  `json:"limit"`
	VoiceFormat int64  `json:"voice_format"`
	OpenKfid    string `json:"open_kfid"`
}

// Generated by https://quicktype.io

type KfSyncMsgResponse struct {
	CommonResponse

	NextCursor string    `json:"next_cursor"`
	HasMore    int64     `json:"has_more"`
	MsgList    []MsgList `json:"msg_list"`
}

// Generated by https://quicktype.io

type KfSendMsgRequest struct {
	Touser       string        `json:"touser"`
	OpenKfid     string        `json:"open_kfid"`
	Msgid        string        `json:"msgid,omitempty"`
	Msgtype      string        `json:"msgtype"`
	Text         *Text         `json:"text,omitempty"`
	Image        *Image        `json:"image,omitempty"`
	Link         *Link         `json:"link,omitempty"`
	Voice        *Voice        `json:"voice,omitempty"`
	Video        *Video        `json:"video,omitempty"`
	File         *File         `json:"file,omitempty"`
	Msgmenu      *Msgmenu      `json:"msgmenu,omitempty"`
	BusinessCard *BusinessCard `json:"business_card,omitempty"`
	CaLink       *CaLink       `json:"ca_link,omitempty"`
}

// CaLink 获客链接
type CaLink struct {
	LinkURL string `json:"link_url"`
}

func (t *CaLink) isMsgPayload() {}

type KfSendMsgResponse struct {
	CommonResponse

	Msgid string `json:"msgid"`
}

// SetPayload of KfSendMsgRequest
func (req *KfSendMsgRequest) SetPayload(msgType string, payload MsgPayload) {
	switch msgType {
	case "text":
		req.Text = payload.(*Text)
	case "image":
		req.Image = payload.(*Image)
	case "link":
		req.Link = payload.(*Link)
	case "voice":
		req.Voice = payload.(*Voice)
	case "video":
		req.Video = payload.(*Video)
	case "file":
		req.File = payload.(*File)
	case "msgmenu":
		req.Msgmenu = payload.(*Msgmenu)
	case "miniprogram":
		req.BusinessCard = payload.(*BusinessCard)
	case "ca_link":
		req.CaLink = payload.(*CaLink)
	}
}

// Generated by https://quicktype.io

type GetCorpTokenRequest struct {
	AuthCorpid    string `json:"auth_corpid"`
	PermanentCode string `json:"permanent_code"`
}

// Generated by https://quicktype.io

type GetCorpTokenResponse struct {
	CommonResponse

	AccessToken string `json:"access_token"`
	ExpiresIn   int64  `json:"expires_in"`
}

// Generated by https://quicktype.io

type KfSendOnEventRequest struct {
	Code    string   `json:"code"`
	Msgid   string   `json:"msgid,omitempty"`
	Msgtype string   `json:"msgtype"`
	Text    *Text    `json:"text"`
	Msgmenu *Msgmenu `json:"msgmenu"`
}

// Generated by https://quicktype.io

type KfSendOnEventResponse struct {
	CommonResponse

	Msgid string `json:"msgid"`
}

type UploadMediaRequest struct {
	Type     string `json:"type"`
	Filename string `json:"filename"`
	Path     string `json:"path"`
}

type UploadMediaResponse struct {
	CommonResponse

	MediaID   string `json:"media_id"`
	CreatedAt string `json:"created_at"`
}

type UpdateKfAccountRequest struct {
	OpenKfid string `json:"open_kfid"`
	Name     string `json:"name"`
	MediaID  string `json:"media_id"`
}

type UpdateKfAccountResponse struct {
	CommonResponse
}

type DeleteKfAccountRequest struct {
	OpenKfid string `json:"open_kfid"`
}

type DeleteKfAccountResponse struct {
	CommonResponse
}

type ListCustomerAcquisitionRequest struct {
	Limit  int64  `json:"limit"`
	Cursor string `json:"cursor"`
}

type ListCustomerAcquisitionResponse struct {
	CommonResponse

	LinkIDList []string `json:"link_id_list"`
	NextCursor string   `json:"next_cursor"`
}

type ListCustomerAcquisitionLinksResponse struct {
	CommonResponse

	LinkIDList []AcquisitionLink `json:"link_id_list"`
	NextCursor string            `json:"next_cursor"`
}

type CreateCustomerAcquisitionRequest struct {
	LinkName   string `json:"link_name"`
	Range      Range  `json:"range"`
	SkipVerify bool   `json:"skip_verify"`
}

type Range struct {
	UserList       []string `json:"user_list"`
	DepartmentList []int64  `json:"department_list"`
}

type CreateCustomerAcquisitionResponse struct {
	CommonResponse

	Link Link `json:"link"`
}

type Link struct {
	LinkID     string `json:"link_id"`
	LinkName   string `json:"link_name"`
	URL        string `json:"url"`
	CreateTime int64  `json:"create_time"`
}

type DeleteCustomerAcquisitionRequest struct {
	LinkID string `json:"link_id"`
}

type DeleteCustomerAcquisitionResponse struct {
	CommonResponse
}

type UpdateCustomerAcquisitionRequest struct {
	LinkID     string `json:"link_id"`
	LinkName   string `json:"link_name"`
	Range      Range  `json:"range"`
	SkipVerify bool   `json:"skip_verify"`
}

type UpdateCustomerAcquisitionResponse struct {
	CommonResponse
}

type FollowUsersRequest struct {
}

type FollowUsersResponse struct {
	CommonResponse
	FollowUser []string `json:"follow_user"`
}

type DepartmentListRequest struct {
}

type DepartmentListResponse struct {
	CommonResponse
	Department []Department `json:"department"`
}

type Department struct {
	ID               int64    `json:"id"`
	Name             string   `json:"name"`
	NameEn           string   `json:"name_en"`
	DepartmentLeader []string `json:"department_leader"`
	Parentid         int64    `json:"parentid"`
	Order            int64    `json:"order"`
}

type DepartmentUserListRequest struct {
	DepartmentID int64  `json:"department_id"`
	Cursor       string `json:"cursor,omitempty"`
}

type DepartmentUserListResponse struct {
	CommonResponse
	UserList   []DeptUser `json:"userlist"`
	NextCursor string     `json:"next_cursor"`
}

type AddCustomersRequest struct {
	LinkID string `json:"link_id"`
	Limit  int64  `json:"limit"`
	Cursor string `json:"cursor"`
}

type AddCustomersResponse struct {
	CommonResponse
	CustomerList []CustomerList `json:"customer_list"`
	NextCursor   string         `json:"next_cursor"`
}

type CustomerList struct {
	ExternalUserid string `json:"external_userid"`
	Userid         string `json:"userid"`
	ChatStatus     int64  `json:"chat_status"`
	State          string `json:"state"`
}

type GetUserInfoRequest struct {
}

type GetUserInfoResponse struct {
	CommonResponse

	Userid         string `json:"userid"`
	UserTicket     string `json:"user_ticket"`
	Openid         string `json:"openid"`
	ExternalUserid string `json:"external_userid"`
}

type UserInfo struct {
	Userid           string          `json:"userid"`
	UserTicket       string          `json:"user_ticket"`
	Name             string          `json:"name"`
	Department       []int64         `json:"department"`
	Order            []int64         `json:"order"`
	Position         string          `json:"position"`
	Mobile           string          `json:"mobile"`
	Gender           string          `json:"gender"`
	Email            string          `json:"email"`
	BizMail          string          `json:"biz_mail"`
	IsLeaderInDept   []int64         `json:"is_leader_in_dept"`
	DirectLeader     []string        `json:"direct_leader"`
	Avatar           string          `json:"avatar"`
	ThumbAvatar      string          `json:"thumb_avatar"`
	Telephone        string          `json:"telephone"`
	Alias            string          `json:"alias"`
	Address          string          `json:"address"`
	OpenUserid       string          `json:"open_userid"`
	MainDepartment   int64           `json:"main_department"`
	Extattr          Extattr         `json:"extattr"`
	Status           int64           `json:"status"`
	QrCode           string          `json:"qr_code"`
	ExternalPosition string          `json:"external_position"`
	ExternalProfile  ExternalProfile `json:"external_profile"`
}

type ExtUserInfo struct {
	Openid         string `json:"openid"`
	ExternalUserid string `json:"external_userid"`
}

type GetUserRequest struct {
}

type GetUserResponse struct {
	CommonResponse

	Userid           string          `json:"userid"`
	Name             string          `json:"name"`
	Department       []int64         `json:"department"`
	Order            []int64         `json:"order"`
	Position         string          `json:"position"`
	Mobile           string          `json:"mobile"`
	Gender           string          `json:"gender"`
	Email            string          `json:"email"`
	BizMail          string          `json:"biz_mail"`
	IsLeaderInDept   []int64         `json:"is_leader_in_dept"`
	DirectLeader     []string        `json:"direct_leader"`
	Avatar           string          `json:"avatar"`
	ThumbAvatar      string          `json:"thumb_avatar"`
	Telephone        string          `json:"telephone"`
	Alias            string          `json:"alias"`
	Address          string          `json:"address"`
	OpenUserid       string          `json:"open_userid"`
	MainDepartment   int64           `json:"main_department"`
	Extattr          Extattr         `json:"extattr"`
	Status           int64           `json:"status"`
	QrCode           string          `json:"qr_code"`
	ExternalPosition string          `json:"external_position"`
	ExternalProfile  ExternalProfile `json:"external_profile"`
}

type User struct {
	Userid           string          `json:"userid"`
	Name             string          `json:"name"`
	Department       []int64         `json:"department"`
	Order            []int64         `json:"order"`
	Position         string          `json:"position"`
	Mobile           string          `json:"mobile"`
	Gender           string          `json:"gender"`
	Email            string          `json:"email"`
	BizMail          string          `json:"biz_mail"`
	IsLeaderInDept   []int64         `json:"is_leader_in_dept"`
	DirectLeader     []string        `json:"direct_leader"`
	Avatar           string          `json:"avatar"`
	ThumbAvatar      string          `json:"thumb_avatar"`
	Telephone        string          `json:"telephone"`
	Alias            string          `json:"alias"`
	Address          string          `json:"address"`
	OpenUserid       string          `json:"open_userid"`
	MainDepartment   int64           `json:"main_department"`
	Extattr          Extattr         `json:"extattr"`
	Status           int64           `json:"status"`
	QrCode           string          `json:"qr_code"`
	ExternalPosition string          `json:"external_position"`
	ExternalProfile  ExternalProfile `json:"external_profile"`
}

type Extattr struct {
	Attrs []Attr `json:"attrs"`
}

type Attr struct {
	Type        int64        `json:"type"`
	Name        string       `json:"name"`
	Text        *Text        `json:"text,omitempty"`
	Web         *Web         `json:"web,omitempty"`
	Miniprogram *Miniprogram `json:"miniprogram,omitempty"`
}

type Web struct {
	URL   string `json:"url"`
	Title string `json:"title"`
}

type ExternalProfile struct {
	ExternalCorpName string         `json:"external_corp_name"`
	WechatChannels   WechatChannels `json:"wechat_channels"`
	ExternalAttr     []Attr         `json:"external_attr"`
}

type GetUserDetailRequest struct {
	UserTicket string `json:"user_ticket"`
}

type GetUserDetailResponse struct {
	CommonResponse

	Userid  string `json:"userid"`
	Gender  string `json:"gender"`
	Avatar  string `json:"avatar"`
	QrCode  string `json:"qr_code"`
	Mobile  string `json:"mobile"`
	Email   string `json:"email"`
	BizMail string `json:"biz_mail"`
	Address string `json:"address"`
}

type GetUserIdsRequest struct {
	Cursor string `json:"cursor,omitempty"`
}

type GetUserIdsResponse struct {
	CommonResponse
	NextCursor string     `json:"next_cursor"`
	DeptUser   []DeptUser `json:"dept_user"`
}

type DeptUser struct {
	Name       string `json:"name"`
	Userid     string `json:"userid"`
	Department []int  `json:"department"`
}

type AppMessage struct {
	ToUser                 string    `json:"touser"`
	ToParty                string    `json:"toparty"`
	ToTag                  string    `json:"totag"`
	MsgType                string    `json:"msgtype"`
	AgentID                int       `json:"agentid"`
	Text                   *AppText  `json:"text,omitempty"`
	TextCard               *TextCard `json:"textcard,omitempty"`
	Safe                   int       `json:"safe"`
	EnableIDTrans          int       `json:"enable_id_trans"`
	EnableDuplicateCheck   int       `json:"enable_duplicate_check"`
	DuplicateCheckInterval int       `json:"duplicate_check_interval"`
}

type AppText struct {
	Content string `json:"content"`
}

// Generated by https://quicktype.io

type TextCard struct {
	Title       string `json:"title"`
	Description string `json:"description"`
	URL         string `json:"url"`
	Btntxt      string `json:"btntxt"`
}

type AppMessageResponse struct {
	CommonResponse

	InvalidUser    string `json:"invaliduser"`
	InvalidParty   string `json:"invalidparty"`
	InvalidTag     string `json:"invalidtag"`
	UnlicensedUser string `json:"unlicenseduser"`
	MsgID          string `json:"msgid"`
	ResponseCode   string `json:"response_code"`
}

type GetJSAPITicketRequest struct{}

// Generated by https://quicktype.io

type GetJSAPITicketResponse struct {
	CommonResponse

	Ticket    string `json:"ticket"`
	ExpiresIn int64  `json:"expires_in"`
}

// 获取客户基础信息
type GetCustomerInfoRequest struct {
	ExternalUseridList []string `json:"external_userid_list"`
}

type GetCustomerInfoResponse struct {
	CommonResponse

	CustomerList          []CustomerInfo `json:"customer_list"`
	InvalidExternalUserid []string       `json:"invalid_external_userid"`
}

type CustomerInfo struct {
	ExternalUserid string `json:"external_userid"`
	Nickname       string `json:"nickname"`
	Avatar         string `json:"avatar"`
	Gender         int    `json:"gender"`
	Unionid        string `json:"unionid"`
}

// UnionidToExternalUseridRequest unionid转换为服务商external_userid的请求
type UnionidToExternalUseridRequest struct {
	Unionid     string `json:"unionid"`
	Openid      string `json:"openid"`
	SubjectType int    `json:"subject_type"` // 1-服务商主体
}

// UnionidToExternalUseridResponse unionid转换为服务商external_userid的响应
type UnionidToExternalUseridResponse struct {
	CommonResponse
	ExternalUserid string `json:"external_userid"` // 服务商主体下的external_userid
	PendingID      string `json:"pending_id"`      // 待定ID
}

// GetNewExternalUseridRequest 旧external_userid转换为新external_userid的请求
type GetNewExternalUseridRequest struct {
	ExternalUseridList []string `json:"external_userid_list"` // 旧的external_userid列表
}

// GetNewExternalUseridResponse 旧external_userid转换为新external_userid的响应
type GetNewExternalUseridResponse struct {
	CommonResponse
	ExternalUseridMapping []ExternalUseridMapping `json:"external_userid_mapping"`
}

// ExternalUseridMapping external_userid映射关系
type ExternalUseridMapping struct {
	ExternalUserid    string `json:"external_userid"`     // 旧的external_userid
	NewExternalUserid string `json:"new_external_userid"` // 新的external_userid
}

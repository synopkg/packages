import enum

class SMBSecurityMode(enum.IntFlag):
	NEGOTIATE_USER_SECURITY = 0x01
	NEGOTIATE_ENCRYPT_PASSWORDS = 0x02
	NEGOTIATE_SECURITY_SIGNATURES_ENABLED = 0x04
	NEGOTIATE_SECURITY_SIGNATURES_REQUIRED = 0x08
	#others are Reserved


class SMBCapabilities(enum.IntFlag):
	CAP_RAW_MODE         = 0x00000001
	CAP_MPX_MODE         = 0x00000002
	CAP_UNICODE          = 0x00000004
	CAP_LARGE_FILES      = 0x00000008
	CAP_NT_SMBS          = 0x00000010
	CAP_RPC_REMOTE_APIS  = 0x00000020
	CAP_STATUS32         = 0x00000040
	CAP_LEVEL_II_OPLOCKS = 0x00000080
	CAP_LOCK_AND_READ    = 0x00000100
	CAP_NT_FIND          = 0x00000200
	CAP_BULK_TRANSFER    = 0x00000400
	CAP_COMPRESSED_DATA  = 0x00000800
	CAP_DFS              = 0x00001000
	CAP_QUADWORD_ALIGNED = 0x00002000
	CAP_LARGE_READX      = 0x00004000
	CAP_NT_EXTENDED_SECURITY = 0x80000000
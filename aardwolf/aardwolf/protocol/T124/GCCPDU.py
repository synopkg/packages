GCCPDU = """

-- ASN module extracted from ITU-T T.124 (01/2007)

-- Module GCC-PROTOCOL (T.127:08/2007)
GCC-PROTOCOL {itu-t(0) recommendation(0) t(20) t124(124) version(0) 2 asn1Modules(2) gcc-protocol(1)} 
DEFINITIONS AUTOMATIC TAGS ::=
BEGIN

-- Export all symbols
-- =============================================================================
-- Part 1:  Elements of which messages are composed
-- =============================================================================
ChannelID ::= INTEGER(1..65535)

StaticChannelID ::= INTEGER(1..1000)

-- Those assigned by specifications
DynamicChannelID ::= INTEGER(1001..65535)

-- Those created and deleted by MCS
UserID ::= DynamicChannelID

TokenID ::= INTEGER(1..65535)

StaticTokenID ::= INTEGER(1..16383)

-- Those assigned by specifications
DynamicTokenID ::= INTEGER(16384..65535)

-- Those assigned by the registry
Time ::= INTEGER(-2147483648..2147483647)

-- Time in seconds
Handle ::= INTEGER(0..4294967295)

-- 32-bit value
H221NonStandardIdentifier ::= OCTET STRING(SIZE (4..255))

-- First four octets shall be country code and
-- Manufacturer code, assigned as specified in
-- Annex A/H.221 for NS-cap and NS-comm
Key ::= CHOICE -- Identifier of a standard or non-standard object
         {
  object           OBJECT IDENTIFIER,
  h221NonStandard  H221NonStandardIdentifier
}

NonStandardParameter ::= SEQUENCE {key   Key,
                                   data  OCTET STRING
}

TextString ::= BMPString(SIZE (0..255))

-- Basic Multilingual Plane of ISO/IEC 10646-1 (Unicode)
simpleTextFirstCharacter UniversalString ::= {0, 0, 0, 0}

simpleTextLastCharacter UniversalString ::= {0, 0, 0, 255}

SimpleTextString ::=
  BMPString(SIZE (0..255))
    (FROM ("0..255"))

SimpleNumericString ::= NumericString(SIZE (1..255))(FROM ("0123456789"))

DiallingString ::= NumericString(SIZE (1..16))(FROM ("0123456789"))

SubAddressString ::= NumericString(SIZE (1..40))(FROM ("0123456789"))

ExtraDiallingString ::= TextString(SIZE (1..255))(FROM ("0123456789#*,"))

UserData ::= SET OF SEQUENCE {key    Key,
                              value  OCTET STRING OPTIONAL}

Password ::= SEQUENCE {
  numeric         SimpleNumericString,
  text            SimpleTextString OPTIONAL,
  ...,
  unicodeText     TextString OPTIONAL
}

PasswordSelector ::= CHOICE {
  numeric      SimpleNumericString,
  text         SimpleTextString,
  ...,
  unicodeText  TextString
}

ChallengeResponseItem ::= CHOICE {
  passwordString  PasswordSelector,
  responseData    UserData,
  ...
}

ChallengeResponseAlgorithm ::= CHOICE {
  passwordInTheClear    NULL,
  nonStandardAlgorithm  NonStandardParameter,
  ...
}

ChallengeItem ::= SEQUENCE {
  responseAlgorithm  ChallengeResponseAlgorithm,
  challengeData      UserData,
  ...
}

ChallengeRequest ::= SEQUENCE {
  challengeTag  INTEGER,
  challengeSet  SET OF ChallengeItem,
  -- Set of algorithms offered for response
  ...
}

ChallengeResponse ::= SEQUENCE {
  challengeTag       INTEGER,
  responseAlgorithm  ChallengeResponseAlgorithm,
  -- Specific algorithm selected from the set of
  -- items presented in the ChallengeRequest
  responseItem       ChallengeResponseItem,
  ...
}

PasswordChallengeRequestResponse ::= CHOICE {
  passwordInTheClear        PasswordSelector,
  challengeRequestResponse
    SEQUENCE {challengeRequest   ChallengeRequest OPTIONAL,
              challengeResponse  ChallengeResponse OPTIONAL,
              ...},
  ...
}

ConferenceName ::= SEQUENCE {
  numeric         SimpleNumericString,
  text            SimpleTextString OPTIONAL,
  ...,
  unicodeText     TextString OPTIONAL
}

ConferenceNameSelector ::= CHOICE {
  numeric      SimpleNumericString,
  text         SimpleTextString,
  ...,
  unicodeText  TextString
}

ConferenceNameModifier ::= SimpleNumericString

Privilege ::= ENUMERATED {
  terminate(0), ejectUser(1), add(2), lockUnlock(3), transfer(4), ...
  }

TerminationMethod ::= ENUMERATED {automatic(0), manual(1), ...
                                  }

ConferencePriorityScheme ::= CHOICE {
  nonStandardScheme  NonStandardParameter,
  ...
}

ConferencePriority ::= SEQUENCE {
  priority  INTEGER(0..65535),
  scheme    ConferencePriorityScheme,
  ...
}

NodeCategory ::= CHOICE {
  conventional         NULL,
  counted              NULL,
  anonymous            NULL,
  nonStandardCategory  NonStandardParameter,
  ...
}

ConferenceMode ::= CHOICE {
  conventional-only     NULL,
  counted-only          NULL,
  anonymous-only        NULL,
  conventional-control  NULL,
  unrestricted-mode     NULL,
  non-standard-mode     NonStandardParameter,
  ...
}

NetworkAddress ::=
  SEQUENCE (SIZE (1..64)) OF
    CHOICE -- Listed in order of use
     {aggregatedChannel
        SEQUENCE {transferModes
                    SEQUENCE -- One or more-- {speech         BOOLEAN,
                                              voice-band     BOOLEAN,
                                              digital-56k    BOOLEAN,
                                              digital-64k    BOOLEAN,
                                              digital-128k   BOOLEAN,
                                              digital-192k   BOOLEAN,
                                              digital-256k   BOOLEAN,
                                              digital-320k   BOOLEAN,
                                              digital-384k   BOOLEAN,
                                              digital-512k   BOOLEAN,
                                              digital-768k   BOOLEAN,
                                              digital-1152k  BOOLEAN,
                                              digital-1472k  BOOLEAN,
                                              digital-1536k  BOOLEAN,
                                              digital-1920k  BOOLEAN,
                                              packet-mode    BOOLEAN,
                                              frame-mode     BOOLEAN,
                                              atm            BOOLEAN,
                                              ...},
                  internationalNumber     DiallingString,
                  subAddress              SubAddressString OPTIONAL,
                  extraDialling           ExtraDiallingString OPTIONAL,
                  highLayerCompatibility
                    SEQUENCE {telephony3kHz    BOOLEAN,
                              telephony7kHz    BOOLEAN,
                              videotelephony   BOOLEAN,
                              videoconference  BOOLEAN,
                              audiographic     BOOLEAN,
                              audiovisual      BOOLEAN,
                              multimedia       BOOLEAN,
                              ...} OPTIONAL,
                  ...},
      transportConnection
        SEQUENCE {nsapAddress        OCTET STRING(SIZE (1..20)),
                  transportSelector  OCTET STRING OPTIONAL},
      nonStandard          NonStandardParameter,
      ...}

MediaList ::= SEQUENCE {audio  BOOLEAN,
                        video  BOOLEAN,
                        data   BOOLEAN,
                        ...
}

ChannelAggregationMethod ::= CHOICE {
  h221           NULL,
  h244           NULL,
  iso-iec-13871  NULL,
  -- The actual mode of bonding is dynamically selected according
  -- to the procedures described in ISO/IEC 13871.
  nonStandard    NonStandardParameter,
  ...
}

Profile ::= CHOICE {
  simpleProfile
    CHOICE {-- Basic transfer modes:
            speech             NULL, -- Simple telephony--
            telephony-3kHz     NULL, -- Rec. G.711--
            telephony-7kHz     NULL, -- Rec. G.722--
            voice-band         NULL, -- Modems--
            frameRelay         NULL,
            -- T.120-only data profiles (Rec. T.123):
            t123-pstn-basic    NULL,
            t123-psdn-basic    NULL,
            t123-b-isdn-basic  NULL},
  multimediaProfile
    SEQUENCE {profile
                CHOICE {h310   NULL,
                        h320   NULL,
                        h321   NULL,
                        h322   NULL,
                        h323   NULL,
                        h324   NULL,
                        h324m  NULL,
                        asvd   NULL,
                        dsvd   NULL},
              t120Data  BOOLEAN},
  dsmccDownloadProfile  NULL,
  nonStandard           NonStandardParameter,
  ...
}

ExtendedE164NetworkAddress ::= SEQUENCE {
  internationalNumber  DiallingString,
  subAddress           SubAddressString OPTIONAL,
  extraDialling        ExtraDiallingString OPTIONAL,
  ...
}

TransportAddress ::= SEQUENCE {
  nsapAddress        OCTET STRING(SIZE (1..20)),
  transportSelector  OCTET STRING OPTIONAL
}

GSTNConnection ::= SEQUENCE {networkAddress  ExtendedE164NetworkAddress,
                             ...
}

ISDNConnection ::= SEQUENCE {
  circuitTypes
    SET OF
      CHOICE {digital-64k         NULL,
              digital-2x64k       NULL,
              digital-384k        NULL,
              digital-1536        NULL,
              digital-1920k       NULL,
              multirate-base-64k  INTEGER(1..30) -- See Note 1
    },
  networkAddress          ExtendedE164NetworkAddress,
  highLayerCompatibility
    SEQUENCE {-- Those are supported code points for IE HLC of the D
              -- protocol (Rec. Q.931).
              telephony3kHz    BOOLEAN,
              telephony7kHz    BOOLEAN,
              videotelephony   BOOLEAN,
              videoconference  BOOLEAN,
              audiographic     BOOLEAN,
              audiovisual      BOOLEAN,
              multimedia       BOOLEAN,
              ...} OPTIONAL,
  ...
}

-- Note 1:	digital-2x64k differs from multirate-base-64k 
-- 			with a multiplier value of 2; 
--			in the first case 
--			the network is requested an 8 kHz integrity with Restricted
--			Differential Time Delay (RDTD); 
--			in the second case
--			the network is requested a Time Slot 
--			Sequence integrity (see 4.5.5/Q.931)

CSDNConnection ::= SEQUENCE {
  circuitTypes    SET OF CHOICE {digital-56k  NULL,
                                 digital-64k  NULL},
  networkAddress  ExtendedE164NetworkAddress,
  ...
}

PSDNConnection ::= SEQUENCE {
  networkAddress
    CHOICE {extendedE164NetworkAddress  ExtendedE164NetworkAddress,
            transportAddress            TransportAddress,
            nonStandard                 NonStandardParameter},
  ...
}

ATMConnection ::= SEQUENCE {
  networkAddress
    CHOICE {extendedE164  ExtendedE164NetworkAddress,
            nsapAddress   TransportAddress,
            -- this case is reserved for NSAPs only: the 
            -- optional transport selector shall never be used
            nonStandard   NonStandardParameter},
  maxTransferRate  INTEGER(0..MAX) OPTIONAL,
  -- in cells per seconds
  ...
}

NetworkConnection ::= CHOICE {
  gstnConnection              GSTNConnection,
  isdnConnection              ISDNConnection,
  csdnConnection              CSDNConnection,
  psdnConnection              PSDNConnection,
  atmConnection               ATMConnection,
  extendedE164NetworkAddress  ExtendedE164NetworkAddress,
  -- Note: LAN connections and leased
  transportAddress            TransportAddress,
  -- lines (Rec. G.703/G.704) may be 
  nonStandard                 NonStandardParameter,
  -- covered by one of these
  ...
}

NetworkAddressV2 ::=
  SET OF
    SEQUENCE {networkConnection
                CHOICE {singleConnection       NetworkConnection,
                        aggregatedConnections
                          SEQUENCE {connectionList
                                      SET (SIZE (1..30)) OF
                                        CHOICE {isdnConnection  ISDNConnection,
                                                csdnConnection  CSDNConnection,
                                                ...},
                                    aggregationMethods
                                      SET OF ChannelAggregationMethod OPTIONAL,
                                    ...}},
              profiles           SET OF Profile OPTIONAL,
              mediaConcerned     MediaList OPTIONAL,
              ...}

NodeType ::= ENUMERATED {terminal(0), multiportTerminal(1), mcu(2), ...
                         }

NodeProperties ::= SEQUENCE {
  managementDevice  BOOLEAN,
  -- Is the node a device such as a reservation system
  peripheralDevice  BOOLEAN,
  -- Is the node a peripheral to a primary node
  ...
}

AsymmetryIndicator ::= CHOICE {
  callingNode  NULL,
  calledNode   NULL,
  unknown      INTEGER(0..4294967295)
  -- Uniformly distributed 32-bit random number
}

AlternativeNodeID ::= CHOICE {h243NodeID  OCTET STRING(SIZE (2)),
                              ...
}

ConferenceDescriptor ::= SEQUENCE {
  conferenceName              ConferenceName,
  conferenceNameModifier      ConferenceNameModifier OPTIONAL,
  conferenceDescription       TextString OPTIONAL,
  lockedConference            BOOLEAN,
  passwordInTheClearRequired  BOOLEAN,
  networkAddress              NetworkAddress OPTIONAL,
  ...,
  defaultConferenceFlag       BOOLEAN,
  conferenceMode              ConferenceMode
}

NodeRecord ::= SEQUENCE {
  superiorNode         UserID OPTIONAL,
  -- Not present only for the Top GCC Provider
  nodeType             NodeType,
  nodeProperties       NodeProperties,
  nodeName             TextString OPTIONAL,
  participantsList     SEQUENCE OF TextString OPTIONAL,
  siteInformation      TextString OPTIONAL,
  networkAddress       NetworkAddress OPTIONAL,
  alternativeNodeID    AlternativeNodeID OPTIONAL,
  userData             UserData OPTIONAL,
  ...,
  nodeCategory         NodeCategory OPTIONAL,
  networkAddressV2     NetworkAddressV2 OPTIONAL
}

SessionKey ::= SEQUENCE {
  applicationProtocolKey  Key,
  sessionID               ChannelID OPTIONAL
}

ChannelType ::= ENUMERATED {
  static(0), dynamicMulticast(1), dynamicPrivate(2), dynamicUserId(3)
}

ApplicationRecord ::= SEQUENCE {
  applicationActive           BOOLEAN,
  -- Active/Inactive flag
  conductingOperationCapable  BOOLEAN,
  -- Maximum one per node per session
  startupChannel              ChannelType OPTIONAL,
  applicationUserID           UserID OPTIONAL,
  -- User ID assigned to the Application Protocol Entity
  nonCollapsingCapabilities
    SET OF
      SEQUENCE {capabilityID     CapabilityID,
                applicationData  OCTET STRING OPTIONAL} OPTIONAL,
  ...
}

CapabilityID ::= CHOICE {
  standard     INTEGER(0..65535),
  -- Assigned by Application Protocol specifications
  nonStandard  Key
}

CapabilityClass ::= CHOICE {
  logical      NULL,
  unsignedMin  INTEGER(0..MAX), -- Capability value
  unsignedMax  INTEGER(0..MAX), -- Capability value
  ...
}

EntityID ::= INTEGER(0..65535)

ApplicationInvokeSpecifier ::= SEQUENCE {
  sessionKey             SessionKey,
  expectedCapabilitySet
    SET OF
      SEQUENCE {capabilityID     CapabilityID,
                capabilityClass  CapabilityClass,
                ...} OPTIONAL,
  startupChannel         ChannelType OPTIONAL,
  mandatoryFlag          BOOLEAN,
  -- TRUE indicates required Application Protocol Entity
  ...
}

RegistryKey ::= SEQUENCE {
  sessionKey  SessionKey,
  resourceID  OCTET STRING(SIZE (0..64))
}

RegistryItem ::= CHOICE {
  channelID  DynamicChannelID,
  tokenID    DynamicTokenID,
  parameter  OCTET STRING(SIZE (0..64)),
  vacant     NULL,
  ...
}

RegistryEntryOwner ::= CHOICE {
  owned
    SEQUENCE {nodeID    UserID, -- Node ID of the owning node--
              entityID  EntityID -- Entity ID of the owning
}, 
-- Appliction Protocol Entity
  notOwned  NULL -- There is no current owner
}

RegistryModificationRights ::= ENUMERATED {owner(0), session(1), public(2)}

-- ============================================================================
-- Part 2:  PDU Messages
-- ============================================================================
UserIDIndication ::= SEQUENCE {tag  INTEGER,
                               ...
}

ConferenceCreateRequest ::=
  SEQUENCE { -- MCS-Connect-Provider request user data
  conferenceName          ConferenceName,
  convenerPassword        Password OPTIONAL,
  password                Password OPTIONAL,
  lockedConference        BOOLEAN,
  listedConference        BOOLEAN,
  conductibleConference   BOOLEAN,
  terminationMethod       TerminationMethod,
  conductorPrivileges     SET OF Privilege OPTIONAL,
  conductedPrivileges     SET OF Privilege OPTIONAL,
  nonConductedPrivileges  SET OF Privilege OPTIONAL,
  conferenceDescription   TextString OPTIONAL,
  callerIdentifier        TextString OPTIONAL,
  userData                UserData OPTIONAL,
  ...,
  conferencePriority      ConferencePriority OPTIONAL,
  conferenceMode          ConferenceMode OPTIONAL
}

ConferenceCreateResponse ::=
  SEQUENCE { -- MCS-Connect-Provider response user data
  nodeID    UserID, -- Node ID of the sending node
  tag       INTEGER,
  result
    ENUMERATED {success(0), userRejected(1), resourcesNotAvailable(2),
                rejectedForSymmetryBreaking(3),
                lockedConferenceNotSupported(4), ...
                },
  userData  UserData OPTIONAL,
  ...
}

ConferenceQueryRequest ::= SEQUENCE { -- MCS-Connect-Provider request user data
  nodeType            NodeType,
  asymmetryIndicator  AsymmetryIndicator OPTIONAL,
  userData            UserData OPTIONAL,
  ...
}

ConferenceQueryResponse ::=
  SEQUENCE { -- MCS-Connect-Provider response user data
  nodeType                     NodeType,
  asymmetryIndicator           AsymmetryIndicator OPTIONAL,
  conferenceList               SET OF ConferenceDescriptor,
  result                       ENUMERATED {success(0), userRejected(1), ...
                                           },
  userData                     UserData OPTIONAL,
  ...,
  waitForInvitationFlag        BOOLEAN OPTIONAL,
  noUnlistedConferenceFlag     BOOLEAN OPTIONAL
}

ConferenceJoinRequest ::=
  SEQUENCE { -- MCS-Connect-Provider request user data as well as
  -- MCS-Send-Data on Node ID Channel of Top GCC sent
  -- by the receiver of the MCS-Connect-Provider
  conferenceName          ConferenceNameSelector OPTIONAL,
  -- Required when part of MCS-Connect-Provider
  conferenceNameModifier  ConferenceNameModifier OPTIONAL,
  tag                     INTEGER OPTIONAL,
  -- Filled in when sent on Node ID Channel of Top GCC
  password                PasswordChallengeRequestResponse OPTIONAL,
  convenerPassword        PasswordSelector OPTIONAL,
  callerIdentifier        TextString OPTIONAL,
  userData                UserData OPTIONAL,
  ...,
  nodeCategory            NodeCategory OPTIONAL
}

ConferenceJoinResponse ::=
  SEQUENCE { -- MCS-Connect-Provider response user data as well as
  -- MCS-Send-Data on Node ID Channel of
  -- the receiver of the MCS-Connect-Provider
  nodeID                      UserID OPTIONAL,
  -- Node ID of directly connected node only
  topNodeID                   UserID,
  -- Node ID of Top GCC Provider
  tag                         INTEGER,
  conferenceNameAlias         ConferenceNameSelector OPTIONAL,
  passwordInTheClearRequired  BOOLEAN,
  lockedConference            BOOLEAN,
  listedConference            BOOLEAN,
  conductibleConference       BOOLEAN,
  terminationMethod           TerminationMethod,
  conductorPrivileges         SET OF Privilege OPTIONAL,
  -- No privilege shall be listed more than once
  conductedPrivileges         SET OF Privilege OPTIONAL,
  -- No privilege shall be listed more than once
  nonConductedPrivileges      SET OF Privilege OPTIONAL,
  -- No privilege shall be listed more than once
  conferenceDescription       TextString OPTIONAL,
  password                    PasswordChallengeRequestResponse OPTIONAL,
  result
    ENUMERATED {success(0), userRejected(1), invalidConference(2),
                invalidPassword(3), invalidConvenerPassword(4),
                challengeResponseRequired(5), invalidChallengeResponse(6), 
                ...
                },
  userData                    UserData OPTIONAL,
  ...,
  nodeCategory                NodeCategory OPTIONAL,
  conferenceMode              ConferenceMode OPTIONAL
}

ConferenceInviteRequest ::=
  SEQUENCE { -- MCS-Connect-Provider request user data
  conferenceName              ConferenceName,
  nodeID                      UserID, -- Node ID of the sending node
  topNodeID                   UserID, -- Node ID of Top GCC Provider
  tag                         INTEGER,
  passwordInTheClearRequired  BOOLEAN,
  lockedConference            BOOLEAN,
  listedConference            BOOLEAN,
  conductibleConference       BOOLEAN,
  terminationMethod           TerminationMethod,
  conductorPrivileges         SET OF Privilege OPTIONAL,
  -- No privilege shall be listed more than once
  conductedPrivileges         SET OF Privilege OPTIONAL,
  -- No privilege shall be listed more than once
  nonConductedPrivileges      SET OF Privilege OPTIONAL,
  -- No privilege shall be listed more than once
  conferenceDescription       TextString OPTIONAL,
  callerIdentifier            TextString OPTIONAL,
  userData                    UserData OPTIONAL,
  ...,
  conferencePriority          ConferencePriority OPTIONAL,
  nodeCategory                NodeCategory OPTIONAL,
  conferenceMode              ConferenceMode OPTIONAL
}

ConferenceInviteResponse ::=
  SEQUENCE { -- MCS-Connect-Provider response user data
  result    ENUMERATED {success(0), userRejected(1), ...
                        },
  userData  UserData OPTIONAL,
  ...
}

ConferenceAddRequest ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of Top GCC or
  -- Node ID Channel of Adding MCU if specified
  networkAddress       NetworkAddress,
  requestingNode       UserID,
  tag                  INTEGER,
  addingMCU            UserID OPTIONAL,
  userData             UserData OPTIONAL,
  ...,
  nodeCategory         NodeCategory OPTIONAL,
  networkAddressV2     NetworkAddressV2
}

ConferenceAddResponse ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of requester
  tag       INTEGER,
  result
    ENUMERATED {success(0), invalidRequester(1), invalidNetworkType(2),
                invalidNetworkAddress(3), addedNodeBusy(4), networkBusy(5),
                noPortsAvailable(6), connectionUnsuccessful(7), ...
                },
  userData  UserData OPTIONAL,
  ...
}

ConferenceLockRequest ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of Top GCC
  -- No parameters
  ...
}

ConferenceLockResponse ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of requester
  result  ENUMERATED {success(0), invalidRequester(1), alreadyLocked(2), ...
                      },
  ...
}

ConferenceLockIndication ::=
  SEQUENCE { -- MCS-Uniform-Send-Data on GCC-Broadcast-Channel
  -- or MCS-Send-Data on Node ID Channel
  -- No parameters
  ...
}

ConferenceUnlockRequest ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of Top GCC
  -- No parameters
  ...
}

ConferenceUnlockResponse ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of requester
  result  ENUMERATED {success(0), invalidRequester(1), alreadyUnlocked(2), ...
                      },
  ...
}

ConferenceUnlockIndication ::=
  SEQUENCE { -- MCS-Uniform-Send-Data on GCC-Broadcast-Channel
  -- or MCS-Send-Data on Node ID Channel
  -- No parameters
  ...
}

ConferenceTerminateRequest ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of Top GCC
  reason  ENUMERATED {userInitiated(0), timedConferenceTermination(1), ...
                      },
  ...
}

ConferenceTerminateResponse ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of requester
  result  ENUMERATED {success(0), invalidRequester(1), ...
                      },
  ...
}

ConferenceTerminateIndication ::=
  SEQUENCE { -- MCS-Uniform-Send-Data on GCC-Broadcast-Channel
  reason  ENUMERATED {userInitiated(0), timedConferenceTermination(1), ...
                      },
  ...
}

ConferenceEjectUserRequest ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of Top GCC
  nodeToEject  UserID, -- Node ID of the node to eject
  reason       ENUMERATED {userInitiated(0), ...
                           },
  ...
}

ConferenceEjectUserResponse ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of requester
  nodeToEject  UserID, -- Node ID of the node to eject
  result
    ENUMERATED {success(0), invalidRequester(1), invalidNode(2), ...
                },
  ...
}

ConferenceEjectUserIndication ::=
  SEQUENCE { -- MCS-Uniform-Send-Data on GCC-Broadcast-Channel
  nodeToEject  UserID, -- Node ID of the node to eject
  reason
    ENUMERATED {userInitiated(0), higherNodeDisconnected(1),
                higherNodeEjected(2), ...
                },
  ...
}

ConferenceTransferRequest ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of Top GCC
  conferenceName          ConferenceNameSelector,
  -- Name of conference to transfer to
  conferenceNameModifier  ConferenceNameModifier OPTIONAL,
  networkAddress          NetworkAddress OPTIONAL,
  transferringNodes       SET (SIZE (1..65536)) OF UserID OPTIONAL,
  password                PasswordSelector OPTIONAL,
  ...,
  networkAddressV2        NetworkAddressV2 OPTIONAL
}

ConferenceTransferResponse ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of requester
  conferenceName          ConferenceNameSelector,
  -- Name of conference to transfer to
  conferenceNameModifier  ConferenceNameModifier OPTIONAL,
  transferringNodes       SET (SIZE (1..65536)) OF UserID OPTIONAL,
  result                  ENUMERATED {success(0), invalidRequester(1), ...
                                      },
  ...
}

ConferenceTransferIndication ::=
  SEQUENCE { -- MCS-Uniform-Send-Data on GCC-Broadcast-Channel
  conferenceName          ConferenceNameSelector,
  -- Name of conference to transfer to
  conferenceNameModifier  ConferenceNameModifier OPTIONAL,
  networkAddress          NetworkAddress OPTIONAL,
  transferringNodes       SET (SIZE (1..65536)) OF UserID OPTIONAL,
  -- List of Node IDs,
  -- not present if destined for all nodes
  password                PasswordSelector OPTIONAL,
  ...,
  networkAddressV2        NetworkAddressV2 OPTIONAL
}

RosterUpdateIndication ::= SEQUENCE { -- MCS-Send-Data on Node ID Channel or
  -- MCS-Uniform-Send-Data on GCC-Broadcast-Channel
  fullRefresh             BOOLEAN,
  -- Conference Roster and all 
  -- ApplicationProtocol Sessions refreshed
  nodeInformation
    SEQUENCE {nodeRecordList
                CHOICE {noChange  NULL,
                        refresh
                          SET (SIZE (1..65536)) OF
                            SEQUENCE
                             -- One for each node in the conference;
                            -- no node shall be listed more than once
                            {nodeID      UserID, -- Node ID of the node--
                             nodeRecord  NodeRecord},
                        update
                          SET (SIZE (1..65536)) OF
                            SEQUENCE
                             -- One for each node changing its node record;
                            -- no node shall be listed more than once
                            {nodeID      UserID, -- Node ID of the node--
                             nodeUpdate
                               CHOICE {addRecord      NodeRecord,
                                       replaceRecord  NodeRecord,
                                       removeRecord   NULL,
                                       ...}},
                        ...},
              rosterInstanceNumber  INTEGER(0..65535),
              nodesAdded            BOOLEAN,
              -- Nodes have been added since last instance
              nodesRemoved          BOOLEAN,
              -- Nodes have been removed since last instance
              ...},
  applicationInformation
    SET (SIZE (0..65535)) OF
      SEQUENCE
       -- One for each Application Protocol Session;
      -- all Application Protocol Sessions if full refresh;
      -- no Application Protocol Session shall be
      -- listed more than once
      {sessionKey                   SessionKey,
       applicationRecordList
         CHOICE {noChange  NULL,
                 refresh
                   SET (SIZE (0..65535)) OF
                     SEQUENCE
                      -- One for each node with the
                     -- Application Protocol Session enrolled;
                     -- no node shall be listed more than once
                     {nodeID             UserID,
                      -- Node ID of node
                      entityID           EntityID,
                      -- ID for this Application Protocol Entity at this node
                      applicationRecord  ApplicationRecord},
                 update
                   SET (SIZE (1..65536)) OF
                     SEQUENCE
                      -- One for each node modifying its Application Record;
                     -- no node shall be listed more than once
                     {nodeID             UserID,
                      -- Node ID of node
                      entityID           EntityID,
                      -- ID for this Application Protocol Entity at this node
                      applicationUpdate
                        CHOICE {addRecord      ApplicationRecord,
                                replaceRecord  ApplicationRecord,
                                removeRecord   NULL,
                                ...}},
                 ...},
       applicationCapabilitiesList
         CHOICE {noChange  NULL,
                 refresh
                   SET OF
                     SEQUENCE {capabilityID      CapabilityID,
                               capabilityClass   CapabilityClass,
                               numberOfEntities  INTEGER(1..65536),
                               -- Number of Application Protocol Entities
                               -- which issued the capability
                               ...},
                 ...},
       rosterInstanceNumber         INTEGER(0..65535),
       peerEntitiesAdded            BOOLEAN,
       -- Peer Entities have been added since last instance
       peerEntitiesRemoved          BOOLEAN,
       -- Peer Entities have been removed since last instance
       ...},
  ...
}

ApplicationInvokeIndication ::=
  SEQUENCE { -- MCS-Send-Data or MCS-Uniform-Send-Data
  -- on GCC-Broadcast-Channel or Node ID Channel
  applicationProtocolEntiyList
    SET (SIZE (1..65536)) OF ApplicationInvokeSpecifier,
  destinationNodes              SET (SIZE (1..65536)) OF UserID OPTIONAL,
  -- List of Node IDs,
  -- not present if destined for all nodes
  ...
}

RegistryRegisterChannelRequest ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of Top GCC
  entityID   EntityID,
  key        RegistryKey,
  channelID  DynamicChannelID,
  ...
}

RegistryAssignTokenRequest ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of Top GCC
  entityID  EntityID,
  key       RegistryKey,
  ...
}

RegistrySetParameterRequest ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of Top GCC
  entityID            EntityID,
  key                 RegistryKey,
  parameter           OCTET STRING(SIZE (0..64)),
  modificationRights  RegistryModificationRights OPTIONAL,
  ...
}

RegistryRetrieveEntryRequest ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of Top GCC
  entityID  EntityID,
  key       RegistryKey,
  ...
}

RegistryDeleteEntryRequest ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of Top GCC
  entityID  EntityID,
  key       RegistryKey,
  ...
}

RegistryMonitorEntryRequest ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of Top GCC
  entityID  EntityID,
  key       RegistryKey,
  ...
}

RegistryMonitorEntryIndication ::=
  SEQUENCE { -- MCS-Uniform-Send-Data on GCC-Broadcast-Channel
  key                 RegistryKey,
  item                RegistryItem,
  -- Contents: channel, token, parameter, or empty
  owner               RegistryEntryOwner,
  modificationRights  RegistryModificationRights OPTIONAL,
  ...
}

RegistryAllocateHandleRequest ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of Top GCC
  entityID         EntityID,
  numberOfHandles  INTEGER(1..1024),
  ...
}

RegistryAllocateHandleResponse ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of requester
  entityID         EntityID,
  numberOfHandles  INTEGER(1..1024),
  firstHandle      Handle,
  result           ENUMERATED {successful(0), noHandlesAvailable(1), ...
                               },
  ...
}

RegistryResponse ::=
  SEQUENCE { -- MCS-Send-Data on Node ID Channel of requester
  entityID            EntityID,
  -- Entity ID of the requesting Application Protocol Entity
  primitiveType
    ENUMERATED {registerChannel(0), assignToken(1), setParameter(2),
                retrieveEntry(3), deleteEntry(4), monitorEntry(5), ...
                },
  key                 RegistryKey,
  -- Database index
  item                RegistryItem,
  -- Contents: channel, token, parameter, or vacant
  owner               RegistryEntryOwner,
  modificationRights  RegistryModificationRights OPTIONAL,
  result
    ENUMERATED {successful(0), belongsToOther(1), tooManyEntries(2),
                inconsistentType(3), entryNotFound(4), entryAlreadyExists(5),
                invalidRequester(6), ...
                },
  ...
}

ConductorAssignIndication ::=
  SEQUENCE { -- MCS-Uniform-Send-Data on GCC-Broadcast-Channel
  conductingNode  UserID,
  ...
}

ConductorReleaseIndication ::=
  SEQUENCE { -- MCS-Uniform-Send-Data on GCC-Broadcast-Channel
  -- No parameters
  ...
}

ConductorPermissionAskIndication ::=
  SEQUENCE { -- MCS-Uniform-Send-Data on GCC-Broadcast-Channel
  grantFlag  BOOLEAN,
  -- TRUE to request permission grant, FALSE to release
  ...
}

ConductorPermissionGrantIndication ::=
  SEQUENCE { -- MCS-Uniform-Send-Data on GCC-Broadcast-Channel
  permissionList  SEQUENCE (SIZE (0..65535)) OF UserID,
  -- Node ID of nodes granted permission
  waitingList     SEQUENCE (SIZE (1..65536)) OF UserID OPTIONAL,
  -- Node ID of nodes waiting form permission
  ...
}

ConferenceTimeRemainingIndication ::=
  SEQUENCE { -- MCS-Send-Data on GCC-Broadcast-Channel
  timeRemaining  Time,
  nodeID         UserID OPTIONAL,
  ...
}

ConferenceTimeInquireIndication ::=
  SEQUENCE { -- MCS-Send-Data on GCC-Convener-Channel
  nodeSpecificTimeFlag  BOOLEAN,
  -- FALSE for conference-wide, TRUE for node-specific
  ...
}

ConferenceTimeExtendIndication ::=
  SEQUENCE { -- MCS-Send-Data on GCC-Convener-Channel
  timeToExtend          Time,
  nodeSpecificTimeFlag  BOOLEAN,
  -- FALSE for conference-wide, TRUE for node-specific
  ...
}

ConferenceAssistanceIndication ::=
  SEQUENCE { -- MCS-Uniform-Send-Data on GCC-Broadcast-Channel
  userData  UserData OPTIONAL,
  ...
}

TextMessageIndication ::= SEQUENCE { -- MCS-Send-Data or MCS-Uniform-Send-Data
  message  TextString,
  -- on GCC-Broadcast-Channel or Node ID Channel
  ...
}

RosterRefreshRequest ::= SEQUENCE {
  nodeID                UserID,
  nodeCategory          NodeCategory,
  fullRefresh           BOOLEAN,
  sendConferenceRoster  BOOLEAN OPTIONAL,
  applicationList
    SEQUENCE {applicationKeyList
                SET OF
                  SEQUENCE {applicationProtocolKey  Key,
                            nonStandardParameter
                              NonStandardParameter OPTIONAL,
                            ...},
              nonStandardParameter  NonStandardParameter OPTIONAL,
              ...} OPTIONAL,
  sessionList
    SEQUENCE {sessionKeyList
                SET OF
                  SEQUENCE {sessionKey            SessionKey,
                            nonStandardParameter  NonStandardParameter OPTIONAL,
                            ...},
              nonStandardParameter  NonStandardParameter OPTIONAL,
              ...} OPTIONAL,
  nonStandardParameter  NonStandardParameter OPTIONAL,
  ...
}

FunctionNotSupportedResponse ::= SEQUENCE {request  RequestPDU
}

NonStandardPDU ::= SEQUENCE {data  NonStandardParameter,
                             ...
}

-- ==========================================================================
-- Part 3:  Messages sent as MCS-Connect-Provider user data
-- ==========================================================================
ConnectData ::= SEQUENCE {
  t124Identifier  Key,
  -- This shall be set to the value {itu-t recommendation t 124 version(0) 1}
  connectPDU      OCTET STRING
}

ConnectGCCPDU ::= CHOICE {
  conferenceCreateRequest   ConferenceCreateRequest,
  conferenceCreateResponse  ConferenceCreateResponse,
  conferenceQueryRequest    ConferenceQueryRequest,
  conferenceQueryResponse   ConferenceQueryResponse,
  conferenceJoinRequest     ConferenceJoinRequest,
  conferenceJoinResponse    ConferenceJoinResponse,
  conferenceInviteRequest   ConferenceInviteRequest,
  conferenceInviteResponse  ConferenceInviteResponse,
  ...
}

-- ============================================================================
-- Part 4:  Messages sent using MCS-Send-Data or MCS-Uniform-Send-Data
-- ============================================================================
GCCPDU ::= CHOICE {
  request     RequestPDU,
  response    ResponsePDU,
  indication  IndicationPDU
}

RequestPDU ::= CHOICE {
  conferenceJoinRequest           ConferenceJoinRequest,
  conferenceAddRequest            ConferenceAddRequest,
  conferenceLockRequest           ConferenceLockRequest,
  conferenceUnlockRequest         ConferenceUnlockRequest,
  conferenceTerminateRequest      ConferenceTerminateRequest,
  conferenceEjectUserRequest      ConferenceEjectUserRequest,
  conferenceTransferRequest       ConferenceTransferRequest,
  registryRegisterChannelRequest  RegistryRegisterChannelRequest,
  registryAssignTokenRequest      RegistryAssignTokenRequest,
  registrySetParameterRequest     RegistrySetParameterRequest,
  registryRetrieveEntryRequest    RegistryRetrieveEntryRequest,
  registryDeleteEntryRequest      RegistryDeleteEntryRequest,
  registryMonitorEntryRequest     RegistryMonitorEntryRequest,
  registryAllocateHandleRequest   RegistryAllocateHandleRequest,
  nonStandardRequest              NonStandardPDU,
  ...
}

ResponsePDU ::= CHOICE {
  conferenceJoinResponse          ConferenceJoinResponse,
  conferenceAddResponse           ConferenceAddResponse,
  conferenceLockResponse          ConferenceLockResponse,
  conferenceUnlockResponse        ConferenceUnlockResponse,
  conferenceTerminateResponse     ConferenceTerminateResponse,
  conferenceEjectUserResponse     ConferenceEjectUserResponse,
  conferenceTransferResponse      ConferenceTransferResponse,
  registryResponse                RegistryResponse,
  registryAllocateHandleResponse  RegistryAllocateHandleResponse,
  functionNotSupportedResponse    FunctionNotSupportedResponse,
  nonStandardResponse             NonStandardPDU,
  ...
}

IndicationPDU ::= CHOICE {
  userIDIndication                    UserIDIndication,
  conferenceLockIndication            ConferenceLockIndication,
  conferenceUnlockIndication          ConferenceUnlockIndication,
  conferenceTerminateIndication       ConferenceTerminateIndication,
  conferenceEjectUserIndication       ConferenceEjectUserIndication,
  conferenceTransferIndication        ConferenceTransferIndication,
  rosterUpdateIndication              RosterUpdateIndication,
  applicationInvokeIndication         ApplicationInvokeIndication,
  registryMonitorEntryIndication      RegistryMonitorEntryIndication,
  conductorAssignIndication           ConductorAssignIndication,
  conductorReleaseIndication          ConductorReleaseIndication,
  conductorPermissionAskIndication    ConductorPermissionAskIndication,
  conductorPermissionGrantIndication  ConductorPermissionGrantIndication,
  conferenceTimeRemainingIndication   ConferenceTimeRemainingIndication,
  conferenceTimeInquireIndication     ConferenceTimeInquireIndication,
  conferenceTimeExtendIndication      ConferenceTimeExtendIndication,
  conferenceAssistanceIndication      ConferenceAssistanceIndication,
  textMessageIndication               TextMessageIndication,
  nonStandardIndication               NonStandardPDU,
  ...
}

END

-- Generated by Asnp, the ASN.1 pretty-printer of France Telecom R&D

"""